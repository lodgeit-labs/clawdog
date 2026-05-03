"""Per-jurisdiction fiscal-year date conventions.

S5c: replaces the AU-only hard-coded `_period_meta_for_label` in
`pipeline.py` with a jurisdiction-aware lookup. The temporal *atom*
(`FY25`) stays bare in the Prolog database — see `clawdog-brain`
Standing Rule #6 (Hoffman Temporal-Dimension Discipline) — and the
*interpretation* of that atom into specific (StartDate, EndDate)
pairs is a local jurisdictional concern handled here, in the Python
bridge, not in the core logic engine.

Three jurisdictions are supported at landing:

  * AU — Australian fiscal year (1 July YY-1 — 30 June YY).
  * UK — UK personal/corporation tax year (6 April YY-1 — 5 April YY).
  * US — US calendar year (1 January YY — 31 December YY).

The default jurisdiction is ``'AU'`` so existing single-entity
ledgers see zero behavioural change. Group manifests already carry
explicit ``period_start`` / ``period_end`` dates and are unaffected
by this module entirely; the AU-default leak existed only in the
single-entity filename-convention path.

Period-label convention: ``FY{YY}`` where ``YY`` is the *ending*
year (two digits, century-prefixed by ``20``). ``FY25`` therefore
denotes:

  * AU: 2024-07-01 .. 2025-06-30
  * UK: 2024-04-06 .. 2025-04-05
  * US: 2025-01-01 .. 2025-12-31

The same atom (`FY25`) carries different date ranges per
jurisdiction. The atom remains opaque to the Prolog audit engine;
it is just an entity-period key (per `memory/2026-05-03-s5b-pickup-
carryover.md` § "S5c risks").
"""

import re

_FY_LABEL_RE = re.compile(r'^FY(\d{2})$')

# Supported jurisdictions and their (start_month, start_day,
# end_month, end_day, end_year_offset) conventions. `end_year_offset`
# is added to the FY label's century-prefixed year to produce the
# end year; `start_year` is `end_year - 1` for AU/UK and `end_year`
# for US (because US uses calendar-year fiscal years, FY25 = 2025).
_CONVENTIONS = {
    'AU': {
        'start_month': 7, 'start_day': 1,
        'end_month':   6, 'end_day':   30,
        'start_year_relative': 'minus_one',  # start = end - 1
    },
    'UK': {
        'start_month': 4, 'start_day': 6,
        'end_month':   4, 'end_day':   5,
        'start_year_relative': 'minus_one',  # start = end - 1
    },
    'US': {
        'start_month': 1, 'start_day': 1,
        'end_month':   12, 'end_day':  31,
        'start_year_relative': 'same',       # start = end (calendar year)
    },
}

SUPPORTED_JURISDICTIONS = tuple(sorted(_CONVENTIONS.keys()))
DEFAULT_JURISDICTION = 'AU'


def period_meta_for_label(period_label, jurisdiction=DEFAULT_JURISDICTION):
    """Map a fiscal-year label like ``FY25`` to a period_meta dict
    under the given jurisdiction's date convention.

    Returns a dict ``{'PeriodLabel', 'StartDate', 'EndDate'}`` on
    success, or ``None`` if ``period_label`` does not match the
    ``FY\\d{2}`` pattern. Unknown jurisdictions raise ``ValueError``
    rather than silently defaulting — Standing Rule #3 (Zero-
    Hallucination Law) forbids silent inference of missing data.

    The period atom in the returned dict is the input ``period_label``
    unchanged. Jurisdiction is metadata, not embedded in the label.
    """
    if jurisdiction not in _CONVENTIONS:
        raise ValueError(
            f"Unknown jurisdiction {jurisdiction!r}; "
            f"supported: {SUPPORTED_JURISDICTIONS}"
        )
    m = _FY_LABEL_RE.match(period_label)
    if not m:
        return None
    yy = int(m.group(1))
    end_year = 2000 + yy
    conv = _CONVENTIONS[jurisdiction]
    if conv['start_year_relative'] == 'minus_one':
        start_year = end_year - 1
    else:
        start_year = end_year
    return {
        'PeriodLabel': period_label,
        'StartDate':   f"{start_year:04d}-{conv['start_month']:02d}-{conv['start_day']:02d}",
        'EndDate':     f"{end_year:04d}-{conv['end_month']:02d}-{conv['end_day']:02d}",
    }
