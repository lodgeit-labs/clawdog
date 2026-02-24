import os
import json
import yaml # Requires pyyaml

def extract_yaml_frontmatter(filepath):
    """Isolates and parses the JSON-LD YAML block from a Markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1])
            except yaml.YAMLError as e:
                print(f"[ERROR] YAML parsing failed in {filepath}: {e}")
                return None
    return None

def scan_directory(directory):
    """Scans a target vault directory and maps the ontological state."""
    registry = []
    if not os.path.exists(directory):
        print(f"[WARNING] Directory not found: {directory}")
        return registry
        
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                frontmatter = extract_yaml_frontmatter(filepath)
                
                if frontmatter:
                    # Enforce strict extraction of SBRM and Ontological axioms
                    node_data = {
                        "file_name": file,
                        "@id": frontmatter.get("@id"),
                        "gist_equivalent": frontmatter.get("gist_equivalent"),
                        "hypercube_context": frontmatter.get("hypercube_context"),
                        "parameters_exposed": frontmatter.get("parameters_exposed"),
                        "edges": frontmatter.get("edges")
                    }
                    registry.append(node_data)
    return registry

if __name__ == "__main__":
    print("[SYSTEM] Initiating multidimensional vault state extraction...")
    
    # Target the Ground Truth and Logic layers
    ontology_data = scan_directory('./01_Ontology')
    rules_data = scan_directory('./02_Rules')
    
    export_payload = {
        "metrics": {
            "total_ontology_nodes": len(ontology_data),
            "total_rule_nodes": len(rules_data)
        },
        "ontology_nodes": ontology_data,
        "rule_nodes": rules_data
    }
    
    output_file = 'vault_state_export.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_payload, f, indent=2)
        
    print(f"[SUCCESS] Vault state mapped. {export_payload['metrics']['total_ontology_nodes']} Ontology nodes and {export_payload['metrics']['total_rule_nodes']} Rule nodes extracted.")
    print(f"[ACTION REQUIRED] Output saved to {output_file}.")