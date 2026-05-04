import os
import re
import glob
import pandas as pd
import yaml
from jinja2 import Template
from pyswip import Prolog

from engine.heuristic_mapper import map_account_to_mini
from engine.yaml_adjustments import parse_adjustment
from engine.jurisdiction_periods import (
    DEFAULT_JURISDICTION as _DEFAULT_JURISDICTION,
    period_meta_for_label as _jurisdiction_period_meta,
)


# ---------------------------------------------------------------------------
# S3: Prolog audit lift — points 1–4 + 6 of the legacy 6-Point Thermodynamic
# Safeguard now live in engine/audit.pl. This Python module is a thin shim
# that derives the audit facts (from the JSON-LD accounts dict and per-row
# CSV equity-rollforward parsing), injects them into the shared
# sbrm_consolidation:sbrm_fact/6 multifile predicate, and queries
# sbrm_audit:audit_all/3 for the structured failure list.
#
# Point 5 (cashflow transaction-flow analysis) stays in Python because the
# current sbrm_fact/6 schema is balance-snapshot-oriented; lifting it would
# require a separate transaction-fact schema (out of S3's scope, marked TODO).
#
# What this lift removes:
#   * The four duplicated arithmetic invariants (points 1–4) previously
#     hand-coded in pre_flight_audit — source of truth is now Prolog.
#   * The S1 Point 7 Prolog/Python shadow-verifier on equity roll-forward.
#     Once point 6 IS Prolog (here), the shadow disappears: there is only
#     one source of truth, no second to disagree with.
#   * verify_equity_via_prolog and the S1 _CONSOLIDATION_LOADED gate — their
#     job is now done by the audit shim's _ensure_audit_loaded gate.
#
# Brain canon: GLOBAL_NOTES/CLAWDOG/107_CONSOLIDATION_LOGIC.md
# Engine:      engine/audit.pl (consults engine/consolidation.pl for the
#              shared sbrm_fact/6 schema).
# ---------------------------------------------------------------------------

_AUDIT_LOADED = False

def _ensure_audit_loaded(prolog):
    """Consult engine/audit.pl (which transitively consults engine/
    consolidation.pl for the shared multifile sbrm_fact/6 predicate) into
    the Prolog database once. Subsequent pyswip Prolog() instances share
    the same database, so a single load suffices for the process."""
    global _AUDIT_LOADED
    if not _AUDIT_LOADED:
        prolog.consult('engine/audit.pl')
        _AUDIT_LOADED = True

_AUDIT_FAILURE_RE = re.compile(
    r'fail\(\s*point\((\d+)\)\s*,\s*([a-z_]+)\s*,\s*\[(.*?)\]\s*\)')

def _format_audit_failure(term_string):
    """Pretty-print one fail(point(N), Reason, Details) term emitted by
    engine/audit.pl::audit_all/3 for inclusion in the audit error list."""
    m = _AUDIT_FAILURE_RE.match(term_string)
    if not m:
        # Defensive: pyswip marshalling shape changed; surface raw term
        # rather than silently formatting it as something else.
        return f"FATAL (audit): unparseable failure term {term_string!r}"
    point, reason, details = m.groups()
    label_map = {
        'tensegrity':           'Balance Sheet Tensegrity Failed',
        'asset_rollup':         'Asset Rollup Failed',
        'liab_equity_rollup':   'Liab & Eq Rollup Failed',
        'pl_net_income':        'P&L Math Failed',
        'equity_rollforward':   'Equity Rollforward Failed',
        'missing_fact':         'Required audit fact missing',
    }
    label = label_map.get(reason, reason)
    return f"FATAL ({point}): {label}. {details}"

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

def _derive_equity_rollforward_scalars(csv_file):
    """Re-parse the raw CSV to extract the three scalars needed for the
    equity roll-forward audit point: opening equity, capital injections,
    and dividends paid. NetIncome is sourced separately from the JSON-LD
    accounts dict; closing equity is mini_Equity from the same source.

    This function exists because the JSON-LD layer aggregates equity into
    a single closing balance; the rollforward components are only
    distinguishable at the per-row level via Description/Account_Name
    heuristics. A future schema cleanup could push these into the
    JSON-LD layer directly; until then, the audit shim re-parses.
    """
    df = pd.read_csv(csv_file)
    opening_eq = 0.0
    cap_inj = 0.0
    divs = 0.0
    for _, row in df.iterrows():
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
    return opening_eq, cap_inj, divs

def _load_and_validate_adjustments(adjustments_dir):
    """Load and validate YAML adjustments from the specified directory."""
    adjustments = []
    for file in os.listdir(adjustments_dir):
        if file.endswith('.yaml'):
            with open(os.path.join(adjustments_dir, file), 'r') as f:
                adjustment = yaml.safe_load(f)
                # Validate the adjustment using the existing logic
                validated_adjustment = parse_adjustment(adjustment)
                adjustments.append(validated_adjustment)
    return adjustments

