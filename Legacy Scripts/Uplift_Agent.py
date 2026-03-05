import csv
import os
import uuid
import hashlib

# Configuration
CSV_FILE = 'trial_balance.csv'
OUTPUT_DIR = './01_Ontology'

def calculate_sha256(body_text):
    normalized_body = body_text.strip()
    return hashlib.sha256(normalized_body.encode('utf-8')).hexdigest()

def map_sbrm_hypercube(sbrm_class):
    """Dynamically maps the flat CSV classification to the 3D SBRM Hypercube."""
    if sbrm_class in ['TotalRevenue', 'Expenses']:
        return "StatementOfComprehensiveIncome", "RollUp"
    elif sbrm_class in ['TotalEquity']:
        return "StatementOfChangesInEquity", "RollForward"
    else:
        return "StatementOfFinancialPosition", "Hierarchy"

def generate_markdown_node(row):
    account_code = row['AccountCode']
    account_name = row['AccountName']
    debit = float(row['Debit'])
    credit = float(row['Credit'])
    sbrm_class = row['SBRM_Classification']
    
    balance = debit if debit > 0 else credit
    safe_name = account_name.lower().replace(' ', '-').replace('&', 'and')
    filename = f"fact-uplift-{safe_name}-2026.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    unique_id = f"urn:uuid:{uuid.uuid4()}"
    
    # Map to the new ontological structure
    primary_hypercube, pattern = map_sbrm_hypercube(sbrm_class)
    
    body_content = f"""
# {account_name} (Account: {account_code})
Balance: {balance}
Classification: {sbrm_class}
Source: Legacy CSV Trial Balance Import
"""
    content_hash = calculate_sha256(body_content)
    
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

hypercube_context:
  primary_hypercube: "{primary_hypercube}"
  arrangement_pattern: "{pattern}"

integrity:
  source_uri: "internal://ingestion/csv/trial_balance"
  content_hash: "{content_hash}"
---"""

    full_file_content = yaml_frontmatter + "\n" + body_content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_file_content)
    print(f"[MINTED & HASHED] {filename} -> {primary_hypercube} ({pattern})")

def run_uplift_pipeline():
    print("=== INITIATING HYPERCUBE-AWARE UPLIFT PIPELINE ===")
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            for row in csv.DictReader(file): generate_markdown_node(row)
        print("=== UPLIFT COMPLETE: Nodes mathematically injected into SBRM Hypercubes ===")
    except FileNotFoundError:
        print(f"[!] ERROR: Could not find {CSV_FILE}.")

if __name__ == "__main__":
    run_uplift_pipeline()