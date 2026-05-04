%% Test suite for engine/adjustments.pl (Sprint A2)
%%
%% Run from repo root:    swipl -g run_tests -t halt engine/tests/test_adjustments.pl
%% Or from this directory: swipl -g run_tests -t halt test_adjustments.pl
%%
%% Covers:
%%   * Balance proof — balanced journal returns ok.
%%   * Balance proof — unbalanced journal returns structured failure.
%%   * Balance proof — missing-postings returns structured failure.
%%   * Balance proof — epsilon tolerance absorbs sub-cent drift.
%%   * Composition — base + adjustment composes correctly.
%%   * Composition — base-only (no adjustments) returns base unchanged.
%%   * Composition — adjustments-only (no base) returns adjustment sum.
%%   * Composition — neither base nor adjustments → FAIL (Standing Rule #3).
%%   * Composition — multiple adjustments aggregate correctly.
%%   * Composition — base sbrm_fact/6 untouched after composed_value/4
%%     query (audit-trail preservation discipline).
%%   * Multi-AdjId isolation — balance proof per AdjId, not global.
%%
%% Brain canon: GLOBAL_NOTES/CLAWDOG/108_LAST_MILE_ARCHITECTURE.md § 4.2
%% Author    : ClawDog ∮

:- use_module('../adjustments', [
       audit_adjustment_balance/4,
       composed_value/4,
       adjustment_epsilon/1
   ]).

% Helper: clear adjustment + base facts for the test entity.
clear_adj_facts(Entity) :-
    retractall(sbrm_consolidation:sbrm_adjustment(Entity, _, _, _, _, _)),
    retractall(sbrm_consolidation:sbrm_fact(Entity, _, _, _, _, _)).

% Helper: assert a balanced two-line journal.
%   debit  Concept_D  Amount
%   credit Concept_C  Amount
balanced_two_line(Entity, Period, AdjId, ConceptD, ConceptC, Amount) :-
    NegAmount is -Amount,
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, Period, AdjId,
                                               ConceptD, Amount,    debit)),
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, Period, AdjId,
                                               ConceptC, NegAmount, credit)).

run_tests :-
    test_balanced_journal_returns_ok,
    test_unbalanced_journal_returns_structured_failure,
    test_missing_postings_returns_structured_failure,
    test_epsilon_tolerance_absorbs_subcent_drift,
    test_compose_base_plus_adjustment,
    test_compose_base_only_returns_base_unchanged,
    test_compose_adjustments_only_returns_sum,
    test_compose_no_base_no_adjustments_fails,
    test_compose_multiple_adjustments_aggregate,
    test_base_fact_untouched_after_compose,
    test_multi_adj_id_isolation,
    test_audit_adjustment_balance_requires_atom_adj_id,
    format("~n=================================~n", []),
    format("ALL ADJUSTMENT TESTS PASSED ✓~n", []),
    format("=================================~n", []).

% =============================================================================
%  Balance proof tests
% =============================================================================

test_balanced_journal_returns_ok :-
    Entity = test_balanced_ok,
    clear_adj_facts(Entity),
    %% 1250 debit DepAndAmort + 1250 credit AccumTaxDep = 0
    balanced_two_line(Entity, 'FY25', adj_001,
                      'mini_DepreciationAndAmortization',
                      'audit_AccumulatedTaxDepreciation',
                      1250.0),
    audit_adjustment_balance(Entity, 'FY25', adj_001, Result),
    (   Result == ok
    ->  true
    ;   format("FAIL test_balanced_journal_returns_ok: got ~w~n", [Result]),
        fail
    ),
    clear_adj_facts(Entity),
    format("✓ test_balanced_journal_returns_ok~n").