def _run_prolog_audit(accounts, csv_file, client_name,
                     entity='client', period='current'):
    # NOTE (S5b / Standing Rule #6): callers may pass a real period label
    # (e.g. 'FY25', 'FY24') so the same Prolog database can hold multiple
    # periods of audit facts simultaneously without cross-period leakage.
    # The retractall below is per-(entity, period); see the period atom
    # passed through to the assertz / query.
    """Inject the audit facts derived from `accounts` and `csv_file` into
    sbrm_consolidation:sbrm_fact/6, then query sbrm_audit:audit_all/3 and
    return the formatted failure-message list (empty list on clean pass).

    Standing Rule #3 alignment: Python defaults `accounts.get(..., 0.0)`
    are preserved here for the mini_* concepts because the legacy
    pipeline already projected JSON-LD nulls as zeros at the json_ld
    layer. The audit lift is faithful to that legacy semantic; tightening
    to no-silent-zero at the mini layer is a separate sprint (would
    require json_ld emission to fail loudly on missing concepts too).
    """
    # Use a per-client entity atom so concurrent ledgers can coexist in
    # the shared Prolog database without leakage. Sanitise to atoms.
    entity_atom = re.sub(r'[^A-Za-z0-9_]', '_', client_name)

    # Load and validate adjustments
    adjustments = _load_and_validate_adjustments('data/sample_ledgers/adjustments')

    prolog = Prolog()

    # Assert adjustments into Prolog
    for adj in adjustments:
        if adj.entity == client_name and adj.period == period:
            for posting in adj.postings:
                prolog.assertz(
                    f"sbrm_consolidation:sbrm_fact('{entity_atom}',"
                    f"'{period}','{posting.concept}',{posting.amount},"
                    f"'ADJ','{posting.direction}')")
    _ensure_audit_loaded(prolog)

    # Use a per-client entity atom so concurrent ledgers can coexist in
    # the shared Prolog database without leakage. Sanitise to atoms.
    entity_atom = re.sub(r'[^A-Za-z0-9_]', '_', client_name)

    # Clean any prior asserts in the consolidation namespace for this
    # entity at this period only — leave other periods alone so the same
    # process can audit FY25 and FY24 (S5b) without losing the prior pass.
    period_atom = re.sub(r'[^A-Za-z0-9_]', '_', str(period))
    list(prolog.query(
        f"retractall(sbrm_consolidation:sbrm_fact('{entity_atom}','{period_atom}',_,_,_,_))"))
    period = period_atom

    # Project mini_* accounts into facts. Concepts the audit predicates
    # consume are listed explicitly so unrelated noise in the JSON-LD
    # dict doesn't pollute the audit fact base.
    audit_concepts = [
        'mini_Assets', 'mini_CurrentAssets', 'mini_NoncurrentAssets',
        'mini_LiabilitiesAndEquity', 'mini_Liabilities', 'mini_Equity',
        'mini_Sales', 'mini_CostOfGoodsSold', 'mini_OperatingExpenses',
        'mini_NonoperatingIncomeExpense', 'mini_NetIncomeLoss',
    ]
    for concept in audit_concepts:
        if concept not in accounts:
            # Match legacy Python semantic: mini_* missing → treat as 0.0.
            # (See Standing-Rule-#3 note in the function docstring.)
            value = 0.0
        else:
            value = float(accounts[concept])
        list(prolog.query(
            f"assertz(sbrm_consolidation:sbrm_fact('{entity_atom}',"
            f"'{period}','{concept}',{value},'AUD','Leaf'))"))

    # Equity-rollforward scalars derived from the CSV. These are the
    # audit_* concepts (deliberately distinct from mini_* to make it
    # explicit they are audit-only inputs, not part of the public mini
    # ontology surface).
    opening_eq, cap_inj, divs = _derive_equity_rollforward_scalars(csv_file)
    rollforward_facts = [
        ('audit_OpeningEquity',     opening_eq),
        ('audit_CapitalInjections', cap_inj),
        ('audit_DividendsPaid',     divs),
    ]
    for concept, value in rollforward_facts:
        list(prolog.query(
            f"assertz(sbrm_consolidation:sbrm_fact('{entity_atom}',"
            f"'{period}','{concept}',{float(value)},'AUD','Leaf'))"))

    # Run the aggregator. audit_all/3 binds Failures to a (possibly empty)
    # list of fail(point(N), Reason, Details) terms.
    query = f"sbrm_audit:audit_all('{entity_atom}','{period}',Failures)"
    results = list(prolog.query(query))
    if not results:
        # Should never happen — audit_all/3 always succeeds with at least
        # an empty Failures list. Surface explicitly rather than silently.
        return ["FATAL (audit): sbrm_audit:audit_all/3 returned no solution"]
    failures = results[0]['Failures']
    return [_format_audit_failure(term) for term in failures]

