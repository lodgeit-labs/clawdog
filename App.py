import streamlit as st
import json
import pandas as pd
import time

# --- UI CONFIGURATION ---
st.set_page_config(page_title="ClientRelay | SBRM Dashboard", layout="wide")
st.title("⚡ ClientRelay SBRM Dashboard")
st.markdown("### Powered by LodgeiT Global Neurosemantic Engine")

# --- DATA INGESTION ---
@st.cache_data
def load_data():
    try:
        with open('vault_report_export.jsonld', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

data = load_data()

if not data:
    st.error("⚠️ Could not locate vault_report_export.jsonld. Please run the backend compilers.")
else:
    facts = data.get('facts', [])

    # Helper to extract values from the JSON-LD semantic graph
    def get_val(section_id):
        return sum(f['value'] for f in facts if f.get('context', {}).get('parentSection', {}).get('@id') == section_id)

    # Extract our Master Nodes
    assets = get_val('section:total-assets')
    liab = get_val('section:total-liabilities')
    equity = get_val('section:total-equity')
    rev = get_val('section:revenue')
    exp = get_val('section:expenses')
    pl = get_val('section:profit-loss')

    # --- TOP METRICS ROW ---
    st.header("Financial Overview (SBRM Master Nodes)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Assets", f"${assets:,.2f}")
    col2.metric("Total Liabilities", f"${liab:,.2f}")
    col3.metric("Total Equity", f"${equity:,.2f}")
    col4.metric("Net Profit", f"${pl:,.2f}")

    st.divider()

    # --- THE REASONER BUTTON (SIMULATING API CALL) ---
    st.subheader("🛡️ Multidimensional Integrity Reasoner")
    st.markdown("Click below to run the underlying 'Zero Hallucination' mathematical proof.")
    
    if st.button("Execute SBRM Proof"):
        with st.spinner("Connecting to L402 Gateway... Executing Proofs..."):
            time.sleep(1.5) # Simulating network latency
            
            # Layer C Checks
            if abs(assets - (liab + equity)) < 0.01:
                st.success(f"✅ **Layer C.1 PASS:** Accounting Equation Holds (Assets ${assets:,.2f} = Liab ${liab:,.2f} + Equity ${equity:,.2f})")
            else:
                st.error("❌ **Layer C.1 FAIL:** Accounting Equation Broken")
            
            if abs((rev - exp) - pl) < 0.01:
                st.success(f"✅ **Layer C.3 PASS:** P&L Articulation Valid (Rev ${rev:,.2f} - Exp ${exp:,.2f} = P&L ${pl:,.2f})")
            else:
                st.error("❌ **Layer C.3 FAIL:** P&L Articulation Broken")

    st.divider()

    # --- SUB-LEDGER VISUALIZATION ---
    st.subheader("Live Semantic Ledger")
    
    # Flatten JSON-LD facts into a nice visual table
    df_data = []
    for f in facts:
        sec = f.get('context', {}).get('parentSection', {}).get('@id', '').replace('section:', '')
        df_data.append({
            "SBRM Concept": sec.replace('-', ' ').title(), 
            "Value (AUD)": f['value'], 
            "Period Type": f.get('context', {}).get('periodType', 'instant')
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)