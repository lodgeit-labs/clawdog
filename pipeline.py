import os
import glob
import pandas as pd
import yaml
from jinja2 import Template
from pyswip import Prolog

from engine.heuristic_mapper import map_account_to_mini


# ---------------------------------------------------------------------------
# S1: Prolog shadow-verification of the equity roll-forward (Point #6).
#
# The legacy 6-Point Thermodynamic Safeguard implements equity roll-forward in
# Python (`calculate_cashflow_and_equity` below). engine/consolidation.pl now
# implements the same equation in Prolog with stricter determinism guarantees
# (no silent zero, unique-FX-rate enforcement, epsilon-tolerant equality).
#
# This helper runs the Prolog version *alongside* the Python check and surfaces
# any disagreement as a Point #7 FATAL. In mono-currency mode (TargetCurrency =
# entity reporting currency, identity FX) the two implementations should agree
# exactly. Disagreement points at a real bug in either layer.
#
# Brain canon: GLOBAL_NOTES/CLAWDOG/107_CONSOLIDATION_LOGIC.md
# Engine:      engine/consolidation.pl
# ---------------------------------------------------------------------------

_CONSOLIDATION_LOADED = False

def _ensure_consolidation_loaded(prolog):
    """Consult engine/consolidation.pl into the shared Prolog database once."""
    global _CONSOLIDATION_LOADED
    if not _CONSOLIDATION_LOADED:
        prolog.consult('engine/consolidation.pl')
        _CONSOLIDATION_LOADED = True

def verify_equity_via_prolog(opening_equity, profit_plus_capital, dividends_paid,
                             closing_equity, currency='AUD',
                             opening_period='OPENING', action_period='ACTION',
                             closing_period='CLOSING', entity='client'):
    """Run engine/consolidation.pl::verify_temporal_equity/5 over the four
    equity-roll-forward inputs and return (balanced, expected_closing).

    `balanced` is True iff:
        opening_equity + profit_plus_capital - dividends_paid == closing_equity
    within engine/consolidation.pl's fx_epsilon tolerance (1e-6).

    Note: the legacy Python equation conflates capital injections with net
    income into a single "profit" term. We feed that conflation as-is into
    sbr:NetProfit so the two layers compute over identical inputs. Breaking
    out capital injections as a separate fact-stream is a future sprint.
    """
    prolog = Prolog()
    _ensure_consolidation_loaded(prolog)

    # Clean any prior asserts in the consolidation namespace for this entity.
    list(prolog.query(
        f"retractall(sbrm_consolidation:sbrm_fact('{entity}',_,_,_,_,_))"))

    # Inject the four roll-forward facts. Currency is identity (AUD->AUD) in
    # mono-currency mode; no fx_rate facts needed because convert_value/5
    # short-circuits on identity.
    facts = [
        (opening_period, 'sbr:OpeningEquity',  float(opening_equity)),
        (action_period,  'sbr:NetProfit',      float(profit_plus_capital)),
        (action_period,  'sbr:DividendsPaid',  float(dividends_paid)),
        (closing_period, 'sbr:ClosingEquity',  float(closing_equity)),
    ]
    for period, concept, value in facts:
        list(prolog.query(
            f"assertz(sbrm_consolidation:sbrm_fact('{entity}','{period}',"
            f"'{concept}',{value},'{currency}','Leaf'))"))

    # Run the verifier.
    query = (f"sbrm_consolidation:verify_temporal_equity('{entity}',"
             f"'{opening_period}','{action_period}','{closing_period}',"
             f"'{currency}')")
    balanced = bool(list(prolog.query(query)))

    expected_closing = opening_equity + profit_plus_capital - dividends_paid
    return balanced, expected_closing

