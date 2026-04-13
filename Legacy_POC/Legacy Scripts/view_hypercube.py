import os
import yaml

def render_sbrm_hypercubes():
    ontology_path = './01_Ontology'
    hypercubes = {}

    print("\n=== LODGEIT GLOBAL: SBRM HYPERCUBE VISUALIZER ===")
    
    for filename in os.listdir(ontology_path):
        if not filename.endswith(".md"): continue
            
        with open(os.path.join(ontology_path, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            parts = content.split('---')
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    hc = metadata.get('hypercube_context', {})
                    
                    # Extract architectural parameters
                    primary = hc.get('primary_hypercube', 'Unclassified_Nodes')
                    pattern = hc.get('arrangement_pattern', 'Unknown_Pattern')
                    node_id = metadata.get('@id', 'No ID')
                    
                    if primary not in hypercubes:
                        hypercubes[primary] = {}
                    if pattern not in hypercubes[primary]:
                        hypercubes[primary][pattern] = []
                        
                    hypercubes[primary][pattern].append({
                        "name": filename.replace('.md', ''),
                        "id": node_id
                    })
                except Exception as e:
                    pass

    # Render the nested SBRM architecture
    for cube_name, patterns in sorted(hypercubes.items()):
        print(f"\n[Hypercube: {cube_name}]")
        for pattern, nodes in sorted(patterns.items()):
            print(f"  └── Pattern: {pattern}")
            for node in sorted(nodes, key=lambda x: x['name']):
                print(f"      ├── {node['name']}")

    print("\n=== End of Architecture ===")

if __name__ == "__main__":
    render_sbrm_hypercubes()