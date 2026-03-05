# LodgeiT Global: Neurosemantic SBRM & L402 Engine

## 1. Executive Overview
This repository contains the core neurosymbolic accounting and tax compliance architecture for LodgeiT Global. It fundamentally rejects legacy relational databases in favor of a decentralized, multidimensional knowledge graph built on a strict **"File over App"** philosophy.

The system utilizes a **Dual-State Architecture**:
1. **The State (Immutable Truth):** Financial facts, structural taxonomies, and ontological boundaries are stored as locally addressable, human-readable Markdown files (`.md`) wrapped in strict YAML metadata.
2. **The Logic (Active Reasoning):** Deterministic financial and jurisdictional logic is executed via a stateless neurosymbolic engine (SWI-Prolog), completely decoupled from the data layer.

## 2. Core Vault Architecture
The repository is organized into strict, functional domains:

* **`00_Architecture/`**: Governs the structural axioms, system manifests, and architectural design documentation (e.g., `Architecture_Rules_and_Execution.md`).
* **`01_Ontology/`**: The "Ground Truth" layer containing reporting entities, reporting periods, and the atomic Standard Business Reporting Model (SBRM) financial fact nodes.
* **`02_Rules/`**: The execution layer containing immutable SBRM Markdown boundaries (`rule-*.md`) alongside the active SWI-Prolog Knowledge Bases (`sbrm_kb.pl`, `gst_tax_rules.pl`).
* **`03_Registry/`**: Master indexes for namespace resolution and cross-domain mappings.
* **`_legacy_scripts/`**: Archived scaffolding, ingestion agents, and transitional scripts from early development phases.

## 3. Cryptographic Sovereignty & GitOps (The Gatekeeper)
To ensure a "Zero Hallucination" inference environment, the repository enforces strict cryptographic integrity. 
* Every active SBRM node utilizes a **SHA-256 content hash** to prevent "Truth Decay."
* The repository is protected by a Git `pre-commit` hook powered by **`audit_ontology_v2.py`**. 
* If a node's YAML parameters violate Charles Hoffman's multidimensional constraints, or if the markdown body is edited without authorization, the commit is mathematically rejected.

## 4. The Core Application Layer
The root directory contains three primary Python execution points that interact with the underlying Prolog reasoning engine:

| Application | Description |
| :--- | :--- |
| **`audit_ontology_v2.py`** | The Cryptographic Gatekeeper. Scans the local directory to verify the semantic and structural integrity of all SBRM nodes. |
| **`prolog_app.py`** | The L402 Execution Wrapper. A Tkinter desktop GUI that intercepts simulated Lightning Network (L402) micropayments and triggers headless, stateless Prolog subprocesses for cross-domain tax inference. |
| **`App.py`** | The SBRM Visualizer. A Streamlit web dashboard that parses the `vault_report_export.jsonld` payload to render multidimensional balance sheets, P&L statements, and multidimensional integrity proofs. |

## 5. Developer Onboarding
If you are cloning this repository for the first time, you must verify your local environment before executing any logic. 

Please see **`Developer Onboarding.md`** for the mandatory 4-Phase execution runbook:
1. Verify Ontological Integrity
2. Verify Raw Prolog Inference
3. Verify the Stateless Python Wrapper
4. Verify the Visual Web Graph