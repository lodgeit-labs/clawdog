import os
import yaml

def extract_yaml_frontmatter(filepath):
    """Isolates and parses the JSON-LD YAML block from a Markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1])
            except yaml.YAMLError:
                return None
    return None

def compile_knowledge_base():
    rules_dir = './02_Rules'
    ontology_dir = './01_Ontology'
    pl_output_path = os.path.join(rules_dir, 'sbrm_kb.pl')

    if not os.path.exists(rules_dir):
        os.makedirs(rules_dir)

    with open(pl_output_path, 'w', encoding='utf-8') as kb:
        kb.write("% =========================================================\n")
        kb.write("% SYSTEM: OPEN-SOURCE SBRM HYPERCUBE\n")
        kb.write("% LAYER: LOGIC & INFERENCE (SWI-PROLOG)\n")
        kb.write("% =========================================================\n\n")
        
        kb.write(":- dynamic sbrm_fact/6.\n\n")
        kb.write("% --- 1. DECENTRALIZED FACT ASSERTIONS ---\n")
        kb.write("% Arity 6: sbrm_fact(Entity, Period, Concept, Magnitude, Unit, ArrangementPattern).\n\n")

        fact_count = 0
        for root, _, files in os.walk(ontology_dir):
            for file in files:
                if not file.endswith('.md'):
                    continue
                
                filepath = os.path.join(root, file)
                fm = extract_yaml_frontmatter(filepath)
                if not fm:
                    continue

                # Enforce ontological boundary: Skip epistemic nodes/definitions lacking a hypercube context
                hc = fm.get('hypercube_context')
                if not hc or hc.get('arrangement_pattern') == 'SemanticLink':
                    continue

                edges = fm.get('edges', [])
                if not edges:
                    continue

                # Resolve SBRM Semantic Triples
                entity = next((e['target'] for e in edges if e['rel'] == 'sbrm:hasReportingEntity'), 'unknown')
                period = next((e['target'] for e in edges if e['rel'] == 'sbrm:hasReportingPeriod'), 'unknown')
                concept = next((e['target'] for e in edges if e['rel'] == 'sbrm:isInstanceOfConcept'), 'unknown')

                # Extract magnitude (fallback to an unbound Prolog variable '_' if not explicitly defined yet)
                magnitude = fm.get('value', fm.get('magnitude', fm.get('fact_value', '_')))
                pattern = hc.get('arrangement_pattern', 'Unknown')

                kb.write(f"sbrm_fact('{entity}', '{period}', '{concept}', {magnitude}, 'AUD', '{pattern}').\n")
                fact_count += 1

        kb.write(f"\n% [SYSTEM] {fact_count} Multidimensional Facts Compiled.\n\n")

        kb.write("% --- 2. SBRM OPERATIVE PREDICATES ---\n\n")
        
        # Fundamental Accounting Equation
        kb.write("% Rule: rule-sbrm-accounting-equation\n")
        kb.write("is_balanced(Entity, Period) :-\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-assets', Assets, _, 'Hierarchy'),\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-liabilities', Liabilities, _, 'Hierarchy'),\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-equity', Equity, _, 'RollForward'),\n")
        kb.write("    Assets =:= Liabilities + Equity.\n\n")

        # Roll-Up: Asset Hierarchy
        kb.write("% Rule: rule-sbrm-asset-rollup\n")
        kb.write("validate_asset_rollup(Entity, Period) :-\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-current-assets', CA, _, 'Hierarchy'),\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-non-current-assets', NCA, _, 'Hierarchy'),\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-assets', TA, _, 'Hierarchy'),\n")
        kb.write("    TA =:= CA + NCA.\n\n")

        # Roll-Forward: Equity Timeline
        kb.write("% Rule: rule-sbrm-equity-rollforward\n")
        kb.write("validate_equity_rollforward(Entity, Period) :-\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-opening-equity', Opening, _, 'RollForward'),\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-profit-loss', PL, _, 'RollUp'),\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-dividends-paid', Div, _, 'RollForward'),\n")
        kb.write("    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-equity', Closing, _, 'RollForward'),\n")
        kb.write("    Closing =:= Opening + PL - Div.\n\n")

    print(f"[SUCCESS] Prolog Knowledge Base compiled to {pl_output_path}")
    print(f"[SYSTEM] Minted {fact_count} deterministic SBRM facts.")

if __name__ == "__main__":
    compile_knowledge_base()