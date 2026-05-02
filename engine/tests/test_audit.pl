%% Test suite for engine/audit.pl
%%
%% Run from repo root:    swipl -g run_tests -t halt engine/tests/test_audit.pl
%% Or from this directory: swipl -g run_tests -t halt test_audit.pl
%%
%% Covers:
%%   * Each of the five lifted audit points (1, 2, 3, 4, 6) on a
%%     deliberately-balanced fixture \u2014 should pass cleanly with [].
%%   * Each point's structured failure when the corresponding invariant
%%     is violated.
%%   * The fail-loud guard for missing facts (Standing Rule #3) on each
%%     point.
%%   * The legacy semantic that NonoperatingIncomeExpense missing \u2192 0.
%%   * The aggregator audit_all/3 collecting multiple failures in order.
%%
%% Brain canon: GLOBAL_NOTES/CLAWDOG/107_CONSOLIDATION_LOGIC.md
%% Author    : ClawDog \u222e

:- use_module('../audit', [
       audit_all/3,
       audit_balance_sheet_tensegrity/3,
       audit_asset_rollup/3,
       audit_liability_equity_rollup/3,
       audit_pl_net_income/3,
       audit_equity_rollforward/3
   ]).

% Helper: clear ALL audit-relevant facts for a given test entity.
clear_facts(Entity) :-
    retractall(sbrm_consolidation:sbrm_fact(Entity, _, _, _, _, _)).

% Helper: assert a balanced fixture covering all five audit points.
balanced_fixture(Entity, Period) :-
    clear_facts(Entity),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Assets',                   1000.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_CurrentAssets',             400.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_NoncurrentAssets',          600.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_LiabilitiesAndEquity',     1000.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Liabilities',               300.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Equity',                    700.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Sales',                     500.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_CostOfGoodsSold',           200.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_OperatingExpenses',         100.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_NetIncomeLoss',             200.0, 'AUD', 'Leaf')),
    %% Equity roll-forward: 600 opening + 0 cap_inj + 200 NI - 100 divs = 700 closing
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'audit_OpeningEquity',            600.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'audit_CapitalInjections',          0.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'audit_DividendsPaid',            100.0, 'AUD', 'Leaf')).

run_tests :-
    test_clean_balanced_fixture_passes,
    test_point1_tensegrity_violation_caught,
    test_point2_asset_rollup_violation_caught,
    test_point3_liab_equity_rollup_violation_caught,
    test_point4_pl_net_income_violation_caught,
    test_point4_nonop_missing_treated_as_zero,
    test_point6_equity_rollforward_violation_caught,
    test_point1_missing_fact_fails_loud,
    test_point4_missing_fact_fails_loud,
    test_audit_all_collects_multiple_failures_in_order,
    test_epsilon_tolerance_absorbs_subcent_drift,
    %% S5b: period-comparative regression tests \u2014 multi-period in one DB.
    test_two_periods_coexist_without_leakage,
    test_audit_distinguishes_period_atoms,
    format("~n=================================~n", []),
    format("ALL AUDIT TESTS PASSED \u2713~n", []),
    format("=================================~n", []).

%% S5b helper: assert a balanced fixture with custom totals at a chosen
%% (Entity, Period). The closing equity is implied by the rollforward:
%% Closing = Opening + CapInj + NI - Divs.
balanced_fixture_for(Entity, Period, Opening, CapInj, NI, Divs) :-
    Closing is Opening + CapInj + NI - Divs,
    %% Make the BS work: Assets = LiabEq, both = Closing + Liab. We pick
    %% Liabilities to match Closing (i.e. Liab=Equity for clarity), but
    %% any number balances as long as Assets = Liab + Equity.
    Liab = 100.0,
    Assets is Liab + Closing,
    LiabEq = Assets,
    %% Asset rollup: Current + NonCurrent = Assets. Pick a clean split.
    Current is Assets * 0.4,
    NonCurrent is Assets - Current,
    %% P&L: Sales - COGS - OpEx + NonOp = NI. We absorb NI into Sales
    %% by picking COGS=OpEx=NonOp=0.
    Sales = NI,
    retractall(sbrm_consolidation:sbrm_fact(Entity, Period, _, _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Assets',                  Assets,    'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_CurrentAssets',           Current,   'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_NoncurrentAssets',        NonCurrent,'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_LiabilitiesAndEquity',    LiabEq,    'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Liabilities',             Liab,      'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Equity',                  Closing,   'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Sales',                   Sales,     'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_CostOfGoodsSold',         0.0,       'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_OperatingExpenses',       0.0,       'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_NetIncomeLoss',           NI,        'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'audit_OpeningEquity',          Opening,   'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'audit_CapitalInjections',      CapInj,    'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'audit_DividendsPaid',          Divs,      'AUD', 'Leaf')).

