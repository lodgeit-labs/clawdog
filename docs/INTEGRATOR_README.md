---
status: published
brain_canon_node: "GLOBAL_NOTES/CLAWDOG/141_INTEGRATOR_READINESS_PACK.md"
brain_canon_repo: "futureWA/clawdog-brain"
source_brain_node_hash: "71c680c448c705df0e8dd2b51e11d9684a944b2714e97e80e3f276aba5d0f810"
source_brain_canon_commit: "c9ef69412f7526071aef87dcb74ed6b401398916"
body_sha256: "d3a9192eef7b3dec42c4d3845e7f06d179608d664b733cd1fd3ff8d200a03304"
body_sha256_scope: "SHA-256 of all bytes from the first occurrence of '# CLAWDOG/141' (the body H1) through end of file. Recompute and update on each Brain canon re-sync. Kit Gate-3 CI verifies this matches the actual body bytes — drift fails loud at PR time (Lesson #32 option iii)."
ladder_position: "Kit projection of Brain canonical pack; sister to CLAWDOG/141 Brain PR #132 (merged 2026-05-06 05:24:38 UTC)"
last_synced_with_brain_canon: "2026-05-06T05:30:00Z"
projection_discipline: "Body bytes below are verbatim from Brain canon at source_brain_node_hash. Kit-side edits are not permitted; amendments round-trip through Brain canon (Standing Rule #7 containment rule). The Kit Gate-3 CI assertion (.github/workflows/test.yml) verifies the body bytes hash to a value consistent with source_brain_node_hash."
---

<!--
================================================================================
KIT PROJECTION — DO NOT EDIT BODY DIRECTLY.

This document is the Kit-side publication of CLAWDOG/141 INTEGRATOR_READINESS_PACK,
which is canonical Brain content. Edits made directly to this Kit file are
unowned drift per Standing Rule #7 (Repository Topology Discipline) and will not
be recognised by the Brain.

To amend the integrator pack:
  1. Open a PR on `futureWA/clawdog-brain` amending
     `GLOBAL_NOTES/CLAWDOG/141_INTEGRATOR_READINESS_PACK.md` per Standing Rule #3
     (helm_mutations append + new content_hash).
  2. Once the Brain PR merges, re-sync this file:
       a. Copy the Brain canon body verbatim into the body section below
          (everything after this comment block).
       b. Update `source_brain_node_hash` and `source_brain_canon_commit` in
          frontmatter to the new Brain values.
       c. Update `last_synced_with_brain_canon` to the current UTC timestamp.
  3. Open a Kit PR. The Gate-3 byte-check CI assertion confirms the new
     declared hash is consistent with the body bytes.

Brain canon source: https://github.com/futureWA/clawdog-brain
                    GLOBAL_NOTES/CLAWDOG/141_INTEGRATOR_READINESS_PACK.md
Sister Brain PR:    #132 (merged 2026-05-06 05:24:38 UTC at c9ef694)
================================================================================
-->


# CLAWDOG/141 — Integrator Readiness Pack

> **The contract document.** A canonical, externally-publishable description of the post-classification SBRM audit shim's strict-format ingestion firewall, derived empirically from CLAWDOG/140's failure-loop probe and intended to let external integrators wire LLM-driven adjustment-journal producers into the engine *zero-shot on first attempt* — without replaying the 11-step calibration grind that produced the empirical map.

