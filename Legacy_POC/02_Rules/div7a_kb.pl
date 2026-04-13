% =========================================================
% SYSTEM: OPEN-SOURCE SBRM HYPERCUBE
% LAYER: LOGIC & INFERENCE (DIV 7A EXTENSION)
% =========================================================

:- dynamic sbrm_fact/6.
:- use_module(library(date)).

% ==========================================
% 1. Validation & Rule Enforcement
% ==========================================
validate_term(unsecured, Term) :- Term =< 7, !.
validate_term(secured, Term) :- Term =< 25, !.

% ==========================================
% 2. SBRM OPERATIVE PREDICATES for Div7A
% ==========================================
% Pure Logic Lens: Calculate the Minimum Yearly Repayment based on facts in the SBRM graph.
calculate_myr(Entity, Period, LoanID, MYR) :-
    % 1. Dynamically read the facts injected from the Markdown files
    sbrm_fact(Entity, Period, 'urn:uuid:def-div7a-amalgamated-loan', BaseL, 'AUD', 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-div7a-benchmark-rate', Rate, 'RATE', 'Hierarchy'),
    sbrm_fact(Entity, Period, 'urn:uuid:def-div7a-term-years', Term, 'YEARS', 'Hierarchy'),
    
    % 2. Execute the mathematical constraint
    Denominator is 1 - (1 + Rate)**(-Term),
    RawMYR is (BaseL * Rate) / Denominator,
    MYR is round(RawMYR * 100) / 100.
