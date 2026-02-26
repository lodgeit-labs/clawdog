% =========================================================
% SYSTEM: OPEN-SOURCE SBRM HYPERCUBE
% LAYER: LOGIC & INFERENCE (SWI-PROLOG)
% =========================================================

:- dynamic sbrm_fact/6.

:- discontiguous sbrm_parent/2.

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

% Rule: rule-sbrm-net-profit
validate_net_profit(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue', Revenue, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-expenses', Expenses, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-profit-loss', PL, _, 'RollUp'),
    PL =:= Revenue - Expenses.

% Rule: rule-sbrm-revenue-breakdown
validate_revenue_breakdown(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue-blue', RevBlue, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue-green', RevGreen, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue-red', RevRed, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue-yellow', RevYellow, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue', TotalRevenue, _, 'RollUp'),
    TotalRevenue =:= RevBlue + RevGreen + RevRed + RevYellow.

% --- 3. HEALTH CHECK WRAPPER ---

run_health_checks :-
    write('========================================='), nl,
    write('      SBRM HEALTH CHECK REPORT           '), nl,
    write('========================================='), nl,
    
    Entity = 'urn:uuid:def-sbrm-reporting-entity',
    InstantPeriod = 'urn:uuid:def-sbrm-reporting-period',
    DurationPeriod = 'urn:uuid:def-sbrm-reporting-period-2026-duration',

    % Check 1: Accounting Equation
    ( is_balanced(Entity, InstantPeriod) ->
        write('[PASS] Accounting Equation (A = L + E)'), nl
    ;   write('[FAIL] Accounting Equation (A = L + E)'), nl
    ),

    % Check 2: Asset Rollup
    ( validate_asset_rollup(Entity, InstantPeriod) ->
        write('[PASS] Asset Rollup (CA + NCA = TA)'), nl
    ;   write('[FAIL] Asset Rollup (CA + NCA = TA)'), nl
    ),

    % Check 3: Equity Roll-forward
    ( validate_equity_rollforward_v2(Entity) ->
        write('[PASS] Equity Roll-forward (Open + P&L - Div = Close)'), nl
    ;   write('[FAIL] Equity Roll-forward (Open + P&L - Div = Close)'), nl
    ),
    
    % Check 4: Net Profit
    ( validate_net_profit(Entity, DurationPeriod) ->
        write('[PASS] Net Profit (Revenue - Expenses = P&L)'), nl
    ;   write('[FAIL] Net Profit (Revenue - Expenses = P&L)'), nl
    ),

    % Check 5: Revenue Breakdown
    ( validate_revenue_breakdown(Entity, DurationPeriod) ->
        write('[PASS] Revenue Breakdown (Sum of slices = Total Revenue)'), nl
    ;   write('[FAIL] Revenue Breakdown (Sum of slices = Total Revenue)'), nl
    ),
    
    write('========================================='), nl.

% --- 4. ONTOLOGICAL BRANCH STRUCTURE (TAXONOMY) ---
% Defining the isPartOf relationships (Child -> Parent)
sbrm_parent('urn:uuid:def-sbr-current-assets', 'urn:uuid:def-sbr-total-assets').
sbrm_parent('urn:uuid:def-sbr-non-current-assets', 'urn:uuid:def-sbr-total-assets').
sbrm_parent('urn:uuid:def-sbr-cash-at-bank', 'urn:uuid:def-sbr-current-assets').
sbrm_parent('urn:uuid:def-wp-bank-statement-balance', 'urn:uuid:def-sbr-cash-at-bank').
sbrm_parent('urn:uuid:def-sbr-plant-at-cost', 'urn:uuid:def-sbr-non-current-assets').
sbrm_parent('urn:uuid:def-sbr-accumulated-depreciation', 'urn:uuid:def-sbr-non-current-assets').
% Equity Structure
sbrm_parent('urn:uuid:def-sbr-opening-equity', 'urn:uuid:def-sbr-total-equity').
sbrm_parent('urn:uuid:def-sbr-profit-loss', 'urn:uuid:def-sbr-total-equity').
sbrm_parent('urn:uuid:def-sbr-dividends-paid', 'urn:uuid:def-sbr-total-equity').

% Recursive rule to walk the graph and generate the branch structure
generate_branch_structure(Node, Indent) :-
    tab(Indent), write('-> '), write(Node), nl,
    NewIndent is Indent + 4,
    forall(sbrm_parent(Child, Node), generate_branch_structure(Child, NewIndent)).

sbrm_parent('urn:uuid:def-sbr-current-liabilities', 'urn:uuid:def-sbr-total-liabilities').
sbrm_parent('urn:uuid:def-sbr-non-current-liabilities', 'urn:uuid:def-sbr-total-liabilities').





