---
status: published
brain_canon_node: "GLOBAL_NOTES/CLAWDOG/141_INTEGRATOR_READINESS_PACK.md"
brain_canon_repo: "futureWA/clawdog-brain"
source_brain_node_hash: "ece491ef543cb1c5713e75391abb43972e95f034bf9538f325542aca427a6a50"
source_brain_canon_commit: "19467aabfccfc62e5d2b5c2148d6b0ee1d0a9f06"
body_sha256: "755865200d8177b159b71b2c2af71a6e14a5679f49ae39ea8af5466351546447"
body_sha256_scope: "SHA-256 of all bytes from the first occurrence of '# CLAWDOG/141' (the body H1) through end of file. Recompute and update on each Brain canon re-sync. Kit Gate-3 CI verifies this matches the actual body bytes — drift fails loud at PR time (Lesson #32 option iii)."
ladder_position: "Kit projection of Brain canonical pack (mc23 re-sync); sister to CLAWDOG/141 Brain PR #133 (merged 2026-05-06 06:35:19 UTC at 19467aa). Replaces the mc22 projection from Kit PR #11 (merged 0e3ec10 05:36:46 UTC); the mc22 publication carried fabricated §3.1 / §4 / §6.2 content that the production engine would have rejected on every field — see helm_mutations entry in the Brain canon for the full forensic record."
last_synced_with_brain_canon: "2026-05-06T06:45:00Z"
projection_discipline: "Body bytes below are verbatim from Brain canon at source_brain_node_hash. Kit-side edits are not permitted; amendments round-trip through Brain canon (Standing Rule #7 containment rule). The Kit Gate-3 CI assertion (.github/workflows/test.yml) verifies the body bytes hash to a value consistent with body_sha256."
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
       c. Recompute body_sha256 over the body bytes (everything from '# CLAWDOG/141'
          to EOF) and update frontmatter.
       d. Update `last_synced_with_brain_canon` to the current UTC timestamp.
  3. Open a Kit PR. The Gate-3 byte-check CI assertion confirms the new
     declared body_sha256 matches the body bytes.

Brain canon source: https://github.com/futureWA/clawdog-brain
                    GLOBAL_NOTES/CLAWDOG/141_INTEGRATOR_READINESS_PACK.md
mc22 (initial publication):    Brain PR #132 / Kit PR #11.
mc23 (factual correction):     Brain PR #133 (merged at 19467aa) / THIS Kit PR.
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

### §3.1 Template (lifted byte-identical from CLAWDOG/140 §1.4)

> **Authoritative source.** The YAML template below is **byte-identical** to CLAWDOG/140 §1.4 (the empirical record). The mc23 amendment (this revision) byte-diffed the lifted text against CLAWDOG/140's source before content-hash-locking. If a future integrator finds a discrepancy between this template and CLAWDOG/140's record, CLAWDOG/140 wins — file an issue and this node will be amended via `helm_mutations` per Standing Rule #3.

```yaml
adjustment:
  adj_id: adj_<generate_unique_hex>
  entity: <Target_Entity_Name_Snake_Case_Only>
  period: <Target_Period>
  description: <Overall event description>
  postings:
    - concept: mini_<ConceptName>
      amount: <Float>
      direction: <debit or credit>
      description: <Specific line item narration>
  approved_status: pending
  source_provenance:
    service: clawdog/orchestrator
    service_version: "1.0.0"
    trace_id: <generate_32_char_hex>
    authored_at: "2026-05-06T10:00:34Z"
    human_approver: "System Admin"
    approved_at: "2026-05-06T10:00:34Z"
```

### §3.1.1 LLM system-prompt framing for the template

The template above is the *contract*. Integrators wiring an LLM-driven adjustment-journal producer typically embed the contract inside an LLM system prompt with framing prose. A minimal sufficient framing (empirically validated by the CLAWDOG/140 probe with `gpt-4o`-via-Aider, 5/5 GLs PASS):

