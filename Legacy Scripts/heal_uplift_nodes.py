import os
import re
import yaml

DIR = './01_Ontology'

def heal_nodes():
    count = 0
    for file in os.listdir(DIR):
        if file.startswith('fact-uplift-') and file.endswith('.md'):
            filepath = os.path.join(DIR, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            parts = content.split('---', 2)
            if len(parts) < 3: continue
            
            fm = yaml.safe_load(parts[1])
            body = parts[2].strip()
            
            # Extract literal magnitude from the Markdown body
            match = re.search(r'Balance:\s*([0-9.]+)', body)
            if not match: continue
            balance = float(match.group(1))
            
            # Derive the SBRM Concept from the standard filename
            concept_name = file.replace('fact-uplift-', '').replace('-2026.md', '')
            concept_urn = f"urn:uuid:def-sbr-{concept_name}"
            
            # Inject missing multidimensional properties
            fm['value'] = balance
            fm['edges'] = [
                {"rel": "sbrm:isInstanceOfConcept", "target": concept_urn},
                {"rel": "sbrm:hasReportingEntity", "target": "urn:uuid:def-sbrm-reporting-entity"},
                {"rel": "sbrm:hasReportingPeriod", "target": fm.get('project_context', {}).get('reporting_period', 'urn:uuid:period-2026')}
            ]
            
            # Re-write file with repaired frontmatter
            new_yaml = yaml.dump(fm, sort_keys=False)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"---\n{new_yaml}---\n{body}\n")
            
            print(f"[HEALED] {file} -> Value: {balance} | Concept: {concept_urn}")
            count += 1
            
    print(f"=== REPAIR COMPLETE: {count} nodes mathematically injected into SBRM Hypercubes ===")

if __name__ == "__main__":
    print("=== INITIATING SEMANTIC REPAIR ON UPLIFTED NODES ===")
    heal_nodes()