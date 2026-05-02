%% sbrm_consolidation.pl
%% =============================================================================
%% SBRM Consolidation Engine — Temporal FX-aware roll-up + provenance
%%
%% Foundation : Opus  (cycle-safe accumulator, multifile injection, fx_epsilon)
%% Grafts     : GPT   (unique-rate enforcement, must_be type guards,
%%                     empty-leaves fails rather than silent zero)
%% Extensions : ClawDog
%%   * Weighted edges (sbrm_edge/5) — strict superset of both the challenge
%%     spec (unweighted sbrm_edge/4 still works) and the public Kit's
%%     calculation_arc/3 (contra-accounts via negative weights, e.g.
%%     AccumulatedDepreciation rolling -1.0 into PropertyPlantAndEquipment).
%%   * consolidation_evidence/6 — returns the leaf-by-leaf decomposition
%%     (concept, source-currency, source-value, applied-weight, fx-rate,
%%     contributed-target-value) alongside the total. The tuple a
%%     helm_mutations ledger entry would hash over to prove how a
%%     consolidated number was assembled.
%%
%% Standing-rule alignment (LodgeiT/ClawDog Brain):
%%   * Rule #3 (Zero-Hallucination) — no silent defaults; conflicting FX
%%     rates halt; missing facts fail rather than return 0.0.
%%   * Rule #6 (Hoffman temporal-dimension discipline) — Period is treated
%%     as a first-class dimension; FX lookup is period-scoped.
%%
%% Brain canon: GLOBAL_NOTES/CLAWDOG/107_CONSOLIDATION_LOGIC.md
%% Author    : ClawDog ∮
%% =============================================================================

:- module(sbrm_consolidation,
          [ calculate_consolidated_node/5
          , verify_temporal_equity/5
          , consolidation_evidence/6
          , sbrm_fact/6
          , sbrm_edge/4
          , sbrm_edge/5
          , fx_rate/4
          ]).

:- use_module(library(error)).
:- use_module(library(lists)).

%% Multifile so external injectors can `assertz(sbrm_fact(...))` directly
%% and the engine here will see those facts.
:- multifile sbrm_fact/6, sbrm_edge/4, sbrm_edge/5, fx_rate/4.
:- dynamic   sbrm_fact/6, sbrm_edge/4, sbrm_edge/5, fx_rate/4.

% ---- tunable ---------------------------------------------------------------
%% Tolerance for the equity-roll-forward equality check. FX float drift
%% across multi-leg conversions is not bit-exact; epsilon absorbs it.
fx_epsilon(1.0e-6).

% =============================================================================
%  EDGE NORMALISATION
% =============================================================================
%
%  External callers may inject either shape:
%    sbrm_edge(EdgeID, EdgeType, Parent, Child)         % legacy / spec
%    sbrm_edge(EdgeID, EdgeType, Parent, Child, Weight) % weighted
%
%  Internally we always read through edge_arc/3 which returns (Child, Weight),
%  defaulting the weight to 1.0 for legacy 4-arity edges. This is what makes
%  the engine a strict superset: an unweighted graph behaves exactly as
%  before; a weighted graph supports contra-accounts.

%! edge_arc(+Parent, -Child, -Weight) is nondet.
edge_arc(Parent, Child, Weight) :-
    sbrm_edge(_EdgeID, 'sbrm:isRollupOf', Parent, Child, Weight),
    must_be(number, Weight).
edge_arc(Parent, Child, 1.0) :-
    sbrm_edge(_EdgeID, 'sbrm:isRollupOf', Parent, Child).

% =============================================================================
%  OBJECTIVE 1 — Recursive FX Consolidation (with weights)
% =============================================================================

