%% engine/audit.pl
%% =============================================================================
%% SBRM Pre-flight Audit Engine \u2014 Prolog rules over balance-snapshot facts
%%
%% Lifts the 6-Point Thermodynamic Safeguard's points 1-4 + 6 from Python
%% (pipeline.py::pre_flight_audit) into deterministic Prolog rules. Point 5
%% (cashflow transaction-flow analysis) stays in Python because the current
%% sbrm_fact/6 schema is balance-snapshot-oriented; lifting it requires a
%% separate transaction-fact schema which is out of S3's scope.
%%
%% Standing-rule alignment (LodgeiT/ClawDog Brain):
%%   * Rule #3 (Zero-Hallucination) \u2014 no silent defaults. Each audit rule
%%     has a guard clause: missing facts FAIL the rule with a structured
%%     `missing_fact(...)` term, NOT a default-to-zero pass.
%%   * Rule #6 (Hoffman temporal-dimension discipline) \u2014 Period is a
%%     first-class dimension on every fact lookup.
%%
%% Schema:
%%   * Reuses sbrm_consolidation:sbrm_fact/6 as the single fact-injection
%%     surface. The pipeline.py audit shim asserts facts there, then queries
%%     audit_all/3 here, which reads from the same multifile predicate.
%%   * Reuses sbrm_consolidation:fx_rate/4 for any cross-currency audit
%%     (currently unused at the audit layer because the Python shim feeds
%%     post-consolidation reporting-currency values; the dependency is
%%     declared so a future multi-currency audit can opt in without a
%%     schema change).
%%
%% Brain canon:
%%   GLOBAL_NOTES/CLAWDOG/107_CONSOLIDATION_LOGIC.md (sbrm_fact/6 schema)
%%   memory/2026-05-02-s2-pickup-carryover.md (S3 design notes)
%%
%% Author: ClawDog \u222e
%% =============================================================================

:- module(sbrm_audit,
          [ audit_all/3
          , audit_balance_sheet_tensegrity/3
          , audit_asset_rollup/3
          , audit_liability_equity_rollup/3
          , audit_pl_net_income/3
          , audit_equity_rollforward/3
          , audit_epsilon/1
          ]).

:- use_module(library(error)).
:- use_module(library(lists)).
:- use_module(consolidation, [sbrm_fact/6]).

%% Tolerance for accounting equality. The Python original used 0.01 (one
%% cent) which we preserve verbatim. Tighter than fx_epsilon in the
%% consolidation engine because audit checks are post-consolidation \u2014
%% FX drift has already been absorbed by the consolidator's epsilon.
audit_epsilon(0.01).

% =============================================================================
%  FACT LOOKUP \u2014 fail-loud on missing
% =============================================================================
%
%  fact_value(+Entity, +Period, +Concept, -Value) is semidet.
%
%  Returns the Value of a single sbrm_fact for (Entity, Period, Concept).
%  FAILS if the fact is absent. Multiple facts for the same key fail with
%  a deliberate has-conflict signature (caller wraps as missing_fact for
%  the failure tuple). This is Standing Rule #3 in action: no silent zero.

fact_value(Entity, Period, Concept, Value) :-
    findall(V,
            sbrm_consolidation:sbrm_fact(Entity, Period, Concept, V, _, _),
            Vs),
    Vs = [Value],
    must_be(number, Value).

% =============================================================================
%  POINT 1 \u2014 Balance Sheet Tensegrity Proof
% =============================================================================
%
%  Assets must equal Liabilities + Equity (the foundational accounting
%  identity, tagged "tensegrity proof" in the Python original).

audit_balance_sheet_tensegrity(Entity, Period, ok) :-
    fact_value(Entity, Period, 'mini_Assets', Assets),
    fact_value(Entity, Period, 'mini_LiabilitiesAndEquity', LiabEq),
    audit_epsilon(Eps),
    abs(Assets - LiabEq) =< Eps, !.
audit_balance_sheet_tensegrity(Entity, Period,
        fail(point(1), tensegrity, [assets-Assets, liab_eq-LiabEq])) :-
    fact_value(Entity, Period, 'mini_Assets', Assets),
    fact_value(Entity, Period, 'mini_LiabilitiesAndEquity', LiabEq), !.
