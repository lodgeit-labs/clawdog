% --- DIRECTIVES: PREVENT WARNINGS & CRASHES ---
:- dynamic sporting_club/1.
:- dynamic charity/1.
:- dynamic community_group/1.
:- dynamic professional_association/1.
:- dynamic declared_entity/1.
:- dynamic uber_driver/1.
:- dynamic does_not_operate_for_profit/1.
:- dynamic monthly_turnover/2.
:- dynamic past_11_months_turnover/2.
:- dynamic next_11_months_turnover/2.
:- dynamic has_turnover/2.
:- dynamic has_projected_turnover/2.
:- dynamic gst_included/2.
:- dynamic sales_associates/2.
:- dynamic disconnected_sales/2.
:- dynamic input_taxed/2.
:- dynamic exports/2.
:- dynamic sales_third_parties/2.

:- discontiguous declared_entity/1.
:- discontiguous does_not_operate_for_profit/1.
:- discontiguous has_turnover/2.
:- discontiguous has_projected_turnover/2.
:- discontiguous gst_included/2.
:- discontiguous sales_associates/2.
:- discontiguous disconnected_sales/2.
:- discontiguous input_taxed/2.
:- discontiguous exports/2.
:- discontiguous sales_third_parties/2.

% --- 1. ONTOLOGY ---
entity(E) :- sporting_club(E).
entity(E) :- charity(E).
entity(E) :- community_group(E).
entity(E) :- professional_association(E).
entity(E) :- declared_entity(E). 

ride_sourcing_service(E) :- uber_driver(E).
not_for_profit(Entity) :- does_not_operate_for_profit(Entity).

% --- 2. KNOWLEDGE BASE (GST RULES) ---
must_register_for_gst(Entity) :- entity(Entity), ride_sourcing_service(Entity).

must_register_for_gst(Entity) :- entity(Entity), not_for_profit(Entity), has_turnover(Entity, Turnover), Turnover >= 150000.
must_register_for_gst(Entity) :- entity(Entity), not_for_profit(Entity), has_projected_turnover(Entity, Projection), Projection >= 150000.

must_register_for_gst(Entity) :- entity(Entity), \+ not_for_profit(Entity), has_turnover(Entity, Turnover), Turnover >= 75000.
must_register_for_gst(Entity) :- entity(Entity), \+ not_for_profit(Entity), has_projected_turnover(Entity, Projection), Projection >= 75000.

has_turnover(Entity, CurrentTurnover) :- monthly_turnover(Entity, Monthly), past_11_months_turnover(Entity, Past), CurrentTurnover is Monthly + Past.
has_projected_turnover(Entity, ProjectedTurnover) :- monthly_turnover(Entity, Monthly), next_11_months_turnover(Entity, Future), ProjectedTurnover is Monthly + Future.

total_business_income(Scenario, TBI) :- gst_included(Scenario, _GST), sales_associates(Scenario, SalesAssoc), disconnected_sales(Scenario, Disconnected), input_taxed(Scenario, InputTaxed), exports(Scenario, Exports), sales_third_parties(Scenario, Sales), TBI is SalesAssoc + Disconnected + InputTaxed + Exports + Sales.
gst_turnover(Scenario, GSTTurnover) :- total_business_income(Scenario, TBI), gst_included(Scenario, GST), sales_associates(Scenario, SalesAssoc), disconnected_sales(Scenario, Disconnected), input_taxed(Scenario, InputTaxed), exports(Scenario, Exports), GSTTurnover is TBI - GST - SalesAssoc - Disconnected - InputTaxed - Exports.

% --- 3. DEMO SCENARIOS & TESTS ---
declared_entity('Cherrio Charity').
does_not_operate_for_profit('Cherrio Charity').
has_turnover('Cherrio Charity', 160000).

declared_entity('sporting club').
does_not_operate_for_profit('sporting club').
has_projected_turnover('sporting club', 100000).

declared_entity('Tom s Bakery').
has_turnover('Tom s Bakery', 80000).

declared_entity(mario).
uber_driver(mario).

declared_entity('Demo Company').
has_turnover('Demo Company', 120000).

gst_included(typical, 9090.91).
sales_associates(typical, 0).
disconnected_sales(typical, 0).
input_taxed(typical, 5000).
exports(typical, 0).
sales_third_parties(typical, 100000).

gst_included(significant_exports, 6818.18).
sales_associates(significant_exports, 10000).
disconnected_sales(significant_exports, 2000).
input_taxed(significant_exports, 0).
exports(significant_exports, 50000).
sales_third_parties(significant_exports, 75000).