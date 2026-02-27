import os
import hashlib
import re
import csv

DIR = './01_Ontology'

def mint_from_clean_payload(filepath='transformed_payload.csv'):
    """
    Ingests a flat, clean CSV from the Transform module and mints SBRM Markdown facts.
    Expected CSV Headers: Account_Name, Period, Value, LodgeiT_Classification
    """
    os.makedirs(DIR, exist_ok=True)
    print("=== INITIATING CLIENTRELAY SBRM MINTER ===")
    mint_count = 0

    try:
        # utf-8-sig ensures any Excel BOM artifacts left in the payload are stripped
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                account_name = row.get('Account_Name', '').strip()
                period = row.get('Period', '').strip()
                classification = row.get('LodgeiT_Classification', 'Unmapped').strip()
                
                try:
                    value = float(row.get('Value', 0.0))
                except ValueError:
                    value = 0.0
                    
                if not account_name or value == 0.0:
                    continue
                    
                # 1. Determine SBRM Hypercube context
                class_lower = classification.lower()
                if 'profit & loss' in class_lower or 'revenue' in class_lower or 'expense' in class_lower or 'cost' in class_lower:
                    hypercube = "StatementOfComprehensiveIncome"
                else:
                    hypercube = "StatementOfFinancialPosition"
                    
                # 2. Sanitize filename (Protecting the YAML parser from triple-hyphens)
                safe_name = account_name.replace(' ', '-').replace('&', 'and').lower()
                safe_name = "".join(c for c in safe_name if c.isalnum() or c == '-')
                safe_name = re.sub(r'-+', '-', safe_name).strip('-')
                
                filename = f"fact-lodgeit-{safe_name}-{period}.md"
                out_path = os.path.join(DIR, filename)
                
                # 3. Construct Body and Cryptographic Hash
                body = f"# {account_name}\nLodgeiT Classification: {classification}\n"
                content_hash = hashlib.sha256(body.encode('utf-8')).hexdigest()
                
                # 4. Construct JSON-LD/YAML Frontmatter
                frontmatter = f"""---
"@context": "ipfs://bafkreifcontext...[Base_Context]"
"@id": "urn:uuid:fact-{safe_name}-{period}"
ontological_class: "AccountBalance"
gist_equivalent: "gist:Magnitude"
value: {value}
period: "{period}"
hypercube_context:
  primary_hypercube: "{hypercube}"
  arrangement_pattern: "RollUp"
content_hash: "{content_hash}"
---
{body}"""
                
                # 5. Mint to Vault
                with open(out_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(frontmatter)
                    
                mint_count += 1
                
                # Terminal output for visual validation
                route_display = classification.split(' > ')[0] if ' > ' in classification else classification
                print(f"[MINTED] {filename} -> ${value} | SBR Route: {route_display}")
                
        print(f"=== SBRM MINTER COMPLETE: {mint_count} Semantic Facts Minted ===")

    except FileNotFoundError:
        print(f"[ERROR] Could not find the clean payload file: {filepath}")
        print("Please ensure the Transform module has generated 'transformed_payload.csv' in the root directory.")

if __name__ == '__main__':
    mint_from_clean_payload()