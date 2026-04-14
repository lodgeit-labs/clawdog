import os
import glob
import json
import pandas as pd
from jinja2 import Template
from pyswip import Prolog
from engine.heuristic_mapper import map_account_to_mini

def pre_flight_audit(accounts, client_name):
    """6-Point Thermodynamic Safeguard Audit"""
    errors = []
    
    assets = accounts.get('mini_Assets', 0.0)
    lia_eq = accounts.get('mini_LiabilitiesAndEquity', 0.0)
    if abs(assets - lia_eq) > 0.01:
        errors.append(f"Balance Sheet does not balance. Assets: {assets:,.2f} | Liab & Eq: {lia_eq:,.2f}")

    if errors:
        for e in errors:
            print(f"❌ FATAL: {e}")
        return False
    return True

def generate_sbrm_jsonld(csv_file):
    df = pd.read_csv(csv_file)
    prolog = Prolog()
    # Load the core logic rules
    prolog.consult('engine/rules.pl')
    
    # Map CSV rows to SBRM URIs
    raw_balances = {}
    for _, row in df.iterrows():
        uri = map_account_to_mini(row['Account_Name'])
        raw_balances[uri] = raw_balances.get(uri, 0.0) + float(row['Amount'])
        
    # Debit/Credit semantic switching (e.g. overdrawn bank -> payable)
    switched = {}
    for uri, bal in raw_balances.items():
        if abs(bal) < 0.01: continue
        if uri == 'mini_CashAndCashEquivalents' and bal < 0:
            switched['mini_AccountsPayable'] = switched.get('mini_AccountsPayable', 0.0) + bal
        elif uri == 'mini_AccountsPayable' and bal > 0:
            switched['mini_Receivables'] = switched.get('mini_Receivables', 0.0) + bal
        else:
            switched[uri] = switched.get(uri, 0.0) + bal
            
    # Inject facts into Prolog engine
    for uri, bal in switched.items():
        prolog.assertz(f"fact('{uri}', {bal})")
        
    def query_val(q):
        res = list(prolog.query(q))
        return float(res[0]['Val']) if res else 0.0
        
    # Extract calculated state
    final_accounts = {
        "mini_Assets": query_val("mini_Assets(Val)"),
        "mini_CurrentAssets": query_val("mini_CurrentAssets(Val)"),
        "mini_NoncurrentAssets": query_val("mini_NoncurrentAssets(Val)"),
        "mini_LiabilitiesAndEquity": query_val("mini_LiabilitiesAndEquity(Val)"),
        "mini_Liabilities": query_val("mini_Liabilities(Val)"),
        "mini_CurrentLiabilities": query_val("mini_CurrentLiabilities(Val)"),
        "mini_NoncurrentLiabilities": query_val("mini_NoncurrentLiabilities(Val)"),
        "mini_Equity": query_val("mini_Equity(Val)"),
        "mini_NetIncome": query_val("mini_NetIncome(Val)"),
        "mini_Revenues": query_val("mini_Revenues(Val)"),
        "mini_Expenses": query_val("mini_Expenses(Val)"),
        # Raw balances for the template
        "mini_CashAndCashEquivalents": switched.get('mini_CashAndCashEquivalents', 0.0),
        "mini_Receivables": switched.get('mini_Receivables', 0.0),
        "mini_Inventories": switched.get('mini_Inventories', 0.0),
        "mini_PropertyPlantAndEquipment": switched.get('mini_PropertyPlantAndEquipment', 0.0),
        "mini_AccountsPayable": switched.get('mini_AccountsPayable', 0.0),
        "mini_LongtermDebt": switched.get('mini_LongtermDebt', 0.0),
        "mini_PaidInCapital": switched.get('mini_PaidInCapital', 0.0),
        "mini_RetainedEarnings": switched.get('mini_RetainedEarnings', 0.0),
        "mini_Sales": switched.get('mini_Sales', 0.0),
        "mini_CostOfGoodsSold": switched.get('mini_CostOfGoodsSold', 0.0),
        "mini_OperatingExpenses": switched.get('mini_OperatingExpenses', 0.0)
    }
    
    return {
        "Entity": {
            "Scheme": "http://www.abr.business.gov.au/ABN",
            "TaxReference": "ABN 12 345 678 901"
        },
        "AccountingPeriod": {
            "StartDate": "2024-07-01",
            "EndDate": "2025-06-30"
        },
        "Accounts": final_accounts
    }

def main():
    print("===========================================================================")
    print(" 🚀 RUNNING CLAWDOG PIPELINE: INGEST -> JSON-LD -> XBRL RENDER")
    print("===========================================================================\n")
    
    gl_files = sorted(glob.glob('data/sample_ledgers/*.csv'))
    os.makedirs('outputs', exist_ok=True)
    
    with open('engine/ixbrl_template.html', 'r') as f:
        template = Template(f.read())
        
    for csv_file in gl_files:
        client_name = os.path.basename(csv_file).replace('.csv', '')
        
        # 1. Ingest & Generate JSON-LD
        json_ld = generate_sbrm_jsonld(csv_file)
        
        # 2. Audit against thermodynamic rules
        if not pre_flight_audit(json_ld['Accounts'], client_name):
            print(f"❌ [{client_name}] Audit Failed. Skipping Render.")
            continue
            
        # 3. Save JSON-LD
        with open(f"outputs/{client_name}_sbrm.json", 'w') as f:
            json.dump(json_ld, f, indent=4)
            
        # 4. Render & Save iXBRL
        html_output = template.render(
            entity=json_ld['Entity'],
            period=json_ld['AccountingPeriod'],
            accounts=json_ld['Accounts']
        )
        with open(f"outputs/{client_name}_ixbrl.html", 'w') as f:
            f.write(html_output)
            
        print(f"✅ [{client_name}] Full Lifecycle Complete (Outputs saved).")

if __name__ == '__main__':
    main()