def pre_flight_audit(accounts, csv_file, client_name, period='current'):
    """
    THE 6-POINT STRICT SBRM THERMODYNAMIC SAFEGUARD (S3 Prolog-lifted form).

    Points 1–4 + 6 are now Prolog rules in engine/audit.pl, queried via
    _run_prolog_audit. Point 5 (cashflow transaction-flow) stays in Python
    pending a transaction-fact schema (TODO in this function).

    S5b: `period` (default `'current'` for legacy single-period callers) is
    plumbed all the way to the Prolog fact base so multiple periods can
    coexist in the shared database during a comparative-period run.
    """
    errors = []

    # Points 1–4 + 6 — Prolog audit lift.
    try:
        prolog_failures = _run_prolog_audit(
            accounts, csv_file, client_name, period=period)
        errors.extend(prolog_failures)
    except Exception as e:
        errors.append(f"FATAL (audit): Prolog audit shim error: {e}")

    # Point 5 — Cashflow integrity.
    # TODO: lift to Prolog once a transaction-fact schema lands. The current
    # sbrm_fact/6 schema is balance-snapshot-oriented; cashflow validation
    # requires per-transaction analysis (which non-cash accounts moved
    # alongside each cash movement) which doesn't fit cleanly without a
    # new fact shape. Tracked as a future sprint.
    try:
        stated_ni = float(accounts.get('mini_NetIncomeLoss', 0.0))
        calc_cash, _calc_equity = calculate_cashflow_and_equity(csv_file, stated_ni)
        df = pd.read_csv(csv_file)
        actual_raw_cash = df[df['Account_Name'].apply(
            lambda x: map_account_to_mini(x) == 'mini_CashAndCashEquivalents'
        )]['Amount'].sum()
        if abs(calc_cash - actual_raw_cash) > 0.01:
            errors.append(
                f"FATAL (5): Cashflow Integrity Failed. "
                f"Calculated Ending Cash: {calc_cash:,.2f} | "
                f"Actual Ledger Cash: {actual_raw_cash:,.2f}")
    except Exception as e:
        errors.append(f"FATAL (5): Error calculating cashflow flow: {e}")

    if errors:
        print(f"\n❌ [{client_name}] 6-POINT AUDIT FAILED. ABORTING RENDER.")
        for err in errors:
            print(f"  -> {err}")
        return False

    print(f"✅ [{client_name}] 6-Point Audit Passed. Thermodynamic Integrity Verified.")
    return True

