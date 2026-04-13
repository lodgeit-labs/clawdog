
:- consult('sbrm_kb.pl').
:- consult('hp_kb.pl').

% Dynamically injected facts from the Markdown files (Archetype A nodes)
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-hp-principal', 235000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-hp-annual-rate', 0.0519, 'RATE', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-hp-term-months', 60, 'MONTHS', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-hp-payment-type', "in_arrears", 'ENUM', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-hp-period-freq', "monthly", 'ENUM', 'Hierarchy').

:- initialization(main).
main :-
    calculate_hp_schedule('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'asset-001', Output),
    TotalInt = Output.total_interest_paid,
    format('SUCCESS: Calculated Hire Purchase Amortization based on SBRM Graph Facts.~n', []),
    format('Total Interest Computed: $~w~n', [TotalInt]),
    halt.
main :-
    writeln('ERROR: Could not compute Amortization.'),
    halt.
