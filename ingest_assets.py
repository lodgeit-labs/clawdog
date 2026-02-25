import json
import os
import hashlib

DIR = './01_Ontology'

def mint_node(asset_id, label, attribute, value, metadata, concept_suffix):
    filename = f"fact-asset-{asset_id}-{concept_suffix}-2026.md"
    filepath = os.path.join(DIR, filename)
    
    body = f"# {label} ({attribute})\n{metadata}\n"
    content_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()
    
    # Strip spaces for the Ontological Class definition
    onto_class = attribute.replace(' ', '')
    
    frontmatter = f"""---
"@context": "ipfs://bafkreifcontext...[Base_Context]"
"@id": "urn:uuid:fact-asset-{asset_id}-{concept_suffix}-001"
ontological_class: "FixedAsset{onto_class}"
gist_equivalent: "gist:Magnitude"
value: {value}
edges:
  - rel: "sbrm:isInstanceOfConcept"
    target: "urn:uuid:def-sbr-asset-{asset_id}-{concept_suffix}"
  - rel: "sbrm:hasReportingEntity"
    target: "urn:uuid:def-sbrm-reporting-entity"
content_hash: "{content_hash}"
---
{body}"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
    print(f"[MINTED] {filename} -> ${value}")

def ingest():
    print("=== INITIATING SUB-LEDGER ASSET INGESTION (v2) ===")
    if not os.path.exists('asset_register.json'):
        print("[ERROR] asset_register.json not found.")
        return
        
    with open('asset_register.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for asset in data.get('assets', []):
        asset_id = asset['@id'].split(':')[-1]
        label = asset['label']
        cost = asset['cost']['value']
        accdep = asset['accumulatedDepreciation']['value']
        depexp = asset['depreciationExpense']['value'] # <-- NEW P&L EXTRACTION
        
        # Mint Balance Sheet Nodes
        mint_node(asset_id, label, "Cost", cost, f"Purchase Date: {asset.get('purchaseDate')}", "cost")
        mint_node(asset_id, label, "Accumulated Depreciation", accdep, f"Method: {asset.get('depreciationMethod')}", "accumulated")
        
        # Mint P&L Node
        mint_node(asset_id, label, "Depreciation Expense", depexp, f"Method: {asset.get('depreciationMethod')}\nRate: {asset.get('depreciationRate')}", "expense")

    print("=== FIXED ASSETS & P&L DEPRECIATION INGESTED INTO SBRM GRAPH ===")

if __name__ == '__main__':
    ingest()