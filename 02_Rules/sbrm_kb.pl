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

 
%% Temporal Bridge Repair 
validate_equity_rollforward_v2(Entity) :- 
    sbrm_fact(Entity, _, 'urn:uuid:def-sbr-opening-equity', Opening, _, 'RollForward'), 
    sbrm_fact(Entity, _, 'urn:uuid:def-sbr-profit-loss', PL, _, 'RollUp'), 
    sbrm_fact(Entity, _, 'urn:uuid:def-sbr-dividends-paid', Div, _, 'RollForward'), 
    sbrm_fact(Entity, _, 'urn:uuid:def-sbr-total-equity', Closing, _, 'RollForward'), 
    Closing =:= Opening + PL - Div. 
 
%% --- JURISDICTIONAL ROUTING: ATO IAWO --- 
calculate_iawo_deduction(Entity, Period, Deduction) :- 
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-plant-at-cost', AssetCost, 'AUD', 'Hierarchy'), 
    ( AssetCost =< 20000.0 -> Deduction = AssetCost ; Deduction = 0.0 ). 

% Custom Rule C.2: Validate Equity Roll-Forward
validate_equity_roll_forward :-
    % 1. Fetch Opening Balance
    get_recursive_section_value('section:opening-equity', OpeningEquity),
    
    % 2. Fetch Equity Movements (Flows)
    get_recursive_section_value('section:capital-introduced', Capital),
    get_recursive_section_value('section:retained-earnings', Earnings),
    get_recursive_section_value('section:dividends-paid', Dividends), % Assuming standard subtraction for dividends
    
    % 3. Fetch Closing Balance (Total Equity)
    get_recursive_section_value('section:total-equity', ClosingEquity),

    % 4. Verify Temporal Types (Strict OIM Requirement)
    section_has_type('section:opening-equity', 'instant'),
    section_has_type('section:total-equity', 'instant'),

    % 5. Calculate & Check
    % Formula: Opening + Capital + Earnings - Dividends = Closing
    CalculatedClosing is OpeningEquity + Capital + Earnings - Dividends,
    
    ( abs(CalculatedClosing - ClosingEquity) < 0.01 ->
        format('PASS: Equity Roll-forward valid. Calculated: ~w, Reported: ~w.', [CalculatedClosing, ClosingEquity])
    ;
        format('FAIL: Equity Roll-forward mismatch! Calculated ~w does not equal Reported ~w.', [CalculatedClosing, ClosingEquity]),
        fail
    ).


