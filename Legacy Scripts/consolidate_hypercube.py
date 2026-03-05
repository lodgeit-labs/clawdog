import os
import yaml

DIR = './01_Ontology'

def read_val(filename):
    path = os.path.join(DIR, filename)
    if not os.path.exists(path): return 0.0
    with open(path, 'r', encoding='utf-8') as f:
        parts = f.read().split('---', 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1])
            magnitude = fm.get('value', fm.get('magnitude', fm.get('fact_value', 0.0)))
            try:
                return float(magnitude)
            except:
                return 0.0
    return 0.0

def update_val(filename, new_val):
    path = os.path.join(DIR, filename)
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---', 2)
    if len(parts) < 3: return
    fm = yaml.safe_load(parts[1])
    fm['value'] = float(new_val)
    new_yaml = yaml.dump(fm, sort_keys=False)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"---\n{new_yaml}---\n{parts[2]}")

def consolidate():
    print("=== INITIATING IDEMPOTENT CONSOLIDATION (v3) ===")
    
    # HARDCODED PHASE 1 ATOMIC BASES TO PREVENT COMPOUNDING
    cash_base = 50000.0
    curr_liab_base = 30000.0
    exp_base = 80000.0
    rev_base = 100000.0
    
    # UPLIFTS
    cash_up = read_val('fact-uplift-cash-at-bank-2026.md')
    ar_up = read_val('fact-uplift-accounts-receivable-2026.md')
    nab_up = read_val('fact-uplift-nab-5510-2026.md')
    
    plant = read_val('fact-plant-at-cost-2026.md')
    acc_dep = read_val('fact-accumulated-depreciation-2026.md')
    
    ap_up = read_val('fact-uplift-accounts-payable-2026.md')
    non_curr_liab = read_val('fact-non-current-liabilities-2026.md')
    
    open_eq = read_val('fact-opening-equity-2025.md')
    cap_intro = read_val('fact-uplift-capital-introduced-2026.md')
    ret_earn = read_val('fact-uplift-retained-earnings-2026.md')
    div_paid = read_val('fact-dividends-paid-2026.md')
    
    rev_up = read_val('fact-uplift-sales-revenue-2026.md')
    exp_up = read_val('fact-uplift-operating-expenses-2026.md')
    
    # 3D SBRM MATHEMATICS
    curr_assets = cash_base + cash_up + ar_up + nab_up # 160k
    total_assets = curr_assets + plant - acc_dep # 235k
    
    total_liab = curr_liab_base + ap_up + non_curr_liab # 110k
    
    total_rev = rev_base + rev_up # 200k
    total_exp = exp_base + exp_up # 155k
    profit_loss = total_rev - total_exp # 45k
    
    total_eq = open_eq + cap_intro + ret_earn + profit_loss - div_paid # 125k
    
    # FORCE PRECISE VALUES INTO MASTER NODES
    update_val('fact-cash-ledger-2026.md', cash_base)
    update_val('fact-current-liabilities-2026.md', curr_liab_base)
    update_val('fact-expenses-2026.md', total_exp) # Rollup
    
    update_val('fact-current-assets-2026.md', curr_assets)
    update_val('fact-total-assets-2026.md', total_assets)
    update_val('fact-total-liabilities-2026.md', total_liab)
    update_val('fact-revenue-2026.md', total_rev)
    update_val('fact-profit-loss-2026.md', profit_loss)
    update_val('fact-total-equity-2026.md', total_eq)
    
    print("=== SYNCHRONIZATION COMPLETE ===")

if __name__ == '__main__':
    consolidate()