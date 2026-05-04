"""YAML adjustment-journal loader, validator, and polarity resolver.

Sprint A2 (Phase II realignment). Implements the bridge-side half of the
sbrm_adjustment/6 schema locked in Brain canon
GLOBAL_NOTES/CLAWDOG/108_LAST_MILE_ARCHITECTURE.md § 4.2.

Responsibilities:
  1. Load a YAML file conforming to the locked envelope shape (§ 4.2.2).
  2. Validate every required field, format, and cross-field rule (D-A1.4).
  3. Resolve debit/credit polarity into signed amounts (D-A1.5; bridge-
     resolves by Andrew's ruling 2026-05-04 01:57 UTC). Prolog reasons
     over signed numbers only.
  4. Emit a sequence of (Entity, Period, AdjId, Concept, SignedAmount,
     Direction) tuples ready for assertz into
     sbrm_consolidation:sbrm_adjustment/6.

Discipline:
  * stdlib + pyyaml only — no Pydantic, no third-party validators.
    Aligns with engine.jurisdiction_periods (zero third-party imports
    in engine/* modules where possible). Lesson #19 (stdlib-only is
    sometimes the right dependency choice) applies; the validation
    rules from D-A1.4 are simple enough to hand-code.
  * Fail-loud on every malformed envelope. Standing Rule #3: no silent
    coercion, no default values for required fields.
  * Pure functions where possible; no I/O outside load_adjustment_yaml.

Polarity convention (per the bridge-resolves ruling):
  * debit  → SignedAmount = +amount
  * credit → SignedAmount = -amount

  Rationale: debit-positive on assets and expenses, credit-positive on
  liabilities and equity is the convention the existing pipeline.py
  CSV ingestion uses (cash receipts negative, expense rows positive).
  This convention aligns with the Australian double-entry signing the
  Wind Tunnel CSVs already use; jurisdiction-specific reporting
  conventions (UK FRS 102 vs AU SBRM) are handled at the consumption
  layer, not here. Future jurisdictional polarity differences (if they
  exist) would surface at YAML schema time as an explicit field, not
  as a silent translation here.

Brain canon: GLOBAL_NOTES/CLAWDOG/108_LAST_MILE_ARCHITECTURE.md
Author    : ClawDog ∮
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class AdjustmentValidationError(ValueError):
    """Raised when a YAML adjustment envelope violates the locked schema.

    Standing Rule #3: structured, loud failure with the field path that
    triggered the violation. Never silently coerce or default."""


# ---------------------------------------------------------------------------
# Validation primitives
# ---------------------------------------------------------------------------

_APPROVED_STATUSES = frozenset({"pending", "approved", "proven", "rejected"})
_DIRECTIONS = frozenset({"debit", "credit"})
_ATOM_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_ADJ_ID_RE = re.compile(r"^adj_[0-9a-f]{32}$")
# Service identifier must look like "<name>/<version>". Names may contain
# hyphens (e.g. "lodgeit-depreciation-api") and versions may contain dots,
# pluses, and pre-release suffixes (e.g. "v1", "1.4.2", "2.0.0-beta.3",
# "1.0.0+build.42"). The 108 § 4.2.2 description called this "\w+/\w+" as
# loose shorthand; the implementation must accept the realistic shape.
# Lesson #15 — the most important constraint is the one your own validator
# violates.
_SERVICE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.+\-]*/[A-Za-z0-9][A-Za-z0-9_.+\-]*$")
_HEX_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$|^[0-9a-f]{64}$")
_TRACE_ID_MAX_LEN = 128


def _require_field(obj: dict, key: str, *, path: str) -> object:
    """Return obj[key] or raise with a path-tagged error."""
    if not isinstance(obj, dict):
        raise AdjustmentValidationError(
            f"{path}: expected mapping, got {type(obj).__name__}")
    if key not in obj:
        raise AdjustmentValidationError(
            f"{path}.{key}: required field is missing")
    return obj[key]


def _parse_iso8601_utc(value: object, *, path: str) -> datetime:
    """Parse an ISO-8601 UTC timestamp with a Z or +00:00 suffix.

    Standing Rule #3 — loud failure on any non-conforming string."""
    if not isinstance(value, str):
        raise AdjustmentValidationError(
            f"{path}: expected ISO-8601 UTC string, got {type(value).__name__}")
    s = value.strip()
    # Tolerate trailing Z by converting to +00:00 for fromisoformat.
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError as exc:
        raise AdjustmentValidationError(
            f"{path}: not parseable as ISO-8601: {value!r}") from exc
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(None):
        # Either no timezone or non-UTC. Both fail loud.
        raise AdjustmentValidationError(
            f"{path}: must be UTC (Z or +00:00 suffix); got {value!r}")
    return dt


