
:- consult('sbrm_kb.pl').
:- consult('div7a_kb.pl').

% Dynamically injected facts from the Markdown files
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-div7a-amalgamated-loan', 70000.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-div7a-benchmark-rate', 0.0877, 'RATE', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-div7a-term-years', 7, 'YEARS', 'Hierarchy').

:- initialization(main).
main :-
    calculate_myr('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'L001', MYR),
    format('SUCCESS: Calculated Div7A MYR based on SBRM Graph Facts: ~w~n', [MYR]),
    halt.
main :-
    writeln('ERROR: Could not compute MYR.'),
    halt.