def calculate_cashflow_and_equity(csv_file, net_income):
    """
    Parses the raw CSV to calculate the thermodynamic flow of Cash and Equity.
    Returns (calculated_closing_cash, calculated_closing_equity)
    """
    df = pd.read_csv(csv_file)
    
    # Cash Flow Tracking
    opening_cash = 0.0
    operating_cf = 0.0
    investing_cf = 0.0
    financing_cf = 0.0
    
    # Equity Tracking
    opening_equity = 0.0
    capital_injections = 0.0
    dividends_paid = 0.0
    
    def is_cash(acc):
        return map_account_to_mini(acc) == 'mini_CashAndCashEquivalents'
        
    grouped = df.groupby('Transaction_ID')
    
    for tx_id, group in grouped:
        # --- CASH FLOW LOGIC ---
        cash_rows = group[group['Account_Name'].apply(is_cash)]
        if not cash_rows.empty:
            cash_movement = cash_rows['Amount'].sum()
            if abs(cash_movement) >= 0.01:
                non_cash_rows = group[~group['Account_Name'].apply(is_cash)]
                uris = [map_account_to_mini(row['Account_Name']) for _, row in non_cash_rows.iterrows()]
                
                if not uris:
                    opening_cash += cash_movement
                elif 'mini_PropertyPlantAndEquipment' in uris:
                    investing_cf += cash_movement
                elif any(u in uris for u in ['mini_PaidInCapital', 'mini_RetainedEarnings', 'mini_LongtermDebt']):
                    financing_cf += cash_movement
                else:
                    operating_cf += cash_movement

        # --- EQUITY LOGIC ---
        for _, row in group.iterrows():
            uri = map_account_to_mini(row['Account_Name'])
            amt = float(row['Amount'])
            
            if uri == 'mini_PaidInCapital':
                if 'Opening' in str(row['Description']):
                    opening_equity += -amt
                else:
                    capital_injections += -amt
            elif uri == 'mini_RetainedEarnings':
                if 'Opening' in str(row['Description']):
                    opening_equity += -amt
                elif 'Dividend' in str(row['Account_Name']) or 'Drawings' in str(row['Account_Name']):
                    dividends_paid += amt
                    
    calculated_cash = opening_cash + operating_cf + investing_cf + financing_cf
    calculated_equity = opening_equity + capital_injections - dividends_paid + net_income
    
    return calculated_cash, calculated_equity

