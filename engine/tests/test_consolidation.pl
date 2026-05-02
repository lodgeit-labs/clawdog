%% Test suite for engine/consolidation.pl
%%
%% Run from repo root:    swipl -g run_tests -t halt engine/tests/test_consolidation.pl
%% Or from this directory: swipl -g run_tests -t halt test_consolidation.pl
%%
%% Covers: cycle-safe accumulator traversal, multifile fact injection,
%% epsilon-tolerant equity check (Opus baseline); unique-rate FX enforcement,
%% must_be type guards, no-silent-zero discipline (GPT grafts); weighted
%% edges with contra-account semantics + leaf-by-leaf provenance via
%% consolidation_evidence/6 (ClawDog extensions).
%%
%% Brain canon: GLOBAL_NOTES/CLAWDOG/107_CONSOLIDATION_LOGIC.md
%% (clawdog-brain repo, content_hash 5282338ae508…)

:- use_module('../consolidation', [
       calculate_consolidated_node/5,
       verify_temporal_equity/5,
       consolidation_evidence/6
   ]).

run_tests :-
    %% --- Baseline (Opus + GPT, ported from earlier suite) ---
    test_basic_consolidation,
    test_balanced_rollforward,
    test_unbalanced_rollforward_rejected,
    test_cycle_safety,
    test_target_concept_is_leaf,
    test_conflicting_fx_rates_halt,
    test_duplicate_identical_fx_ok,
    test_missing_facts_fails_not_zero,
    test_must_be_rejects_non_number,
    test_epsilon_absorbs_fx_drift,
    %% --- Weighted-edge extension (ClawDog) ---
    test_unweighted_edges_default_to_one,
    test_contra_account_negative_weight,
    test_mixed_weighted_and_unweighted,
    test_public_kit_ppe_pattern,
    %% --- Evidence/provenance extension (ClawDog) ---
    test_evidence_invariant_sum_equals_total,
    test_evidence_records_identity_fx,
    test_evidence_records_contra_weight,
    test_evidence_fails_on_no_facts,
    format("~n=================================~n"),
    format("ALL CONSOLIDATION TESTS PASSED ✓~n"),
    format("=================================~n").

reset_state :-
    retractall(sbrm_consolidation:sbrm_edge(_,_,_,_)),
    retractall(sbrm_consolidation:sbrm_edge(_,_,_,_,_)),
    retractall(sbrm_consolidation:sbrm_fact(_,_,_,_,_,_)),
    retractall(sbrm_consolidation:fx_rate(_,_,_,_)).

ok(Name) :- format("~w: PASS~n", [Name]).
fail_msg(Name, Detail) :- format("~w: FAIL (~w)~n", [Name, Detail]), fail.

% ============================================================================
%  Baseline tests (must still pass — proves the weight extension is a
%  zero-cost addition to unweighted graphs)
% ============================================================================