audit_balance_sheet_tensegrity(Entity, Period,
        fail(point(1), missing_fact, [entity-Entity, period-Period])).

% =============================================================================
%  POINT 2 \u2014 Asset Rollup Integrity
% =============================================================================
%
%  Assets must equal CurrentAssets + NoncurrentAssets.

audit_asset_rollup(Entity, Period, ok) :-
    fact_value(Entity, Period, 'mini_Assets', Assets),
    fact_value(Entity, Period, 'mini_CurrentAssets', Current),
    fact_value(Entity, Period, 'mini_NoncurrentAssets', NonCurrent),
    audit_epsilon(Eps),
    abs(Assets - (Current + NonCurrent)) =< Eps, !.
audit_asset_rollup(Entity, Period,
        fail(point(2), asset_rollup,
             [assets-Assets, current-Current, noncurrent-NonCurrent])) :-
    fact_value(Entity, Period, 'mini_Assets', Assets),
    fact_value(Entity, Period, 'mini_CurrentAssets', Current),
    fact_value(Entity, Period, 'mini_NoncurrentAssets', NonCurrent), !.
audit_asset_rollup(Entity, Period,
        fail(point(2), missing_fact, [entity-Entity, period-Period])).

% =============================================================================
%  POINT 3 \u2014 Liability & Equity Rollup Integrity
% =============================================================================
%
%  LiabilitiesAndEquity must equal Liabilities + Equity.

audit_liability_equity_rollup(Entity, Period, ok) :-
    fact_value(Entity, Period, 'mini_LiabilitiesAndEquity', LiabEq),
    fact_value(Entity, Period, 'mini_Liabilities', Liab),
    fact_value(Entity, Period, 'mini_Equity', Equity),
    audit_epsilon(Eps),
    abs(LiabEq - (Liab + Equity)) =< Eps, !.
audit_liability_equity_rollup(Entity, Period,
        fail(point(3), liab_equity_rollup,
             [liab_eq-LiabEq, liab-Liab, equity-Equity])) :-
    fact_value(Entity, Period, 'mini_LiabilitiesAndEquity', LiabEq),
    fact_value(Entity, Period, 'mini_Liabilities', Liab),
    fact_value(Entity, Period, 'mini_Equity', Equity), !.
audit_liability_equity_rollup(Entity, Period,
        fail(point(3), missing_fact, [entity-Entity, period-Period])).

