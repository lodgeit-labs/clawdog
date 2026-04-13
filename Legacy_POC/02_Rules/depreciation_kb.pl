% =========================================================
% SYSTEM: OPEN-SOURCE SBRM HYPERCUBE
% LAYER: LOGIC & INFERENCE (DEPRECIATION EXTENSION)
% =========================================================

:- dynamic sbrm_fact/6.
:- use_module(library(date)).
:- use_module(library(lists)).

% 1. ATO TAXONOMY & ROUTER
% (Usually loaded via taxonomy.pl, but mocked here for SBRM integration demonstration)
taxonomy(heavy_machinery, 'Legacy Plant & Equipment', 15).
taxonomy(desktop_computers, 'Legacy Plant & Equipment', 4).
taxonomy(light_commercial, 'Legacy Motor Vehicles', 7).
taxonomy(sedans, 'Legacy Motor Vehicles', 8).
taxonomy(unknown_asset, 'Legacy Plant & Equipment', 5).

keyword_map('machine', heavy_machinery).
keyword_map('bobcat', heavy_machinery).
keyword_map('computer', desktop_computers).
keyword_map('hilux', light_commercial).
keyword_map('toyota', light_commercial).
keyword_map('corolla', sedans).

classify_asset(RawName, Category, Life) :-
    downcase_atom(RawName, LowerName),
    atomic_list_concat(Tokens, ' ', LowerName),
    (   match_keywords(Tokens, ClassID)
    ->  taxonomy(ClassID, Category, Life)
    ;   taxonomy(unknown_asset, Category, Life)
    ).

match_keywords([Token|_], Class) :- keyword_map(Token, Class), !.
match_keywords([_|Tail], Class) :- match_keywords(Tail, Class).

% 2. CORE MATH
days_between(StartStr, EndStr, Days) :-
    parse_time(StartStr, iso_8601, StartStamp),
    parse_time(EndStr, iso_8601, EndStamp),
    Days is round((EndStamp - StartStamp) / 86400).

simulate_wdv(Cost, Life, Days, WDV, AccumDep) :-
    YearlyDep is Cost / Life,
    CalculatedDep is YearlyDep * (Days / 365),
    (   CalculatedDep >= Cost
    ->  AccumDep = Cost, WDV = 0.0
    ;   AccumDep = CalculatedDep, WDV is Cost - AccumDep
    ).

% 3. SBRM OPERATIVE PREDICATES (Stateless Audit/Resurrect)
evaluate_asset_audit(Entity, Period, AssetID, TransitionDate, AuditReport) :-
    sbrm_fact(Entity, Period, 'urn:uuid:def-dep-name', AssetNameStr, 'STR', 'Hierarchy'),
    atom_string(AssetName, AssetNameStr),
    sbrm_fact(Entity, Period, 'urn:uuid:def-dep-cost', Cost, 'AUD', 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-dep-purchase-date', PurchaseDate, 'DATE', 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-dep-tax-method', TaxMethodStr, 'ENUM', 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-dep-accum-dep', CurrentAccDep, 'AUD', 'Hierarchy'),
    
    classify_asset(AssetName, Category, Life),
    days_between(PurchaseDate, TransitionDate, Days),
    simulate_wdv(Cost, Life, Days, _, TargetAccDep),
    
    TargetAccDepR is round(TargetAccDep * 100) / 100,
    Variance is abs(TargetAccDepR - CurrentAccDep),
    VarianceR is round(Variance * 100) / 100,
    
    string_lower(TaxMethodStr, CleanMethod),
    (CleanMethod == "dv" -> MethodFlag = 'Warning: Asset uses Tax DV. Consider transitioning to PC.' ; MethodFlag = 'OK'),
    (VarianceR > 10.00 -> VarFlag = 'Warning: Material variance between ideal accounting depreciation and current ledger balance.' ; VarFlag = 'OK'),
    
    AuditReport = _{
        asset_id: AssetID,
        asset_name: AssetNameStr,
        asset_category: Category,
        target_accum_dep: TargetAccDepR,
        actual_ledger_accum_dep: CurrentAccDep,
        variance_amount: VarianceR,
        flags: _{ method_check: MethodFlag, variance_check: VarFlag }
    }.