test_unbalanced_journal_returns_structured_failure :-
    Entity = test_unbalanced,
    clear_adj_facts(Entity),
    %% 1250 debit + (-1000) credit = 250 (unbalanced; > 0.01 epsilon).
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_002,
                                               'mini_DepreciationAndAmortization',
                                               1250.0, debit)),
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_002,
                                               'audit_AccumulatedTaxDepreciation',
                                               -1000.0, credit)),
    audit_adjustment_balance(Entity, 'FY25', adj_002, Result),
    (   Result = fail(point(adj), unbalanced, Details)
    ->  memberchk(adj_id-adj_002, Details),
        memberchk(sum-Sum, Details),
        memberchk(eps-_Eps, Details),
        Sum =:= 250.0
    ;   format("FAIL test_unbalanced: got ~w~n", [Result]),
        fail
    ),
    clear_adj_facts(Entity),
    format("✓ test_unbalanced_journal_returns_structured_failure~n").

test_missing_postings_returns_structured_failure :-
    Entity = test_missing_postings,
    clear_adj_facts(Entity),
    %% No postings injected for adj_999 — should fail with missing_postings.
    audit_adjustment_balance(Entity, 'FY25', adj_999, Result),
    (   Result = fail(point(adj), missing_postings, [adj_id-adj_999])
    ->  true
    ;   format("FAIL test_missing_postings: got ~w~n", [Result]),
        fail
    ),
    format("✓ test_missing_postings_returns_structured_failure~n").

test_epsilon_tolerance_absorbs_subcent_drift :-
    Entity = test_epsilon,
    clear_adj_facts(Entity),
    %% 1250.001 - 1250.000 = 0.001 (sub-cent; should pass).
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_003,
                                               'mini_DepreciationAndAmortization',
                                               1250.001, debit)),
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_003,
                                               'audit_AccumulatedTaxDepreciation',
                                               -1250.000, credit)),
    audit_adjustment_balance(Entity, 'FY25', adj_003, Result),
    (   Result == ok
    ->  true
    ;   format("FAIL test_epsilon: sub-cent drift should be tolerated; got ~w~n",
               [Result]),
        fail
    ),
    clear_adj_facts(Entity),
    format("✓ test_epsilon_tolerance_absorbs_subcent_drift~n").

% =============================================================================
%  Composition tests
% =============================================================================

test_compose_base_plus_adjustment :-
    Entity = test_compose_base_plus_adj,
    clear_adj_facts(Entity),
    %% Base: depreciation 5000.
    assertz(sbrm_consolidation:sbrm_fact(Entity, 'FY25',
                                         'mini_DepreciationAndAmortization',
                                         5000.0, 'AUD', 'Leaf')),
    %% Adjustment: +1250 debit (signed +1250).
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_010,
                                               'mini_DepreciationAndAmortization',
                                               1250.0, debit)),
    composed_value(Entity, 'FY25', 'mini_DepreciationAndAmortization', Final),
    %% 5000 + 1250 = 6250.
    (   abs(Final - 6250.0) < 0.001
    ->  true
    ;   format("FAIL test_compose_base_plus_adj: got ~w~n", [Final]),
        fail
    ),
    clear_adj_facts(Entity),
    format("✓ test_compose_base_plus_adjustment~n").

test_compose_base_only_returns_base_unchanged :-
    Entity = test_compose_base_only,
    clear_adj_facts(Entity),
    assertz(sbrm_consolidation:sbrm_fact(Entity, 'FY25', 'mini_Sales',
                                         10000.0, 'AUD', 'Leaf')),
    composed_value(Entity, 'FY25', 'mini_Sales', Final),
    (   abs(Final - 10000.0) < 0.001
    ->  true
    ;   format("FAIL test_compose_base_only: got ~w~n", [Final]),
        fail
    ),
    clear_adj_facts(Entity),
    format("✓ test_compose_base_only_returns_base_unchanged~n").

test_compose_adjustments_only_returns_sum :-
    %% No base sbrm_fact for this concept; only an adjustment.
    %% Documented behaviour (108 § 4.2.3 case 3): returns the adjustment sum.
    Entity = test_compose_adj_only,
    clear_adj_facts(Entity),
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_020,
                                               'audit_Div7ALoan',
                                               5000.0, debit)),
    composed_value(Entity, 'FY25', 'audit_Div7ALoan', Final),
    (   abs(Final - 5000.0) < 0.001
    ->  true
    ;   format("FAIL test_compose_adj_only: got ~w~n", [Final]),
        fail
    ),
    clear_adj_facts(Entity),
    format("✓ test_compose_adjustments_only_returns_sum~n").

