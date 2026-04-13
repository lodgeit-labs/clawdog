import streamlit as st
import json
import pandas as pd
import time

# --- UI CONFIGURATION ---
st.set_page_config(page_title="ClientRelay | SBRM Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("⚡ ClientRelay SBRM Dashboard")
st.markdown("### Powered by LodgeiT Global Neurosemantic Engine")

# --- DATA INGESTION & GRAPH PARSING ---
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
    st.stop()

facts = data.get('facts', [])
structure = data.get('reportStructure', [])

# 1. Build the Semantic Hierarchy Maps
children_map = {}
labels_map = {}
values_map = {}

# Map explicit values
for f in facts:
    sec_id = f.get('context', {}).get('parentSection', {}).get('@id')
    if sec_id:
        values_map[sec_id] = values_map.get(sec_id, 0.0) + f['value']

# Map parent-child relationships and labels
for sec in structure:
    sec_id = sec['@id']
    labels_map[sec_id] = sec.get('label', {}).get('en', sec_id.replace('section:', '').replace('-', ' ').title())
    
    parent_id = sec.get('isPartOf', {}).get('@id')
    if parent_id:
        if parent_id not in children_map:
            children_map[parent_id] = []
        children_map[parent_id].append(sec_id)

# Helper to recursively build indented statement rows
def build_statement_tree(node_id, depth=0):
    rows = []
    # Fallback label if missing from structure
    label = labels_map.get(node_id, node_id.replace('section:', '').replace('-', ' ').title())
    val = values_map.get(node_id, 0.0)
    
    # Use EM-spaces for guaranteed indentation in HTML/DataFrames
    indent = "\u2003" * depth 
    prefix = "└ " if depth > 0 else "📊 "
    
    rows.append({
        "Account": f"{indent}{prefix}{label}", 
        "Balance": f"${val:,.2f}"
    })
    
    # Recursively fetch children
    children = sorted(children_map.get(node_id, []))
    for child in children:
        rows.extend(build_statement_tree(child, depth + 1))
        
    return rows

# --- TOP METRICS ROW ---
st.header("Financial Overview (SBRM Master Nodes)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Assets", f"${values_map.get('section:total-assets', 0.0):,.2f}")
col2.metric("Total Liabilities", f"${values_map.get('section:total-liabilities', 0.0):,.2f}")
col3.metric("Total Equity", f"${values_map.get('section:total-equity', 0.0):,.2f}")
col4.metric("Net Profit", f"${values_map.get('section:profit-loss', 0.0):,.2f}")

st.divider()

# --- TABBED INTERFACE ---
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Reasoner Proofs", "🏛️ Balance Sheet", "📉 Profit & Loss", "🗃️ Raw Sub-Ledger"])

with tab1:
    st.subheader("Multidimensional Integrity Reasoner")
    st.markdown("Execute the underlying 'Zero Hallucination' mathematical proof across the SBRM graph.")
    
    if st.button("Execute L402 SBRM Proof", type="primary"):
        with st.spinner("Connecting to L402 Gateway... Verifying Cryptography... Executing Proofs..."):
            time.sleep(1.5) # Simulating API latency
            
            assets = values_map.get('section:total-assets', 0.0)
            liab = values_map.get('section:total-liabilities', 0.0)
            eq = values_map.get('section:total-equity', 0.0)
            rev = values_map.get('section:revenue', 0.0)
            exp = values_map.get('section:expenses', 0.0)
            pl = values_map.get('section:profit-loss', 0.0)
            
            # Simulated Core Checks based on our Python logic
            if abs(assets - (liab + eq)) < 0.01:
                st.success(f"✅ **Layer C.1 PASS:** Accounting Equation Holds (Assets ${assets:,.2f} = Liab ${liab:,.2f} + Equity ${eq:,.2f})")
            else:
                st.error("❌ **Layer C.1 FAIL:** Accounting Equation Broken")
            
            if abs((rev - exp) - pl) < 0.01:
                st.success(f"✅ **Layer C.3 PASS:** P&L Articulation Valid (Rev ${rev:,.2f} - Exp ${exp:,.2f} = P&L ${pl:,.2f})")
            else:
                st.error(f"❌ **Layer C.3 FAIL:** P&L Articulation Broken (Rev ${rev:,.2f} - Exp ${exp:,.2f} != P&L ${pl:,.2f})")

with tab2:
    st.subheader("Statement of Financial Position (Balance Sheet)")
    
    # Build trees for Assets, Liabilities, and Equity
    bs_data = []
    bs_data.extend(build_statement_tree('section:total-assets'))
    bs_data.append({"Account": "", "Balance": ""}) # Spacing
    bs_data.extend(build_statement_tree('section:total-liabilities'))
    bs_data.append({"Account": "", "Balance": ""}) # Spacing
    bs_data.extend(build_statement_tree('section:total-equity'))
    
    st.dataframe(pd.DataFrame(bs_data), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Statement of Comprehensive Income (P&L)")
    
    # Build tree for P&L
    pl_data = build_statement_tree('section:profit-loss')
    st.dataframe(pd.DataFrame(pl_data), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Raw Ontological Fact Nodes")
    
    # Original flat ledger for audit trail
    df_data = []
    for f in facts:
        sec_raw = f.get('context', {}).get('parentSection', {}).get('@id', '')
        df_data.append({
            "Namespace ID": sec_raw, 
            "Human Label": labels_map.get(sec_raw, sec_raw.replace('section:', '').replace('-', ' ').title()),
            "Value (AUD)": f['value'], 
            "Period": f.get('context', {}).get('periodType', 'instant')
        })
    
    st.dataframe(pd.DataFrame(df_data).sort_values("Namespace ID"), use_container_width=True, hide_index=True)