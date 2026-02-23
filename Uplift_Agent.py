import csv
import os
import uuid
import hashlib

# Configuration
CSV_FILE = 'trial_balance.csv'
OUTPUT_DIR = './01_Ontology'

def calculate_sha256(body_text):
    """Calculates the SHA-256 hash of the node's body."""
    normalized_body = body_text.strip()
    return hashlib.sha256(normalized_body.encode('utf-8')).hexdigest()

def generate_markdown_node(row):
    """Mints a new Markdown file for a single Trial Balance row."""
    account_code = row['AccountCode']
    account_name = row['AccountName']
    debit = float(row['Debit'])
    credit = float(row['Credit'])
    sbrm_class = row['SBRM_Classification']
    
    # Calculate net balance (Simplified: Debits positive for assets/expenses, Credits positive for liab/eq/rev)
    # For a real engine we'd use natural account balances, but this works for our pipeline test!
    balance = debit if debit > 0 else credit
    
    # Format a safe filename
    safe_name = account_name.lower().replace(' ', '-').replace('&', 'and')
    filename = f"fact-uplift-{safe_name}-2026.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    unique_id = f"urn:uuid:{uuid.uuid4()}"
    
    # The Ground Truth Body
    body_content = f"""
# {account_name} (Account: {account_code})
Balance: {balance}
Classification: {sbrm_class}
Source: Legacy CSV Trial Balance Import
"""
    # Calculate the cryptographic hash of the body
    content_hash = calculate_sha256(body_content)
    
    # The YAML Frontmatter (Notice the quotes around @ keys to satisfy PyYAML!)
    yaml_frontmatter = f"""---
"@context": "ipfs://bafkreifcontext...[Base_Context]"
"@id": "{unique_id}"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"
domain_tags:
  - "SBRM"
  - "Trial-Balance-Ingestion"
  - "Uplifted-Fact"

project_context:
  reporting_entity: "urn:uuid:entity-lodgeit-demo"
  reporting_period: "urn:uuid:period-2026"

integrity:
  source_uri: "internal://ingestion/csv/trial_balance"
  content_hash: "{content_hash}"
---"""

    # Assemble and write the file
    full_file_content = yaml_frontmatter + "\n" + body_content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_file_content)
        
    print(f"[MINTED & HASHED] {filename} -> {sbrm_class}: {balance}")

def run_uplift_pipeline():
    print("=== INITIATING SBRM SEMANTIC UPLIFT PIPELINE ===")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                generate_markdown_node(row)
        print("=== UPLIFT COMPLETE: Nodes minted to 01_Ontology ===")
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {CSV_FILE}. Please ensure it is in the same directory.")

if __name__ == "__main__":
    run_uplift_pipeline()