# ---------------------------------------------------------------------------
# Locked dataclasses (mirror the YAML envelope shape § 4.2.2)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SourceProvenance:
    trace_id: str
    authored_at: datetime
    service: str
    service_endpoint: str | None
    service_version: str | None
    service_commit: str | None
    human_approver: str
    approved_at: datetime


@dataclass(frozen=True)
class Posting:
    concept: str           # mini_*/audit_*/sbrm_* atom
    amount: float          # raw (positive); signed_amount holds the resolved value
    direction: str         # 'debit' | 'credit'
    description: str
    signed_amount: float   # +amount for debit, -amount for credit (D-A1.5)


@dataclass(frozen=True)
class AuditTrail:
    injected_at: datetime | None
    balance_check: dict | None
    six_point_recheck: list | None
    rejected_reason: str | None


@dataclass(frozen=True)
class Adjustment:
    adj_id: str             # adj_<32-hex> opaque UUID atom (D-A1.2)
    entity: str
    period: str             # bare period atom (Lesson #36 / S5c)
    description: str
    approved_status: str    # lifecycle lattice
    postings: tuple[Posting, ...]
    source_provenance: SourceProvenance
    audit_trail: AuditTrail


# ---------------------------------------------------------------------------
# Field-level validators
# ---------------------------------------------------------------------------

def _validate_atom_shape(value: object, *, path: str) -> str:
    if not isinstance(value, str):
        raise AdjustmentValidationError(
            f"{path}: expected atom-shaped string, got {type(value).__name__}")
    if not _ATOM_RE.match(value):
        raise AdjustmentValidationError(
            f"{path}: must be atom-shape (^[A-Za-z_][A-Za-z0-9_]*$); got {value!r}")
    return value


def _validate_adj_id(value: object, *, path: str) -> str:
    if not isinstance(value, str):
        raise AdjustmentValidationError(
            f"{path}: expected string, got {type(value).__name__}")
    if not _ADJ_ID_RE.match(value):
        raise AdjustmentValidationError(
            f"{path}: must match ^adj_[0-9a-f]{{32}}$ (opaque UUID); got {value!r}")
    return value


def _validate_approved_status(value: object, *, path: str) -> str:
    if value not in _APPROVED_STATUSES:
        raise AdjustmentValidationError(
            f"{path}: must be one of {sorted(_APPROVED_STATUSES)}; got {value!r}")
    return value


def _validate_direction(value: object, *, path: str) -> str:
    if value not in _DIRECTIONS:
        raise AdjustmentValidationError(
            f"{path}: must be 'debit' or 'credit'; got {value!r}")
    return value


