# ClawDog Pipeline

This repository contains the standalone, stripped-down ClawDog **Wind Tunnel** — a development harness that demonstrates the neurosemantic approach to financial reporting: taking raw General Ledger CSV files, mapping them to the SBRM taxonomy, running them through a strict Prolog physics engine (to ensure double-entry accounting math holds true), and rendering the final output to JSON-LD and iXBRL format.

> **Wind Tunnel vs Production.** The code under `wind_tunnel/` is a *local development harness* for proving Prolog logic against small CSV ledgers. It is **not** the production ingestion path. Production uses the `fano-classifier` Cloud Run service → SBRM atoms → `clawdog-calculator-api` (Cloud Run) → per-calculator engines + MCP parallel client. See Brain canon [`GLOBAL_NOTES/CLAWDOG/114_WIND_TUNNEL_VS_PRODUCTION.md`](https://github.com/futureWA/clawdog-brain/blob/master/GLOBAL_NOTES/CLAWDOG/114_WIND_TUNNEL_VS_PRODUCTION.md) (content_hash `5d8b39a773fcc8db0db58623cd9f7e6812d330843701db8253e261c0957b2d73`) for the production-vs-harness boundary.

## Setup

1. Make sure you have Python 3 and SWI-Prolog installed on your machine.
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Engine

To run the full thermodynamic lifecycle on the sample trial balances:

```bash
python -m wind_tunnel.wind_tunnel
```

## What Happens?

When you run the Wind Tunnel harness:
1. **Ingest:** It reads the raw Trial Balance CSVs from `data/sample_ledgers/`.
2. **Map:** `wind_tunnel/heuristic_mapper.py` maps the raw string names to SBRM URIs. This is a *stand-in* for the production Fano classifier — do not lift these heuristics into the deterministic engine.
3. **Prolog Engine:** It loads `engine/rules.pl` and evaluates all equations to ensure total mathematical integrity.
4. **Audit:** It runs the Thermodynamic Safeguard (Assets = Liabilities + Equity).
5. **Output:** It drops the fully audited `.json` and `_ixbrl.html` files into the `outputs/` folder.

## Wiring an LLM-driven adjustment-journal producer into ClawDog?

See [`docs/INTEGRATOR_README.md`](docs/INTEGRATOR_README.md) — the Master Configuration Template and 18+2 documented rejection modes for the post-classification audit shim. Empirically validated zero-shot against the production engine.

## Multi-Period Multi-Currency Consolidation (`engine/consolidation.pl`)

The legacy `engine/rules.pl` handles mono-period mono-currency rollups via `node_value/2` and `calculation_arc/3`. The companion module `engine/consolidation.pl` is a strict semantic superset that adds:

- **Period as a first-class dimension** — every fact and FX rate is period-keyed.
- **Currency + FX** — period-scoped `fx_rate/4` lookup with unique-rate enforcement (conflicting rates halt rather than silently first-pick).
- **Weighted edges** — `sbrm_edge/5` preserves the contra-account semantics of `calculation_arc/3` (e.g. `AccumulatedDepreciation` rolls into `PropertyPlantAndEquipment` with weight `-1.0`); legacy `sbrm_edge/4` is treated as weight `1.0`.
- **Provenance** — `consolidation_evidence/6` returns the leaf-by-leaf decomposition behind every consolidated number, suitable for cryptographic ledger anchoring.
- **Determinism by paranoia** — no silent-zero fallback, `must_be(number, ...)` boundary guards, cycle-safe traversal, epsilon-tolerant equity check.

Run the regression suite (18 tests):

```bash
swipl -g run_tests -t halt engine/tests/test_consolidation.pl
```

Full contract documented at `GLOBAL_NOTES/CLAWDOG/107_CONSOLIDATION_LOGIC.md` in the Brain repo (canonical Brain anchor; content_hash `5282338ae508…`).

## Acknowledgments

ClawDog's neurosemantic architecture is deeply indebted to the pioneering work of **Charles Hoffman, CPA**. The core logic engine and taxonomy structure adopted in this project are built directly upon Hoffman's **Seattle Method** and his foundational **Standard Business Reporting Model (SBRM)** taxonomy. We recognize and appreciate his massive contributions to the digitalization, logical structuring, and mathematical formalization of financial reporting.