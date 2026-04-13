import json
import subprocess
import hashlib
from datetime import datetime
from heuristic_mapper import process_trial_balance

def run_pipeline():
    print("--- 1. Running Neuro-Semantic Filter ---")
    facts = process_trial_balance(
        "02_Data/dummy_tb.csv", 
        "01_Ontology/core_mini_taxonomy.yaml", 
        "03_Registry/Quarantine/"
    )

    print("\n--- 2. Aggregating Magnitudes for Prolog ---")
    buckets = {"Assets": 0.0, "Liabilities": 0.0, "Equity": 0.0, "Revenue": 0.0, "Expenses": 0.0}
    
    for f in facts:
        concept = f["mapped_concept"]
        balance = float(f["balance"])
        
        # Convert trial balance (Debits +, Credits -) to absolute magnitudes for the SBRM equations
        if concept in ["Assets", "Expenses"]:
            buckets[concept] += balance
        elif concept in ["Liabilities", "Equity", "Revenue"]:
            buckets[concept] += -balance # Invert credit balances to positive magnitudes

    print(f"Magnitudes: {buckets}")

    print("\n--- 3. Engaging Prolog Physics Engine ---")
    # Call SWI-Prolog via subprocess to mathematically prove the equations
    pl_cmd = (
        f"swipl -q -l 00_Architecture/sbrm_core.pl -g "
        f"\"verify_report_set({buckets['Assets']}, {buckets['Liabilities']}, {buckets['Equity']}, "
        f"{buckets['Revenue']}, {buckets['Expenses']}, IsConsistent), "
        f"find_delta({buckets['Assets']}, {buckets['Liabilities']}, {buckets['Equity']}, "
        f"{buckets['Revenue']}, {buckets['Expenses']}, Delta), "
        f"format('~w|~w', [IsConsistent, Delta]), halt.\""
    )
    
    result = subprocess.check_output(pl_cmd, shell=True, text=True).strip()
    is_consistent, delta_str = result.split('|')
    is_consistent_bool = True if is_consistent == "true" else False
    
    print(f"Prolog Verification: {'✅ PASS' if is_consistent_bool else '❌ FAIL'}")
    if not is_consistent_bool:
        print(f"Thermodynamic Void (Delta): {delta_str}")

    print("\n--- 4. Generating Deterministic JSON-LD ---")
    report_id = hashlib.sha256(str(buckets).encode()).hexdigest()
    
    jsonld = {
        "@context": {
            "sbrm": "https://lodgeit.global/ontology/sbrm/v1#",
            "core": "https://lodgeit.global/ontology/core/v1#",
            "ReportSet": "sbrm:ReportSet",
            "ValidationState": "sbrm:ValidationState",
            "Fact": "sbrm:Fact",
            "hasFact": {"@id": "sbrm:hasFact", "@container": "@set"},
            "hasValidation": {"@id": "sbrm:hasValidation", "@container": "@set"}
        },
        "@id": f"urn:lodgeit:reportset:sha256:{report_id}",
        "@type": "ReportSet",
        "entity": "urn:abn:12345678901",
        "asOfDate": datetime.utcnow().isoformat() + "Z",
        "hasValidation": [
            {
                "@type": "ValidationState",
                "ruleTested": "core:BalanceSheetEquation",
                "isConsistent": is_consistent_bool,
                "calculatedDelta": float(delta_str)
            }
        ],
        "hasFact": [
            {
                "@id": f"urn:lodgeit:fact:{f['raw_account'].lower().replace(' ', '_')}",
                "@type": "Fact",
                "concept": f"core:{f['mapped_concept']}",
                "value": f["balance"],
                "unit": "iso4217:AUD"
            } for f in facts
        ]
    }
    
    output_path = "03_Registry/final_report.jsonld"
    with open(output_path, "w") as f:
        json.dump(jsonld, f, indent=2)
        
    print(f"✅ SBRM Report Set successfully minted to: {output_path}")

if __name__ == "__main__":
    run_pipeline()
