import json
import os

def load_report(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate_report(report):
    print("\n=== SBRM & OIM MULTIDIMENSIONAL REASONER (v2.1) ===")
    
    facts = report.get('facts', [])
    structure = report.get('reportStructure', [])
    
    # Build strict hierarchy map
    children_map = {}
    for sec in structure:
        sec_id = sec['@id']
        parent_id = sec.get('isPartOf', {}).get('@id')
        if parent_id:
            if parent_id not in children_map:
                children_map[parent_id] = []
            children_map[parent_id].append(sec_id)

    def get_asserted_value(section_id):
        """Gets the explicitly declared scalar value for a parent node."""
        return sum(f['value'] for f in facts if f.get('context', {}).get('parentSection', {}).get('@id') == section_id)

    def get_weight(section_id):
        """Applies SBRM contra-account weightings."""
        s = section_id.lower()
        if 'accumulated' in s or 'dividend' in s or 'expense' in s:
            return -1.0
        return 1.0

    def get_calculated_value(section_id):
        """Recursively sums only leaf nodes to prevent double-counting."""
        children = children_map.get(section_id, [])
        if not children:
            return get_asserted_value(section_id) * get_weight(section_id)
        return sum(get_calculated_value(c) for c in children)

    # --- LAYER A: OIM FIDELITY ---
    print("\n--- Layer A: OIM Fidelity ---")
    if not [f for f in facts if 'decimals' not in f]: print("[PASS] Rule A.1: Mandatory precision (decimals) present.")
    if not [f for f in facts if not (f.get('unit', '').startswith('iso4217:') or f.get('unit', '').startswith('xbrli:'))]: print("[PASS] Rule A.2: Valid namespaces.")
    if not [s for s in structure if 'en' not in s.get('label', {})]: print("[PASS] Rule A.3: Multi-language Label Maps valid.")

    # --- LAYER B: HYPERCUBE ROLL-UP INTEGRITY ---
    print("\n--- Layer B: Hypercube Roll-Up Integrity ---")
    
    assets_asserted = get_asserted_value('section:total-assets')
    assets_calc = get_calculated_value('section:total-assets')
    liab_asserted = get_asserted_value('section:total-liabilities')
    liab_calc = get_calculated_value('section:total-liabilities')
    pl_asserted = get_asserted_value('section:profit-loss')
    pl_calc = get_calculated_value('section:profit-loss')
    
    if assets_asserted == assets_calc: print(f"[PASS] Asset Hierarchy sums perfectly ({assets_asserted}).")
    else: print(f"[WARN] Asset Hierarchy mismatch! Asserted: {assets_asserted} | Calculated from Leaves: {assets_calc}")

    if liab_asserted == liab_calc: print(f"[PASS] Liability Hierarchy sums perfectly ({liab_asserted}).")
    else: print(f"[WARN] Liability Hierarchy mismatch! Asserted: {liab_asserted} | Calculated from Leaves: {liab_calc}")

    # NEW: P&L Hierarchy Check
    if pl_asserted == pl_calc: print(f"[PASS] P&L Hierarchy sums perfectly ({pl_asserted}).")
    else: print(f"[WARN] P&L Hierarchy mismatch! Asserted: {pl_asserted} | Calculated from Leaves: {pl_calc}")

    # --- LAYER C: ACCOUNTING LOGIC ---
    print("\n--- Layer C: Multidimensional Accounting Logic ---")
    
    equity_asserted = get_asserted_value('section:total-equity')
    
    if abs(assets_asserted - (liab_asserted + equity_asserted)) < 0.01:
        print(f"[PASS] Rule C.1: Core Accounting Equation Holds: Assets ({assets_asserted}) = Liab ({liab_asserted}) + Equity ({equity_asserted}).")
    else:
        print(f"[FAIL] Rule C.1: Core Accounting Equation Broken.")

    opening = get_asserted_value('section:opening-equity')
    cap_intro = get_asserted_value('section:capital-introduced')
    ret_earn = get_asserted_value('section:retained-earnings')
    dividends = get_asserted_value('section:dividends-paid') * -1.0  
    
    calc_close = opening + cap_intro + ret_earn + pl_asserted + dividends
    
    if abs(calc_close - equity_asserted) < 0.01:
        print(f"[PASS] Rule C.2: Temporal Roll-Forward Valid.")
        print(f"       -> Open ({opening}) + CapInt ({cap_intro}) + RetEarn ({ret_earn}) + P&L ({pl_asserted}) + Div ({dividends}) = Close ({equity_asserted}).")
    else:
        print(f"[FAIL] Rule C.2: Roll-Forward calculation mismatch.")

    # NEW: Rule C.3 - P&L Articulation
    rev_calc = get_calculated_value('section:revenue')
    exp_calc = get_calculated_value('section:expenses') * -1.0 # Reverse weight for display
    
    if abs((rev_calc - exp_calc) - pl_asserted) < 0.01:
        print(f"[PASS] Rule C.3: P&L Articulation Valid. Rev ({rev_calc}) - Exp ({exp_calc}) = P&L ({pl_asserted}).")
    else:
        print(f"[FAIL] Rule C.3: P&L Articulation Broken! Rev ({rev_calc}) - Exp ({exp_calc}) != P&L ({pl_asserted}).")
        
    print("\n=== EVALUATION COMPLETE ===\n")

if __name__ == "__main__":
    report_file = 'vault_report_export.jsonld'
    if os.path.exists(report_file):
        evaluate_report(load_report(report_file))
    else:
        print(f"[ERROR] Could not locate {report_file}. Run export_jsonld_report.py first.")