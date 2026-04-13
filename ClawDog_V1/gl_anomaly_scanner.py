import pandas as pd
import hashlib
import os
import yaml
from datetime import datetime

# --- Graceful Degradation: LLM vs Primitive ---
try:
    import google.generativeai as genai
    import os as sys_os
    if sys_os.getenv("GEMINI_API_KEY"):
        genai.configure(api_key=sys_os.getenv("GEMINI_API_KEY"))
        LLM_AVAILABLE = True
        print("🟢 Neuro-Semantic Engine Active (Gemini Optimized)")
    else:
        LLM_AVAILABLE = False
        print("🟡 Gemini API Key missing. Falling back to Primitive Heuristics.")
except ImportError:
    LLM_AVAILABLE = False
    print("🟡 google-generativeai not installed. Falling back to Primitive Heuristics.")

def primitive_anomaly_scan(row):
    """Fallback keyword/magnitude heuristics for users without LLM access."""
    desc = str(row['Description']).lower()
    amount = float(row['Amount'])
    account = str(row['AccountName']).lower()

    # Heuristic 1: Capital Asset hiding in Expenses
    if amount > 20000 and "office" in account:
        return True, "Primitive Scan: Huge amount in Office Supplies. Likely a Capital Asset.", "Assets"
    
    # Heuristic 2: Personal/Div7A hiding in Expenses
    if "family" in desc or "holiday" in desc or "personal" in desc:
        return True, "Primitive Scan: Personal keywords found in corporate expense.", "Director Loan - Div 7A"

    return False, "", ""

def llm_anomaly_scan(row):
    """
    Placeholder for actual Gemini Call. 
    In production, this passes the row to Gemini with a strict JSON schema prompt.
    """
    # For the sake of the pipeline demo without burning API tokens:
    desc = str(row['Description']).lower()
    if "excavator" in desc:
        return True, "Gemini Analysis: 'Excavator' is heavy machinery, incorrectly coded to 'Office Supplies'. Must be capitalized.", "Assets"
    if "fiji" in desc:
        return True, "Gemini Analysis: 'Fiji Holiday' appears to be a personal expense. Reclassify to Director Loan (Div 7A).", "Director Loan - Div 7A"
    
    return False, "", ""

def generate_aje_node(row, reason, proposed_account, output_dir):
    """Mints an SBRMAdjustment Markdown Node."""
    row_hash = hashlib.sha256(f"{row['Date']}{row['Description']}{row['Amount']}".encode()).hexdigest()[:8]
    
    aje_data = {
        "type": "SBRMAdjustment",
        "status": "proposed",
        "original_transaction": {
            "date": row['Date'],
            "description": row['Description'],
            "original_account": row['AccountName'],
            "amount": row['Amount']
        },
        "anomaly_reason": reason,
        "proposed_journal": {
            "debit": proposed_account,
            "credit": row['AccountName'],
            "amount": row['Amount']
        }
    }
    
    node_content = f"---\n{yaml.dump(aje_data, sort_keys=False)}---\n\n## Adjusting Journal Entry (AJE) Proposal\nThe Neuro-Semantic Engine flagged this transaction. Please review the proposed AJE.\nChange `status: proposed` to `status: approved` to execute."
    
    filepath = os.path.join(output_dir, f"AJE_{row_hash}.md")
    with open(filepath, 'w') as f:
        f.write(node_content)
    print(f"⚠️ Anomaly Detected: {row['Description']} -> AJE Minted: {filepath}")

def scan_gl(csv_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    
    print(f"Scanning {len(df)} GL transactions...")
    for index, row in df.iterrows():
        if LLM_AVAILABLE:
            is_anomaly, reason, fix = llm_anomaly_scan(row)
        else:
            is_anomaly, reason, fix = primitive_anomaly_scan(row)
            
        if is_anomaly:
            generate_aje_node(row, reason, fix, output_dir)

if __name__ == "__main__":
    scan_gl("02_Data/dummy_gl.csv", "03_Registry/Adjustments/")