test_basic_consolidation :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','sbr:Equity','sbr:Cash')),
    assertz(sbrm_consolidation:sbrm_edge(e2,'sbrm:isRollupOf','sbr:Equity','sbr:Inventory')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:Cash',2000.0,'USD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:Inventory',300.0,'EUR','Leaf')),
    assertz(sbrm_consolidation:fx_rate('USD','AUD','FY25',1.55)),
    assertz(sbrm_consolidation:fx_rate('EUR','AUD','FY25',1.65)),
    sbrm_consolidation:calculate_consolidated_node('e','FY25','AUD','sbr:Equity',Total),
    Expected is 2000.0*1.55 + 300.0*1.65,
    ( abs(Total - Expected) < 1.0e-9
    -> ok(test_basic_consolidation)
    ;  fail_msg(test_basic_consolidation, got(Total, Expected))
    ).

test_balanced_rollforward :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_fact('e','FY24','sbr:OpeningEquity',1000.0,'USD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:NetProfit',500.0,'EUR','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:DividendsPaid',100.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:ClosingEquity',2225.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:fx_rate('USD','AUD','FY24',1.50)),
    assertz(sbrm_consolidation:fx_rate('EUR','AUD','FY25',1.65)),
    ( sbrm_consolidation:verify_temporal_equity('e','FY24','FY25','FY25','AUD')
    -> ok(test_balanced_rollforward)
    ;  fail_msg(test_balanced_rollforward, did_not_balance)
    ).

test_unbalanced_rollforward_rejected :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_fact('e','FY24','sbr:OpeningEquity',1000.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:NetProfit',500.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:DividendsPaid',100.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:ClosingEquity',9999.0,'AUD','Leaf')),
    ( sbrm_consolidation:verify_temporal_equity('e','FY24','FY25','FY25','AUD')
    -> fail_msg(test_unbalanced_rollforward_rejected, should_have_failed)
    ;  ok(test_unbalanced_rollforward_rejected)
    ).

test_cycle_safety :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','A','B')),
    assertz(sbrm_consolidation:sbrm_edge(e2,'sbrm:isRollupOf','B','C')),
    assertz(sbrm_consolidation:sbrm_edge(e3,'sbrm:isRollupOf','C','A')),
    assertz(sbrm_consolidation:sbrm_edge(e4,'sbrm:isRollupOf','C','D')),
    assertz(sbrm_consolidation:sbrm_fact('e','P','D',42.0,'AUD','Leaf')),
    sbrm_consolidation:calculate_consolidated_node('e','P','AUD','A',Total),
    ( Total =:= 42.0 -> ok(test_cycle_safety)
    ; fail_msg(test_cycle_safety, total(Total))
    ).

test_target_concept_is_leaf :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_fact('e','P','sbr:Cash',77.0,'USD','Leaf')),
    assertz(sbrm_consolidation:fx_rate('USD','AUD','P',2.0)),
    sbrm_consolidation:calculate_consolidated_node('e','P','AUD','sbr:Cash',Total),
    ( Total =:= 154.0 -> ok(test_target_concept_is_leaf)
    ; fail_msg(test_target_concept_is_leaf, total(Total))
    ).

test_conflicting_fx_rates_halt :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_fact('e','P','sbr:Cash',100.0,'USD','Leaf')),
    assertz(sbrm_consolidation:fx_rate('USD','AUD','P',1.50)),
    assertz(sbrm_consolidation:fx_rate('USD','AUD','P',1.55)),
    ( sbrm_consolidation:calculate_consolidated_node('e','P','AUD','sbr:Cash',_)
    -> fail_msg(test_conflicting_fx_rates_halt, should_refuse)
    ;  ok(test_conflicting_fx_rates_halt)
    ).

test_duplicate_identical_fx_ok :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_fact('e','P','sbr:Cash',100.0,'USD','Leaf')),
    assertz(sbrm_consolidation:fx_rate('USD','AUD','P',1.50)),
    assertz(sbrm_consolidation:fx_rate('USD','AUD','P',1.50)),
    sbrm_consolidation:calculate_consolidated_node('e','P','AUD','sbr:Cash',Total),
    ( Total =:= 150.0 -> ok(test_duplicate_identical_fx_ok)
    ; fail_msg(test_duplicate_identical_fx_ok, total(Total))
    ).

test_missing_facts_fails_not_zero :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','sbr:Equity','sbr:Cash')),
    ( sbrm_consolidation:calculate_consolidated_node('e','P','AUD','sbr:Equity',T)
    -> fail_msg(test_missing_facts_fails_not_zero, returned(T))
    ;  ok(test_missing_facts_fails_not_zero)
    ).

test_must_be_rejects_non_number :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_fact('e','P','sbr:Cash','not_a_number','AUD','Leaf')),
    ( catch(
        sbrm_consolidation:calculate_consolidated_node('e','P','AUD','sbr:Cash',_),
        error(type_error(number,_),_),
        true)
    -> ok(test_must_be_rejects_non_number)
    ;  fail_msg(test_must_be_rejects_non_number, no_type_error)
    ).

