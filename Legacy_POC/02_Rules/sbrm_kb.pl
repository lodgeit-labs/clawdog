% =========================================================
% SYSTEM: OPEN-SOURCE SBRM HYPERCUBE
% LAYER: LOGIC & INFERENCE (SWI-PROLOG)
% =========================================================

:- dynamic sbrm_edge/4.
:- dynamic sbrm_fact/6.
:- discontiguous sbrm_parent/2.

% --- 1. DECENTRALIZED FACT ASSERTIONS ---
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

% --- 2. SBRM OPERATIVE PREDICATES ---
is_balanced(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-assets', Assets, _, 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-liabilities', Liabilities, _, 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-equity', Equity, _, 'RollForward'),
    Assets =:= Liabilities + Equity.

validate_asset_rollup(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-current-assets', CA, _, 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-non-current-assets', NCA, _, 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-assets', TA, _, 'Hierarchy'),
    TA =:= CA + NCA.

validate_equity_rollforward(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-opening-equity', Opening, _, 'RollForward'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-profit-loss', PL, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-dividends-paid', Div, _, 'RollForward'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-total-equity', Closing, _, 'RollForward'),
    Closing =:= Opening + PL - Div.

validate_equity_rollforward_v2(Entity) :- 
    sbrm_fact(Entity, _, 'urn:uuid:def-sbr-opening-equity', Opening, _, 'RollForward'), 
    sbrm_fact(Entity, _, 'urn:uuid:def-sbr-profit-loss', PL, _, 'RollUp'), 
    sbrm_fact(Entity, _, 'urn:uuid:def-sbr-dividends-paid', Div, _, 'RollForward'), 
    sbrm_fact(Entity, _, 'urn:uuid:def-sbr-total-equity', Closing, _, 'RollForward'), 
    Closing =:= Opening + PL - Div. 

% --- SEMANTIC BRIDGE ---
% Links the SBRM UUID to the GST Logic Engine's named entity
entity_name_map('urn:uuid:def-sbrm-reporting-entity', 'Demo Company').

% --- DYNAMIC IAWO RULE ---
calculate_iawo_deduction(Entity, Period, Deduction) :- 
    % 1. Get the asset cost from SBRM
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-plant-at-cost', AssetCost, 'AUD', 'Hierarchy'), 
    
    % 2. Cross the bridge to get the human name
    entity_name_map(Entity, NamedEntity),
    
    % 3. Query the GST rules for this entity's turnover
    has_turnover(NamedEntity, Turnover),
    
    % 4. Logic: If Turnover < $10m (SBE), threshold is $150k. Else, $20k.
    ( Turnover < 10000000 -> Threshold = 150000.0 ; Threshold = 20000.0 ),
    
    % 5. Apply the deduction
    ( AssetCost =< Threshold -> Deduction = AssetCost ; Deduction = 0.0 ).

validate_net_profit(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue', Revenue, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-expenses', Expenses, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-profit-loss', PL, _, 'RollUp'),
    PL =:= Revenue - Expenses.

validate_revenue_breakdown(Entity, Period) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue-blue', RevBlue, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue-green', RevGreen, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue-red', RevRed, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue-yellow', RevYellow, _, 'RollUp'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-sbr-revenue', TotalRevenue, _, 'RollUp'),
    TotalRevenue =:= RevBlue + RevGreen + RevRed + RevYellow.

% --- 4. ONTOLOGICAL BRANCH STRUCTURE (TAXONOMY) ---
sbrm_parent('urn:uuid:def-sbr-current-assets', 'urn:uuid:def-sbr-total-assets').
sbrm_parent('urn:uuid:def-sbr-non-current-assets', 'urn:uuid:def-sbr-total-assets').
sbrm_parent('urn:uuid:def-sbr-cash-at-bank', 'urn:uuid:def-sbr-current-assets').
sbrm_parent('urn:uuid:def-wp-bank-statement-balance', 'urn:uuid:def-sbr-cash-at-bank').
sbrm_parent('urn:uuid:def-sbr-plant-at-cost', 'urn:uuid:def-sbr-non-current-assets').
sbrm_parent('urn:uuid:def-sbr-accumulated-depreciation', 'urn:uuid:def-sbr-non-current-assets').
sbrm_parent('urn:uuid:def-sbr-opening-equity', 'urn:uuid:def-sbr-total-equity').
sbrm_parent('urn:uuid:def-sbr-profit-loss', 'urn:uuid:def-sbr-total-equity').
sbrm_parent('urn:uuid:def-sbr-dividends-paid', 'urn:uuid:def-sbr-total-equity').
sbrm_parent('urn:uuid:def-sbr-current-liabilities', 'urn:uuid:def-sbr-total-liabilities').
sbrm_parent('urn:uuid:def-sbr-non-current-liabilities', 'urn:uuid:def-sbr-total-liabilities').

% =============================================================================
% MASTER HEALTH CHECK & BRANCH REASONER
% =============================================================================

run_health_checks :-
    writeln('========================================='),
    writeln('        SBRM HEALTH CHECK REPORT         '),
    writeln('========================================='),
    
    % 1. Accounting Equation
    (   is_balanced('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period')
    ->  writeln('[PASS] Accounting Equation (A = L + E)')
    ;   writeln('[FAIL] Accounting Equation Broken')
    ),
    
    % 2. Asset Rollup
    (   validate_asset_rollup('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period')
    ->  writeln('[PASS] Asset Rollup (CA + NCA = TA)')
    ;   writeln('[FAIL] Asset Rollup Broken')
    ),
    
    % 3. Net Profit
    (   validate_net_profit('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration')
    ->  writeln('[PASS] Net Profit (Revenue - Expenses = P&L)')
    ;   writeln('[FAIL] Net Profit Broken')
    ),
    
    % 4. Revenue Fan-out
    (   validate_revenue_breakdown('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2026-duration')
    ->  writeln('[PASS] Revenue Breakdown (Sum of slices = Total)')
    ;   writeln('[FAIL] Revenue Breakdown Broken')
    ),
    writeln('=========================================').

% Recursive Branch Structure Generator
generate_branch_structure(TargetUUID, IndentLevel) :-
    % Print the current node with indentation
    tab(IndentLevel), write('-> '), writeln(TargetUUID),
    
    % Find all children where the TargetUUID is the parent/total
    % (Assuming your data structure uses sbrm_edge for parent-child relations)
    % Adjust the edge name 'sbrm:isRollupOf' if your ontology uses a different predicate.
    forall(
        sbrm_edge(_, 'sbrm:isRollupOf', TargetUUID, ChildUUID),
        (
            NextIndent is IndentLevel + 4,
            generate_branch_structure(ChildUUID, NextIndent)
        )
    ).

% --- END OF FILE ---