def pre_flight_audit(accounts, csv_file, client_name):
    """
    THE 6-POINT STRICT SBRM THERMODYNAMIC SAFEGUARD
    """
    errors = []
    
    # 1. The Tensegrity Proof
    assets = accounts.get('mini_Assets', 0.0)
    lia_eq = accounts.get('mini_LiabilitiesAndEquity', 0.0)
    if abs(assets - lia_eq) > 0.01:
        errors.append(f"FATAL (1): Balance Sheet Tensegrity Failed. Assets: {assets:,.2f} | Liab & Eq: {lia_eq:,.2f}")

    # 2. Asset Rollup Integrity
    current_assets = accounts.get('mini_CurrentAssets', 0.0)
    non_current_assets = accounts.get('mini_NoncurrentAssets', 0.0)
    if abs(assets - (current_assets + non_current_assets)) > 0.01:
        errors.append(f"FATAL (2): Asset Rollup Failed. Current({current_assets:,.2f}) + NonCurrent({non_current_assets:,.2f}) != Total Assets({assets:,.2f})")

    # 3. Liability & Equity Rollup Integrity
    liab = accounts.get('mini_Liabilities', 0.0)
    eq = accounts.get('mini_Equity', 0.0)
    if abs(lia_eq - (liab + eq)) > 0.01:
        errors.append(f"FATAL (3): Liab & Eq Rollup Failed. Liab({liab:,.2f}) + Equity({eq:,.2f}) != Total L&E({lia_eq:,.2f})")

    # 4. P&L Net Income Verification
    rev = accounts.get('mini_Sales', 0.0)
    cogs = accounts.get('mini_CostOfGoodsSold', 0.0)
    opex = accounts.get('mini_OperatingExpenses', 0.0)
    non_op = accounts.get('mini_NonoperatingIncomeExpense', 0.0)
    stated_ni = accounts.get('mini_NetIncomeLoss', 0.0)
    calculated_ni = rev - cogs - opex + non_op
    
    if abs(stated_ni - calculated_ni) > 0.01:
        errors.append(f"FATAL (4): P&L Math Failed. Calculated NI: {calculated_ni:,.2f} | Stated NI: {stated_ni:,.2f}")

    # 5 & 6. Cashflow and Equity Proofs
    try:
        calc_cash, calc_equity = calculate_cashflow_and_equity(csv_file, stated_ni)
        
        # Grab actual ending balances from the JSON-LD state
        # Cash is tricky because if it was overdrawn, it was switched to Liabilities.
        # We need the absolute raw cash position to verify the cashflow statement.
        df = pd.read_csv(csv_file)
        actual_raw_cash = df[df['Account_Name'].apply(lambda x: map_account_to_mini(x) == 'mini_CashAndCashEquivalents')]['Amount'].sum()
        
        # 5. Cashflow Verification
        if abs(calc_cash - actual_raw_cash) > 0.01:
            errors.append(f"FATAL (5): Cashflow Integrity Failed. Calculated Ending Cash: {calc_cash:,.2f} | Actual Ledger Cash: {actual_raw_cash:,.2f}")
            
        # 6. Equity Verification
        # Note: The JSON-LD stated equity includes retained earnings + paid in capital
        stated_total_equity = accounts.get('mini_Equity', 0.0)
        if abs(calc_equity - stated_total_equity) > 0.01:
            errors.append(f"FATAL (6): Equity Rollforward Failed. Calculated Closing Equity: {calc_equity:,.2f} | Stated Total Equity: {stated_total_equity:,.2f}")

        # 7. Prolog shadow-verification of point 6 (S1 integration).
        # Re-runs the equity equation through engine/consolidation.pl and
        # cross-checks against the Python result. Disagreement = real bug.
        try:
            # Reconstruct the four roll-forward inputs from the same source as
            # calculate_cashflow_and_equity above. The function is run twice
            # here only because we need the four scalar inputs separately for
            # the Prolog call; this is intentionally cheap.
            df_eq = pd.read_csv(csv_file)
            opening_eq = 0.0
            cap_inj = 0.0
            divs = 0.0
            for _, row in df_eq.iterrows():
                uri = map_account_to_mini(row['Account_Name'])
                amt = float(row['Amount'])
                if uri == 'mini_PaidInCapital':
                    if 'Opening' in str(row['Description']):
                        opening_eq += -amt
                    else:
                        cap_inj += -amt
                elif uri == 'mini_RetainedEarnings':
                    if 'Opening' in str(row['Description']):
                        opening_eq += -amt
                    elif 'Dividend' in str(row['Account_Name']) or 'Drawings' in str(row['Account_Name']):
                        divs += amt
            profit_term = cap_inj + stated_ni
            balanced, expected = verify_equity_via_prolog(
                opening_eq, profit_term, divs, stated_total_equity)

            python_balanced = abs(calc_equity - stated_total_equity) <= 0.01
            if balanced != python_balanced:
                errors.append(
                    f"FATAL (7): Prolog/Python disagreement on equity "
                    f"roll-forward. Python balanced={python_balanced} "
                    f"(calc_equity={calc_equity:,.2f} vs stated={stated_total_equity:,.2f}) | "
                    f"Prolog balanced={balanced} "
                    f"(opening={opening_eq:,.2f} + profit={profit_term:,.2f} "
                    f"- divs={divs:,.2f} = expected={expected:,.2f} "
                    f"vs closing={stated_total_equity:,.2f})")
        except Exception as e:
            errors.append(f"FATAL (7): Prolog shadow-verifier error: {str(e)}")

    except Exception as e:
        errors.append(f"FATAL: Error calculating thermodynamic flows: {str(e)}")

    if errors:
        print(f"\n❌ [{client_name}] 6-POINT AUDIT FAILED. ABORTING RENDER.")
        for e in errors:
            print(f"  -> {e}")
        return False
        
    print(f"✅ [{client_name}] 6-Point Audit Passed. Thermodynamic Integrity Verified.")
    return True

