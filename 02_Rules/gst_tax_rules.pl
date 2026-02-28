% =================================================================
% ATO GST REGISTRATION LOGIC ENGINE
% Compiled from Logical English Specification
% =================================================================

:- dynamic does_not_operate_for_profit/1.
:- dynamic has_turnover/2.
:- dynamic has_projected_turnover/2.
:- dynamic uber_driver/1.

% --- 1. ONTOLOGY ---
% Entities
entity(E) :- sporting_club(E).
entity(E) :- charity(E).
entity(E) :- community_group(E).
entity(E) :- professional_association(E).
entity(E) :- declared_entity(E). % Catch-all for basic declared entities

% Service Classifications
ride_sourcing_service(E) :- uber_driver(E).

% Structural Logic
not_for_profit(Entity) :- does_not_operate_for_profit(Entity).

% --- 2. KNOWLEDGE BASE (GST RULES) ---

% Rule 1: Ride-Sourcing Services MUST register regardless of turnover.
must_register_for_gst(Entity) :-
    entity(Entity),
    ride_sourcing_service(Entity).

% Rule 2: Not-For-Profits MUST register if turnover or projection >= $150,000.
must_register_for_gst(Entity) :-
    entity(Entity),
    not_for_profit(Entity),
    has_turnover(Entity, Turnover),
    Turnover >= 150000.

must_register_for_gst(Entity) :-
    entity(Entity),
    not_for_profit(Entity),
    has_projected_turnover(Entity, Projection),
    Projection >= 150000.

% Rule 3: For-Profits (Standard Entities) MUST register if turnover or projection >= $75,000.
must_register_for_gst(Entity) :-
    entity(Entity),
    \+ not_for_profit(Entity),
    has_turnover(Entity, Turnover),
    Turnover >= 75000.

must_register_for_gst(Entity) :-
    entity(Entity),
    \+ not_for_profit(Entity),
    has_projected_turnover(Entity, Projection),
    Projection >= 75000.

% Rule 4 & 5: Dynamic Turnover Calculation (Monthly + Past/Next 11 Months)
has_turnover(Entity, CurrentTurnover) :-
    monthly_turnover(Entity, Monthly),
    past_11_months_turnover(Entity, Past),
    CurrentTurnover is Monthly + Past.

has_projected_turnover(Entity, ProjectedTurnover) :-
    monthly_turnover(Entity, Monthly),
    next_11_months_turnover(Entity, Future),
    ProjectedTurnover is Monthly + Future.

% Rule 6 & 7: Total Business Income (TBI) and GST Turnover Formularies
total_business_income(Scenario, TBI) :-
    gst_included(Scenario, _GST),
    sales_associates(Scenario, SalesAssoc),
    disconnected_sales(Scenario, Disconnected),
    input_taxed(Scenario, InputTaxed),
    exports(Scenario, Exports),
    sales_third_parties(Scenario, Sales),
    TBI is SalesAssoc + Disconnected + InputTaxed + Exports + Sales.

gst_turnover(Scenario, GSTTurnover) :-
    total_business_income(Scenario, TBI),
    gst_included(Scenario, GST),
    sales_associates(Scenario, SalesAssoc),
    disconnected_sales(Scenario, Disconnected),
    input_taxed(Scenario, InputTaxed),
    exports(Scenario, Exports),
    GSTTurnover is TBI - GST - SalesAssoc - Disconnected - InputTaxed - Exports.

% =================================================================
% 3. DEMO SCENARIOS & TESTS
% =================================================================

% Scenario A: Cherrio Charity
declared_entity('Cherrio Charity').
does_not_operate_for_profit('Cherrio Charity').
has_turnover('Cherrio Charity', 160000).

% Scenario B: Sporting Club
declared_entity('sporting club').
does_not_operate_for_profit('sporting club').
has_projected_turnover('sporting club', 100000).

% Scenario C: Tom's Bakery
declared_entity('Tom s Bakery').
has_turnover('Tom s Bakery', 80000).

% Scenario Uber: Mario
declared_entity(mario).
uber_driver(mario).

% Scenario: Typical Financials
gst_included(typical, 9090.91).
sales_associates(typical, 0).
disconnected_sales(typical, 0).
input_taxed(typical, 5000).
exports(typical, 0).
sales_third_parties(typical, 100000).

% Scenario: Significant Exports Financials
gst_included(significant_exports, 6818.18).
sales_associates(significant_exports, 10000).
disconnected_sales(significant_exports, 2000).
input_taxed(significant_exports, 0).
exports(significant_exports, 50000).
sales_third_parties(significant_exports, 75000).

% Scenario: Small Business Financials
gst_included(small_business, 0).
sales_associates(small_business, 5000).
disconnected_sales(small_business, 1000).
input_taxed(small_business, 0).
exports(small_business, 0).
sales_third_parties(small_business, 0).