% =============================================================================
%  POINT 4 \u2014 P&L Net Income Verification
% =============================================================================
%
%  NetIncomeLoss must equal Sales - CostOfGoodsSold - OperatingExpenses
%  + NonoperatingIncomeExpense. NonoperatingIncomeExpense defaults to 0 in
%  the legacy Python flow (`accounts.get(..., 0.0)`); we preserve that
%  semantic here \u2014 if the fact is absent, treat it as 0. This is the ONE
%  place we depart from strict no-silent-zero, and we do it because the
%  Python original treated absence as zero and we are lifting, not
%  redesigning. A future tightening can require an explicit
%  mini_NonoperatingIncomeExpense fact at all times (likely a useful
%  Standing-Rule-#3 cleanup).

audit_pl_net_income(Entity, Period, ok) :-
    fact_value(Entity, Period, 'mini_Sales', Sales),
    fact_value(Entity, Period, 'mini_CostOfGoodsSold', COGS),
    fact_value(Entity, Period, 'mini_OperatingExpenses', OpEx),
    nonop_income_expense(Entity, Period, NonOp),
    fact_value(Entity, Period, 'mini_NetIncomeLoss', StatedNI),
    Calculated is Sales - COGS - OpEx + NonOp,
    audit_epsilon(Eps),
    abs(StatedNI - Calculated) =< Eps, !.
audit_pl_net_income(Entity, Period,
        fail(point(4), pl_net_income,
             [stated-StatedNI, calculated-Calculated,
              sales-Sales, cogs-COGS, opex-OpEx, nonop-NonOp])) :-
    fact_value(Entity, Period, 'mini_Sales', Sales),
    fact_value(Entity, Period, 'mini_CostOfGoodsSold', COGS),
    fact_value(Entity, Period, 'mini_OperatingExpenses', OpEx),
    nonop_income_expense(Entity, Period, NonOp),
    fact_value(Entity, Period, 'mini_NetIncomeLoss', StatedNI),
    Calculated is Sales - COGS - OpEx + NonOp, !.
audit_pl_net_income(Entity, Period,
        fail(point(4), missing_fact, [entity-Entity, period-Period])).

%% Legacy semantic: NonoperatingIncomeExpense missing \u2192 treated as 0.
%% Tracked here as a single named clause so it can be tightened in one
%% place if/when we want to make it strict.
nonop_income_expense(Entity, Period, NonOp) :-
    fact_value(Entity, Period, 'mini_NonoperatingIncomeExpense', NonOp), !.
nonop_income_expense(_Entity, _Period, 0.0).

% =============================================================================
%  POINT 6 \u2014 Equity Roll-forward Verification
% =============================================================================
%
%  Closing Equity must equal:
%      OpeningEquity + CapitalInjections + NetIncome - DividendsPaid
%
%  The Python original derived Opening / CapitalInjections / DividendsPaid
%  by re-parsing the raw CSV. The Prolog audit takes those four scalars as
%  pre-injected facts under audit-specific concept names, so the audit
%  layer is decoupled from CSV-parsing duties. The pipeline.py shim is
%  responsible for the CSV \u2192 facts projection.
%
%  audit_OpeningEquity, audit_CapitalInjections, audit_DividendsPaid are
%  the audit-only rollforward inputs. mini_Equity (closing) and
%  mini_NetIncomeLoss come from the standard mini ontology.

audit_equity_rollforward(Entity, Period, ok) :-
    fact_value(Entity, Period, 'audit_OpeningEquity', Opening),
    fact_value(Entity, Period, 'audit_CapitalInjections', CapInj),
    fact_value(Entity, Period, 'mini_NetIncomeLoss', NI),
    fact_value(Entity, Period, 'audit_DividendsPaid', Divs),
    fact_value(Entity, Period, 'mini_Equity', Closing),
    Calculated is Opening + CapInj + NI - Divs,
    audit_epsilon(Eps),
    abs(Closing - Calculated) =< Eps, !.
audit_equity_rollforward(Entity, Period,
        fail(point(6), equity_rollforward,
             [closing-Closing, calculated-Calculated,
              opening-Opening, cap_inj-CapInj, ni-NI, divs-Divs])) :-
    fact_value(Entity, Period, 'audit_OpeningEquity', Opening),
    fact_value(Entity, Period, 'audit_CapitalInjections', CapInj),
    fact_value(Entity, Period, 'mini_NetIncomeLoss', NI),
    fact_value(Entity, Period, 'audit_DividendsPaid', Divs),
    fact_value(Entity, Period, 'mini_Equity', Closing),
    Calculated is Opening + CapInj + NI - Divs, !.
audit_equity_rollforward(Entity, Period,
        fail(point(6), missing_fact, [entity-Entity, period-Period])).

% =============================================================================
%  AGGREGATOR \u2014 audit_all/3
% =============================================================================
%
%  Runs all five lifted points and returns the list of failure terms.
%  An empty list means CLEAN. Any non-empty list is the structured set of
%  failures, ordered by point number.
%
%  Note: point 5 (cashflow) is intentionally NOT in this list. It stays
%  in Python until the schema supports transaction-flow analysis. The
%  pipeline.py shim runs Python point 5 separately and prepends/appends
%  any failure to the Prolog audit's failure list.

audit_all(Entity, Period, Failures) :-
    audit_balance_sheet_tensegrity(Entity, Period, R1),
    audit_asset_rollup(Entity, Period, R2),
    audit_liability_equity_rollup(Entity, Period, R3),
    audit_pl_net_income(Entity, Period, R4),
    audit_equity_rollforward(Entity, Period, R6),
    include(is_failure, [R1, R2, R3, R4, R6], Failures).

is_failure(fail(_, _, _)).