def generate_sbrm_jsonld(csv_file):
    df = pd.read_csv(csv_file)
    prolog = Prolog()
    prolog.consult('engine/rules.pl')
    
    raw_balances = {}
    for _, row in df.iterrows():
        uri = map_account_to_mini(row['Account_Name'])
        raw_balances[uri] = raw_balances.get(uri, 0.0) + float(row['Amount'])
        
    switched = {}
    for uri, bal in raw_balances.items():
        if abs(bal) < 0.01: continue
        if uri == 'mini_CashAndCashEquivalents' and bal < 0:
            switched['mini_AccountsPayable'] = switched.get('mini_AccountsPayable', 0.0) + bal
        elif uri == 'mini_AccountsPayable' and bal > 0:
            switched['mini_Receivables'] = switched.get('mini_Receivables', 0.0) + bal
        else:
            switched[uri] = switched.get(uri, 0.0) + bal
            
    total_rev = 0.0
    total_exp = 0.0
    non_op = 0.0
    real_accounts = {}
    
    for uri, bal in switched.items():
        if abs(bal) < 0.01: continue
        if uri == 'mini_Sales' and bal < 0:
            total_rev += abs(bal)
        elif uri in ['mini_CostOfGoodsSold', 'mini_OperatingExpenses'] and bal > 0:
            total_exp += bal
        elif uri == 'mini_NonoperatingIncomeExpense':
            non_op += -bal
        else:
            real_accounts[uri] = bal
            
    net_income = total_rev - total_exp + non_op
    real_accounts['mini_RetainedEarnings'] = real_accounts.get('mini_RetainedEarnings', 0.0) - net_income
    
    prolog.retractall("raw_fact(_, _)")
    for uri, bal in real_accounts.items():
        magnitude = bal if uri in ['mini_CashAndCashEquivalents', 'mini_Receivables', 'mini_Inventories', 'mini_PropertyPlantAndEquipment'] else -bal
        if abs(magnitude) > 0.01: prolog.assertz(f"raw_fact('{uri}', {magnitude})")
        
    cogs = sum([bal for u, bal in switched.items() if u == 'mini_CostOfGoodsSold'])
    opex = sum([bal for u, bal in switched.items() if u == 'mini_OperatingExpenses'])
    
    prolog.assertz(f"raw_fact('mini_Sales', {total_rev})")
    prolog.assertz(f"raw_fact('mini_CostOfGoodsSold', {cogs})")
    prolog.assertz(f"raw_fact('mini_OperatingExpenses', {opex})")
    prolog.assertz(f"raw_fact('mini_NonoperatingIncomeExpense', {non_op})")
    prolog.assertz(f"raw_fact('mini_NetIncomeLoss', {net_income})")
    
    nodes = ['mini_CashAndCashEquivalents', 'mini_Receivables', 'mini_Inventories', 'mini_PropertyPlantAndEquipment', 
             'mini_CurrentAssets', 'mini_NoncurrentAssets', 'mini_Assets',
             'mini_AccountsPayable', 'mini_CurrentLiabilities', 'mini_NoncurrentLiabilities', 'mini_Liabilities', 
             'mini_PaidInCapital', 'mini_RetainedEarnings', 'mini_Equity', 'mini_LiabilitiesAndEquity',
             'mini_Sales', 'mini_CostOfGoodsSold', 'mini_OperatingExpenses', 'mini_NonoperatingIncomeExpense', 'mini_NetIncomeLoss']
             
    final_accounts = {}
    for node in nodes:
        res = list(prolog.query(f"node_value('{node}', Total)"))
        final_accounts[node] = float(res[0]['Total']) if res else 0.0
        
    client_name = os.path.basename(csv_file).replace('.csv', '')
    
    return {
        "@context": "https://xbrlsite.azurewebsites.net/seattlemethod/platinum/mini",
        "@type": "StatutoryAccounts",
        "Entity": {
            "CompanyName": client_name,
            "TaxReference": "ABN 12 345 678 901"
        },
        "AccountingPeriod": {
            "StartDate": "2024-07-01",
            "EndDate": "2025-06-30"
        },
        "Accounts": final_accounts
    }

# ---------------------------------------------------------------------------
# S2: Multi-currency consolidated ingestion
#
# A group manifest (YAML) describes a parent + N subsidiaries, each with their
# own ledger CSV in their own functional currency. The consolidator reads each
# member ledger, FX-translates any non-reporting-currency rows, and synthesises
# a single in-memory consolidated CSV that the existing audit pipeline can
# process unchanged.
#
# CSV schema extension: an optional `Currency` column. Legacy ledgers without
# the column are treated as the manifest's reporting currency (default AUD).
# Each entity's books must self-balance in their own functional currency before
# consolidation — the consolidator does not validate that, the per-entity audit
# implicitly does (assuming you also run the entity's CSV directly).
# ---------------------------------------------------------------------------

def _load_fx_rates(fx_csv_path):
    """Read fx_rates.csv and return {(src, tgt, period): rate}."""
    rates = {}
    if not os.path.exists(fx_csv_path):
        return rates
    df = pd.read_csv(fx_csv_path)
    for _, row in df.iterrows():
        rates[(row['Source'], row['Target'], row['Period'])] = float(row['Rate'])
    return rates

