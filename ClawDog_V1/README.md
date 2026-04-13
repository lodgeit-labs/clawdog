# LodgeiT ClawDog V1 (Baby Release)

**Purpose-built for MyClaw & Gemini 3.0**  
A zero-hallucination, neuro-symbolic accounting engine designed for the **File over App** ecosystem. 

This repository proves that we can marry the chaos-tolerance of LLMs (to ingest messy general ledgers) with the strict, mathematical determinism of SWI-Prolog (to calculate tax and prove accounting equations), outputting a cryptographic JSON-LD SBRM Report.

## 🧠 Neuro-Semantic Engine & Graceful Degradation
This package is heavily optimized for **Gemini 3.0** via the MyClaw/OpenClaw environment.
However, if you are running OpenClaw locally without a Gemini API key (or prefer not to use LLMs), **the system fails down gracefully**. It will automatically bypass the Gemini APIs and rely on primitive, algorithmic heuristics (keyword/magnitude scanning) requiring minimal to zero additional installs.

## 🚀 Quick Start

### Prerequisites
* Python 3.10+
* SWI-Prolog (`swipl`)
* `pip install pandas pyyaml`
* *(Optional)* `pip install google-generativeai` (For Gemini neuro-semantic mapping)

### 1. Run the GL Anomaly Scanner
Scans the General Ledger for line-item anomalies (e.g. capitalizing assets hidden in expenses) and mints Adjusting Journal Entry (AJE) markdown nodes.
```bash
python3 gl_anomaly_scanner.py
```
*Check `03_Registry/Adjustments/` for the generated AJE proposals.*

### 2. Run the Core SBRM Pipeline
Ingests the Trial Balance, maps it to the Core Taxonomy via heuristics, pauses for Human-in-the-Loop (HITL) resolution if confidence is low, and mathematically proves the ledger via Prolog before generating JSON-LD.
```bash
python3 bridge_pipeline.py
```
*Check `03_Registry/Quarantine/` for anomalies requiring your human resolution.*
*Check `03_Registry/final_report.jsonld` for the mathematically proven output.*

## 📂 Repository Structure
* `/00_Architecture/` - The Prolog physics engine (`sbrm_core.pl`) and the manifesto.
* `/01_Ontology/` - The `core_mini_taxonomy.yaml` mapping targets.
* `/02_Data/` - The raw, immutable CSV inputs (`dummy_tb.csv`, `dummy_gl.csv`).
* `/03_Registry/` - Where the Agentic Socket stores Markdown state (Quarantines, AJEs) and final JSON-LD reports.

## 📖 Architecture
Read the `00_Architecture/V1_ARCHITECTURE_MANIFESTO.md` to understand the Infoverse Protocol, Cryptographic Mereology, and the Markdown State Machine.