"""Unit tests for engine/yaml_adjustments.py (Sprint A2).

Run from repo root:
    python3 -m unittest engine.tests.test_yaml_adjustments -v

Discipline:
  * stdlib unittest only — no pytest, no third-party deps. Aligns with
    test_jurisdiction_periods.py's existing convention.
  * Every D-A1.4 validation rule has at least one positive and one
    negative test.
  * Every D-A1.5 polarity case (debit and credit) tested explicitly
    with arithmetic equality.
  * The lifecycle lattice (D-A1.3) tested via accept/reject of each
    valid value and one invalid value.

Brain canon: GLOBAL_NOTES/CLAWDOG/108_LAST_MILE_ARCHITECTURE.md § 4.2
Author    : ClawDog ∮
"""
from __future__ import annotations

import textwrap
import unittest
from datetime import datetime, timezone

import yaml  # type: ignore[import-untyped]

# Module under test.
from engine.yaml_adjustments import (
    Adjustment,
    AdjustmentValidationError,
    Posting,
    SourceProvenance,
    adjustment_facts,
    parse_adjustment,
)


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

_VALID_YAML = textwrap.dedent("""
    adjustment:
      adj_id: "adj_a3f8c1d2e7b59f4a8c1e3b6d9f2a5c7e"
      entity: "Bluey_Builders_Pty_Ltd"
      period: "FY25"
      description: "Tax depreciation adjustment for FY25"
      approved_status: "proven"
      postings:
        - concept: "mini_DepreciationAndAmortization"
          amount: 1250.00
          direction: "debit"
          description: "Tax-flavored depreciation under Div 40"
        - concept: "audit_AccumulatedTaxDepreciation"
          amount: 1250.00
          direction: "credit"
          description: "Counter-entry to accounting depreciation"
      source_provenance:
        trace_id: "dep_api_2026Q1_a3f8c1"
        authored_at: "2026-05-04T01:50:00Z"
        service: "lodgeit-depreciation-api/v1"
        service_endpoint: "https://depreciation.lodgeit.org/v1/calculate"
        service_version: "1.4.2"
        service_commit: null
        human_approver: "andrew@lodgeit.org"
        approved_at: "2026-05-04T01:52:00Z"
      audit_trail:
        injected_at: null
        balance_check: null
        six_point_recheck: null
        rejected_reason: null
""").strip()


def _doc_with(path: list[str], value: object) -> dict:
    """Load _VALID_YAML and override one nested field to test invalid cases."""
    doc = yaml.safe_load(_VALID_YAML)
    cursor = doc
    for key in path[:-1]:
        cursor = cursor[key]
    if value is _DELETE:
        del cursor[path[-1]]
    else:
        cursor[path[-1]] = value
    return doc


_DELETE = object()  # sentinel for "delete this field" in _doc_with


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

