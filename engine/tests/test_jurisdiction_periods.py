"""Unit tests for engine.jurisdiction_periods (S5c).

Stdlib unittest — zero new test-framework dependencies. Run via:

    python3 -m unittest engine.tests.test_jurisdiction_periods -v

Coverage:
  * AU/UK/US × FY24/FY25/FY26 = 9 positive cases (3 jurisdictions ×
    3 periods).
  * Default jurisdiction is AU (legacy single-entity behaviour).
  * Unknown jurisdiction raises ValueError (Standing Rule #3).
  * Malformed period labels return None (preserves the existing
    ``_period_meta_for_label`` contract).
  * Period atom in the returned dict equals the input label
    (jurisdiction is metadata, not embedded in the label).
"""

import os
import sys
import unittest

# Allow `engine.jurisdiction_periods` to import when tests run from
# repo root via ``python3 -m unittest engine.tests.test_jurisdiction_periods``.
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from engine.jurisdiction_periods import (
    DEFAULT_JURISDICTION,
    SUPPORTED_JURISDICTIONS,
    period_meta_for_label,
)


class TestJurisdictionPeriods(unittest.TestCase):

    # -- Positive cases ----------------------------------------------------

    def test_au_fy24(self):
        self.assertEqual(
            period_meta_for_label('FY24', 'AU'),
            {'PeriodLabel': 'FY24',
             'StartDate':   '2023-07-01',
             'EndDate':     '2024-06-30'},
        )

    def test_au_fy25(self):
        self.assertEqual(
            period_meta_for_label('FY25', 'AU'),
            {'PeriodLabel': 'FY25',
             'StartDate':   '2024-07-01',
             'EndDate':     '2025-06-30'},
        )

    def test_au_fy26(self):
        self.assertEqual(
            period_meta_for_label('FY26', 'AU'),
            {'PeriodLabel': 'FY26',
             'StartDate':   '2025-07-01',
             'EndDate':     '2026-06-30'},
        )

    def test_uk_fy24(self):
        self.assertEqual(
            period_meta_for_label('FY24', 'UK'),
            {'PeriodLabel': 'FY24',
             'StartDate':   '2023-04-06',
             'EndDate':     '2024-04-05'},
        )

    def test_uk_fy25(self):
        self.assertEqual(
            period_meta_for_label('FY25', 'UK'),
            {'PeriodLabel': 'FY25',
             'StartDate':   '2024-04-06',
             'EndDate':     '2025-04-05'},
        )

    def test_uk_fy26(self):
        self.assertEqual(
            period_meta_for_label('FY26', 'UK'),
            {'PeriodLabel': 'FY26',
             'StartDate':   '2025-04-06',
             'EndDate':     '2026-04-05'},
        )

    def test_us_fy24(self):
        self.assertEqual(
            period_meta_for_label('FY24', 'US'),
            {'PeriodLabel': 'FY24',
             'StartDate':   '2024-01-01',
             'EndDate':     '2024-12-31'},
        )

    def test_us_fy25(self):
        self.assertEqual(
            period_meta_for_label('FY25', 'US'),
            {'PeriodLabel': 'FY25',
             'StartDate':   '2025-01-01',
             'EndDate':     '2025-12-31'},
        )

    def test_us_fy26(self):
        self.assertEqual(
            period_meta_for_label('FY26', 'US'),
            {'PeriodLabel': 'FY26',
             'StartDate':   '2026-01-01',
             'EndDate':     '2026-12-31'},
        )

    # -- Default jurisdiction ----------------------------------------------

    def test_default_jurisdiction_is_au(self):
        # Legacy callers (single-entity ledgers without a sidecar)
        # MUST see exactly the AU date convention they had pre-S5c.
        self.assertEqual(DEFAULT_JURISDICTION, 'AU')
        self.assertEqual(
            period_meta_for_label('FY25'),                 # no juris arg
            period_meta_for_label('FY25', 'AU'),
        )

    def test_supported_jurisdictions_are_sorted_tuple(self):
        # Stable enumeration order keeps test output deterministic
        # and prevents accidental dict-iteration-order regressions.
        self.assertEqual(SUPPORTED_JURISDICTIONS, ('AU', 'UK', 'US'))

    # -- Standing Rule #3 (Zero-Hallucination) -----------------------------

    def test_unknown_jurisdiction_raises(self):
        # Standing Rule #3 forbids silent inference of missing data.
        # An unknown jurisdiction MUST raise, not silently default.
        with self.assertRaises(ValueError) as cm:
            period_meta_for_label('FY25', 'NZ')
        self.assertIn('NZ', str(cm.exception))
        self.assertIn('AU', str(cm.exception))   # supported list surfaces
        self.assertIn('UK', str(cm.exception))
        self.assertIn('US', str(cm.exception))

    # -- Malformed labels --------------------------------------------------

    def test_malformed_label_returns_none(self):
        # Preserves the existing pipeline._period_meta_for_label contract:
        # returns None for non-FYxx labels, lets the caller decide what
        # to do (raise, skip, fall through to manifest, etc.).
        for bad_label in ['FY2025', 'fy25', 'FY-25', 'Q1-2024',
                          '2024H2', '', 'FY5', 'FY255']:
            with self.subTest(label=bad_label):
                self.assertIsNone(period_meta_for_label(bad_label, 'AU'))

    def test_malformed_label_returns_none_under_uk(self):
        # Same contract under non-default jurisdictions.
        self.assertIsNone(period_meta_for_label('Q1-2024', 'UK'))
        self.assertIsNone(period_meta_for_label('2024-25', 'UK'))

    # -- Period atom abstraction (Standing Rule #6) ------------------------

    def test_period_label_unchanged_across_jurisdictions(self):
        # The atom is opaque to the Prolog audit engine. It must
        # round-trip identically regardless of jurisdiction; only
        # the date interpretation differs.
        for juris in SUPPORTED_JURISDICTIONS:
            with self.subTest(jurisdiction=juris):
                meta = period_meta_for_label('FY25', juris)
                self.assertEqual(meta['PeriodLabel'], 'FY25')


if __name__ == '__main__':
    unittest.main()