def generate_sbrm_jsonld(csv_file, period_meta=None):
    """Build the SBRM JSON-LD for a single CSV. `period_meta` is an optional
    dict carrying explicit period dates (`StartDate`, `EndDate`, `period_label`).
    When omitted, the legacy FY25 defaults are used so existing single-period
    callers see zero behavioural change. S5b passes per-period metadata so
    comparatives don't all share the same accounting period."""
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

    if period_meta is None:
        accounting_period = {
            "StartDate": "2024-07-01",
            "EndDate":   "2025-06-30",
            "PeriodLabel": "FY25",
        }
    else:
        accounting_period = {
            "StartDate":   period_meta.get('StartDate', '2024-07-01'),
            "EndDate":     period_meta.get('EndDate',   '2025-06-30'),
            "PeriodLabel": period_meta.get('PeriodLabel', 'FY25'),
        }

    return {
        "@context": "https://xbrlsite.azurewebsites.net/seattlemethod/platinum/mini",
        "@type": "StatutoryAccounts",
        "Entity": {
            "CompanyName": client_name,
            "TaxReference": "ABN 12 345 678 901"
        },
        "AccountingPeriod": accounting_period,
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

def _consolidate_member_set(period, members, reporting_ccy, fx, ledgers_dir,
                            fx_path):
    """Translate a parent + subsidiaries member set into the reporting
    currency for `period` and return the consolidated row list. Shared by
    both the current-period and comparative-period passes (S5b)."""
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
            entity_label = (member.get('name')
                            or os.path.basename(member_csv))
            consolidated_rows.append({
                'Transaction_ID': f"{entity_label[:6]}-{row['Transaction_ID']}",
                'Date': row['Date'],
                'Account_Name': row['Account_Name'],
                'Description': f"[{row_ccy}->{reporting_ccy}] {row['Description']}" if row_ccy != reporting_ccy else row['Description'],
                'Amount': round(translated, 2),
                'Currency': reporting_ccy,
            })
    return consolidated_rows

def _resolve_comparative_members(manifest):
    """S5b: build the comparator member-set from the manifest's `comparative`
    block. Each comparator entity inherits its functional_currency from the
    current-period sibling (matched by `name` for subsidiaries; parent is
    matched positionally). Returns (period, period_meta, members) or None
    if no comparative is declared.

    Standing Rule #3: missing comparator file declarations FAIL loud. A
    manifest that declares a `comparative` block must declare a comparator
    for the parent and every subsidiary; partial declarations are rejected.
    """
    comp = manifest.get('comparative')
    if not comp:
        return None

    if 'parent' not in comp or 'file' not in comp.get('parent', {}):
        raise ValueError(
            "Manifest declares `comparative` but is missing a parent file. "
            "Required: comparative.parent.file")

    current_subs = manifest.get('subsidiaries', [])
    comp_subs_decl = comp.get('subsidiaries', [])
    if len(comp_subs_decl) != len(current_subs):
        raise ValueError(
            f"Manifest declares {len(current_subs)} current-period "
            f"subsidiaries but {len(comp_subs_decl)} comparator subsidiaries. "
            f"Each subsidiary must have a comparator file.")

    # Match comparator subsidiaries to current ones by `name`. Standing
    # Rule #3 again: ambiguous or missing matches fail loud rather than
    # silently picking the wrong file.
    by_name = {s.get('name'): s for s in current_subs}
    members = [{
        'file': comp['parent']['file'],
        'functional_currency': manifest['parent']['functional_currency'],
        'name': manifest['parent'].get('name'),
    }]
    for cs in comp_subs_decl:
        name = cs.get('name')
        if name not in by_name:
            raise ValueError(
                f"Comparator subsidiary name {name!r} does not match any "
                f"current-period subsidiary in this manifest.")
        members.append({
            'file': cs['file'],
            'functional_currency': by_name[name]['functional_currency'],
            'name': name,
            'ownership': by_name[name].get('ownership', 1.0),
        })

    period = comp.get('period', 'FY24')
    period_meta = {
        'PeriodLabel': period,
        'StartDate':   comp.get('period_start', '2023-07-01'),
        'EndDate':     comp.get('period_end',   '2024-06-30'),
    }
    return period, period_meta, members

def consolidate_group(manifest_path):
    """Read a group manifest, translate each member's ledger into the group's
    reporting currency, and write a consolidated CSV to outputs/. When the
    manifest declares a `comparative` block (S5b), also produce a comparator
    consolidated CSV.

    Returns a dict:
        {
          'group_name':        str,
          'reporting_currency': str,
          'current': {
             'csv':         <path>,
             'period':      <label>,
             'period_meta': {StartDate, EndDate, PeriodLabel},
          },
          'comparative': None | {
             'csv':         <path>,
             'period':      <label>,
             'period_meta': {StartDate, EndDate, PeriodLabel},
          }
        }
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
    current_period_meta = {
        'PeriodLabel': period,
        'StartDate':   manifest.get('period_start', '2024-07-01'),
        'EndDate':     manifest.get('period_end',   '2025-06-30'),
    }

    consolidated_rows = _consolidate_member_set(
        period, members, reporting_ccy, fx, ledgers_dir, fx_path)
    os.makedirs('outputs', exist_ok=True)
    current_out = os.path.join('outputs', f"{group_name}_consolidated_{period}.csv")
    pd.DataFrame(consolidated_rows).to_csv(current_out, index=False)

    result = {
        'group_name': group_name,
        'reporting_currency': reporting_ccy,
        'current': {
            'csv':         current_out,
            'period':      period,
            'period_meta': current_period_meta,
        },
        'comparative': None,
    }

    comp = _resolve_comparative_members(manifest)
    if comp is not None:
        comp_period, comp_period_meta, comp_members = comp
        comp_rows = _consolidate_member_set(
            comp_period, comp_members, reporting_ccy, fx, ledgers_dir, fx_path)
        comp_out = os.path.join(
            'outputs', f"{group_name}_consolidated_{comp_period}.csv")
        pd.DataFrame(comp_rows).to_csv(comp_out, index=False)
        result['comparative'] = {
            'csv':         comp_out,
            'period':      comp_period,
            'period_meta': comp_period_meta,
        }

    return result

# ---------------------------------------------------------------------------
# S4: iXBRL provenance trails consuming consolidation_evidence/6.
#
# After a group's audit passes, the renderer queries engine/consolidation.pl's
# consolidation_evidence/6 predicate to produce a per-row, per-member,
# per-currency provenance trail. Each non-reporting-currency fact contributed
# by a member entity is rendered as a Translation Note row showing source
# value, FX rate, and the AUD-translated contribution.
#
# Crucially: the rendered values are emitted by Prolog, not recomputed by the
# Python renderer. The Python layer only shapes presentation. This is what
# makes the provenance trail authoritative — it's the same predicate that
# would back a helm_mutations cryptographic anchor.
#
# Sub-option B.i (Translation Note section): smallest-scope, highest-demo-value
# slice of the iXBRL provenance story. Inline `<aria-describedby>` (B.ii) and
# side-by-side dual-currency columns (B.iii) are future sprints.
#
# Brain canon: GLOBAL_NOTES/CLAWDOG/107_CONSOLIDATION_LOGIC.md
# Engine:      engine/consolidation.pl::consolidation_evidence/6
# ---------------------------------------------------------------------------

_EVIDENCE_RE = re.compile(
    r'evidence\(\s*([^,]+?)\s*,\s*([^,]+?)\s*,\s*([^,]+?)\s*,'
    r'\s*([^,]+?)\s*,\s*([^,]+?)\s*,\s*([^)]+?)\s*\)'
)

def _parse_evidence_term(term_string):
    """Parse a single 'evidence(Concept, SrcCcy, SrcVal, Wt, FxRate, Contrib)'
    term as returned by pyswip into a structured dict. pyswip marshals
    compound terms as their string repr; we don't risk evaluating them, we
    parse positionally."""
    m = _EVIDENCE_RE.match(term_string)
    if not m:
        raise ValueError(f"Unparseable evidence term: {term_string!r}")
    concept, src_ccy, src_val, weight, fx_rate, contribution = m.groups()
    return {
        'concept': concept.strip(),
        'source_currency': src_ccy.strip(),
        'source_value': float(src_val),
        'weight': float(weight),
        'fx_rate': float(fx_rate),
        'contribution': float(contribution),
    }

def build_translation_evidence(manifest_path, period_override=None,
                              members_override=None):
    """Run engine/consolidation.pl::consolidation_evidence/6 over each member
    entity's ledger, collecting every non-reporting-currency fact and its
    translation into the group's reporting currency.

    Returns (evidence_rows, total_contribution) where evidence_rows is a list
    of dicts (one per non-reporting-currency source fact, keyed by entity name,
    concept, source_currency, source_value, fx_rate, contribution) and
    total_contribution is the sum of contributions across all rows. Returns
    ([], 0.0) if no non-reporting-currency facts exist.

    `period_override` and `members_override` (S5b): when supplied, run the
    evidence collection against the given period + member list rather than
    the manifest's current-period block. Used to produce comparator-period
    Translation Note totals without duplicating this 70-line function.

    The evidence is sourced from Prolog — not recomputed in Python — so the
    rendered Translation Note is authoritative against engine/consolidation.pl.
    """
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    reporting_ccy = manifest['reporting_currency']
    period = period_override or manifest.get('period', 'FY25')
    ledgers_dir = os.path.dirname(manifest_path)
    fx_path = os.path.join(
        ledgers_dir, manifest.get('fx_rate_source', 'fx_rates.csv'))
    fx_rates = _load_fx_rates(fx_path)

    if members_override is not None:
        members = members_override
    else:
        members = [manifest['parent']] + manifest.get('subsidiaries', [])

    prolog = Prolog()
    _ensure_audit_loaded(prolog)

    evidence_rows = []
    total = 0.0

    for member in members:
        functional_ccy = member['functional_currency']
        if functional_ccy == reporting_ccy:
            # No translation needed; nothing for the Translation Note.
            continue

        member_csv = os.path.join(ledgers_dir, member['file'])
        entity_name = member.get('name', os.path.basename(member_csv))
        entity_atom = re.sub(r"[^A-Za-z0-9_]", '_', entity_name)

        # Clean any prior asserts in the consolidation namespace for this
        # entity (idempotent across multiple ledgers in one process).
        list(prolog.query(
            f"retractall(sbrm_consolidation:sbrm_fact('{entity_atom}',_,_,_,_,_))"))
        list(prolog.query(
            f"retractall(sbrm_consolidation:fx_rate(_,_,_,_))"))

        # Inject FX rates relevant to this period.
        for (src, tgt, per), rate in fx_rates.items():
            if per != period:
                continue
            list(prolog.query(
                f"assertz(sbrm_consolidation:fx_rate('{src}','{tgt}','{per}',{rate}))"))

        # Inject one sbrm_fact per non-reporting-currency CSV row, keyed by
        # the heuristic-mapped mini_* concept. We aggregate by concept first
        # so the Translation Note has one row per (entity, concept), not one
        # per raw transaction line — matches what an auditor expects to see.
        df = pd.read_csv(member_csv)
        per_concept = {}
        for _, row in df.iterrows():
            row_ccy = row.get('Currency', functional_ccy)
            if pd.isna(row_ccy):
                row_ccy = functional_ccy
            if row_ccy == reporting_ccy:
                continue
            concept = map_account_to_mini(row['Account_Name'])
            key = (concept, row_ccy)
            per_concept[key] = per_concept.get(key, 0.0) + float(row['Amount'])

        # Drop near-zero aggregates (offsetting transactions cancelling out).
        for (concept, src_ccy), value in list(per_concept.items()):
            if abs(value) < 0.01:
                continue
            list(prolog.query(
                f"assertz(sbrm_consolidation:sbrm_fact('{entity_atom}',"
                f"'{period}','{concept}',{value},'{src_ccy}','Leaf'))"))

        # Query consolidation_evidence/6 once per (concept, src_ccy) tuple.
        # With a leaf-only graph (no sbrm_edge entries for these concepts),
        # consolidation_evidence/6 returns the concept's own injected fact
        # as a single evidence row with the FX rate applied.
        for (concept, src_ccy), _value in per_concept.items():
            if abs(_value) < 0.01:
                continue
            query = (
                f"sbrm_consolidation:consolidation_evidence('{entity_atom}',"
                f"'{period}','{reporting_ccy}','{concept}',Total,Evidence)")
            results = list(prolog.query(query))
            if not results:
                # Should not happen — every injected fact should produce
                # evidence — but if it does, surface explicitly rather than
                # silently dropping.
                raise RuntimeError(
                    f"consolidation_evidence/6 returned no rows for "
                    f"({entity_atom}, {period}, {concept}). Likely missing "
                    f"FX rate {src_ccy} -> {reporting_ccy} @ {period}.")
            for term in results[0]['Evidence']:
                row = _parse_evidence_term(term)
                row['entity'] = entity_name
                evidence_rows.append(row)
                total += row['contribution']

    return evidence_rows, total

def render_ixbrl(json_ld, output_path, translation_evidence=None,
                 translation_evidence_total=0.0,
                 comparative_json_ld=None,
                 comparative_translation_evidence_total=None):
    """Render the iXBRL template against a JSON-LD result and (optionally) a
    Translation Note evidence list.

    S5b: when `comparative_json_ld` is supplied, the template emits prior-
    period columns alongside the current period. Each ix:nonFraction cell is
    paired with a sibling cell carrying contextRef="*-prior" and the
    comparative period gets its own xbrli:context block in the hidden header.
    Translation Note (option c): current-period only, comparative summary as
    footer text.

    Writes the rendered HTML to output_path and returns the rendered string.
    """
    template_path = os.path.join('engine', 'ixbrl_template.html')
    with open(template_path) as f:
        template_src = f.read()
    template = Template(template_src)

    # Provide accounts as an attribute-style dict so {{ accounts.mini_X }}
    # resolves cleanly. Jinja2's default dict access gives us this via
    # __getitem__; the template already uses dotted access, so we wrap.
    class _Attrs(dict):
        def __getattr__(self, k):
            return self.get(k, 0.0)

    accounts = _Attrs({k: v for k, v in json_ld['Accounts'].items()})
    entity = _Attrs(json_ld['Entity'])
    period = _Attrs({
        'StartDate':   json_ld['AccountingPeriod']['StartDate'],
        'EndDate':     json_ld['AccountingPeriod']['EndDate'],
        'PeriodLabel': json_ld['AccountingPeriod'].get('PeriodLabel', 'FY25'),
    })

    if comparative_json_ld is not None:
        comparative_accounts = _Attrs({
            k: v for k, v in comparative_json_ld['Accounts'].items()
        })
        comparative_period = _Attrs({
            'StartDate':   comparative_json_ld['AccountingPeriod']['StartDate'],
            'EndDate':     comparative_json_ld['AccountingPeriod']['EndDate'],
            'PeriodLabel': comparative_json_ld['AccountingPeriod'].get(
                'PeriodLabel', 'FY24'),
        })
    else:
        comparative_accounts = None
        comparative_period = None

    rendered = template.render(
        entity=entity,
        period=period,
        accounts=accounts,
        translation_evidence=translation_evidence,
        translation_evidence_total=translation_evidence_total,
        comparative_accounts=comparative_accounts,
        comparative_period=comparative_period,
        comparative_translation_evidence_total=(
            comparative_translation_evidence_total),
    )
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(rendered)
    return rendered

_FY_SUFFIX_RE = re.compile(r'^(?P<base>.+)_FY(?P<yy>\d{2})\.csv$')

def _discover_single_entity_comparator(csv_path):
    """S5b: filename-convention comparator discovery for single-entity
    ledgers. If `csv_path` ends in `_FYxx.csv` and a sibling `_FY(xx-1).csv`
    exists in the same directory, return (comparator_path, current_period,
    comparator_period). Otherwise return None.

    The convention is intentionally narrow: only `_FYxx` (two-digit) is
    recognised. `xx` decrements by one for the comparator. No support for
    irregular fiscal-year labels in this sprint.
    """
    base = os.path.basename(csv_path)
    m = _FY_SUFFIX_RE.match(base)
    if not m:
        return None
    base_stem = m.group('base')
    yy = int(m.group('yy'))
    current_period = f"FY{yy:02d}"
    comparator_period = f"FY{(yy - 1):02d}"
    comparator_name = f"{base_stem}_{comparator_period}.csv"
    comparator_path = os.path.join(os.path.dirname(csv_path), comparator_name)
    if not os.path.exists(comparator_path):
        return None
    return comparator_path, current_period, comparator_period

def _period_meta_for_label(period_label, jurisdiction=_DEFAULT_JURISDICTION):
    """Map a fiscal-year label like `FY25` to a period_meta dict under
    the given jurisdiction's date convention.

    S5c: this is now a thin wrapper around
    ``engine.jurisdiction_periods.period_meta_for_label`` so the same
    AU/UK/US lookup serves the rest of the pipeline. Default jurisdiction
    is ``'AU'`` so existing single-entity ledgers (no sidecar present)
    see exactly the AU date convention they had pre-S5c.

    Used for single-entity ledgers; group manifests carry explicit
    period_start/period_end dates and bypass this helper entirely.
    """
    return _jurisdiction_period_meta(period_label, jurisdiction)


_META_SIDECAR_RE = re.compile(r'\.csv$')


def _jurisdiction_for_csv(csv_path):
    """S5c: discover the jurisdiction for a single-entity ledger via an
    optional ``<basename>_meta.yaml`` sidecar next to the CSV.

    The sidecar is opt-in. When absent, the default jurisdiction
    (``'AU'``) is returned, preserving legacy behaviour exactly. When
    present, the YAML must declare a top-level ``jurisdiction:`` key
    whose value is one of the supported jurisdictions; an unknown
    value raises ``ValueError`` rather than silently defaulting
    (Standing Rule #3).

    Sidecar shape (minimal):

        # GL_07_demo_FY25_meta.yaml
        jurisdiction: UK

    Group manifests are unaffected by this helper — they carry
    explicit ``period_start`` / ``period_end`` dates and do not need
    a jurisdiction lookup.
    """
    sidecar_path = _META_SIDECAR_RE.sub('_meta.yaml', csv_path)
    if not os.path.exists(sidecar_path):
        return _DEFAULT_JURISDICTION
    with open(sidecar_path, 'r', encoding='utf-8') as fh:
        meta = yaml.safe_load(fh) or {}
    juris = meta.get('jurisdiction', _DEFAULT_JURISDICTION)
    # Validate eagerly; period_meta_for_label would raise on first call
    # otherwise, but raising at sidecar-read time gives a clearer error.
    _jurisdiction_period_meta('FY25', juris)   # validation probe
    return juris

def run_all_ledgers():
    print("===========================================================================")
    print(" 🚀 RUNNING FULL 6-POINT THERMODYNAMIC SAFEGUARD AGAINST ALL GLs")
    print("    (Points 1-4 + 6: engine/audit.pl; Point 5: Python cashflow shim)")
    print("===========================================================================\n")

    # Discover legacy single-entity CSVs and multi-entity group manifests.
    csv_files = sorted(glob.glob('data/sample_ledgers/*.csv'))
    csv_files = [f for f in csv_files
                 if 'Div7A' not in f
                 and 'HP_Standard' not in f
                 and not f.endswith('fx_rates.csv')
                 and 'GL_06_Acme_AU_Pty_Ltd' not in f       # Member of GL_06 group
                 and 'GL_06_Acme_UK_Ltd' not in f]          # (rendered via manifest)
    # S5b: when a `_FYxx.csv` ledger has a `_FY(xx-1).csv` sibling, the
    # sibling is rendered as the comparative-period column on the current-
    # period output, not as a standalone artifact.
    comparator_paths = set()
    for f in csv_files:
        info = _discover_single_entity_comparator(f)
        if info is not None:
            comparator_paths.add(info[0])
    csv_files = [f for f in csv_files if f not in comparator_paths]
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

        # S5b: discover comparator. If present, audit both periods
        # independently and pass both to the renderer.
        comp_info = _discover_single_entity_comparator(csv_file)
        comp_json_ld = None
        comp_failed = False
        current_period_label = 'current'
        current_period_meta = None
        if comp_info is not None:
            comp_csv, current_period_label, comp_period_label = comp_info
            # S5c: jurisdiction comes from the optional sidecar; both the
            # current period and the comparator period share the same
            # jurisdiction (an entity does not change tax jurisdiction
            # between adjacent fiscal years in this demo).
            ledger_jurisdiction  = _jurisdiction_for_csv(csv_file)
            current_period_meta  = _period_meta_for_label(current_period_label,
                                                          ledger_jurisdiction)
            comp_period_meta     = _period_meta_for_label(comp_period_label,
                                                          ledger_jurisdiction)
            comp_json_ld = generate_sbrm_jsonld(comp_csv, comp_period_meta)
            comp_client = os.path.basename(comp_csv).replace('.csv', '')
            print(f"🔁 [{client_name}] Comparator detected -> {comp_csv}"
                  f" ({comp_period_label})")
            if not pre_flight_audit(comp_json_ld['Accounts'], comp_csv,
                                    comp_client, period=comp_period_label):
                print(f"   ❌ [{comp_client}] Comparator audit FAILED — "
                      f"comparative columns will be omitted.")
                comp_json_ld = None
                comp_failed = True

        json_ld = generate_sbrm_jsonld(csv_file, current_period_meta)
        if pre_flight_audit(json_ld['Accounts'], csv_file, client_name,
                            period=current_period_label):
            success_count += 1
            # S4: render iXBRL with no Translation Note (single-currency).
            # S5b: include comparative columns when comp_json_ld available.
            try:
                out_html = os.path.join('outputs', f"{client_name}.html")
                render_ixbrl(json_ld, out_html,
                             comparative_json_ld=comp_json_ld)
                comp_tag = (
                    f" + comparative {comp_info[2]}"
                    if (comp_info is not None and comp_json_ld is not None)
                    else (" (comparator audit failed; current-period only)"
                          if comp_failed else ""))
                print(f"   📄 [{client_name}] iXBRL rendered -> {out_html}"
                      f"{comp_tag}")
            except Exception as e:
                print(f"   ⚠️ [{client_name}] iXBRL render failed: {e}")
        else:
            fail_count += 1

    # --- Group manifests (S2: multi-currency consolidation; S5b: comparatives) ---
    for manifest_file in manifest_files:
        try:
            group = consolidate_group(manifest_file)
        except Exception as e:
            print(f"❌ [{os.path.basename(manifest_file)}] Consolidation failed: {e}")
            fail_count += 1
            continue

        group_name = group['group_name']
        current = group['current']
        comparative = group['comparative']
        comp_meta_msg = (f" + comparator {comparative['period']} "
                         f"-> {comparative['csv']}" if comparative else "")
        print(f"🌐 [{group_name}] Consolidated {current['period']} -> "
              f"{current['csv']}{comp_meta_msg}")

        df_check = pd.read_csv(current['csv'])
        if len(df_check) > 250:
            print(f"⚠️ [{group_name}] BLOCKED: Consolidated dataset too "
                  f"large ({len(df_check)} rows).")
            fail_count += 1
            continue

        json_ld = generate_sbrm_jsonld(current['csv'], current['period_meta'])
        json_ld['Entity']['CompanyName'] = group_name

        # Audit comparative period FIRST so its result is known before we
        # report on the current period; comparator failure does NOT block
        # the current-period render but does omit comparative columns.
        comp_json_ld = None
        comp_evidence_total = None
        if comparative is not None:
            comp_df_check = pd.read_csv(comparative['csv'])
            if len(comp_df_check) > 250:
                print(f"⚠️ [{group_name}] BLOCKED comparator: too large.")
            else:
                tmp_comp = generate_sbrm_jsonld(
                    comparative['csv'], comparative['period_meta'])
                tmp_comp['Entity']['CompanyName'] = group_name
                if pre_flight_audit(tmp_comp['Accounts'], comparative['csv'],
                                    f"{group_name}_{comparative['period']}",
                                    period=comparative['period']):
                    comp_json_ld = tmp_comp
                else:
                    print(f"   ❌ [{group_name}] Comparator audit FAILED — "
                          f"comparative columns will be omitted.")

        if pre_flight_audit(json_ld['Accounts'], current['csv'], group_name,
                            period=current['period']):
            success_count += 1
            # S4: render iXBRL with the Translation Note section sourced
            # from engine/consolidation.pl::consolidation_evidence/6.
            # S5b: optional comparative columns + comparative footer total.
            try:
                with open(manifest_file) as f:
                    manifest_doc = yaml.safe_load(f)
                current_members = ([manifest_doc['parent']]
                                   + manifest_doc.get('subsidiaries', []))
                evidence_rows, evidence_total = build_translation_evidence(
                    manifest_file,
                    period_override=current['period'],
                    members_override=current_members)
                if comp_json_ld is not None:
                    comp_resolve = _resolve_comparative_members(manifest_doc)
                    # _resolve_comparative_members returns None if missing;
                    # but we only enter this branch when `comparative` is
                    # truthy, which itself requires the block.
                    _comp_period, _comp_meta, comp_members = comp_resolve
                    _, comp_total = build_translation_evidence(
                        manifest_file,
                        period_override=comparative['period'],
                        members_override=comp_members)
                    comp_evidence_total = comp_total
                out_html = os.path.join('outputs', f"{group_name}_consolidated.html")
                render_ixbrl(json_ld, out_html,
                             translation_evidence=evidence_rows,
                             translation_evidence_total=evidence_total,
                             comparative_json_ld=comp_json_ld,
                             comparative_translation_evidence_total=(
                                 comp_evidence_total))
                comp_tag = (
                    f" + comparative {comparative['period']}"
                    f" (footer total {comp_evidence_total:,.2f})"
                    if comp_json_ld is not None and comp_evidence_total is not None
                    else (" (comparator omitted)" if comparative else ""))
                print(f"   📄 [{group_name}] iXBRL rendered -> {out_html}"
                      f" ({len(evidence_rows)} provenance rows){comp_tag}")
            except Exception as e:
                print(f"   ⚠️ [{group_name}] iXBRL render failed: {e}")
        else:
            fail_count += 1

    print("\n===========================================================================")
    print(f" PIPELINE COMPLETE | ✅ {success_count} Passed | ❌ {fail_count} Aborted")
    print("===========================================================================")

if __name__ == '__main__':
    run_all_ledgers()
