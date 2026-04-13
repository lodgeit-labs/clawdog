import pandas as pd
import yaml
import hashlib
import os
import glob

def load_resolved_quarantines(quarantine_dir):
    """Loads any human-resolved mappings from the quarantine directory."""
    resolved = {}
    if os.path.exists(quarantine_dir):
        for filepath in glob.glob(os.path.join(quarantine_dir, "*.md")):
            with open(filepath, 'r') as f:
                content = f.read()
                # Simple parser for the YAML frontmatter
                if "status: resolved" in content:
                    lines = content.split('\n')
                    account = next((l.split(': ')[1] for l in lines if l.startswith('raw_account_name: ')), None)
                    resolution = next((l.split(': ')[1] for l in lines if l.startswith('human_resolution: ')), None)
                    if account and resolution and resolution != "pending":
                        resolved[account] = resolution.strip()
    return resolved

def mock_llm_semantic_mapping(raw_account_name, raw_balance, taxonomy_keys, resolved_overrides):
    """
    Simulates the LLM taking a raw string and balance to map it to our Core Taxonomy.
    Checks human overrides first!
    """
    if raw_account_name in resolved_overrides:
        return resolved_overrides[raw_account_name], 1.0 # 100% confidence because human said so

    raw = raw_account_name.lower()
    
    # Switching Logic for Director Loans based on balance (Debit = Positive, Credit = Negative)
    if "loan" in raw and "director" in raw:
        if raw_balance > 0:
            return "Assets", 0.99  # Debit balance = Director owes company (Asset)
        else:
            return "Liabilities", 0.99 # Credit balance = Company owes director (Liability)

    if "cash" in raw or "bank" in raw or "operating account" in raw: return "Assets", 0.99
    if "sales" in raw or "revenue" in raw: return "Revenue", 0.98
    if "expense" in raw or "fee" in raw: return "Expenses", 0.98
    if "suspense" in raw or "unknown" in raw: return "Unknown", 0.40 # High entropy!
    
    # Default fallback
    return "Equity", 0.70

def process_trial_balance(csv_path, taxonomy_path, quarantine_dir):
    print(f"Loading taxonomy from {taxonomy_path}...")
    with open(taxonomy_path, 'r') as f:
        taxonomy = yaml.safe_load(f)
    valid_concepts = list(taxonomy['elements'].keys())

    print(f"Ingesting chaotic CSV from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    resolved_facts = []
    
    os.makedirs(quarantine_dir, exist_ok=True)

    resolved_overrides = load_resolved_quarantines(quarantine_dir)
    print(f"Loaded {len(resolved_overrides)} human-resolved overrides.")

    for index, row in df.iterrows():
        raw_name = row['AccountName']
        raw_balance = row['Balance']
        
        # Ask the LLM to map the concept
        mapped_concept, confidence = mock_llm_semantic_mapping(raw_name, raw_balance, valid_concepts, resolved_overrides)
        
        # The Confidence Tripwire (HITL)
        if confidence >= 0.95:
            # Auto-map successful
            resolved_facts.append({
                "raw_account": raw_name,
                "mapped_concept": mapped_concept,
                "balance": raw_balance,
                "status": "auto_resolved"
            })
        else:
            # Quarantine triggered! Generate the Markdown State Node
            quarantine_data = {
                "type": "SBRMMappingException",
                "status": "quarantined",
                "raw_account_name": raw_name,
                "heuristic_guess": mapped_concept,
                "semantic_confidence": confidence,
                "human_resolution": "pending"
            }
            
            yaml_frontmatter = yaml.dump(quarantine_data, sort_keys=False)
            node_content = f"---\n{yaml_frontmatter}---\n\n## Quarantine Report\nThe heuristic engine failed to map this account with high confidence. Human intervention is required to unblock the Virtual Close.\n\n**Instructions:**\n1. Change `status` to `resolved`.\n2. Change `human_resolution` to the correct Taxonomy Concept (e.g., Assets, Liabilities, Equity, Revenue, Expenses).\n3. Save this file."
            
            node_hash = hashlib.sha256(raw_name.encode()).hexdigest()[:8]
            filepath = os.path.join(quarantine_dir, f"quarantine_{node_hash}.md")
            
            with open(filepath, 'w') as f:
                f.write(node_content)
                
            print(f"⚠️  QUARANTINE TRIGGERED: '{raw_name}' (Confidence: {confidence}). Node saved to {filepath}")

    return resolved_facts

if __name__ == "__main__":
    facts = process_trial_balance(
        "dummy_tb.csv", 
        "01_Ontology/core_mini_taxonomy.yaml", 
        "03_Registry/Quarantine/"
    )
    
    print("\n--- Auto-Resolved Facts (Ready for Prolog) ---")
    for f in facts:
        print(f"✅ {f['raw_account']} -> {f['mapped_concept']} ({f['balance']})")