```text
You are an SBRM (Standard Business Reporting Model) adjustment-journal producer
operating downstream of a deterministic Prolog audit shim. Your output is YAML
matching the exact template below. Output that does not match is rejected
without partial credit.

TEMPLATE (substitute the angle-bracketed placeholders only; preserve every
other token, including whitespace and key ordering):

<insert the §3.1 template here verbatim>

FIELD CONSTRAINTS:

1. Top-level structure is `adjustment:` (singular dict), NOT `adjustments:`
   (plural list). One adjustment per YAML document.

2. `adj_id` is the literal prefix `adj_` followed by a generated unique hex
   string. The recommended generator is a 32-character hex of cryptographically
   random bytes (CLAWDOG/140 §3.B requires `trace_id` to be 32 hex chars; an
   `adj_id` of similar shape avoids ambiguity at the integration boundary).

3. `entity` is snake_case ONLY. Spaces, hyphens, and CamelCase fail the Prolog
   atom regex `^[A-Za-z_][A-Za-z0-9_]*$` and crash the audit shim.
   `Bluey Builders Pty Ltd` -> `Bluey_Builders_Pty_Ltd`. (CLAWDOG/140 §3.A.4)

4. `period` is your deployment's canonical period token (e.g. `FY25`, `Q1_2025`,
   `2024-25`). The exact form is set by the engine deployment; consult the
   deployment's period registry. The audit shim treats `period` as an opaque
   string; mismatches surface as `(ledger_id, period) pair not found` errors
   downstream.

5. `postings:` is a YAML list of posting records. Each posting has exactly
   four keys: `concept`, `amount`, `direction`, `description`. Every single
   posting MUST carry a `description` (line-level narration); the Prolog
   engine treats postings without `description` as phantom entries and
   crashes. (CLAWDOG/140 §3.A.3)

6. `concept` values match the SBRM mini-taxonomy: `mini_<ConceptName>`,
   CamelCase ConceptName. Examples: `mini_PropertyPlantAndEquipmentGross`,
   `mini_RetainedEarnings`, `mini_CashAndCashEquivalents`. Audit-tier and
   custom concepts use other prefixes (e.g. `audit_AccumulatedTaxDepreciation`).
   The audit shim resolves `concept` against the live SBRM ontology; an
   unresolved concept is rejected.

7. `amount` is a bare YAML float (no quotes, no thousand separators, no
   currency symbol). Use `.` as decimal separator. Use positive numbers only;
   debits and credits are distinguished by `direction`, not by sign.

8. `direction` is exactly one of the lowercase string tokens `debit` or
   `credit`. Aliases (`Dr`/`Cr`, `DEBIT`/`CREDIT`, booleans, integers) are
   rejected.

9. `description` (both the root-level adjustment-wide one AND the per-posting
   one) is a single physical line of YAML. Multi-line descriptions corrupt
   subsequent record parsing; fold long descriptions into one line.

10. `approved_status` sits at the root `adjustment:` level (NOT nested inside
    `source_provenance:`). Permitted tokens: `pending`, `proven`. The
    placement trap is documented in CLAWDOG/140 §3.C — indentation collapse
    onto `source_provenance` is the failure mode the engine surfaces with a
    misleading error message.

11. `source_provenance:` is mandatory. All sub-fields below are mandatory.
    No `null` values are permitted on `human_approver`, `authored_at`,
    `approved_at` even when the adjustment is `pending` (use `"System Admin"`
    and an explicit ISO-8601 UTC timestamp). (CLAWDOG/140 §3.C — the Null Trap)

12. `service` matches the regex `\w+/\w+` (word-chars, forward slash,
    word-chars). `clawdog/orchestrator` passes; `clawdog-orchestrator` fails;
    `myorg/my_producer` passes; `my-org/my-producer` fails. (CLAWDOG/140 §3.B —
    Service Regex)

13. `service_version` is a quoted semver string (e.g. `"1.0.0"`) OR
    `service_commit` is a 40-char git SHA. At least one is mandatory; the
    audit shim rejects "anonymous or untraceable logic." (CLAWDOG/140 §3.B —
    Version Control)

14. `trace_id` is a 32-character hex string generated for every action.
    (CLAWDOG/140 §3.B — Trace ID)

15. `authored_at` and `approved_at` are explicit ISO-8601 UTC strings
    (e.g. `"2026-05-06T10:00:34Z"`). Loose date formats (e.g. `2026-05-06`)
    or `null` are rejected. (CLAWDOG/140 §3.C — Strict ISO-8601 UTC)

DOUBLE-ENTRY ALGEBRA:

Within a single adjustment, the sum of `debit` posting amounts MUST equal
the sum of `credit` posting amounts. The audit shim enforces this as part
of the 6-Point Thermodynamic Safeguard; an unbalanced adjustment is rejected.

OUTPUT FORMAT:

- Emit ONLY the YAML document. No prose preamble, no commentary, no code
  fences, no markdown.
- Begin with the literal token `adjustment:` at column zero.
- End with a final newline character.
- Indent with two spaces per level (NOT tabs).

REJECTION HANDLING:

The audit shim emits one of 10 documented schema-rejection categories
(§4) plus the double-entry balance check (§4.D). Each category names
the firewall rule triggered. Treat any rejection as a signal to re-read this
contract; do NOT "fix" the YAML by guessing what the shim wants. Re-read,
then re-emit.
```

