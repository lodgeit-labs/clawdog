# LodgeiT ClawDog V1 (Baby Release)

**Purpose-built for MyClaw & Gemini 3.0**  
A zero-hallucination, neuro-symbolic accounting engine designed for the **File over App** ecosystem. 

This repository proves that we can marry the chaos-tolerance of LLMs (to ingest messy general ledgers) with the strict, mathematical determinism of SWI-Prolog (to calculate tax and prove accounting equations), outputting a cryptographic JSON-LD SBRM Report.

## 🧠 Neuro-Semantic Engine & Graceful Degradation
This package is heavily optimized for **Gemini 3.0** via the MyClaw/OpenClaw environment.
However, if you are running OpenClaw locally without a Gemini API key (or prefer not to use LLMs), **the system fails down gracefully**. It will automatically bypass the Gemini APIs and rely on primitive, algorithmic heuristics (keyword/magnitude scanning) requiring minimal to zero additional installs.

## 🚀 How to Run

### Path A: The Accountant (Zero-Install via MyClaw)
*Coming soon.*
For accounting professionals, this engine will be available as a one-click **AgentSkill** via a LodgeiT landing page. By subscribing to MyClaw (with Gemini 3.0), the ClawDog engine runs autonomously in the background. No terminal, no Python, no Git required.

### Path B: The Developer (Local Execution)
For developers contributing to the physics engine or building Heuristic Packs:
1. Ensure Python 3.10+ and SWI-Prolog are installed.
2. `pip install pandas pyyaml`
3. Run the pipeline:

*Check `03_Registry/Quarantine/` for anomalies requiring your human resolution.*
*Check `03_Registry/final_report.jsonld` for the mathematically proven output.*

## 📂 Repository Structure
* `/00_Architecture/` - The Prolog physics engine (`sbrm_core.pl`) and the manifesto.
* `/01_Ontology/` - The `core_mini_taxonomy.yaml` mapping targets.
* `/02_Data/` - The raw, immutable CSV inputs (`dummy_tb.csv`, `dummy_gl.csv`).
* `/03_Registry/` - Where the Agentic Socket stores Markdown state (Quarantines, AJEs) and final JSON-LD reports.

## ⚖️ License & Attribution
This project is licensed under the MIT License with a strict attribution clause. 
Any derivative works or integrations **must prominently display**: 
*"Powered by the LodgeiT ClawDog SBRM Engine."*
See `LICENSE` for details.
