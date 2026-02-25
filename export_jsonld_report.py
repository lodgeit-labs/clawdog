import os
import json
import yaml

def extract_yaml_frontmatter(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1])
    except Exception as e:
        print(f"[ERROR] Failed to read {filepath}: {e}")
    return None

def map_hierarchy(concept_id):
    """Maps flat SBRM concepts to their presentation layer hierarchy."""
    c = concept_id.lower()
    
    if c in ['section:total-assets', 'section:total-liabilities', 'section:total-equity', 'section:profit-loss']:
        return None 
        
    if 'cash' in c or 'receivable' in c or 'nab' in c: return "section:current-assets"
    if 'plant' in c or 'accumulated' in c: return "section:non-current-assets"
    if c == 'section:current-assets' or c == 'section:non-current-assets': return "section:total-assets"
    
    if 'payable' in c or 'other-current-liab' in c: return "section:current-liabilities"
    if c == 'section:current-liabilities' or c == 'section:non-current-liabilities': return "section:total-liabilities"
    
    if 'sales' in c or ('revenue' in c and c != 'section:revenue'): return "section:revenue"
    if c == 'section:revenue': return "section:profit-loss"
    
    if 'expense' in c: return "section:expenses"
    if c == 'section:expenses': return "section:profit-loss"
    
    if 'dividend' in c or 'capital' in c or 'retained' in c or 'opening-equity' in c or c == 'section:profit-loss': 
        return "section:total-equity"
        
    return None

def compile_jsonld_report():
    ontology_dir = './01_Ontology'
    
    report = {
        "@context": [
            "https://lodgeit.net.au/contexts/sbrm.jsonld",
            {
                "iso4217": "http://www.xbrl.org/2003/iso4217#",
                "xbrli": "http://www.xbrl.org/2003/instance#",
                "xsd": "http://www.w3.org/2001/XMLSchema#"
            }
        ],
        "@type": "Report",
        "entity": {
            "identifier": "LodgeiT Global Reporting Entity",
            "scheme": "LodgeiT_SBRM"
        },
        "reportStructure": [],
        "facts": []
    }

    discovered_concepts = set(['section:total-assets', 'section:total-liabilities', 'section:total-equity', 'section:profit-loss'])

    if not os.path.exists(ontology_dir):
        return

    for root, _, files in os.walk(ontology_dir):
        for file in files:
            if not file.endswith('.md'): continue
                
            fm = extract_yaml_frontmatter(os.path.join(root, file))
            if not fm: continue

            hc = fm.get('hypercube_context', {})
            if not hc or hc.get('arrangement_pattern') == 'SemanticLink':
                continue

            edges = fm.get('edges') or []
            concept_urn = next((e['target'] for e in edges if e.get('rel') == 'sbrm:isInstanceOfConcept'), None)
            
            if not concept_urn:
                concept_urn = f"section:{file.replace('.md', '').replace('fact-uplift-', '')}"
                
            concept_id = concept_urn.replace('urn:uuid:def-sbr-', 'section:').replace('urn:uuid:def-wp-', 'section:')
            discovered_concepts.add(concept_id)

            magnitude = fm.get('value', fm.get('magnitude', fm.get('fact_value', 0.0)))
            try:
                mag_val = float(magnitude)
            except (ValueError, TypeError):
                mag_val = 0.0

            pattern = hc.get('arrangement_pattern')
            fact_context = {
                "parentSection": { "@id": concept_id }
            }

            if pattern in ['Hierarchy', 'CrossReference']:
                fact_context["periodType"] = "instant"
                fact_context["as_At"] = "2026-06-30"
            else: 
                fact_context["periodType"] = "duration"
                fact_context["duration"] = {
                    "startDate": "2025-07-01",
                    "endDate": "2026-06-30"
                }

            report['facts'].append({
                "value": mag_val,
                "decimals": 2,
                "unit": "iso4217:AUD",
                "context": fact_context
            })

    for c_id in sorted(list(discovered_concepts)):
        c_label = c_id.replace('section:', '').replace('-', ' ').title()
        section_obj = {
            "@id": c_id,
            "@type": "ReportSection",
            "label": { "en": c_label }
        }
        
        parent_id = map_hierarchy(c_id)
        if parent_id:
            section_obj["isPartOf"] = { "@id": parent_id }
            
        report['reportStructure'].append(section_obj)

    with open('vault_report_export.jsonld', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print("[SUCCESS] JSON-LD Exported")

if __name__ == "__main__":
    compile_jsonld_report()