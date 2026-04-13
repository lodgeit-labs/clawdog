% =======================================================================
% SBRM Core Physics Engine
% The immutable laws of double-entry accounting.
% =======================================================================

:- module(sbrm_core, [
    net_income/3,
    balance_sheet_equation/4,
    verify_report_set/6,
    find_delta/6
]).

% -----------------------------------------------------------------------
% 1. Net Income Equation
% Assuming standard magnitude values (Positive Revenue, Positive Expenses)
% If reading from Trial Balance (where Revenue is Negative/Credit), 
% we take the absolute value or adjust signs accordingly. 
% For strict SBRM multidimensional reporting, magnitudes are typically positive.
% -----------------------------------------------------------------------
net_income(Revenue, Expenses, NetIncome) :-
    NetIncome is Revenue - Expenses.

% -----------------------------------------------------------------------
% 2. Balance Sheet Equation
% Assets = Liabilities + Equity (where Equity includes Current Year Net Income)
% -----------------------------------------------------------------------
balance_sheet_equation(Assets, Liabilities, PriorEquity, NetIncome) :-
    TotalEquity is PriorEquity + NetIncome,
    % We use a small epsilon for floating point arithmetic safety
    Diff is abs(Assets - (Liabilities + TotalEquity)),
    Diff < 0.01.

% -----------------------------------------------------------------------
% 3. The Grand Verification
% Ingests the 5 core elements and mathematically proves consistency.
% -----------------------------------------------------------------------
verify_report_set(Assets, Liabilities, PriorEquity, Revenue, Expenses, IsConsistent) :-
    net_income(Revenue, Expenses, CalculatedNetIncome),
    ( balance_sheet_equation(Assets, Liabilities, PriorEquity, CalculatedNetIncome) ->
        IsConsistent = true
    ;
        IsConsistent = false
    ).

% Helper to evaluate an unbalanced trial balance and find the Delta (Thermodynamic void)
find_delta(Assets, Liabilities, PriorEquity, Revenue, Expenses, Delta) :-
    net_income(Revenue, Expenses, CalculatedNetIncome),
    TotalEquity is PriorEquity + CalculatedNetIncome,
    Delta is Assets - (Liabilities + TotalEquity).
