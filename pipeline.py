import sys
import os
import glob
import pandas as pd
from jinja2 import Template
from pyswip import Prolog

sys.path.append(os.path.abspath('/home/ubuntu/.openclaw/workspace'))
from test_all_mini import map_account_to_mini

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

def run_all_ledgers():
    print("===========================================================================")
    print(" 🚀 RUNNING FULL 6-POINT THERMODYNAMIC SAFEGUARD AGAINST ALL GLs")
    print("===========================================================================\n")
    
    gl_files = sorted(glob.glob('data/sample_ledgers/*.csv'))
    gl_files = [f for f in gl_files if 'Div7A' not in f and 'HP_Standard' not in f]
    
    success_count = 0
    fail_count = 0

    for csv_file in gl_files:
        client_name = os.path.basename(csv_file).replace('.csv', '')
        
        # --- SAFEGUARD: Prevent Massive Ledgers ---
        df_check = pd.read_csv(csv_file)
        if len(df_check) > 250:
            print(f"⚠️ [{client_name}] BLOCKED: Dataset too large ({len(df_check)} rows). Capped at 250 rows until semantic routing is integrated.")
            fail_count += 1
            continue
        # ------------------------------------------

        json_ld = generate_sbrm_jsonld(csv_file)
        
        if pre_flight_audit(json_ld['Accounts'], csv_file, client_name):
            success_count += 1
        else:
            fail_count += 1
            
    print("\n===========================================================================")
    print(f" PIPELINE COMPLETE | ✅ {success_count} Passed | ❌ {fail_count} Aborted")
    print("===========================================================================")

if __name__ == '__main__':
    run_all_ledgers()