%% S5b test 1: same entity, two distinct period atoms, both audit clean
%% with their own independent (but separately-balanced) fact sets in the
%% shared multifile predicate. This is what the pipeline.py shim relies on
%% to audit FY25 and FY24 in one process without cross-period leakage.
test_two_periods_coexist_without_leakage :-
    %% FY24: opening 0, NI 1000, divs 100 \u2192 closing 900.
    balanced_fixture_for(acme, 'FY24', 0.0,   0.0, 1000.0, 100.0),
    %% FY25: opening 900 (carrying forward), NI 2000, divs 200 \u2192 closing 2700.
    balanced_fixture_for(acme, 'FY25', 900.0, 0.0, 2000.0, 200.0),
    audit_all(acme, 'FY24', F24),
    audit_all(acme, 'FY25', F25),
    (   F24 == [], F25 == []
    ->  format("test_two_periods_coexist_without_leakage: PASS~n", [])
    ;   format("test_two_periods_coexist_without_leakage: FAIL F24=~w F25=~w~n",
               [F24, F25]), fail).

%% S5b test 2: when the FY25 net income is corrupted but FY24 is clean,
%% audit_all on the FY25 period reports the failure and audit_all on the
%% FY24 period reports clean. Period atoms are first-class dimensions
%% (Standing Rule #6); they don't bleed across periods.
test_audit_distinguishes_period_atoms :-
    balanced_fixture_for(beta, 'FY24', 0.0,   0.0, 500.0, 0.0),
    balanced_fixture_for(beta, 'FY25', 500.0, 0.0, 700.0, 0.0),
    %% Corrupt FY25 NetIncomeLoss only.
    retractall(sbrm_consolidation:sbrm_fact(beta, 'FY25', 'mini_NetIncomeLoss', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(beta, 'FY25', 'mini_NetIncomeLoss', 999.0, 'AUD', 'Leaf')),
    audit_all(beta, 'FY24', F24),
    audit_all(beta, 'FY25', F25),
    %% FY24 must still be clean; FY25 must report point 4 and point 6.
    (   F24 == [],
        F25 = [fail(point(4), _, _), fail(point(6), _, _)]
    ->  format("test_audit_distinguishes_period_atoms: PASS~n", [])
    ;   format("test_audit_distinguishes_period_atoms: FAIL F24=~w F25=~w~n",
               [F24, F25]), fail).

% -----------------------------------------------------------------------------

test_clean_balanced_fixture_passes :-
    balanced_fixture(t1, p1),
    audit_all(t1, p1, Failures),
    (   Failures == []
    ->  format("test_clean_balanced_fixture_passes: PASS~n", [])
    ;   format("test_clean_balanced_fixture_passes: FAIL ~w~n", [Failures]), fail).

test_point1_tensegrity_violation_caught :-
    balanced_fixture(t2, p1),
    %% Break the BS identity by mutating Assets without touching L&E.
    retractall(sbrm_consolidation:sbrm_fact(t2, p1, 'mini_Assets', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(t2, p1, 'mini_Assets', 1500.0, 'AUD', 'Leaf')),
    %% Asset rollup must also be made consistent with the new Assets so we
    %% only break point 1, not point 2 too. We keep CurrentAssets+Noncurrent
    %% summing to 1500 by bumping NoncurrentAssets.
    retractall(sbrm_consolidation:sbrm_fact(t2, p1, 'mini_NoncurrentAssets', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(t2, p1, 'mini_NoncurrentAssets', 1100.0, 'AUD', 'Leaf')),
    audit_balance_sheet_tensegrity(t2, p1, R),
    (   R = fail(point(1), tensegrity, _)
    ->  format("test_point1_tensegrity_violation_caught: PASS~n", [])
    ;   format("test_point1_tensegrity_violation_caught: FAIL ~w~n", [R]), fail).

test_point2_asset_rollup_violation_caught :-
    balanced_fixture(t3, p1),
    %% Break asset rollup by inflating NoncurrentAssets.
    retractall(sbrm_consolidation:sbrm_fact(t3, p1, 'mini_NoncurrentAssets', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(t3, p1, 'mini_NoncurrentAssets', 999.0, 'AUD', 'Leaf')),
    audit_asset_rollup(t3, p1, R),
    (   R = fail(point(2), asset_rollup, _)
    ->  format("test_point2_asset_rollup_violation_caught: PASS~n", [])
    ;   format("test_point2_asset_rollup_violation_caught: FAIL ~w~n", [R]), fail).

test_point3_liab_equity_rollup_violation_caught :-
    balanced_fixture(t4, p1),
    retractall(sbrm_consolidation:sbrm_fact(t4, p1, 'mini_Equity', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(t4, p1, 'mini_Equity', 999.0, 'AUD', 'Leaf')),
    audit_liability_equity_rollup(t4, p1, R),
    (   R = fail(point(3), liab_equity_rollup, _)
    ->  format("test_point3_liab_equity_rollup_violation_caught: PASS~n", [])
    ;   format("test_point3_liab_equity_rollup_violation_caught: FAIL ~w~n", [R]), fail).

test_point4_pl_net_income_violation_caught :-
    balanced_fixture(t5, p1),
    retractall(sbrm_consolidation:sbrm_fact(t5, p1, 'mini_NetIncomeLoss', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(t5, p1, 'mini_NetIncomeLoss', 999.0, 'AUD', 'Leaf')),
    audit_pl_net_income(t5, p1, R),
    (   R = fail(point(4), pl_net_income, _)
    ->  format("test_point4_pl_net_income_violation_caught: PASS~n", [])
    ;   format("test_point4_pl_net_income_violation_caught: FAIL ~w~n", [R]), fail).

test_point4_nonop_missing_treated_as_zero :-
    %% Build a P&L fixture with NO mini_NonoperatingIncomeExpense fact;
    %% the audit must still pass via the legacy default-to-zero clause.
    Entity = t6, Period = p1,
    clear_facts(Entity),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Sales',             500.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_CostOfGoodsSold',   200.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_OperatingExpenses', 100.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_NetIncomeLoss',     200.0, 'AUD', 'Leaf')),
    audit_pl_net_income(Entity, Period, R),
    (   R == ok
    ->  format("test_point4_nonop_missing_treated_as_zero: PASS~n", [])
    ;   format("test_point4_nonop_missing_treated_as_zero: FAIL ~w~n", [R]), fail).

test_point6_equity_rollforward_violation_caught :-
    balanced_fixture(t7, p1),
    %% Break rollforward: bump dividends without compensating elsewhere.
    retractall(sbrm_consolidation:sbrm_fact(t7, p1, 'audit_DividendsPaid', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(t7, p1, 'audit_DividendsPaid', 50.0, 'AUD', 'Leaf')),
    audit_equity_rollforward(t7, p1, R),
    (   R = fail(point(6), equity_rollforward, _)
    ->  format("test_point6_equity_rollforward_violation_caught: PASS~n", [])
    ;   format("test_point6_equity_rollforward_violation_caught: FAIL ~w~n", [R]), fail).

test_point1_missing_fact_fails_loud :-
    Entity = t8, Period = p1,
    clear_facts(Entity),
    %% No facts at all asserted.
    audit_balance_sheet_tensegrity(Entity, Period, R),
    (   R = fail(point(1), missing_fact, _)
    ->  format("test_point1_missing_fact_fails_loud: PASS~n", [])
    ;   format("test_point1_missing_fact_fails_loud: FAIL ~w~n", [R]), fail).

test_point4_missing_fact_fails_loud :-
    Entity = t9, Period = p1,
    clear_facts(Entity),
    %% Assert SOME P&L facts but omit mini_NetIncomeLoss \u2014 the rule must
    %% fail with missing_fact, NOT pass with default zeros, NOT throw.
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Sales',             500.0, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_CostOfGoodsSold',   200.0, 'AUD', 'Leaf')),
    audit_pl_net_income(Entity, Period, R),
    (   R = fail(point(4), missing_fact, _)
    ->  format("test_point4_missing_fact_fails_loud: PASS~n", [])
    ;   format("test_point4_missing_fact_fails_loud: FAIL ~w~n", [R]), fail).

test_audit_all_collects_multiple_failures_in_order :-
    balanced_fixture(t10, p1),
    %% Break point 1 (tensegrity) AND point 4 (P&L NI). Asset rollup must
    %% stay consistent after the Assets bump so it still passes.
    retractall(sbrm_consolidation:sbrm_fact(t10, p1, 'mini_Assets', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(t10, p1, 'mini_Assets', 1500.0, 'AUD', 'Leaf')),
    retractall(sbrm_consolidation:sbrm_fact(t10, p1, 'mini_NoncurrentAssets', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(t10, p1, 'mini_NoncurrentAssets', 1100.0, 'AUD', 'Leaf')),
    retractall(sbrm_consolidation:sbrm_fact(t10, p1, 'mini_NetIncomeLoss', _, _, _)),
    assertz(sbrm_consolidation:sbrm_fact(t10, p1, 'mini_NetIncomeLoss', 999.0, 'AUD', 'Leaf')),
    audit_all(t10, p1, Failures),
    %% Expect exactly two failures: point 1 and point 4. Plus point 6
    %% which now disagrees because closing equity (700) vs computed
    %% (600 + 0 + 999 - 100 = 1499). So three failures in fact.
    length(Failures, N),
    (   N == 3,
        Failures = [fail(point(1), _, _),
                    fail(point(4), _, _),
                    fail(point(6), _, _)]
    ->  format("test_audit_all_collects_multiple_failures_in_order: PASS (~w failures)~n", [N])
    ;   format("test_audit_all_collects_multiple_failures_in_order: FAIL ~w~n", [Failures]), fail).

test_epsilon_tolerance_absorbs_subcent_drift :-
    Entity = t11, Period = p1,
    clear_facts(Entity),
    %% Assets vs LiabEq differ by 0.005 \u2014 well below the 0.01 epsilon.
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_Assets',             1000.005, 'AUD', 'Leaf')),
    assertz(sbrm_consolidation:sbrm_fact(Entity, Period, 'mini_LiabilitiesAndEquity', 1000.0, 'AUD', 'Leaf')),
    audit_balance_sheet_tensegrity(Entity, Period, R),
    (   R == ok
    ->  format("test_epsilon_tolerance_absorbs_subcent_drift: PASS~n", [])
    ;   format("test_epsilon_tolerance_absorbs_subcent_drift: FAIL ~w~n", [R]), fail).