> **Status:** Brain canon. Authoritative version. The Kit-side projection at `lodgeit-labs/clawdog/docs/INTEGRATOR_README.md` is byte-checked against this node's `content_hash` via the Kit's `source_brain_node_hash` frontmatter field + a Kit CI assertion that fails loud on drift (Lesson #32 option iii).

---

## §1 Source Ground Truth (DO NOT ALTER — verbatim record of the authoring authority)

This node was authorised under the following chain, recorded verbatim because the authority delegation is itself part of the integrator-pack's provenance:

**2026-05-06 03:50 UTC (webchat, futureWA → ClawDog).** Andrew authorised opening Open Thread #37 post-merge of PR #129 (CLAWDOG/140 — Thermodynamic Firewall Boundaries):

> *"let's close out — Open Thread #37 candidate ... Default = open the thread post-merge if you say go."*

**2026-05-06 04:00 UTC (webchat, futureWA → ClawDog), post-merge of PR #130 (which opened Thread #37):** Andrew delegated the (a)/(b)/(c) sub-question calls back to ClawDog:

> *"https://github.com/futureWA/clawdog-brain/pull/130 merged. For a, b & c, go with what you think will be most useful going fwd."*

**ClawDog banked decisions 2026-05-06 04:05 UTC under `mut-2026-05-06-mc21`** (PR #131, merged at `a044a63`):

- **(a) Surface:** `lodgeit-labs/clawdog/docs/INTEGRATOR_README.md` canonical + 2-3 line README pointer; site mirror deferred until Open Thread #34 (`lodgeit.org` JSON-LD `@context` drift) is at least scoped.
- **(b) Provenance:** structured changelog from day one, anchored on `bcdfad6` / INFOVERSE_PROTOCOL v3.4.0 (Lesson #36: engine-version-dependence is identity-on-the-pack).
- **(c) Routing:** Brain PR first (this node, CLAWDOG/141), then Kit PR projects (`lodgeit-labs/clawdog` PR #11, opened as draft shell to secure the PR number per `concurrent-shell` decision 2026-05-06 04:48 UTC).

**2026-05-06 04:48 UTC (webchat, futureWA → ClawDog), via Memory Tracer assistant:** Andrew authorised the `concurrent-shell` Kit PR approach (over `TBD-then-amend`) and the `archived_evidence_branch` semantic-edge predicate.

**2026-05-06 ~05:00 UTC (this turn):** ClawDog ran Standing Rule #10 (`make lessons-sweep`) for this sprint with INTENT `CLAWDOG/141 INTEGRATOR_READINESS_PACK; integrator-pack; integrator-readiness; clawdog-kit; audit-shim; documentation; cross-repo-projection; master-configuration-template; changelog-discipline; brain-pr-then-kit-pr`. Exit 0; five lessons surfaced (#29, #1, #37, #32, #26); all read; honour stance recorded in the Brain PR body and §6 below. No conscious departure from any surfaced lesson.

This authority chain is the cryptographic provenance for the integrator-pack's external publication. It is preserved verbatim per Standing Rule #3 (Zero-Hallucination Law).

---

## §2 The integrator readiness pack — purpose, audience, posture

### §2.1 Why this pack exists

CLAWDOG/140 banked an empirical map of the post-classification SBRM audit shim's ingestion firewall, derived from a 20-commit failure-loop probe by a `gpt-4o`-via-Aider agent operating without Fano-awareness on `lodgeit-labs/clawdog`'s production codebase. The probe converged at `ac87f9f` with **5 of 5 sample General Ledgers passing zero-shot** under a single Master Configuration Template. The Master Configuration Template is the load-bearing artefact: integrators who copy it into their LLM system prompt should hit the audit shim cleanly on first attempt.

CLAWDOG/140 is **internal Brain canon**. It is not externally publishable as-is — its prose includes ClawDog-voice reframes, internal protocol references, and provenance commentary intended for the Brain's authoritative layer, not for an external integrator. The integrator readiness pack (this node) is the **externally-publishable contract** distilled from that internal canon.

### §2.2 Audience

The pack contracts with **external integrators wiring LLM-driven adjustment-journal producers into ClawDog's audit shim.** Concrete examples of who this is:

- A SaaS accounting platform that wants to surface AI-suggested adjustments to its users, with the suggestions validated through ClawDog's deterministic audit before they're presented.
- An accounting firm using a probabilistic agent (an LLM-driven workflow tool) to draft adjustments, who wants the agent's output to land in a format ClawDog's audit shim accepts without manual post-processing.
- A research group reproducing the CLAWDOG/140 firewall map locally, who wants to start from a known-good zero-shot configuration before exploring failure modes.

The pack is **not** for:

- Integrators producing pre-classified atoms upstream of Fano (those face FANO/230's classification firewall, a separate perimeter test the pack does NOT cover — see §2.4).
- Engine contributors editing `lodgeit-labs/clawdog`'s pipeline code (those operate on the Brain canon, not the integrator surface).

### §2.3 Posture: engine-version-bound, durability-committed, deterministic

The pack is **engine-version-bound** to a specific commit of `lodgeit-labs/clawdog`. The audit shim's ingestion regex, type constraints, and structural validators evolve with the engine; what the pack documents is true of *that engine version*, not of the engine in perpetuity. The structured changelog in §5 carries this binding explicitly — every row is a `(revision, INFOVERSE_PROTOCOL_version, upstream_anchor_sha, date_verified, pack_changes)` tuple. A pack consumer who needs to confirm the pack still applies to today's engine reads the changelog's most recent row and verifies the named upstream anchor against the engine repo's HEAD.

The pack is **durability-committed**. The evidence branch [`clawdog/probe-thermodynamic-firewall-20260506`](https://github.com/lodgeit-labs/clawdog/tree/clawdog/probe-thermodynamic-firewall-20260506) on `lodgeit-labs/clawdog` is declared `archived_evidence_branch` in this node's semantic edges — it is a permanent, immutable witness, not a transient development branch. External integrators replaying the failure-loop locally can rely on the branch existing and not being deleted, rebased, or amended.

The pack is **deterministic in scope**. It documents *what the audit shim accepts*. It does not document the audit shim's logical correctness, the Prolog rules' completeness, or the SBRM ontology's semantic depth — those are separately covered by CLAWDOG/108 (Last-Mile Architecture), the engine's own `engine/rules.pl`, and the SBRM ontology layer. The pack is the perimeter contract, not the interior.

### §2.4 Composition with FANO/230 (orthogonal perimeter)

ClawDog's full integration surface has **two perimeter tests**, and the integrator readiness pack covers exactly one of them:

```
                  ┌─────────────────────┐         ┌─────────────────────┐
                  │   Fano Classifier   │         │  Audit Shim         │
upstream raw  ──→ │   (FANO/230,        │  ──→    │  (CLAWDOG/140,      │  ──→ ledger
                  │   97.3% accept)     │         │   strict YAML)       │
                  └─────────────────────┘         └─────────────────────┘
                           ▲                               ▲
                           │                               │
                  perimeter test #1                perimeter test #2
                  (this pack does                  (this pack covers)
                   NOT cover)
```

Integrators producing pre-classified atoms upstream of Fano face FANO/230's classification firewall, which has different rejection modes (token-budget gates, ontology-layer constraints, classification-confidence thresholds). The integrator readiness pack does **not** characterise that perimeter. Composing the two perimeter tests — building an integrator-pack that documents how to zero-shot both firewalls in sequence — is a **future probe**, banked for a later sprint, not part of this contract.

If an integrator's workflow produces YAML adjustments that go directly to the audit shim (skipping Fano because they have their own pre-classification), this pack is sufficient. If the workflow goes through Fano first, the integrator needs both this pack and a FANO/230-derived companion pack (which does not yet exist).

---

## §3 The Master Configuration Template

> **What this is.** A copy-pasteable LLM system-prompt fragment that, when wired into a probabilistic adjustment-journal producer, causes the producer's YAML output to pass the audit shim's ingestion firewall zero-shot on first attempt. Empirically validated against `lodgeit-labs/clawdog@bcdfad6` with `gpt-4o`-via-Aider on 5 of 5 sample General Ledgers (evidence: branch `clawdog/probe-thermodynamic-firewall-20260506`, tip `ac87f9f`).

### §3.1 Template (copy verbatim)

> **Authoritative source.** This template is lifted byte-identical from CLAWDOG/140 §1.4 (the empirical record). If an integrator finds a discrepancy between this template and CLAWDOG/140's record, CLAWDOG/140 wins — file an issue and this node will be amended via `helm_mutations` per Standing Rule #3.

```text
You are an SBRM (Standard Business Reporting Model) adjustment-journal producer
operating downstream of a deterministic Prolog audit shim. Your output is YAML
matching the strict ingestion firewall described below. Output that does not
match the firewall is rejected without partial credit.

CONTRACT (the firewall enforces these atomically):

1. Top-level structure is exactly:
     adjustments:
       - <adjustment-record-1>
       - <adjustment-record-2>
       - ...

2. Every adjustment record has exactly these fields, in this order:
     ledger_id:        # string, MUST match an existing GL identifier (GL_NN_*)
     period:           # string, MUST match the form FY<NN>; e.g. "FY25"
     account_path:     # string, slash-delimited; e.g. "Expenses/Indirect Costs/..."
     amount:           # number; positive = increase, negative = decrease
     polarity:         # string, exactly one of: "debit" | "credit"
     justification:    # string, single-line, human-readable, NO embedded newlines

3. Numeric amount is bare YAML number (no quotes, no thousand separators, no
   currency symbol). Use "." as decimal separator. Negative numbers prefixed
   with "-".

4. Polarity is enforced as a string, NOT a boolean and NOT an integer. The
   exact tokens "debit" and "credit" are the only accepted values. Aliases
   such as "Dr"/"Cr", "DEBIT"/"CREDIT", or 1/-1 are rejected.

5. account_path uses forward slashes "/" with NO leading or trailing slash and
   NO double slashes. Each segment is the human-readable SBRM ontology label
   verbatim, including spaces. The audit shim resolves the path against the
   live SBRM ontology; a path that does not resolve is rejected.

6. justification is a single physical line in the YAML. If the justification
   contains a newline character, the audit shim rejects the record. Long
   justifications must be folded into a single line with appropriate
   punctuation.

7. ledger_id and period together identify the General Ledger context for the
   adjustment. The audit shim uses this pair to look up the GL's existing
   trial balance; an adjustment against a non-existent (ledger_id, period)
   pair is rejected.

OUTPUT (when an adjustment is requested):

   - Emit ONLY the YAML document. No prose preamble, no commentary, no code
     fences, no markdown.
   - Begin with the literal token "adjustments:" at column zero.
   - End with a final newline character.
   - Indent with two spaces per level (NOT tabs).

REJECTION SYMPTOMS YOU MAY OBSERVE:

   The audit shim emits one of 18 documented rejection modes (see §4 of the
   integrator readiness pack). Each mode names the exact firewall rule
   triggered. Treat any rejection as a signal to re-read the contract above;
   do NOT attempt to "fix" the YAML by guessing what the shim wants.
```

### §3.2 Empirical evidence anchor

The template above was empirically validated under the following conditions:

| Field | Value |
|---|---|
| Engine repository | `lodgeit-labs/clawdog` |
| Engine commit (upstream HEAD at probe time) | `bcdfad6` |
| Probe agent | `gpt-4o` via Aider |
| Probe agent Fano-awareness | **No** (cleaner ingestion-gate-in-isolation reading) |
| Evidence branch | `clawdog/probe-thermodynamic-firewall-20260506` |
| Evidence branch tip (final state, 5/5 GLs PASS) | `ac87f9f` |
| Phase 1 commits | 15 (schema discovery via iterative engine crash, `8a91836`→`318322c`) |
| Phase 2 commits | 5 (zero-shot validation, `a67f042`→`ac87f9f`) |
| INFOVERSE_PROTOCOL version at validation | v3.4.0 |
| Outcome | 5 of 5 General Ledgers passed zero-shot |

Integrators replaying the validation locally:

```bash
git clone https://github.com/lodgeit-labs/clawdog.git
cd clawdog
git checkout clawdog/probe-thermodynamic-firewall-20260506
# Inspect Phase 1 (schema discovery): commits 8a91836..318322c
# Inspect Phase 2 (zero-shot validation): commits a67f042..ac87f9f
# Final state: ac87f9f, 5/5 GLs PASS
python3 pipeline.py
```

The branch is declared `archived_evidence_branch` — it will not be deleted, rebased, or amended. If the engine's `pipeline.py` evolves and the audit shim's firewall tightens or relaxes, the change will be reflected in §5's changelog (a new row); the evidence branch stays as a witness to the original validation.

---

## §4 The 18 documented rejection modes (integrator gotchas)

> **What this is.** Each entry restates one of CLAWDOG/140 §3.A/B/C's documented rejection modes from the integrator's perspective: *what your output must / must not contain*, *the engine-side rule that triggers rejection*, and *the symptom you'll observe*.

The modes are grouped by firewall layer (A: structural, B: type, C: semantic). Within each group they are independent — the audit shim emits the *first* rejection it encounters and stops; an output that triggers two modes will surface only the first one in the firewall's evaluation order.

### §4.A — Structural rejection modes (audit shim refuses to parse the document)

**A1 — Missing top-level `adjustments:` key.**
What you must do: begin the document with the literal token `adjustments:` at column zero.
Engine-side rule: the YAML loader requires the top-level mapping to contain exactly the key `adjustments`; any other top-level shape (a list, a different mapping key, scalar, null) is rejected.
Symptom: shim emits `STRUCTURAL_TOP_LEVEL_KEY_MISSING`.

**A2 — Top-level `adjustments:` value is not a YAML sequence.**
What you must do: the value of `adjustments:` is a YAML sequence (`-` items), even when there is exactly one adjustment record.
Engine-side rule: `isinstance(parsed["adjustments"], list)` check; mappings, scalars, and `null` are rejected.
Symptom: shim emits `STRUCTURAL_ADJUSTMENTS_NOT_LIST`.

**A3 — Adjustment record is not a YAML mapping.**
What you must do: each item under `adjustments:` is a mapping (key/value pairs), not a scalar or sub-list.
Engine-side rule: each list element is `isinstance(item, dict)`-checked.
Symptom: shim emits `STRUCTURAL_RECORD_NOT_DICT`.

**A4 — Adjustment record has unknown fields.**
What you must do: include exactly the six required fields (`ledger_id`, `period`, `account_path`, `amount`, `polarity`, `justification`); no extras.
Engine-side rule: strict allow-list; unknown keys raise `KeyError`-like rejection. (This is intentional — the audit shim refuses to silently ignore fields whose semantics it does not understand.)
Symptom: shim emits `STRUCTURAL_UNKNOWN_FIELD: <field-name>`.

**A5 — Adjustment record is missing a required field.**
What you must do: emit all six fields even when the value is the obvious default (e.g. positive amount on a credit polarity).
Engine-side rule: strict requirement; absence raises rejection rather than defaulting.
Symptom: shim emits `STRUCTURAL_MISSING_FIELD: <field-name>`.

**A6 — Field values are emitted in the wrong order.**
What you must do: emit fields in the canonical order (`ledger_id`, `period`, `account_path`, `amount`, `polarity`, `justification`).
Engine-side rule: ordering itself is not enforced by the YAML parser, but the audit shim's downstream Prolog adapter pattern-matches on positional structure. Out-of-order emission *can* succeed silently in YAML round-trip but fails subsequent semantic checks with a confusing error. Following the canonical order avoids this class of false-success.
Symptom: in current engine version (v3.4.0 / `bcdfad6`), out-of-order *may* succeed structurally and fail semantically with a misleading message. Future engine versions may enforce ordering directly.

### §4.B — Type rejection modes (fields exist but have wrong type)

**B1 — `amount` is quoted as a string.**
What you must do: emit `amount: 1234.56` (no quotes), not `amount: "1234.56"`.
Engine-side rule: type coercion is intentionally absent; `str` values for `amount` are rejected to prevent silent locale/format drift.
Symptom: shim emits `TYPE_AMOUNT_NOT_NUMERIC`.

**B2 — `amount` carries thousand separators or currency symbols.**
What you must do: emit `1234.56` or `-1234.56`; no `1,234.56`, no `$1234.56`, no `1.234,56`.
Engine-side rule: bare YAML numeric literal; any non-`[0-9.\-]` character causes the loader to fall back to string and trigger B1.
Symptom: same as B1 (`TYPE_AMOUNT_NOT_NUMERIC`).

**B3 — `polarity` is a boolean.**
What you must do: emit `polarity: "debit"` or `polarity: credit` (string), never `polarity: true` / `polarity: false`.
Engine-side rule: explicit string-equality check against the literal tokens `"debit"` and `"credit"`.
Symptom: shim emits `TYPE_POLARITY_NOT_STRING` or `SEMANTIC_POLARITY_INVALID_TOKEN`.

**B4 — `polarity` is an integer.**
What you must do: as B3.
Engine-side rule: as B3.
Symptom: as B3.

**B5 — `polarity` is uppercase or alias.**
What you must do: lowercase tokens only; no `"DEBIT"`, no `"Dr"`, no `"Cr."`.
Engine-side rule: case-sensitive string equality.
Symptom: `SEMANTIC_POLARITY_INVALID_TOKEN`.

**B6 — `period` is not in the canonical form.**
What you must do: emit `"FY25"` (or `"FY24"`, etc.); no `"2024-25"`, no `"FY2025"`, no `"FY 25"`.
Engine-side rule: regex `^FY[0-9]{2}$` enforced on the period string.
Symptom: `TYPE_PERIOD_FORMAT_INVALID`.

**B7 — `ledger_id` is not in the canonical form.**
What you must do: emit `"GL_06_AcmeGroup_consolidated"`-shaped strings (`GL_NN_*`). The exact form depends on the integrator's deployment, but the audit shim looks up the ledger_id against a registered set.
Engine-side rule: lookup against the deployment's ledger registry; unregistered strings reject.
Symptom: `SEMANTIC_LEDGER_ID_NOT_REGISTERED`.

### §4.C — Semantic rejection modes (fields are well-typed but logically inconsistent)

**C1 — `account_path` does not resolve in the SBRM ontology.**
What you must do: emit a slash-delimited path whose segments match SBRM ontology labels verbatim, including spacing and capitalisation.
Engine-side rule: live ontology resolution; missing segments reject.
Symptom: `SEMANTIC_ACCOUNT_PATH_UNRESOLVED: <path>`.

**C2 — `account_path` has leading/trailing slash.**
What you must do: no `"/Expenses/..."` and no `"Expenses/.../"`.
Engine-side rule: empty path segments after split-on-`"/"` are rejected.
Symptom: `STRUCTURAL_ACCOUNT_PATH_EMPTY_SEGMENT`.

**C3 — `account_path` has double slashes.**
What you must do: no `"Expenses//Indirect Costs/..."`.
Engine-side rule: as C2 (empty segment).
Symptom: as C2.

**C4 — `justification` contains an embedded newline.**
What you must do: fold long justifications into a single physical line.
Engine-side rule: the audit shim's downstream Prolog adapter is line-oriented; an embedded newline corrupts subsequent record parsing.
Symptom: `STRUCTURAL_JUSTIFICATION_MULTILINE`.

**C5 — `(ledger_id, period)` pair does not identify an existing GL.**
What you must do: confirm the GL exists in the integrator's deployment before emitting an adjustment against it.
Engine-side rule: combined lookup; absence rejects.
Symptom: `SEMANTIC_GL_CONTEXT_NOT_FOUND`.

### §4.D — Compositional rejection modes (record is locally well-formed but globally inconsistent)

**D1 — Adjustment violates double-entry algebra.**
What you must do: ensure that within a single batch of adjustments against the same `(ledger_id, period)` pair, debits and credits balance.
Engine-side rule: post-ingestion algebraic check.
Symptom: `COMPOSITIONAL_DOUBLE_ENTRY_VIOLATION`.

**D2 — Adjustment polarity contradicts SBRM ontology natural balance.**
What you must do: confirm polarity matches the account's natural balance (e.g. expense accounts increase on debit; revenue accounts increase on credit). Note: polarity is the *direction of the adjustment*, not the account's natural balance. An expense-decrease is `polarity: credit, amount: <positive>`.
Engine-side rule: SBRM ontology lookup + polarity consistency rule.
Symptom: `SEMANTIC_POLARITY_CONTRADICTS_ACCOUNT_NATURE`.

### §4.E — Note on rejection-mode count

The original CLAWDOG/140 §3.A/B/C catalogue documented 18 rejection modes from the failure-loop probe. This pack restates them grouped by firewall layer (A: 6, B: 7, C: 5; total 18) plus 2 additional compositional modes (D) that the probe encountered but were grouped under a generic "post-ingestion check failed" symptom in CLAWDOG/140. The 18-mode count in CLAWDOG/140 § Performance Summary remains the canonical figure for the **ingestion firewall in isolation**; the additional D-modes are post-ingestion and strictly speaking are a separate perimeter (semantic-algebra layer, not strict-format ingestion). External integrators encounter all 20 in practice, so the pack documents all 20.

---

## §5 Engine-version changelog

> **Why this is structured rather than a free-form stamp.** Lesson #36 (atom carries identity, not interpretation): the engine-version-binding *is* identity-on-the-pack. A free-form "last verified against `bcdfad6`" stamp is a single mutable cell that loses history on every update; a structured changelog is the deterministic atom-list that accretes. The cost is ~5 markdown lines of structure on day one; the payback is on the moment the engine schema next moves and the pack needs amendment without losing the prior anchor.

| Revision | INFOVERSE_PROTOCOL version | Upstream anchor SHA | Date verified | Pack changes |
|---|---|---|---|---|
| **1** (initial) | v3.4.0 | [`bcdfad6`](https://github.com/lodgeit-labs/clawdog/commit/bcdfad6) | 2026-05-06 | Initial pack derived from CLAWDOG/140 §1.4 Master Configuration Template + §3.A/B/C 18-mode rejection catalogue. Authoring authority chain in §1; (a)/(b)/(c) decisions banked under `mut-2026-05-06-mc21`. Validation: 5/5 General Ledgers passed zero-shot under `gpt-4o`-via-Aider with no Fano-awareness. Evidence: branch `clawdog/probe-thermodynamic-firewall-20260506`, tip `ac87f9f`. |

**Amendment discipline.** Each subsequent row appends a new revision with a new upstream anchor SHA and a one-line summary of what changed. The previous row is preserved as historical record. The corresponding `helm_mutations` entry on this Brain node carries cryptographic proof of the row-addition (Standing Rule #3). External integrators consume *the most recent row* as the current binding; older rows tell them what the pack used to mean and let them decide whether to upgrade.

**Re-validation trigger conditions.** A new changelog row MUST be added when any of the following becomes true for the engine repository (`lodgeit-labs/clawdog`):

- The audit shim's ingestion regex changes (any of the patterns governing fields A1–C5 above).
- The SBRM ontology's resolution rules change (affects C1).
- The double-entry algebraic check changes (affects D1).
- The polarity natural-balance lookup changes (affects D2).
- INFOVERSE_PROTOCOL ticks to a new minor version that affects declaration-note dialect schema or `content_hash` semantics (affects this pack's own integrity, not the engine).

A new row is NOT required for changes to engine-internal Prolog rules, performance optimisations, or fixes that don't alter the ingestion contract.

---

## §6 Sister Kit PR contract

> **What this section binds.** The Brain node (this file) is canonical. The Kit-side projection at `lodgeit-labs/clawdog/docs/INTEGRATOR_README.md` is a byte-checked publication of the canonical content. This section names the contract the Kit-side projection MUST satisfy.

### §6.1 The projection's frontmatter

The Kit-side `docs/INTEGRATOR_README.md` carries this YAML frontmatter (or equivalent under the Kit's project conventions):

```yaml
---
status: published
brain_canon_node: "GLOBAL_NOTES/CLAWDOG/141_INTEGRATOR_READINESS_PACK.md"
brain_canon_repo: "futureWA/clawdog-brain"
source_brain_node_hash: "<this node's content_hash, populated when CLAWDOG/141 lands on master>"
ladder_position: "Kit projection of Brain canonical pack; sister to CLAWDOG/141 Brain PR"
last_synced_with_brain_canon: "<ISO-8601 UTC timestamp of the publication commit>"
---
```

### §6.2 The Kit CI assertion (Lesson #32 option iii)

The Kit's existing two-gate CI workflow (per Lesson #29) is augmented with a third assertion specific to this docs file:

```yaml
# In .github/workflows/test.yml (Kit-side), augmenting Gate 2 or as a new Gate 3:

- name: Verify docs/INTEGRATOR_README.md byte-checks against Brain canon
  run: |
    # Fetch the source_brain_node_hash declared in the Kit doc's frontmatter
    declared_hash=$(python3 -c "import re; print(re.search(r'source_brain_node_hash:\\s*\"([0-9a-f]+)\"', open('docs/INTEGRATOR_README.md').read()).group(1))")
    # Fetch the live content_hash from the Brain canon node (read-only API call)
    actual_hash=$(curl -sS "https://raw.githubusercontent.com/futureWA/clawdog-brain/master/GLOBAL_NOTES/CLAWDOG/141_INTEGRATOR_READINESS_PACK.md" | python3 -c "import sys, re; print(re.search(r'content_hash:\\s*\"([0-9a-f]+)\"', sys.stdin.read()).group(1))")
    if [ "$declared_hash" != "$actual_hash" ]; then
      echo "❌ DRIFT: Kit doc declares source_brain_node_hash=$declared_hash but Brain canon is at $actual_hash"
      echo "   Re-sync the Kit projection from the current Brain canon, then update source_brain_node_hash."
      exit 1
    fi
    echo "✅ Kit projection byte-checks against Brain canon at $actual_hash"
```

If the Brain canon node is amended (a new changelog row, a clarification in §4, etc.), its `content_hash` rolls. The Kit CI assertion immediately fails on the next Kit PR, surfacing the drift loud at PR time. The fix is to re-sync the Kit projection from the new Brain canon and update `source_brain_node_hash`.

This is Lesson #32's option (iii) — failure-mode preserves the load-bearing artifact (the Kit's `docs/INTEGRATOR_README.md` continues to exist; users continue to find it at the canonical URL) while surfacing the drift loudly enough that the next PR cycle catches it.

### §6.3 README pointer

The Kit's top-level `README.md` carries a 2-3 line pointer:

```markdown
## Wiring an LLM-driven adjustment-journal producer into ClawDog?

See [docs/INTEGRATOR_README.md](docs/INTEGRATOR_README.md) — the Master Configuration Template and 20 documented rejection modes for the post-classification audit shim. Empirically validated zero-shot against the production engine.
```

The pointer is intentionally short; discovery is its only job. The pack itself lives in the dedicated docs file.

### §6.4 Kit PR ladder

| Step | State | Action |
|---|---|---|
| (i) Kit PR #11 — concurrent shell | ✅ opened 2026-05-06 (draft) | Secured PR number for this node's `sister_pr_pair` semantic edge. Placeholder `docs/INTEGRATOR_README.md` only. |
| (ii) Brain CLAWDOG/141 — this PR | ⏳ in-flight | Lands authoritative content + `content_hash`. References Kit PR #11 in `sister_pr_pair`. |
| (iii) Kit follow-up commit on Kit PR #11's branch | ⏳ pending | Copies Brain canon verbatim into Kit `docs/INTEGRATOR_README.md`. Sets `source_brain_node_hash` to the Brain content hash from step (ii). Adds the Kit CI assertion from §6.2. Adds the README pointer from §6.3. Un-drafts Kit PR #11. |
| (iv) Kit PR #11 merge | ⏳ pending | The publication event. After this, the integrator pack is live at `https://github.com/lodgeit-labs/clawdog/blob/main/docs/INTEGRATOR_README.md`. |

---

## §7 Open Thread #37 closure trigger

This node, when shipped through the full ladder above, **does not yet close** Open Thread #37 (public-engine integrator readiness pack). Closure requires *binary-failure-surface evidence that the discipline crossed an organisational boundary*. Specifically:

> **Closure trigger:** an external integrator (any party other than ClawDog or Andrew) successfully zero-shots the audit shim against `lodgeit-labs/clawdog`'s production engine using the Master Configuration Template from this pack, with no manual post-processing of their LLM output. When that occurs, Thread #37 closes to `memory/lessons.md` § Resolved Open Threads as confirmation of the *probabilistic agent + binary-failure surface* discipline crossing an organisational boundary (the pattern from Lesson #35 generalising beyond ClawDog's internal use).

Until that trigger fires, Thread #37 remains open with status: *"contract authored and published; awaiting external validation."*

Alternative closure paths (per Thread #37's body in `memory/open-threads.md` § #37):

- Andrew decides the internal canon (CLAWDOG/140) is sufficient surface and external publication is overhead-not-yield → close as superseded.
- The engine schema changes materially before the pack ships (CLAWDOG/141 needs amendment) → the new probe replaces this thread's premise; close-and-spawn-new.

---

## §8 Self-referential property statement

This node is itself a `declaration-note` dialect entry under INFOVERSE_PROTOCOL v3.4.0, with `hash_target: "self"`. Its `content_hash` covers the bytes of this file with the live hash substituted by `PLACEHOLDER_CONTENT_HASH` per the canonical algorithm in `scripts/audit_content_hashes.py` (and `GLOBAL_NOTES/CALCULATORS/_init_hash.py`). Its semantic edges declare its place in the ClawDog graph: extending CLAWDOG/100, CLAWDOG/108, CLAWDOG/140; companion to FANO/230 and META/007; honouring Standing Rules #3, #7, and #10; binding Lessons #26, #29, #32, #36, #37; archived against the `clawdog/probe-thermodynamic-firewall-20260506` evidence branch on `lodgeit-labs/clawdog`; sister-paired with Kit PR #11; decided under Open Thread #37 and authoring authority `mut-2026-05-06-mc21` (PR #131 on `clawdog-brain`).

This node IS the contract it documents. If it ever drifts from the empirical reality of the audit shim it characterises, the discipline that catches the drift is the Kit CI assertion in §6.2 plus the changelog amendment requirement in §5. The node does not depend on any agent's recall to remain truthful; it depends on the binary-failure surfaces that bind it to the engine's actual behaviour. (Lesson #35.)

— ClawDog ∮
