import os
import yaml

VAULT_PATH = r"C:\Users\futur\Documents\LodgeiT_Global"

def run_universal_logic_engine(path):
    print("--- Open-Source SBRM Logic Engine: Universal Execution ---\n")
    facts = {}
    rules = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Split YAML from Body
                    parts = content.split('---')
                    if len(parts) < 3: continue
                    
                    try:
                        header = yaml.safe_load(parts[1])
                        if not header: continue
                        
                        nclass = header.get('ontological_class')
                        nid = header.get('@id')

                        # 1. Ingest Facts (Supporting both Financial and Working Paper)
                        if nclass in ["FinancialFact", "WorkingPaperFact"]:
                            val = header.get('fact_value')
                            edges = header.get('edges', [])
                            for edge in edges:
                                target = edge.get('target', '')
                                if "def-sbr-" in target or "def-wp-" in target:
                                    facts[target.strip()] = float(val)

                        # 2. Ingest Rules (Modern Dictionary Handling)
                        if nclass == "CalculationRule":
                            exposed = header.get('parameters_exposed', {})
                            if exposed:
                                # Reformat {Var: {sbrm_label: '...'}} into a list of tuples [('Var', '...')]
                                params = [(k, v.get('sbrm_label')) for k, v in exposed.items()]
                                rules.append({"id": nid, "params": params})
                            
                    except Exception as e:
                        continue # Skip malformed nodes

    print(f"Discovered {len(facts)} SBRM Facts & Working Papers.")
    print(f"Discovered {len(rules)} SBRM Rules.\n")
    
    for rule in rules:
        print(f"EXECUTING RULE: {rule['id']}")
        
        rule_vars = {var_name: facts.get(sbrm_urn) for var_name, sbrm_urn in rule['params']}
        
        for name, val in rule_vars.items():
            print(f"  -> Found {name}: {val if val is not None else 'MISSING'}")
            
        print("  --- Result ---")
        
        # Balance Sheet
        if "TotalEquity" in rule_vars and "TotalAssets" in rule_vars and "TotalLiabilities" in rule_vars and None not in rule_vars.values():
            if rule_vars["TotalAssets"] == (rule_vars["TotalLiabilities"] + rule_vars["TotalEquity"]):
                print("  [PASS] Fundamental Accounting Equation balances.\n")
            else:
                print("  [FAIL] Balance Sheet contradiction!\n")

        # Asset Roll-up
        elif "TotalAssets" in rule_vars and "CurrentAssets" in rule_vars and "NonCurrentAssets" in rule_vars and None not in rule_vars.values():
            if rule_vars["TotalAssets"] == (rule_vars["CurrentAssets"] + rule_vars["NonCurrentAssets"]):
                print("  [PASS] Asset Roll-up is mathematically consistent.\n")
            else:
                print("  [FAIL] Asset contradiction!\n")
                
        # Liability Roll-up
        elif "TotalLiabilities" in rule_vars and "CurrentLiabilities" in rule_vars and "NonCurrentLiabilities" in rule_vars and None not in rule_vars.values():
            if rule_vars["TotalLiabilities"] == (rule_vars["CurrentLiabilities"] + rule_vars["NonCurrentLiabilities"]):
                print("  [PASS] Liability Roll-up is mathematically consistent.\n")
            else:
                print("  [FAIL] Liability contradiction!\n")
                
        # Equity Roll-forward
        elif "OpeningEquity" in rule_vars and "ClosingEquity" in rule_vars and "ProfitLoss" in rule_vars and "Dividends" in rule_vars and None not in rule_vars.values():
            if rule_vars["ClosingEquity"] == (rule_vars["OpeningEquity"] + rule_vars["ProfitLoss"] - rule_vars["Dividends"]):
                print("  [PASS] Equity Roll-Forward (Time Dimension) is mathematically consistent.\n")
            else:
                print("  [FAIL] Equity Roll-Forward contradiction!\n")
                
        # Dimensional Fan-Out (Revenue)
        elif "TotalRevenue" in rule_vars and "RevRed" in rule_vars and None not in rule_vars.values():
            if rule_vars["TotalRevenue"] == (rule_vars["RevRed"] + rule_vars["RevBlue"] + rule_vars["RevGreen"] + rule_vars["RevYellow"]):
                print("  [PASS] Dimensional Revenue Fan-Out is mathematically consistent.\n")
            else:
                print("  [FAIL] Dimensional contradiction: Parts do not equal the Total!\n")
                
        # Profit & Loss
        elif "Revenue" in rule_vars and "Expenses" in rule_vars and "ProfitLoss" in rule_vars and None not in rule_vars.values():
            if rule_vars["ProfitLoss"] == (rule_vars["Revenue"] - rule_vars["Expenses"]):
                print("  [PASS] Profit & Loss Statement is mathematically consistent.\n")
            else:
                print("  [FAIL] Profit & Loss contradiction!\n")
                
        # Bank Reconciliation Cross-Reference
        elif "LedgerCash" in rule_vars and "StatementCash" in rule_vars and None not in rule_vars.values():
            if rule_vars["LedgerCash"] == rule_vars["StatementCash"]:
                print("  [PASS] Bank Reconciliation Working Paper cross-references correctly.\n")
            else:
                print("  [FAIL] Working Paper contradiction: Ledger does not match Statement!\n")
                
        # Fixed Asset Net Book Value
        elif "PlantAtCost" in rule_vars and "AccumulatedDep" in rule_vars and "NonCurrentAssets" in rule_vars and None not in rule_vars.values():
            if rule_vars["NonCurrentAssets"] == (rule_vars["PlantAtCost"] - rule_vars["AccumulatedDep"]):
                print("  [PASS] Fixed Asset Sub-Ledger ties perfectly to Non-Current Assets.\n")
            else:
                print("  [FAIL] Fixed Asset contradiction: Cost minus Dep does not equal Net!\n")
                
        else:
             print("  [PENDING] Missing facts. Cannot execute proof.\n")

# This is the crucial trigger block that was missing!
if __name__ == "__main__":
    if os.path.exists(VAULT_PATH):
        run_universal_logic_engine(VAULT_PATH)
    else:
        print("Path not found. Please check VAULT_PATH.")