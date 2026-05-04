%% engine/adjustments.pl
%% =============================================================================
%% SBRM Adjusting-Journal Engine — Sprint A2 (Phase II realignment)
%%
%% Implements the Brain-canonical sbrm_adjustment/6 schema (locked at
%% Sprint A1, 2026-05-04). See GLOBAL_NOTES/CLAWDOG/108_LAST_MILE_ARCHITECTURE.md
%% § 4.2 for the full schema-locking, ruling history, and rationale.
%%
%% This module exposes two public predicates:
%%
%%   audit_adjustment_balance(+Entity, +Period, +AdjId, -Result)
%%     Proves Σ SignedAmount = 0 across all sbrm_adjustment/6 facts
%%     matching (Entity, Period, AdjId). Polarity is bridge-resolved
%%     into SignedAmount, so a balanced journal sums to zero. Result
%%     mirrors audit_all/3's failure-term shape:
%%
%%       Result = ok
%%              | fail(point(adj), unbalanced, [adj_id-AdjId, sum-S, eps-E])
%%              | fail(point(adj), missing_postings, [adj_id-AdjId])
%%
%%   composed_value(+Entity, +Period, +Concept, -FinalValue)
%%     FinalValue = base + Σ SignedAmount across matching adjustments.
%%     Original sbrm_fact/6 untouched (Standing Rule #3 — no silent
%%     state-rewrite); consumers may query base and composed independently.
%%
%% Standing-rule alignment:
%%   * Rule #3 (Zero-Hallucination) — composed_value/4 fails (rather than
%%     returns 0.0) if no base AND no adjustments match. If base is
%%     present and no adjustments touch the concept, returns base
%%     unmodified. Brand-new predicate; no legacy silent-zero to preserve.
%%   * Rule #6 (Hoffman temporal) — Period is a first-class dimension
%%     on every fact lookup, parallel to engine/audit.pl's discipline.
%%   * Rule #7 (Repository Topology) — this is Kit-side (Egress Interface)
%%     work; Brain canon (108) defines the contract; this implements it.
%%
%% Lesson alignment (named per Standing Rule #10):
%%   * Lesson #36 — atom carries identity (AdjId, Concept, Period bare),
%%     bridge carries interpretation (debit/credit polarity resolved at
%%     YAML load; see engine/yaml_adjustments.py).
%%   * Lesson #37 — this is production-bound logic (the audit and
%%     composition surface that ClawDog will expose to Hub-and-Spoke
%%     LaaS callers); not Wind-Tunnel logic.
%%   * Lesson #25 — diff is small and reviewable. New module + new
%%     multifile decl on consolidation.pl + tests; no existing predicate
%%     touched.
%%
%% Brain canon: GLOBAL_NOTES/CLAWDOG/108_LAST_MILE_ARCHITECTURE.md
%% Author    : ClawDog ∮
%% =============================================================================

:- module(sbrm_adjustments,
          [ audit_adjustment_balance/4
          , composed_value/4
          , adjustment_epsilon/1
          ]).

:- use_module(library(error)).
:- use_module(library(lists)).
:- use_module(library(aggregate)).
:- use_module(consolidation, [sbrm_fact/6, sbrm_adjustment/6]).

%% Tolerance for the per-AdjId balance check. Same magnitude as the
%% audit-engine epsilon (0.01 = one cent) so a journal that sums to
%% sub-cent drift is treated the same way as the 6-Point audit treats
%% sub-cent BS imbalance. See engine/audit.pl::audit_epsilon/1.
adjustment_epsilon(0.01).

% =============================================================================
%  AUDIT — audit_adjustment_balance/4
% =============================================================================
%
%  Proves that all sbrm_adjustment/6 facts under (Entity, Period, AdjId)
%  sum to zero (within epsilon). Because polarity is resolved at the
%  bridge (debit/credit -> signed Amount) the balance check is a single
%  sum: a balanced journal sums to zero by construction.
%
%  Three result shapes:
%    ok                                                 — balanced
%    fail(point(adj), unbalanced, [adj_id-..., sum-..., eps-...])
%                                                       — sum exceeds epsilon
%    fail(point(adj), missing_postings, [adj_id-...])   — no postings exist
%
%  The aggregator on the consumer side (e.g. a future audit_all_with_adjustments/3
%  or the existing audit_all/3 + this predicate composed) decides what to
%  do with the failure term. This module surfaces the verdict; it does
%  not decide whether to abort the pipeline.

audit_adjustment_balance(Entity, Period, AdjId, Result) :-
    must_be(atom, AdjId),
    findall(A,
            sbrm_consolidation:sbrm_adjustment(Entity, Period, AdjId,
                                               _Concept, A, _Direction),
            Amounts),
    (   Amounts == []
    ->  Result = fail(point(adj), missing_postings, [adj_id-AdjId])
    ;   sum_list(Amounts, Sum),
        adjustment_epsilon(Eps),
        (   abs(Sum) =< Eps
        ->  Result = ok
        ;   Result = fail(point(adj), unbalanced,
                          [adj_id-AdjId, sum-Sum, eps-Eps])
        )
    ).

% =============================================================================
%  COMPOSITION — composed_value/4
% =============================================================================
%
%  FinalValue = base + Σ SignedAmount (matching adjustments).
%
%  Read-only over sbrm_fact/6; the base fact is never retracted or
%  rewritten. Consumers who need the original value query sbrm_fact/6
%  directly; consumers who need the post-adjustment value query
%  composed_value/4.
%
%  Three behaviours by case (Standing Rule #3 — no silent zero):
%    1. Base present, no adjustments match: returns Base unmodified.
%    2. Base present, adjustments match:    returns Base + Σ Signed.
%    3. Base absent, adjustments present:   returns 0 + Σ Signed.
%       (Rationale: an adjustment that creates a concept ex-nihilo is
%       legitimate — e.g., a Div7A loan adjustment may introduce an
%       audit_* concept that didn't exist in the base trial balance.
%       The 0-base is documented behaviour, not silent default. The
%       caller still sees a non-null result; if the caller wants
%       fail-loud-on-no-base they can query sbrm_fact/6 first.)
%    4. Base absent, no adjustments:        FAILS (Standing Rule #3 —
%       there is genuinely no value for this concept; do not invent one).
%
%  The base/no-base/adjustment combinations above are tested explicitly
%  in test_adjustments.pl; the discipline is canon at this surface.

composed_value(Entity, Period, Concept, FinalValue) :-
    must_be(atom, Concept),
    %% Resolve base value (fails if no fact at all).
    (   sbrm_consolidation:sbrm_fact(Entity, Period, Concept, BaseValue, _, _)
    ->  Base = BaseValue
    ;   Base = no_base
    ),
    %% Sum any matching adjustments (empty list → 0.0).
    findall(A,
            sbrm_consolidation:sbrm_adjustment(Entity, Period, _AdjId,
                                               Concept, A, _Direction),
            Amounts),
    sum_list(Amounts, AdjSum),
    %% Combine.
    (   Base == no_base
    ->  (   Amounts == []
        ->  fail                              % no base AND no adjustments
        ;   FinalValue = AdjSum               % adjustments-only (ex-nihilo)
        )
    ;   FinalValue is Base + AdjSum
    ),
    must_be(number, FinalValue).