def _validate_amount(value: object, *, path: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AdjustmentValidationError(
            f"{path}: expected number, got {type(value).__name__}")
    f = float(value)
    if f < 0:
        raise AdjustmentValidationError(
            f"{path}: amount must be non-negative (polarity is in 'direction'); got {f}")
    return f


def _resolve_polarity(amount: float, direction: str) -> float:
    """Bridge-side polarity resolution per D-A1.5.

      debit  → +amount
      credit → -amount

    The Prolog engine reasons over signed numbers only; debit/credit
    semantics belong at the bridge boundary."""
    if direction == "debit":
        return amount
    if direction == "credit":
        return -amount
    # _validate_direction must have run before this; defensive.
    raise AdjustmentValidationError(
        f"_resolve_polarity: unknown direction {direction!r}")


def _validate_source_provenance(block: object, *,
                                authored_after: datetime | None = None,
                                path: str) -> SourceProvenance:
    if not isinstance(block, dict):
        raise AdjustmentValidationError(
            f"{path}: expected mapping, got {type(block).__name__}")

    trace_id = _require_field(block, "trace_id", path=path)
    if not isinstance(trace_id, str) or not trace_id:
        raise AdjustmentValidationError(
            f"{path}.trace_id: required non-empty string")
    if len(trace_id) > _TRACE_ID_MAX_LEN:
        raise AdjustmentValidationError(
            f"{path}.trace_id: exceeds {_TRACE_ID_MAX_LEN} chars (got {len(trace_id)})")

    authored_at = _parse_iso8601_utc(
        _require_field(block, "authored_at", path=path),
        path=f"{path}.authored_at")

    service = _require_field(block, "service", path=path)
    if not isinstance(service, str) or not _SERVICE_RE.match(service):
        raise AdjustmentValidationError(
            f"{path}.service: must match \\w+/\\w+ pattern; got {service!r}")

    # service_endpoint is optional; null carve-out for local-agent authorship
    # (D-A1.4 ruling — Andrew confirmed at 2026-05-04 01:57 UTC).
    service_endpoint = block.get("service_endpoint")
    if service_endpoint is not None and not isinstance(service_endpoint, str):
        raise AdjustmentValidationError(
            f"{path}.service_endpoint: must be string or null; got "
            f"{type(service_endpoint).__name__}")

    # service_version XOR service_commit (at least one non-null).
    service_version = block.get("service_version")
    service_commit = block.get("service_commit")
    if service_version is None and service_commit is None:
        raise AdjustmentValidationError(
            f"{path}: at least one of service_version or service_commit must be non-null")
    if service_version is not None and not isinstance(service_version, str):
        raise AdjustmentValidationError(
            f"{path}.service_version: must be string; got {type(service_version).__name__}")
    if service_commit is not None:
        if not isinstance(service_commit, str) or not _HEX_COMMIT_RE.match(service_commit):
            raise AdjustmentValidationError(
                f"{path}.service_commit: must be hex string of 40 or 64 chars; got {service_commit!r}")

    human_approver = _require_field(block, "human_approver", path=path)
    if not isinstance(human_approver, str) or not human_approver:
        raise AdjustmentValidationError(
            f"{path}.human_approver: required non-empty string")

    approved_at = _parse_iso8601_utc(
        _require_field(block, "approved_at", path=path),
        path=f"{path}.approved_at")

    if approved_at < authored_at:
        raise AdjustmentValidationError(
            f"{path}: approved_at ({approved_at.isoformat()}) must be "
            f">= authored_at ({authored_at.isoformat()})")

    return SourceProvenance(
        trace_id=trace_id,
        authored_at=authored_at,
        service=service,
        service_endpoint=service_endpoint,
        service_version=service_version,
        service_commit=service_commit,
        human_approver=human_approver,
        approved_at=approved_at,
    )


def _validate_audit_trail(block: object, *, path: str) -> AuditTrail:
    if block is None:
        # Whole block null is acceptable shorthand for "all four fields null".
        return AuditTrail(injected_at=None, balance_check=None,
                          six_point_recheck=None, rejected_reason=None)
    if not isinstance(block, dict):
        raise AdjustmentValidationError(
            f"{path}: expected mapping or null, got {type(block).__name__}")

    raw_injected = block.get("injected_at")
    injected_at = (None if raw_injected is None
                   else _parse_iso8601_utc(raw_injected,
                                            path=f"{path}.injected_at"))

    balance_check = block.get("balance_check")
    if balance_check is not None and not isinstance(balance_check, dict):
        raise AdjustmentValidationError(
            f"{path}.balance_check: must be mapping or null; got "
            f"{type(balance_check).__name__}")

    six_point = block.get("six_point_recheck")
    if six_point is not None and not isinstance(six_point, list):
        raise AdjustmentValidationError(
            f"{path}.six_point_recheck: must be list or null; got "
            f"{type(six_point).__name__}")

    rejected_reason = block.get("rejected_reason")
    if rejected_reason is not None and not isinstance(rejected_reason, str):
        raise AdjustmentValidationError(
            f"{path}.rejected_reason: must be string or null; got "
            f"{type(rejected_reason).__name__}")

    return AuditTrail(
        injected_at=injected_at,
        balance_check=balance_check,
        six_point_recheck=six_point,
        rejected_reason=rejected_reason,
    )


def _validate_postings(value: object, *, path: str) -> tuple[Posting, ...]:
    if not isinstance(value, list) or not value:
        raise AdjustmentValidationError(
            f"{path}: required non-empty list of postings")
    out: list[Posting] = []
    for i, raw in enumerate(value):
        sub = f"{path}[{i}]"
        if not isinstance(raw, dict):
            raise AdjustmentValidationError(
                f"{sub}: expected mapping, got {type(raw).__name__}")
        concept = _validate_atom_shape(_require_field(raw, "concept", path=sub),
                                       path=f"{sub}.concept")
        amount = _validate_amount(_require_field(raw, "amount", path=sub),
                                  path=f"{sub}.amount")
        direction = _validate_direction(_require_field(raw, "direction", path=sub),
                                        path=f"{sub}.direction")
        description = _require_field(raw, "description", path=sub)
        if not isinstance(description, str):
            raise AdjustmentValidationError(
                f"{sub}.description: must be string; got {type(description).__name__}")
        signed = _resolve_polarity(amount, direction)
        out.append(Posting(concept=concept, amount=amount, direction=direction,
                           description=description, signed_amount=signed))
    return tuple(out)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_adjustment(doc: object, *, path: str = "adjustment") -> Adjustment:
    """Validate a parsed YAML document into a locked Adjustment dataclass.

    Raises AdjustmentValidationError with a path-tagged message on any
    schema violation. Pure function; no I/O."""
    if not isinstance(doc, dict):
        raise AdjustmentValidationError(
            f"{path}: top-level YAML must be a mapping; got {type(doc).__name__}")
    block = _require_field(doc, "adjustment", path="<root>")
    if not isinstance(block, dict):
        raise AdjustmentValidationError(
            "adjustment: top-level 'adjustment' key must map to a mapping")

    adj_id = _validate_adj_id(_require_field(block, "adj_id", path=path),
                              path=f"{path}.adj_id")
    entity = _validate_atom_shape(_require_field(block, "entity", path=path),
                                  path=f"{path}.entity")
    period = _validate_atom_shape(_require_field(block, "period", path=path),
                                  path=f"{path}.period")

    description = _require_field(block, "description", path=path)
    if not isinstance(description, str):
        raise AdjustmentValidationError(
            f"{path}.description: must be string; got {type(description).__name__}")

    approved_status = _validate_approved_status(
        _require_field(block, "approved_status", path=path),
        path=f"{path}.approved_status")

    postings = _validate_postings(
        _require_field(block, "postings", path=path),
        path=f"{path}.postings")

    source_provenance = _validate_source_provenance(
        _require_field(block, "source_provenance", path=path),
        path=f"{path}.source_provenance")

    audit_trail = _validate_audit_trail(block.get("audit_trail"),
                                        path=f"{path}.audit_trail")

    return Adjustment(
        adj_id=adj_id, entity=entity, period=period, description=description,
        approved_status=approved_status, postings=postings,
        source_provenance=source_provenance, audit_trail=audit_trail,
    )


def load_adjustment_yaml(path: str | Path) -> Adjustment:
    """Read a YAML file from disk, parse it, and return a validated Adjustment.

    Convenience wrapper around parse_adjustment; the only I/O entry point
    in this module."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    return parse_adjustment(doc, path=f"<{p.name}>.adjustment")


def adjustment_facts(adj: Adjustment) -> Iterable[tuple[str, str, str, str, float, str]]:
    """Project a validated Adjustment into the (Entity, Period, AdjId,
    Concept, SignedAmount, Direction) tuples that match the Prolog
    sbrm_adjustment/6 schema. Caller is responsible for assertz-ing them
    into sbrm_consolidation:sbrm_adjustment/6."""
    for posting in adj.postings:
        yield (
            adj.entity, adj.period, adj.adj_id,
            posting.concept, posting.signed_amount, posting.direction,
        )