class HappyPathTests(unittest.TestCase):

    def test_valid_envelope_parses_cleanly(self):
        doc = yaml.safe_load(_VALID_YAML)
        adj = parse_adjustment(doc)
        self.assertIsInstance(adj, Adjustment)
        self.assertEqual(adj.adj_id, "adj_a3f8c1d2e7b59f4a8c1e3b6d9f2a5c7e")
        self.assertEqual(adj.entity, "Bluey_Builders_Pty_Ltd")
        self.assertEqual(adj.period, "FY25")
        self.assertEqual(adj.approved_status, "proven")
        self.assertEqual(len(adj.postings), 2)

    def test_polarity_resolved_correctly(self):
        adj = parse_adjustment(yaml.safe_load(_VALID_YAML))
        debit_posting, credit_posting = adj.postings
        # debit  → +amount
        self.assertAlmostEqual(debit_posting.signed_amount, 1250.00)
        self.assertEqual(debit_posting.direction, "debit")
        # credit → -amount
        self.assertAlmostEqual(credit_posting.signed_amount, -1250.00)
        self.assertEqual(credit_posting.direction, "credit")
        # The journal balances after polarity resolution: 1250 + (-1250) = 0.
        total = sum(p.signed_amount for p in adj.postings)
        self.assertAlmostEqual(total, 0.0)

    def test_facts_projection_yields_six_tuples(self):
        adj = parse_adjustment(yaml.safe_load(_VALID_YAML))
        facts = list(adjustment_facts(adj))
        self.assertEqual(len(facts), 2)
        for f in facts:
            self.assertEqual(len(f), 6)
            entity, period, adj_id, concept, signed, direction = f
            self.assertEqual(entity, "Bluey_Builders_Pty_Ltd")
            self.assertEqual(period, "FY25")
            self.assertTrue(adj_id.startswith("adj_"))
            self.assertIsInstance(signed, float)
            self.assertIn(direction, ("debit", "credit"))

    def test_authored_at_parsed_as_utc(self):
        adj = parse_adjustment(yaml.safe_load(_VALID_YAML))
        self.assertEqual(
            adj.source_provenance.authored_at,
            datetime(2026, 5, 4, 1, 50, 0, tzinfo=timezone.utc),
        )

    def test_service_endpoint_null_carve_out(self):
        """D-A1.4 ruling: service_endpoint may be null for local-agent authorship."""
        doc = _doc_with(
            ["adjustment", "source_provenance", "service_endpoint"], None,
        )
        # service_commit must be set if service_version is null; in this fixture
        # service_version is "1.4.2" so the endpoint=null path is the only
        # variation. Should parse cleanly.
        adj = parse_adjustment(doc)
        self.assertIsNone(adj.source_provenance.service_endpoint)

    def test_service_commit_alternative_to_version(self):
        """source_provenance accepts service_commit when service_version is null."""
        doc = _doc_with(
            ["adjustment", "source_provenance", "service_version"], None,
        )
        # Add a valid commit (40-hex).
        doc["adjustment"]["source_provenance"]["service_commit"] = (
            "9e7f2a1b3c4d5e6f7890a1b2c3d4e5f60718293a"
        )
        adj = parse_adjustment(doc)
        self.assertIsNone(adj.source_provenance.service_version)
        self.assertEqual(
            adj.source_provenance.service_commit,
            "9e7f2a1b3c4d5e6f7890a1b2c3d4e5f60718293a",
        )

    def test_audit_trail_block_null_treated_as_all_null_fields(self):
        doc = _doc_with(["adjustment", "audit_trail"], None)
        adj = parse_adjustment(doc)
        self.assertIsNone(adj.audit_trail.injected_at)
        self.assertIsNone(adj.audit_trail.balance_check)
        self.assertIsNone(adj.audit_trail.six_point_recheck)
        self.assertIsNone(adj.audit_trail.rejected_reason)


# ---------------------------------------------------------------------------
# Negative tests — every D-A1.4 rule has loud failure
# ---------------------------------------------------------------------------

