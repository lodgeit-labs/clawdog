import os, yaml, hashlib

DIR = './01_Ontology'
print("=== INITIATING VAULT HEAL & LEAF MINTING ===")

# 1. Mint "Other Current Liabilities" for the orphaned 30k base
path_curr_liab = os.path.join(DIR, 'fact-current-liabilities-2026.md')
if os.path.exists(path_curr_liab):
    with open(path_curr_liab, 'r', encoding='utf-8') as f:
        parts = f.read().split('---', 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1])
            fm_leaf = fm.copy()
            fm_leaf['@id'] = 'urn:uuid:fact-other-curr-liab-001'
            fm_leaf['value'] = 30000.0
            for edge in fm_leaf.get('edges', []):
                if edge.get('rel') == 'sbrm:isInstanceOfConcept':
                    edge['target'] = 'urn:uuid:def-sbr-other-current-liabilities'

            body = "# Other Current Liabilities\nBase: 30000.0\n"
            fm_leaf['content_hash'] = hashlib.sha256(body.encode('utf-8')).hexdigest()

            with open(os.path.join(DIR, 'fact-other-current-liabilities-2026.md'), 'w', encoding='utf-8') as f:
                f.write(f"---\n{yaml.dump(fm_leaf, sort_keys=False)}---\n{body}")
            print("[MINTED] fact-other-current-liabilities-2026.md")

# 2. Idempotently Reset Master Nodes
fixes = {
    'fact-current-assets-2026.md': 160000.0,
    'fact-total-assets-2026.md': 235000.0,
    'fact-current-liabilities-2026.md': 60000.0,
    'fact-total-liabilities-2026.md': 110000.0,
    'fact-revenue-2026.md': 200000.0,
    'fact-expenses-2026.md': 155000.0,
    'fact-profit-loss-2026.md': 45000.0,
    'fact-total-equity-2026.md': 125000.0,
    'fact-cash-ledger-2026.md': 50000.0
}

for file, val in fixes.items():
    path = os.path.join(DIR, file)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            p = f.read().split('---', 2)
            if len(p) >= 3:
                fm = yaml.safe_load(p[1])
                fm['value'] = float(val)
                fm['content_hash'] = hashlib.sha256(p[2].encode('utf-8')).hexdigest()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"---\n{yaml.dump(fm, sort_keys=False)}---\n{p[2]}")
        print(f"[RESET] {file} -> {val}")

print("=== VAULT HEAL COMPLETE ===")