def consolidate_group(manifest_path):
    """Read a group manifest, translate each member's ledger into the group's
    reporting currency, and write a single consolidated CSV to outputs/.
    Returns (consolidated_csv_path, group_name, reporting_currency).
    """
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    group_name = manifest['group_name']
    reporting_ccy = manifest['reporting_currency']
    period = manifest.get('period', 'FY25')
    ledgers_dir = os.path.dirname(manifest_path)

    fx_path = os.path.join(ledgers_dir, manifest.get('fx_rate_source', 'fx_rates.csv'))
    fx = _load_fx_rates(fx_path)

    members = [manifest['parent']] + manifest.get('subsidiaries', [])
    consolidated_rows = []

    for member in members:
        member_csv = os.path.join(ledgers_dir, member['file'])
        functional_ccy = member['functional_currency']
        df = pd.read_csv(member_csv)
        for _, row in df.iterrows():
            row_ccy = row.get('Currency', functional_ccy)
            if pd.isna(row_ccy):
                row_ccy = functional_ccy
            amount = float(row['Amount'])
            if row_ccy == reporting_ccy:
                translated = amount
            else:
                key = (row_ccy, reporting_ccy, period)
                if key not in fx:
                    raise ValueError(
                        f"FX rate missing for {row_ccy} -> {reporting_ccy} @ {period} "
                        f"(needed for {member_csv}). Add row to {fx_path}.")
                translated = amount * fx[key]
            consolidated_rows.append({
                'Transaction_ID': f"{member.get('name', os.path.basename(member_csv))[:6]}-{row['Transaction_ID']}",
                'Date': row['Date'],
                'Account_Name': row['Account_Name'],
                'Description': f"[{row_ccy}->{reporting_ccy}] {row['Description']}" if row_ccy != reporting_ccy else row['Description'],
                'Amount': round(translated, 2),
                'Currency': reporting_ccy,
            })

    consolidated_df = pd.DataFrame(consolidated_rows)
    os.makedirs('outputs', exist_ok=True)
    out_path = os.path.join('outputs', f"{group_name}_consolidated_{period}.csv")
    consolidated_df.to_csv(out_path, index=False)
    return out_path, group_name, reporting_ccy

def run_all_ledgers():
    print("===========================================================================")
    print(" 🚀 RUNNING FULL 7-POINT THERMODYNAMIC SAFEGUARD AGAINST ALL GLs")
    print("    (Points 1-6: Python; Point 7: engine/consolidation.pl shadow-check)")
    print("===========================================================================\n")

    # Discover legacy single-entity CSVs and multi-entity group manifests.
    csv_files = sorted(glob.glob('data/sample_ledgers/*.csv'))
    csv_files = [f for f in csv_files
                 if 'Div7A' not in f
                 and 'HP_Standard' not in f
                 and not f.endswith('fx_rates.csv')
                 and 'GL_06_Acme_AU_Pty_Ltd' not in f       # Member of GL_06 group
                 and 'GL_06_Acme_UK_Ltd' not in f]          # (rendered via manifest)
    manifest_files = sorted(glob.glob('data/sample_ledgers/*_consolidated.yaml'))

    success_count = 0
    fail_count = 0

    # --- Legacy single-entity ledgers ---
    for csv_file in csv_files:
        client_name = os.path.basename(csv_file).replace('.csv', '')
        df_check = pd.read_csv(csv_file)
        if len(df_check) > 250:
            print(f"⚠️ [{client_name}] BLOCKED: Dataset too large ({len(df_check)} rows). Capped at 250 rows until semantic routing is integrated.")
            fail_count += 1
            continue

        json_ld = generate_sbrm_jsonld(csv_file)
        if pre_flight_audit(json_ld['Accounts'], csv_file, client_name):
            success_count += 1
        else:
            fail_count += 1

    # --- Group manifests (S2: multi-currency consolidation) ---
    for manifest_file in manifest_files:
        try:
            consolidated_csv, group_name, _ = consolidate_group(manifest_file)
            print(f"🌐 [{group_name}] Consolidated -> {consolidated_csv}")
        except Exception as e:
            print(f"❌ [{os.path.basename(manifest_file)}] Consolidation failed: {e}")
            fail_count += 1
            continue

        df_check = pd.read_csv(consolidated_csv)
        if len(df_check) > 250:
            print(f"⚠️ [{group_name}] BLOCKED: Consolidated dataset too large ({len(df_check)} rows).")
            fail_count += 1
            continue

        json_ld = generate_sbrm_jsonld(consolidated_csv)
        if pre_flight_audit(json_ld['Accounts'], consolidated_csv, group_name):
            success_count += 1
        else:
            fail_count += 1

    print("\n===========================================================================")
    print(f" PIPELINE COMPLETE | ✅ {success_count} Passed | ❌ {fail_count} Aborted")
    print("===========================================================================")

if __name__ == '__main__':
    run_all_ledgers()