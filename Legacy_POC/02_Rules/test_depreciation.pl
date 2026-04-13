
:- consult('sbrm_kb.pl').
:- consult('depreciation_kb.pl').

% Dynamically injected facts from the Markdown files
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-dep-name', "Toyota", 'STR', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-dep-cost', 26255.0, 'AUD', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-dep-purchase-date', "2015-01-30", 'DATE', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-dep-tax-method', "dv", 'ENUM', 'Hierarchy').
sbrm_fact('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'urn:uuid:def-dep-accum-dep', 24934.04, 'AUD', 'Hierarchy').

:- initialization(main).
main :-
    evaluate_asset_audit('urn:uuid:def-sbrm-reporting-entity', 'urn:uuid:def-sbrm-reporting-period-2025', 'asset-10', '2025-07-01', AuditReport),
    format('SUCCESS: Calculated Depreciation Audit based on SBRM Graph Facts.~n'),
    Variance = AuditReport.variance_amount,
    MethodFlag = AuditReport.flags.method_check,
    VarFlag = AuditReport.flags.variance_check,
    format('Variance Amount: $~w~n', [Variance]),
    format('Method Check: ~w~n', [MethodFlag]),
    format('Variance Check: ~w~n', [VarFlag]),
    halt.
main :-
    writeln('ERROR: Could not compute Depreciation Audit.'),
    halt.
