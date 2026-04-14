# ClawDog Pipeline

This repository contains the standalone, stripped-down ClawDog pipeline. It demonstrates the neurosemantic approach to financial reporting: taking raw General Ledger CSV files, mapping them to the SBRM taxonomy, running them through a strict Prolog physics engine (to ensure double-entry accounting math holds true), and rendering the final output to JSON-LD and iXBRL format.

## Setup

1. Make sure you have Python 3 and SWI-Prolog installed on your machine.
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Engine

To run the full thermodynamic lifecycle on the sample trial balances:

```bash
python pipeline.py
```

## What Happens?

When you run `pipeline.py`:
1. **Ingest:** It reads the raw Trial Balance CSVs from `data/sample_ledgers/`.
2. **Map:** `engine/heuristic_mapper.py` maps the raw string names to SBRM URIs.
3. **Prolog Engine:** It loads `engine/rules.pl` and evaluates all equations to ensure total mathematical integrity.
4. **Audit:** It runs the Thermodynamic Safeguard (Assets = Liabilities + Equity).
5. **Output:** It drops the fully audited `.json` and `_ixbrl.html` files into the `outputs/` folder.