test_epsilon_absorbs_fx_drift :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_fact('e','FY24','sbr:OpeningEquity',333.3333333333,'USD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:NetProfit',0.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:DividendsPaid',0.0,'AUD','Leaf')),
    Closing is 333.3333333333 * 3.0,
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','sbr:ClosingEquity',Closing,'AUD','Leaf')),
    assertz(sbrm_consolidation:fx_rate('USD','AUD','FY24',3.0)),
    ( sbrm_consolidation:verify_temporal_equity('e','FY24','FY25','FY25','AUD')
    -> ok(test_epsilon_absorbs_fx_drift)
    ;  fail_msg(test_epsilon_absorbs_fx_drift, drift_not_absorbed)
    ).

% ============================================================================
%  Weighted-edge extension tests
% ============================================================================

test_unweighted_edges_default_to_one :-
    %% Mixing legacy 4-arity edges in a graph that has no 5-arity edges
    %% should produce identical results to "every weight = 1.0".
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','top','a')),
    assertz(sbrm_consolidation:sbrm_edge(e2,'sbrm:isRollupOf','top','b')),
    assertz(sbrm_consolidation:sbrm_fact('e','P','a',10.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','P','b',7.0,'AUD','Leaf')),
    sbrm_consolidation:calculate_consolidated_node('e','P','AUD','top',Total),
    ( Total =:= 17.0 -> ok(test_unweighted_edges_default_to_one)
    ; fail_msg(test_unweighted_edges_default_to_one, total(Total))
    ).

test_contra_account_negative_weight :-
    %% PPE = Gross_PPE + (-1.0) * AccumulatedDepreciation
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','PPE','GrossPPE',1.0)),
    assertz(sbrm_consolidation:sbrm_edge(e2,'sbrm:isRollupOf','PPE','AccDep',-1.0)),
    assertz(sbrm_consolidation:sbrm_fact('e','P','GrossPPE',1000.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','P','AccDep',300.0,'AUD','Leaf')),
    sbrm_consolidation:calculate_consolidated_node('e','P','AUD','PPE',Total),
    ( Total =:= 700.0 -> ok(test_contra_account_negative_weight)
    ; fail_msg(test_contra_account_negative_weight, total(Total))
    ).

test_mixed_weighted_and_unweighted :-
    %% Some edges weighted, some legacy 4-arity. Both should compose.
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','top','plus')),       % unweighted -> 1.0
    assertz(sbrm_consolidation:sbrm_edge(e2,'sbrm:isRollupOf','top','minus',-1.0)), % explicit -1
    assertz(sbrm_consolidation:sbrm_fact('e','P','plus',100.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','P','minus',30.0,'AUD','Leaf')),
    sbrm_consolidation:calculate_consolidated_node('e','P','AUD','top',Total),
    ( Total =:= 70.0 -> ok(test_mixed_weighted_and_unweighted)
    ; fail_msg(test_mixed_weighted_and_unweighted, total(Total))
    ).

test_public_kit_ppe_pattern :-
    %% Direct port of the public Kit (engine/rules.pl) PPE+contra pattern,
    %% with currency added. Proves the consolidation engine subsumes
    %% rules.pl's calculation_arc semantics.
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf',
        'mini_PropertyPlantAndEquipment','mini_PropertyPlantAndEquipmentGross',1.0)),
    assertz(sbrm_consolidation:sbrm_edge(e2,'sbrm:isRollupOf',
        'mini_PropertyPlantAndEquipmentGross','mini_Land',1.0)),
    assertz(sbrm_consolidation:sbrm_edge(e3,'sbrm:isRollupOf',
        'mini_PropertyPlantAndEquipmentGross','mini_Buildings',1.0)),
    assertz(sbrm_consolidation:sbrm_edge(e4,'sbrm:isRollupOf',
        'mini_PropertyPlantAndEquipmentGross','mini_Equipment',1.0)),
    assertz(sbrm_consolidation:sbrm_edge(e5,'sbrm:isRollupOf',
        'mini_PropertyPlantAndEquipment','mini_AccumulatedDepreciation',-1.0)),
    assertz(sbrm_consolidation:sbrm_fact('e','P','mini_Land',500.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','P','mini_Buildings',1200.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','P','mini_Equipment',300.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','P','mini_AccumulatedDepreciation',
                                         400.0,'AUD','Leaf')),
    sbrm_consolidation:calculate_consolidated_node('e','P','AUD',
        'mini_PropertyPlantAndEquipment', Total),
    %% 500 + 1200 + 300 - 400 = 1600
    ( Total =:= 1600.0 -> ok(test_public_kit_ppe_pattern)
    ; fail_msg(test_public_kit_ppe_pattern, total(Total))
    ).

% ============================================================================
%  Evidence/provenance tests
% ============================================================================

test_evidence_invariant_sum_equals_total :-
    %% Build a non-trivial mixed-currency, mixed-weight graph and assert
    %% that the sum of evidence-row contributions equals the headline total
    %% returned by the same call.
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','top','cash',1.0)),
    assertz(sbrm_consolidation:sbrm_edge(e2,'sbrm:isRollupOf','top','recv',1.0)),
    assertz(sbrm_consolidation:sbrm_edge(e3,'sbrm:isRollupOf','top','depr',-1.0)),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','cash',1000.0,'USD','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','recv',500.0,'EUR','Leaf')),
    assertz(sbrm_consolidation:sbrm_fact('e','FY25','depr',200.0,'AUD','Leaf')),
    assertz(sbrm_consolidation:fx_rate('USD','AUD','FY25',1.55)),
    assertz(sbrm_consolidation:fx_rate('EUR','AUD','FY25',1.65)),
    sbrm_consolidation:consolidation_evidence('e','FY25','AUD','top',
                                              Total, Evidence),
    findall(C, member(evidence(_,_,_,_,_,C), Evidence), Contribs),
    sum_list(Contribs, Sum),
    Expected is 1000.0*1.55 + 500.0*1.65 - 200.0,
    ( abs(Total - Expected) < 1.0e-9,
      abs(Sum - Total) < 1.0e-9
    -> format("test_evidence_invariant_sum_equals_total: PASS (total=~4f, ~w rows)~n",
              [Total, Evidence])
    ;  fail_msg(test_evidence_invariant_sum_equals_total,
                got(total=Total, sum=Sum, expected=Expected))
    ).

test_evidence_records_identity_fx :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','top','x',1.0)),
    assertz(sbrm_consolidation:sbrm_fact('e','P','x',50.0,'AUD','Leaf')),
    sbrm_consolidation:consolidation_evidence('e','P','AUD','top',
                                              _Total, Evidence),
    %% Identity FX must explicitly record FxRate=1.0 in the evidence row
    ( Evidence = [evidence('x','AUD',50.0,1.0,1.0,50.0)]
    -> ok(test_evidence_records_identity_fx)
    ;  fail_msg(test_evidence_records_identity_fx, got(Evidence))
    ).

test_evidence_records_contra_weight :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','top','x',-1.0)),
    assertz(sbrm_consolidation:sbrm_fact('e','P','x',75.0,'AUD','Leaf')),
    sbrm_consolidation:consolidation_evidence('e','P','AUD','top',
                                              Total, Evidence),
    ( Total =:= -75.0,
      Evidence = [evidence('x','AUD',75.0,-1.0,1.0,-75.0)]
    -> ok(test_evidence_records_contra_weight)
    ;  fail_msg(test_evidence_records_contra_weight,
                got(total=Total, evidence=Evidence))
    ).

test_evidence_fails_on_no_facts :-
    reset_state,
    assertz(sbrm_consolidation:sbrm_edge(e1,'sbrm:isRollupOf','top','x',1.0)),
    %% no facts asserted
    ( sbrm_consolidation:consolidation_evidence('e','P','AUD','top',_,_)
    -> fail_msg(test_evidence_fails_on_no_facts, should_have_failed)
    ;  ok(test_evidence_fails_on_no_facts)
    ).