test_compose_no_base_no_adjustments_fails :-
    %% Standing Rule #3: composed_value/4 fails (rather than returns 0)
    %% when neither base nor adjustments exist for the concept.
    Entity = test_compose_nothing,
    clear_adj_facts(Entity),
    \+ composed_value(Entity, 'FY25', 'mini_NonExistent', _Final),
    format("✓ test_compose_no_base_no_adjustments_fails (correctly failed)~n").

test_compose_multiple_adjustments_aggregate :-
    %% Base 1000; two adjustments +200 and -50; expected 1150.
    Entity = test_compose_multi,
    clear_adj_facts(Entity),
    assertz(sbrm_consolidation:sbrm_fact(Entity, 'FY25', 'mini_OperatingExpenses',
                                         1000.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_030,
                                               'mini_OperatingExpenses',
                                               200.0, debit)),
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_031,
                                               'mini_OperatingExpenses',
                                               -50.0, credit)),
    composed_value(Entity, 'FY25', 'mini_OperatingExpenses', Final),
    (   abs(Final - 1150.0) < 0.001
    ->  true
    ;   format("FAIL test_compose_multi_adj: got ~w~n", [Final]),
        fail
    ),
    clear_adj_facts(Entity),
    format("✓ test_compose_multiple_adjustments_aggregate~n").

test_base_fact_untouched_after_compose :-
    %% Audit-trail discipline: composed_value/4 is read-only over base.
    %% After querying composed_value, sbrm_fact/6 must still return
    %% the original base value, NOT the composed final.
    Entity = test_base_untouched,
    clear_adj_facts(Entity),
    assertz(sbrm_consolidation:sbrm_fact(Entity, 'FY25', 'mini_Sales',
                                         10000.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_040,
                                               'mini_Sales',
                                               -1000.0, credit)),
    %% Query composed (10000 - 1000 = 9000).
    composed_value(Entity, 'FY25', 'mini_Sales', Composed),
    abs(Composed - 9000.0) < 0.001,
    %% Verify base is still 10000.
    sbrm_consolidation:sbrm_fact(Entity, 'FY25', 'mini_Sales', BaseAfter, _, _),
    (   abs(BaseAfter - 10000.0) < 0.001
    ->  true
    ;   format("FAIL test_base_untouched: base mutated to ~w~n", [BaseAfter]),
        fail
    ),
    clear_adj_facts(Entity),
    format("✓ test_base_fact_untouched_after_compose~n").

test_multi_adj_id_isolation :-
    %% Two adjustments under different AdjIds; balance proof must see
    %% each independently. adj_050 is balanced; adj_051 is not.
    Entity = test_multi_adj_id,
    clear_adj_facts(Entity),
    balanced_two_line(Entity, 'FY25', adj_050,
                      'mini_DepreciationAndAmortization',
                      'audit_AccumulatedTaxDepreciation',
                      500.0),
    %% adj_051 deliberately unbalanced.
    assertz(sbrm_consolidation:sbrm_adjustment(Entity, 'FY25', adj_051,
                                               'mini_OperatingExpenses',
                                               300.0, debit)),
    audit_adjustment_balance(Entity, 'FY25', adj_050, R1),
    audit_adjustment_balance(Entity, 'FY25', adj_051, R2),
    R1 == ok,
    (   R2 = fail(point(adj), unbalanced, _)
    ->  true
    ;   format("FAIL multi_adj_id: adj_051 should be unbalanced; got ~w~n", [R2]),
        fail
    ),
    clear_adj_facts(Entity),
    format("✓ test_multi_adj_id_isolation~n").

test_audit_adjustment_balance_requires_atom_adj_id :-
    %% must_be(atom, AdjId) at the entry point. Calling with a non-atom
    %% should throw a type-error, not silently succeed.
    Entity = test_type_check,
    catch(
        ( audit_adjustment_balance(Entity, 'FY25', "string_not_atom", _R),
          format("FAIL: should have thrown type_error~n"),
          fail ),
        error(type_error(atom, _), _),
        true
    ),
    format("✓ test_audit_adjustment_balance_requires_atom_adj_id~n").
