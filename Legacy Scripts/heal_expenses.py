import os, yaml, hashlib

DIR = './01_Ontology'
print("=== INITIATING P&L ORPHAN HEALING ===")

# Mint "Other Expenses" for the remaining 55k base
path_exp = os.path.join(DIR, 'fact-expenses-2026.md')
if os.path.exists(path_exp):
    with open(path_exp, 'r', encoding='utf-8') as f:
        parts = f.read().split('---', 2)
        fm = yaml.safe_load(parts[1])
        
        fm_leaf = fm.copy()
        fm_leaf['@id'] = 'urn:uuid:fact-other-expenses-001'
        fm_leaf['value'] = 55000.0
        fm_leaf['hypercube_context'] = {
            'primary_hypercube': 'StatementOfComprehensiveIncome',
            'arrangement_pattern': 'RollUp'
        }
        for edge in fm_leaf.get('edges', []):
            if edge.get('rel') == 'sbrm:isInstanceOfConcept':
                edge['target'] = 'urn:uuid:def-sbr-other-expenses'

        body = "# Other Base Expenses\nBase: 55000.0 (80k original base - 25k sub-ledger depreciation)\n"
        fm_leaf['content_hash'] = hashlib.sha256(body.encode('utf-8')).hexdigest()

        with open(os.path.join(DIR, 'fact-other-expenses-2026.md'), 'w', encoding='utf-8') as f:
            f.write(f"---\n{yaml.dump(fm_leaf, sort_keys=False)}---\n{body}")
        print("[MINTED] fact-other-expenses-2026.md (55,000.0)")

print("=== P&L HEALING COMPLETE ===")