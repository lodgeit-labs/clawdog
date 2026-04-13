# LodgeiT ClawDog V1: Architecture Manifesto

## The Vision
LodgeiT ClawDog is a neuro-symbolic accounting and tax compliance engine built on the "File over App" philosophy. It leverages the chaos-tolerance of Large Language Models (LLMs) and the strict, mathematical determinism of SWI-Prolog to create a zero-hallucination compliance pipeline.

## The Three Pillars of the Infoverse Protocol

### 1. The Data Pipeline (The Factory Floor)
Raw data is massive, messy, and immutable. We process it via a strict, one-way pipeline:
1. **Raw CSV Ingestion:** General Ledger (GL) and Trial Balance (TB) data is loaded into memory via Pandas. The source files are **never** modified.
2. **Neuro-Semantic Filter (LLM):** The LLM maps human-messy account names and transaction descriptions to strict multidimensional concepts in the SBRM Taxonomy.
3. **Prolog Core Physics:** The mapped facts are evaluated by a Prolog deterministic engine to prove structural equations (e.g., `Assets = Liabilities + Equity`).
4. **Deterministic JSON-LD:** The verified state is serialized into an RDF-compatible JSON-LD graph, cryptographically anchored via SHA-256 hashes.

### 2. The Exception Protocol (The Manager's Desk)
LLMs are probabilistic; accounting is exact. We bridge this gap using the **Markdown State Machine**.
* **Quarantines:** If the LLM confidence falls below 95%, or an anomaly is detected (e.g., a $150k excavator in Office Supplies), the system halts automation for that specific node.
* **Human-in-the-loop (HITL):** It mints a `quarantine_<hash>.md` file with YAML frontmatter.
* **Agentic Socket:** The user resolves the anomaly via chat with their AI agent, which updates the Markdown file. The pipeline instantly resumes.

### 3. The Extension Ecosystem (Knowledge Artifacts)
The system is built to scale fractally. The core physics (`core_mini_taxonomy.yaml` and `sbrm_core.pl`) remain untouched. Domain experts can deploy **Knowledge Artifacts** to expand the system's intelligence.
A Knowledge Artifact consists of:
* `ontology.yaml` (The Vocabulary)
* `heuristics.py` (The LLM mapping rules)
* `logic.pl` (The deterministic tax math)
* *Example:* A "Hire Purchase Pack" automatically detects HP loans, calculates amortization, and mints adjusting entries.

## Cryptographic Mereology (The Adjusting Journal Entry)
When the system calculates a necessary fix (a Thermodynamic Void), it does not alter the raw CSV. Instead, it mints an `SBRMAdjustment_<hash>.md` node. This node cryptographically binds the exact Adjustment (AJE) to the raw data, preserving an unforgeable, step-by-step audit trail of how the final numbers were achieved.