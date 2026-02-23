This **README** serves as the user manual for the "Genesis Seed" you just successfully anchored to GitHub. It explains the "File over App" philosophy, the cryptographic integrity layer, and how to use the ingestion pipeline you've built.

---

# README: LodgeiT Global SBRM Seed

## 1. Executive Overview

This repository represents the **Genesis Seed** for a neurosemantic accounting architecture. It fundamentally rejects legacy relational databases in favor of a decentralized, multidimensional knowledge graph built on the **"File over App"** philosophy.

Every financial fact and logical rule is stored as a locally-addressable, human-readable Markdown file (`.md`) with rich JSON-LD/YAML metadata.

## 2. Core Architecture

The vault is organized into functional domains to ensure logical decoupling:

* **`00_Architecture/`**: Governs the structural axioms, cryptographic sovereignty protocols, and system manifests.
* **`01_Ontology/`**: The "Ground Truth" layer containing reporting entities, periods, and financial facts.
* **`02_Rules/`**: Immutable SBRM-based logic predicates (Accounting equations, roll-ups, and fan-outs).
* **`03_Registry/`**: Master indexes for namespace resolution and L402 Lightning Network access tiers.

## 3. Cryptographic Sovereignty

To ensure a "Zero Hallucination" environment, every node utilizes a **SHA-256 content hash**.

* **Integrity Enforcement**: The system performs a "No Hash, No Logic" policy; nodes with mismatched signatures are quarantined from the inference engine.
* **Agentic Healing**: Local Python agents monitor for "truth decay" and provide automated repair of metadata formatting.

## 4. The Agentic Toolkit

The repository includes a suite of Python-based drivers to manage the hypercube:

| Script | Function |
| --- | --- |
| **`l402_middleware.py`** | API Gateway that issues Lightning invoices (Sats) for logic execution. |
| **`sync_signatures.py`** | Recalculates and injects SHA-256 hashes into Markdown frontmatter. |
| **`Uplift_Agent.py`** | The "Universal Translator" that ingests flat CSV Trial Balances into semantic nodes. |
| **`00_Architecture_Integrity_Scanner.py`** | Performs a cryptographic audit of the entire vault status. |

## 5. Getting Started

1. **Ingest Data**: Place a `trial_balance.csv` in the root and run `python Uplift_Agent.py` to mint new fact nodes.
2. **Verify Integrity**: Run `python sync_signatures.py` followed by the scanner to ensure all nodes are integral.
3. **Execute Logic**: Use the `l402_middleware.py` to simulate a paid API request and trigger the SBRM logic engine.

---