The contract above is empirical: it codifies the failure modes the
`gpt-4o`-via-Aider probe encountered before converging on 5/5 PASS at evidence
branch tip `ac87f9f`. An LLM agent given this contract and a concrete
business-context instruction (e.g. *"the company received an unrecorded
invoice for office supplies of $487.50; produce the adjustment"*) should
produce engine-acceptable YAML zero-shot.

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

## §4 The documented rejection modes (integrator gotchas)

> **What this is.** CLAWDOG/140 §3 documents the schema vulnerabilities the `gpt-4o`-via-Aider failure-loop probe encountered before converging on 5/5 PASS. Three category groups (A, B, C) totalling **10 distinct vulnerabilities**, plus the double-entry algebra check (§4.D below). Each entry below restates one CLAWDOG/140 vulnerability from the integrator's perspective: *what your output must / must not contain*, *the engine-side rule that triggers rejection*, and *the symptom you'll observe*. Source: CLAWDOG/140 §3.A/B/C verbatim, mapped onto integrator-facing language.

The categories are independent — the audit shim emits the *first* rejection it encounters and stops; an output that triggers two simultaneously will surface only the first in the engine's evaluation order. Beyond these 10 schema-level checks, the engine also enforces double-entry balance (§4.D), which fires after schema checks pass.

### §4.A — Structural integrity (4 vulnerabilities)

**A.1 — Root key missing or wrong.**
What you must do: top-level structure is `adjustment:` (singular dict). LLMs default to flat YAML lists or to plural `adjustments:`; both are rejected.
Engine-side rule: `engine/yaml_adjustments.py::parse_adjustment` requires the top-level mapping to contain exactly the key `adjustment` mapping to a dict.
Symptom: `KeyError: 'adjustment'` or `TypeError: 'adjustment' must map to a mapping`.

**A.2 — Hallucinated key names.**
What you must do: use the exact CLAWDOG/140 §1.4 schema keys (`adj_id`, `entity`, `period`, `description`, `postings`, `approved_status`, `source_provenance`). The model may attempt synonyms (e.g. `event:` instead of `description:`); these are rejected.
Engine-side rule: schema keys are immutable; the loader's allow-list rejects unknown keys.
Symptom: `UnknownFieldError: <field-name>` or silent omission of the substituted key from the parsed adjustment, surfacing later as a missing-required-field error.

**A.3 — Line-level narration missing.**
What you must do: every single posting in the `postings:` array carries its own `description:` key. The Prolog engine treats postings without line-level narration as phantom entries.
Engine-side rule: per-posting `description` field is required; absence triggers a fatal audit shim crash.
Symptom: Prolog engine crash with a phantom-entry diagnostic.

**A.4 — Atom-shape identifier violation.**
What you must do: `entity` is snake_case ONLY. Spaces, hyphens, and CamelCase fail the Prolog atom regex `^[A-Za-z_][A-Za-z0-9_]*$`. `Bluey Builders Pty Ltd` -> `Bluey_Builders_Pty_Ltd`.
Engine-side rule: the engine's Prolog adapter constructs an atom from `entity` and crashes on any character outside `[A-Za-z0-9_]`.
Symptom: SWI-Prolog crash with `Type error: 'atom' expected, found ...`.

### §4.B — Provenance layer (cryptographic & version control, 3 vulnerabilities)

**B.1 — `trace_id` missing or wrong shape.**
What you must do: `source_provenance.trace_id` is mandatory. Generate a 32-character hex string for every action.
Engine-side rule: `trace_id` field is required; the audit shim rejects anonymous logic.
Symptom: `MissingProvenance: trace_id is required`.

**B.2 — Version control declaration missing.**
What you must do: declare release state. Either `service_version` (e.g. `"1.0.0"` quoted semver) or `service_commit` (40-char git SHA) is strictly required. Both may be present.
Engine-side rule: at least one of the two fields must be non-null; the audit shim rejects untraceable logic.
Symptom: `MissingProvenance: service_version or service_commit required`.

**B.3 — Service regex violation.**
What you must do: `service` matches the regex `\w+/\w+`. `clawdog/orchestrator` passes; `clawdog-orchestrator` fails (hyphen instead of slash).
Engine-side rule: the engine validates `service` with a forward-slash separator regex; hyphens cause fatal audit failures.
Symptom: `ServiceFormatError: service must match \w+/\w+, got <value>`. (CLAWDOG/140 §3.B.3 — the precise vulnerability bound by Lesson #36 on the original probe: identity-on-the-atom, not interpretation-on-the-atom.)

### §4.C — Temporal & approval exactness (the Null Trap, 3 vulnerabilities)

**C.1 — Null values on mandatory provenance strings.**
What you must do: even when an adjustment is `pending`, `human_approver`, `authored_at`, and `approved_at` cannot be `null`. Use a string (e.g. `"System Admin"`) and an explicit ISO-8601 UTC timestamp.
Engine-side rule: the schema's type-checker strictly enforces string types to prevent downstream Prolog typing errors.
Symptom: `TypeError: human_approver must be string, got NoneType`.

**C.2 — Loose date format.**
What you must do: `authored_at` and `approved_at` are explicit ISO-8601 UTC strings (e.g. `"2026-05-06T10:00:34Z"`). Do not use loose formats (`2026-05-06`, `"2026-05-06 10:00:34"`, `null`).
Engine-side rule: explicit ISO-8601 UTC parsing; loose formats reject.
Symptom: `DateFormatError: expected ISO-8601 UTC, got <value>`.

**C.3 — Indentation trap (`approved_status` placement).**
What you must do: `approved_status` sits at the root `adjustment:` level (NOT nested inside `source_provenance`). `human_approver` and `approved_at`, conversely, MUST nest inside `source_provenance`. The AI repeatedly collapsed `approved_status` into `source_provenance`; that placement is rejected.
Engine-side rule: parse-tree position check; `approved_status` at the wrong tree depth fails an explicit field-location assertion.
Symptom: `SchemaPlacementError: approved_status must be at root, found nested under source_provenance` (or, in some engine versions, a misleading downstream error from the Prolog adapter that doesn't immediately reveal the placement was wrong).

### §4.D — Double-entry algebra (post-schema check)

After all 10 schema vulnerabilities above are satisfied, the engine runs the 6-Point Thermodynamic Safeguard's double-entry balance check:

**D.1 — Sum of debits MUST equal sum of credits within a single adjustment.**
What you must do: across all entries in `postings:`, the total `amount` where `direction: debit` equals the total `amount` where `direction: credit`. Mathematical equality, not approximate.
Engine-side rule: arithmetic check on the parsed adjustment; tolerance is zero (no floating-point slop allowed; the engine treats unbalanced adjustments as a fatal integrity violation).
Symptom: `BalanceCheckFailure: debits=<X> credits=<Y> delta=<X-Y>`.

### §4.E — Note on rejection-mode count

CLAWDOG/140's prose (§2) refers to **"18 documented schema rejections"** — that figure counts the *crashes* in the failure loop, not the catalogue of distinct vulnerability *categories*. Some vulnerabilities trigger multiple crashes during convergence (e.g. the indentation trap C.3 fired several times before the agent learned the placement). The catalogue of distinct schema vulnerabilities at CLAWDOG/140 §3.A/B/C totals **10** (4 + 3 + 3), and that 10 is what §4.A/B/C above documents. The double-entry balance check (§4.D) is a post-schema algebraic check, not a schema vulnerability — we list it because integrators encounter it as an additional rejection class.

*Historical note on this section:* the mc22 original revision of this pack incorrectly stated "18 modes (A:6, B:7, C:5) plus 2 D-modes for 20." That counting was inflated to match CLAWDOG/140's prose figure, and the 2 D-modes were invented. The mc23 amendment (this revision) restates the catalogue from CLAWDOG/140 §3.A/B/C verbatim, with the real counts. The reasoning behind the original error is documented in the helm_mutations entry above for forensic transparency.

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

The Kit's existing two-gate CI workflow (per Lesson #29) is augmented with a third assertion specific to this docs file. **The actual shipped assertion** (on `lodgeit-labs/clawdog` PR #11, merged at `0e3ec10`, 2026-05-06 05:36:46 UTC) is a **body-bytes SHA-256 byte-check** that does NOT require live access to the Brain repo:

```yaml
# In .github/workflows/test.yml (Kit-side), as Gate 3:

- name: Verify docs/INTEGRATOR_README.md body bytes match declared body_sha256
  run: |
    set -e
    python3 - <<'PY'
    import hashlib, re, sys, pathlib
    path = pathlib.Path('docs/INTEGRATOR_README.md')
    content = path.read_text()
    # Extract declared body_sha256 from Kit-side frontmatter
    m = re.search(r'^body_sha256:\s*"([0-9a-f]{64})"', content, re.MULTILINE)
    if not m:
        print(f'❌ frontmatter missing or malformed body_sha256 in {path}')
        sys.exit(1)
    declared = m.group(1)
    # Locate body — first H1 matching the Brain canon's title
    body_m = re.search(r'^# CLAWDOG/141', content, re.MULTILINE)
    if not body_m:
        print(f'❌ {path} missing body H1 "# CLAWDOG/141"')
        sys.exit(1)
    body = content[body_m.start():]
    actual = hashlib.sha256(body.encode('utf-8')).hexdigest()
    if declared != actual:
        print(f'❌ DRIFT: declared body_sha256={declared}; actual={actual}')
        sys.exit(1)
    print(f'✅ body bytes hash to declared body_sha256: {actual}')
    PY
```

The Kit-side frontmatter declares four agreement points: `source_brain_node_hash` (Brain canon's `content_hash`), `source_brain_canon_commit` (the merge SHA on `clawdog-brain` master), `body_sha256` (SHA-256 of all body bytes from the H1 to EOF), and `last_synced_with_brain_canon` (ISO-8601 UTC timestamp). The Gate-3 assertion checks `body_sha256` against the actual body bytes; the other three fields are agreement record only.

**What this catches:**

- (a) Direct edits to the Kit doc's body — anyone editing the body content produces a `body_sha256` mismatch.
- (b) Re-sync without frontmatter update — if a contributor copies a new Brain canon body but forgets to recompute and update `body_sha256`, the mismatch fails CI.

**What this does NOT catch:**

- (c) Brain canon mutated AND Kit body correctly synced AND `body_sha256` updated AND `source_brain_node_hash` left declaring an old Brain hash. That requires a Brain-side mutation announcement mechanism (webhook, RSS, or scheduled comparison job), which is a follow-up not yet implemented.

This is Lesson #32's option (iii) — failure-mode preserves the load-bearing artifact (the Kit's `docs/INTEGRATOR_README.md` continues to exist; users continue to find it at the canonical URL) while surfacing schema drift loudly enough that the next PR cycle catches it.

*Historical note on this section:* the mc22 original revision of this pack illustrated the assertion with a `curl` against `raw.githubusercontent.com` fetching the Brain canon's `content_hash` live. That literal would not work in CI: `futureWA/clawdog-brain` is private, so `raw.githubusercontent.com` returns 404 to unauthenticated fetches, and the Kit runs in a different org without ambient access to a Brain RO PAT. The byte-check approach above is what shipped on Kit PR #11; the mc23 amendment (this revision) corrects the literal example to match the shipped pattern. The reasoning behind the original error is documented in the helm_mutations entry above for forensic transparency.

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
