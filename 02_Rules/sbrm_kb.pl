% =========================================================
% SYSTEM: OPEN-SOURCE SBRM HYPERCUBE
% LAYER: LOGIC & INFERENCE (SWI-PROLOG)
% =========================================================

:- dynamic sbrm_fact/6.

% --- 1. DECENTRALIZED FACT ASSERTIONS ---
% Arity 6: sbrm_fact(Entity, Period, Concept, Magnitude, Unit, ArrangementPattern).

sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026', 'urn:uuid:def-sbr-accumulated-depreciation', 25000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026', 'urn:uuid:def-sbr-cash-at-bank', 50000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period', 'urn:uuid:def-sbr-current-assets', 50000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period', 'urn:uuid:def-sbr-current-liabilities', 30000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration', 'urn:uuid:def-sbr-dividends-paid', 5000.0, 'AUD', 'RollForward').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration', 'urn:uuid:def-sbr-expenses', 80000.0, 'AUD', 'RollUp').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period', 'urn:uuid:def-sbr-non-current-assets', 75000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period', 'urn:uuid:def-sbr-non-current-liabilities', 50000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-sbr-opening-equity', 30000.0, 'AUD', 'RollForward').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026', 'urn:uuid:def-sbr-plant-at-cost', 100000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration', 'urn:uuid:def-sbr-profit-loss', 20000.0, 'AUD', 'RollUp').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration', 'urn:uuid:def-sbr-revenue', 100000.0, 'AUD', 'RollUp').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration', 'urn:uuid:def-sbr-revenue-blue', 25000.0, 'AUD', 'RollUp').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration', 'urn:uuid:def-sbr-revenue-green', 25000.0, 'AUD', 'RollUp').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration', 'urn:uuid:def-sbr-revenue-red', 25000.0, 'AUD', 'RollUp').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration', 'urn:uuid:def-sbr-revenue-yellow', 25000.0, 'AUD', 'RollUp').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period', 'urn:uuid:def-sbr-total-assets', 125000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period', 'urn:uuid:def-sbr-total-equity', 45000.0, 'AUD', 'RollForward').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period', 'urn:uuid:def-sbr-total-liabilities', 80000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026', 'urn:uuid:def-wp-bank-statement-balance', 50000.0, 'AUD', 'CrossReference').

% [SYSTEM] 20 Multidimensional Facts Compiled.

% --- 2. SBRM OPERATIVE PREDICATES ---

% Rule: rule-sbrm-accounting-equation
is_balanced(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-assets', Assets, _, 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-liabilities', Liabilities, _, 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-equity', Equity, _, 'RollForward'),
    Assets =:= Liabilities + Equity.

% Rule: rule-sbrm-asset-rollup
validate_asset_rollup(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-current-assets', CA, _, 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-non-current-assets', NCA, _, 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-assets', TA, _, 'Hierarchy'),
    TA =:= CA + NCA.

% Rule: rule-sbrm-equity-rollforward
validate_equity_rollforward(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-opening-equity', Opening, _, 'RollForward'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-profit-loss', PL, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-dividends-paid', Div, _, 'RollForward'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-equity', Closing, _, 'RollForward'),
    Closing =:= Opening + PL - Div.

