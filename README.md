# LodgeiT Global: Decentralized SBRM & L402 Network

## 1. Executive Overview
This repository represents the **Genesis Seed** for a neurosemantic accounting and tax compliance architecture. It fundamentally rejects legacy relational databases in favor of a decentralized, multidimensional knowledge graph built on the **"File over App"** philosophy.

Every financial fact, structural taxonomy, and logical rule is stored as a locally-addressable, human-readable Markdown file (`.md`) wrapped in rich JSON-LD/YAML metadata. The system bridges deterministic financial logic (SBRM/OIM) via a neurosymbolic Prolog engine, and connects it to a machine-to-machine micro-transactional economy via the Lightning Network.

## 2. Core Vault Architecture
The vault is organized into strict, decoupled functional domains:

* **`00_Architecture/`**: Governs the structural axioms, cryptographic sovereignty protocols, journals, and system manifests.
* **`01_Ontology/`**: The "Ground Truth" layer containing reporting entities, periods, and the atomic SBRM financial facts.
* **`02_Rules/`**: Immutable SBRM-based logic predicates, SWI-Prolog Knowledge Bases (`sbrm_kb.pl`), and jurisdictional tax laws (e.g., ATO Instant Asset Write-Off).
* **`03_Registry/`**: Master indexes for namespace resolution, Trusted Authorities, and L402 access tiers.
* **`04_WorkingPapers/`**: The provenance layer designed to hold physical evidence (e.g., scanned Bank Statement PDFs) cross-referenced to specific ontological facts.

## 3. Cryptographic Sovereignty
To ensure a "Zero Hallucination" inference environment, every node utilizes a **SHA-256 content hash**. The system enforces a "No Hash, No Logic" policy; nodes with mismatched signatures are quarantined from the logic engine.

## 4. The Neurosymbolic Logic Engine (SWI-Prolog)
Unlike standard flat-file databases, LodgeiT Global utilizes a formal deductive logic engine (SWI-Prolog) to execute multidimensional proofs without hallucination. 

* **The Prolog Bridge:** The system parses the Python/YAML knowledge graph and mints strict Arity-6 Prolog facts (`sbrm_fact/6`).
* **Time-Aware Proofs:** The engine natively understands SBRM temporal joins, correctly binding multiple time periods (e.g., 2025 Instant + 2026 Duration) into single logical roll-forward proofs.
* **Jurisdictional Routing:** Universal GAAP facts are conditionally routed through localized tax boundaries (e.g., Australian Taxation Office limits) without polluting the core ontology.

## 5. The Agentic Toolkit
The repository includes a suite of Python-based drivers located in the root directory to manage the hypercube:

| Agent Script | Function |
| :--- | :--- |
| **`Uplift_Agent.py`** | Ingests flat `trial_balance.csv` files and mints 3D SBRM semantic fact nodes. |
| **`heal_vault.py`** | Idempotently resets Master nodes and mints missing OIM leaf nodes to ensure perfect graph symmetry. |
| **`consolidate_hypercube.py`** | Aggregates atomic seeds and CSV uplifts into Master roll-up nodes. |
| **`sync_signatures.py`** | Recalculates and injects SHA-256 cryptographic hashes into the YAML frontmatter. |
| **`export_jsonld_report.py`** | Compiles the multidimensional Markdown facts into a globally standardized `vault_report_export.jsonld` Open Information Model (OIM) document. |
| **`extract_vault_state.py`** | Maps the ontological boundaries and isolates active nodes for the logic engine. |
| **`prolog_bridge.py`** | Translates the JSON-LD graph into a strict SWI-Prolog Knowledge Base. |
| **`evaluate_oim_report.py`** | The deterministic reasoner. Evaluates Layer A (OIM Fidelity), Layer B (Hypercube Roll-ups), and Layer C (Core Accounting Equations). |
| **`l402_middleware.py`** | The decentralized API Gateway. Wraps the logic engine behind a Lightning Network paywall (HTTP 402). |
| **`client_relay_ping.py`** | Simulates a remote ClientRelay node requesting a proof and settling the Satoshi invoice. |

## 6. The Standard Execution Pipeline
To process new data, execute the logic engine, and generate a monetized SBRM proof, run the pipeline in this sequence:

1. **Ingest & Map:** `python Uplift_Agent.py`
2. **Consolidate & Heal:** `python heal_vault.py` followed by `python consolidate_hypercube.py`
3. **Lock Cryptography:** `python sync_signatures.py`
4. **Compile OIM Document:** `python export_jsonld_report.py`
5. **Neurosymbolic Validation:** Run the Prolog logic tests via `python logic.py` and the OIM reasoner via `python evaluate_oim_report.py`.
6