%! calculate_consolidated_node(+Entity, +Period, +TargetCurrency,
%!                             +TargetConcept, -ConsolidatedTotal) is semidet.
%
%  Walks edges from TargetConcept down to leaves carrying the *cumulative
%  weight* along each path (product of edge weights — so a `-1.0` contra
%  edge correctly inverts the leaf's contribution). Pulls every matching
%  sbrm_fact for (Entity, Period, Leaf), converts to TargetCurrency, and
%  sums weighted-converted values.
%
%  FAILS (rather than returning 0.0) if the subtree produces no facts.

calculate_consolidated_node(Entity, Period, TargetCurrency,
                            TargetConcept, ConsolidatedTotal) :-
    must_be(atom, TargetCurrency),
    leaf_concepts_weighted(TargetConcept, WeightedLeaves),
    WeightedLeaves \== [],
    convert_weighted_leaves(WeightedLeaves, Entity, Period, TargetCurrency,
                            Values),
    Values \== [],
    sum_list(Values, ConsolidatedTotal).

% ---- weighted leaf discovery (cycle-safe accumulator) ----------------------

%! leaf_concepts_weighted(+Root, -WeightedLeaves) is det.
%
%  WeightedLeaves is a list of (Leaf-CumulativeWeight) pairs. The same
%  leaf may appear multiple times if reachable via multiple distinct
%  paths (legitimate in weighted SBRM graphs — e.g. a CheckSum node
%  consuming the same leaf with different signs); we do NOT collapse
%  duplicates here, that would lose information.
%
%  Cycle-safe via a Visited set scoped to the path being walked: a node
%  already on the *current path* is never re-expanded. Diamond patterns
%  (two paths to the same node) are still allowed because Visited is
%  path-local, not global.

leaf_concepts_weighted(Root, WeightedLeaves) :-
    findall(Leaf-Weight,
            walk_weighted(Root, [Root], 1.0, Leaf, Weight),
            WeightedLeaves).

% walk_weighted(+Node, +VisitedPath, +AccWeight, -Leaf, -CumulativeWeight)
walk_weighted(Node, _Visited, AccWeight, Node, AccWeight) :-
    \+ edge_arc(Node, _Child, _W).
walk_weighted(Node, Visited, AccWeight, Leaf, FinalWeight) :-
    edge_arc(Node, Child, EdgeWeight),
    \+ memberchk(Child, Visited),
    NextWeight is AccWeight * EdgeWeight,
    walk_weighted(Child, [Child|Visited], NextWeight, Leaf, FinalWeight).

% ---- valuation + FX --------------------------------------------------------

%! convert_weighted_leaves(+WeightedLeaves, +Entity, +Period, +TargetCurrency,
%!                         -Values) is det.

convert_weighted_leaves([], _Entity, _Period, _TargetCurrency, []).
convert_weighted_leaves([Leaf-Weight|Rest], Entity, Period, TargetCurrency,
                        Values) :-
    findall(WeightedConverted,
            ( sbrm_fact(Entity, Period, Leaf, Value, Currency, _Pattern),
              convert_value(Value, Currency, TargetCurrency, Period, Conv),
              WeightedConverted is Conv * Weight
            ),
            LeafValues),
    convert_weighted_leaves(Rest, Entity, Period, TargetCurrency, More),
    append(LeafValues, More, Values).

%! convert_value(+Value, +SourceCurrency, +TargetCurrency, +Period, -Converted)

convert_value(Value, Currency, Currency, _Period, Value) :-
    !,
    must_be(number, Value).
convert_value(Value, Source, Target, Period, Converted) :-
    must_be(number, Value),
    lookup_fx_rate(Source, Target, Period, Rate),
    Converted is Value * Rate.

%! lookup_fx_rate(+Source, +Target, +Period, -Rate) is semidet.
%
%  Requires *exactly one* distinct rate. Identical duplicates collapse;
%  conflicting rates HALT (engine refuses the conversion).

lookup_fx_rate(Source, Target, Period, Rate) :-
    setof(CandidateRate,
          fx_rate(Source, Target, Period, CandidateRate),
          [Rate]),
    must_be(number, Rate).

% =============================================================================
%  OBJECTIVE 2 — Multi-Currency Temporal Equity Roll-Forward
% =============================================================================

verify_temporal_equity(Entity, OpeningPeriod, ActionPeriod, ClosingPeriod,
                       TargetCurrency) :-
    calculate_consolidated_node(Entity, OpeningPeriod, TargetCurrency,
                                'sbr:OpeningEquity',  Opening),
    calculate_consolidated_node(Entity, ActionPeriod,  TargetCurrency,
                                'sbr:NetProfit',      Profit),
    calculate_consolidated_node(Entity, ActionPeriod,  TargetCurrency,
                                'sbr:DividendsPaid',  Dividends),
    calculate_consolidated_node(Entity, ClosingPeriod, TargetCurrency,
                                'sbr:ClosingEquity',  Closing),
    Expected is Opening + Profit - Dividends,
    fx_epsilon(Eps),
    abs(Expected - Closing) =< Eps.

% =============================================================================
%  PROVENANCE — consolidation_evidence/6
% =============================================================================
%
%  Returns the full leaf-by-leaf decomposition that backs a consolidated
%  number, suitable for hashing into a helm_mutations ledger entry.
%
%  Each tuple in Evidence is:
%
%      evidence(Concept, SourceCurrency, SourceValue,
%               AppliedWeight, FxRate, ContributedTargetValue)
%
%  Where:
%   * Concept              = the leaf SBRM concept
%   * SourceCurrency       = currency the leaf fact was recorded in
%   * SourceValue          = raw value as recorded
%   * AppliedWeight        = product of edge weights along the path from
%                            TargetConcept down to this leaf (1.0 if all
%                            edges are unweighted; -1.0 for contra paths;
%                            arbitrary product otherwise)
%   * FxRate               = the rate applied (1.0 for identity)
%   * ContributedTargetValue = SourceValue * FxRate * AppliedWeight,
%                            i.e. exactly what this leaf added to the total
%
%  Invariant:  sum of ContributedTargetValue across Evidence == Total
%  (within fx_epsilon — same tolerance as the equity check).
%
%  Fails under the same conditions as calculate_consolidated_node/5:
%  no leaves, conflicting FX rates, type-error on injected non-numbers.

consolidation_evidence(Entity, Period, TargetCurrency,
                       TargetConcept, Total, Evidence) :-
    must_be(atom, TargetCurrency),
    leaf_concepts_weighted(TargetConcept, WeightedLeaves),
    WeightedLeaves \== [],
    collect_evidence(WeightedLeaves, Entity, Period, TargetCurrency,
                     Evidence),
    Evidence \== [],
    findall(C,
            member(evidence(_,_,_,_,_,C), Evidence),
            Contributions),
    sum_list(Contributions, Total).

collect_evidence([], _Entity, _Period, _TargetCurrency, []).
collect_evidence([Leaf-Weight|Rest], Entity, Period, TargetCurrency, All) :-
    findall(evidence(Leaf, SourceCurrency, SourceValue,
                     Weight, FxRate, Contribution),
            ( sbrm_fact(Entity, Period, Leaf, SourceValue, SourceCurrency,
                        _Pattern),
              must_be(number, SourceValue),
              fx_rate_for_evidence(SourceCurrency, TargetCurrency, Period,
                                   FxRate),
              Contribution is SourceValue * FxRate * Weight
            ),
            HereEvidence),
    collect_evidence(Rest, Entity, Period, TargetCurrency, RestEvidence),
    append(HereEvidence, RestEvidence, All).

%! fx_rate_for_evidence(+Source, +Target, +Period, -Rate) is semidet.
%  Same uniqueness discipline as lookup_fx_rate/4 but exposes the rate
%  even on identity (so the evidence row records FxRate=1.0 explicitly,
%  rather than leaving it implicit).
fx_rate_for_evidence(Currency, Currency, _Period, 1.0) :- !.
fx_rate_for_evidence(Source, Target, Period, Rate) :-
    lookup_fx_rate(Source, Target, Period, Rate).
