import json
import os

def load_report(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate_report(report):
    print("\n=== SBRM & OIM MULTIDIMENSIONAL REASONER ===")
    
    facts = report.get('facts', [])
    structure = report.get('reportStructure', [])
    
    # Build structural hierarchy map
    children_map = {}
    for sec in structure:
        sec_id = sec['@id']
        parent_id = sec.get('isPartOf', {}).get('@id')
        if parent_id:
            if parent_id not in children_map:
                children_map[parent_id] = []
            children_map[parent_id].append(sec_id)

    # Helper: Get scalar value of a node (B.2 Logic)
    def get_node_own_value(section_id):
        return sum(f['value'] for f in facts if f.get('context', {}).get('parentSection', {}).get('@id') == section_id)

    # Helper: Recursive Aggregation (B.2 Logic)
    def get_recursive_value(section_id):
        total = get_node_own_value(section_id)
        for child_id in children_map.get(section_id, []):
            total += get_recursive_value(child_id)
        return total

    # --- LAYER A: OIM FIDELITY CHECKS ---
    print("\n--- Layer A: OIM Fidelity ---")
    
    # Rule A.1: Mandatory Precision
    missing_decimals = [f for f in facts if 'decimals' not in f]
    if not missing_decimals:
        print("[PASS] Rule A.1: All numeric facts possess mandatory 'decimals' attribute.")
    else:
        print(f"[FAIL] Rule A.1: {len(missing_decimals)} facts missing decimals.")

    # Rule A.2: Unit Consistency
    invalid_units = [f for f in facts if not (f.get('unit', '').startswith('iso4217:') or f.get('unit', '').startswith('xbrli:'))]
    if not invalid_units:
        print("[PASS] Rule A.2: All facts utilize valid 'iso4217:' or 'xbrli:' unit namespaces.")
    else:
        print(f"[FAIL] Rule A.2: {len(invalid_units)} facts contain invalid unit namespaces.")

    # Rule A.3: Multi-Language Label Support
    invalid_labels = [s for s in structure if 'en' not in s.get('label', {})]
    if not invalid_labels:
        print("[PASS] Rule A.3: All report sections utilize multi-language Label Maps (en).")
    else:
        print(f"[FAIL] Rule A.3: {len(invalid_labels)} sections lack compliant label structures.")

    # --- LAYER C: ACCOUNTING LOGIC (TEMPORAL STRICTNESS) ---
    print("\n--- Layer B & C: Multidimensional Accounting Logic ---")
    
    # Rule C.1: Accounting Equation
    assets = get_recursive_value('section:total-assets')
    liab = get_recursive_value('section:total-liabilities')
    equity = get_recursive_value('section:total-equity')
    
    # The JSON-LD currently treats liabilities/equity as positive magnitudes, so A = L + E holds conceptually.
    if abs(assets - (liab + equity)) < 0.01:
        print(f"[PASS] Rule C.1: Accounting Equation holds. Assets ({assets}) = Liabilities ({liab}) + Equity ({equity}).")
    else:
        print(f"[FAIL] Rule C.1: Accounting Equation broken! Assets ({assets}) != Liab ({liab}) + Equity ({equity}).")

    # Rule C.2: Strict Temporal Roll-Forward
    # Fetching explicit magnitudes to prove the Roll-Forward timeline
    opening = get_node_own_value('section:opening-equity')
    capital = get_node_own_value('section:capital-introduced')
    pl = get_recursive_value('section:profit-loss') # Roll-up of revenue and expenses
    dividends = get_node_own_value('section:dividends-paid')
    closing = get_node_own_value('section:total-equity')
    
    calc_close = opening + capital + pl - dividends
    
    if abs(calc_close - closing) < 0.01:
        print(f"[PASS] Rule C.2: Strict Temporal Roll-Forward valid.")
        print(f"       -> Opening ({opening}) + CapInt ({capital}) + P&L ({pl}) - Div ({dividends}) = Closing ({closing}).")
    else:
        print(f"[FAIL] Rule C.2: Roll-Forward calculation mismatch.")

    print("\n=== EVALUATION COMPLETE ===\n")

if __name__ == "__main__":
    report_file = 'vault_report_export.jsonld'
    if os.path.exists(report_file):
        report_data = load_report(report_file)
        evaluate_report(report_data)
    else:
        print(f"[ERROR] Could not locate {report_file}. Run export_jsonld_report.py first.")