class FailLoudTests(unittest.TestCase):

    def assert_validation_error(self, doc, *, contains: str):
        """Helper: expect AdjustmentValidationError with `contains` in the message."""
        with self.assertRaises(AdjustmentValidationError) as ctx:
            parse_adjustment(doc)
        self.assertIn(contains, str(ctx.exception))

    # -- top-level shape --

    def test_non_mapping_yaml_root(self):
        self.assert_validation_error("not a mapping", contains="top-level YAML")

    def test_missing_adjustment_block(self):
        self.assert_validation_error({}, contains="required field is missing")

    # -- adj_id format --

    def test_malformed_adj_id_rejected(self):
        doc = _doc_with(["adjustment", "adj_id"], "not_a_uuid_shape")
        self.assert_validation_error(doc, contains="adj_id")

    def test_adj_id_wrong_hex_length_rejected(self):
        # 16 hex chars instead of 32.
        doc = _doc_with(["adjustment", "adj_id"], "adj_a3f8c1d2e7b59f4a")
        self.assert_validation_error(doc, contains="adj_id")

    # -- approved_status lattice --

    def test_invalid_approved_status_rejected(self):
        doc = _doc_with(["adjustment", "approved_status"], "auto-approved")
        self.assert_validation_error(doc, contains="approved_status")

    def test_each_valid_approved_status_accepted(self):
        for status in ("pending", "approved", "proven", "rejected"):
            with self.subTest(status=status):
                doc = _doc_with(["adjustment", "approved_status"], status)
                adj = parse_adjustment(doc)
                self.assertEqual(adj.approved_status, status)

    # -- postings --

    def test_empty_postings_rejected(self):
        doc = _doc_with(["adjustment", "postings"], [])
        self.assert_validation_error(doc, contains="non-empty list")

    def test_negative_amount_rejected(self):
        # Polarity belongs in 'direction', not in the sign of 'amount'.
        doc = yaml.safe_load(_VALID_YAML)
        doc["adjustment"]["postings"][0]["amount"] = -1250.00
        self.assert_validation_error(doc, contains="non-negative")

    def test_invalid_direction_rejected(self):
        doc = yaml.safe_load(_VALID_YAML)
        doc["adjustment"]["postings"][0]["direction"] = "neutral"
        self.assert_validation_error(doc, contains="direction")

    def test_concept_not_atom_shape_rejected(self):
        doc = yaml.safe_load(_VALID_YAML)
        doc["adjustment"]["postings"][0]["concept"] = "Mini Has Spaces"
        self.assert_validation_error(doc, contains="concept")

    # -- source_provenance --

    def test_missing_trace_id_rejected(self):
        doc = _doc_with(["adjustment", "source_provenance", "trace_id"], _DELETE)
        self.assert_validation_error(doc, contains="trace_id")

    def test_oversize_trace_id_rejected(self):
        doc = _doc_with(
            ["adjustment", "source_provenance", "trace_id"], "x" * 200,
        )
        self.assert_validation_error(doc, contains="trace_id")

    def test_authored_at_not_iso8601_rejected(self):
        doc = _doc_with(
            ["adjustment", "source_provenance", "authored_at"],
            "May the 4th, 2026",
        )
        self.assert_validation_error(doc, contains="authored_at")

    def test_authored_at_not_utc_rejected(self):
        doc = _doc_with(
            ["adjustment", "source_provenance", "authored_at"],
            "2026-05-04T01:50:00+10:00",
        )
        self.assert_validation_error(doc, contains="UTC")

    def test_service_pattern_rejected(self):
        doc = _doc_with(
            ["adjustment", "source_provenance", "service"], "no-slash-here",
        )
        self.assert_validation_error(doc, contains="service")

    def test_both_version_and_commit_null_rejected(self):
        doc = yaml.safe_load(_VALID_YAML)
        doc["adjustment"]["source_provenance"]["service_version"] = None
        doc["adjustment"]["source_provenance"]["service_commit"] = None
        self.assert_validation_error(doc, contains="service_version")

    def test_service_commit_wrong_hex_length_rejected(self):
        doc = yaml.safe_load(_VALID_YAML)
        doc["adjustment"]["source_provenance"]["service_version"] = None
        doc["adjustment"]["source_provenance"]["service_commit"] = "abc123"
        self.assert_validation_error(doc, contains="service_commit")

    def test_approved_at_before_authored_at_rejected(self):
        # Cross-field rule: approved_at >= authored_at.
        doc = _doc_with(
            ["adjustment", "source_provenance", "approved_at"],
            "2026-05-04T01:00:00Z",
        )
        # authored_at in fixture is 01:50; approved_at 01:00 violates.
        self.assert_validation_error(doc, contains="approved_at")

    def test_missing_human_approver_rejected(self):
        doc = _doc_with(
            ["adjustment", "source_provenance", "human_approver"], _DELETE,
        )
        self.assert_validation_error(doc, contains="human_approver")


if __name__ == "__main__":
    unittest.main()
