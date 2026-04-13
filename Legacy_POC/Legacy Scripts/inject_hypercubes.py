import os
import yaml

ONTOLOGY_DIR = './01_Ontology'

def determine_hypercube_context(filename):
    """Logically maps facts to their SBRM Hypercube and Concept Arrangement Pattern."""
    name = filename.lower()
    
    # 1. Statement of Comprehensive Income (P&L)
    if any(x in name for x in ['revenue', 'expense', 'profit-loss']):
        return "StatementOfComprehensiveIncome", "RollUp"
        
    # 2. Statement of Changes in Equity
    elif any(x in name for x in ['equity', 'dividend']):
        return "StatementOfChangesInEquity", "RollForward"
        
    # 3. Working Papers
    elif 'wp-' in name:
        return "WorkingPaper_BankReconciliation", "CrossReference"
        
    # 4. Definitions (Non-Financial Facts)
    elif 'def-' in name:
        return "System_Ontology_Definition", "SemanticLink"
        
    # 5. Default to Balance Sheet
    else:
        return "StatementOfFinancialPosition", "Hierarchy"

def safely_inject_context():
    print("=== INITIATING SAFE SBRM HYPERCUBE INJECTION ===")
    
    for filename in os.listdir(ONTOLOGY_DIR):
        if not filename.endswith(".md"): continue
        
        filepath = os.path.join(ONTOLOGY_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Skip if already injected
        if "hypercube_context:" in content:
            print(f"[SKIPPED] {filename} (Already contains hypercube context)")
            continue
            
        hypercube, pattern = determine_hypercube_context(filename)
        
        # Format the new YAML block
        new_yaml_block = f"""
hypercube_context:
  primary_hypercube: "{hypercube}"
  arrangement_pattern: "{pattern}"
"""
        # Safely insert the block right before the 'integrity:' key
        if "\nintegrity:" in content:
            updated_content = content.replace("\nintegrity:", new_yaml_block + "\nintegrity:")
            
            # Invalidate the hash so sync_signatures knows it needs updating
            updated_content = updated_content.replace(
                'content_hash: "sha256:', 'content_hash: "PENDING_HASH')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"[INJECTED] {filename} -> {hypercube} ({pattern})")
        else:
            print(f"[WARNING] Could not find 'integrity:' block in {filename}")

if __name__ == "__main__":
    safely_inject_context()