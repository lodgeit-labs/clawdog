% ============================================================================
% DYNAMICALLY GENERATED PROLOG SBRM ENGINE FROM XBRL CALCULATION LINKBASES
% ============================================================================

:- dynamic raw_fact/2.

% calculation_arc(Parent, Child, Weight)
calculation_arc('mini_Assets', 'mini_CurrentAssets', 1.0).
calculation_arc('mini_CurrentAssets', 'mini_CashAndCashEquivalents', 1.0).
calculation_arc('mini_CurrentAssets', 'mini_Receivables', 1.0).
calculation_arc('mini_CurrentAssets', 'mini_Inventories', 1.0).
calculation_arc('mini_Assets', 'mini_NoncurrentAssets', 1.0).
calculation_arc('mini_NoncurrentAssets', 'mini_PropertyPlantAndEquipment', 1.0).
calculation_arc('mini_LiabilitiesAndEquity', 'mini_Liabilities', 1.0).
calculation_arc('mini_Liabilities', 'mini_CurrentLiabilities', 1.0).
calculation_arc('mini_CurrentLiabilities', 'mini_AccountsPayable', 1.0).
calculation_arc('mini_CurrentLiabilities', 'mini_AccruedExpenses', 1.0).
calculation_arc('mini_Liabilities', 'mini_NoncurrentLiabilities', 1.0).
calculation_arc('mini_NoncurrentLiabilities', 'mini_LongtermDebt', 1.0).
calculation_arc('mini_LiabilitiesAndEquity', 'mini_Equity', 1.0).
calculation_arc('mini_Equity', 'mini_PaidInCapital', 1.0).
calculation_arc('mini_Equity', 'mini_RetainedEarnings', 1.0).
calculation_arc('mini_NetIncomeLoss', 'mini_IncomeLossFromContinuingOperationsBeforeTax', 1.0).
calculation_arc('mini_IncomeLossFromContinuingOperationsBeforeTax', 'mini_OperatingIncomeLoss', 1.0).
calculation_arc('mini_OperatingIncomeLoss', 'mini_GrossProfitLoss', 1.0).
calculation_arc('mini_GrossProfitLoss', 'mini_Sales', 1.0).
calculation_arc('mini_GrossProfitLoss', 'mini_CostsOfSales', -1.0).
calculation_arc('mini_OperatingIncomeLoss', 'mini_OperatingExpenses', -1.0).
calculation_arc('mini_OperatingExpenses', 'mini_SalesGeneralAndAdministrativeExpenses', 1.0).
calculation_arc('mini_OperatingExpenses', 'mini_DepreciationAndAmortization', 1.0).
calculation_arc('mini_IncomeLossFromContinuingOperationsBeforeTax', 'mini_NonoperatingIncomeExpenses', 1.0).
calculation_arc('mini_NonoperatingIncomeExpenses', 'mini_InterestExpense', -1.0).
calculation_arc('mini_NonoperatingIncomeExpenses', 'mini_GainLossOnSalePropertyPlantEquipment', 1.0).
calculation_arc('mini_NetIncomeLoss', 'mini_IncomeTaxExpenseBenefit', -1.0).
calculation_arc('mini_NetCashFlow', 'mini_NetCashFlowOperatingActivities', 1.0).
calculation_arc('mini_NetCashFlowOperatingActivities', 'mini_ProceedsFromCollectionOfReceivables', 1.0).
calculation_arc('mini_NetCashFlowOperatingActivities', 'mini_PaymentOfAccountsPayable', -1.0).
calculation_arc('mini_NetCashFlow', 'mini_NetCashFlowFinancingActivities', 1.0).
calculation_arc('mini_NetCashFlowFinancingActivities', 'mini_ProceedsFromAdditionalLongtermBorrowings', 1.0).
calculation_arc('mini_NetCashFlowFinancingActivities', 'mini_PaymentForReductionOfLongtermBorrowings', -1.0).
calculation_arc('mini_NetCashFlowFinancingActivities', 'mini_PaymentInterest', -1.0).
calculation_arc('mini_NetCashFlowFinancingActivities', 'mini_ProceedsFromInvestmentsByOwner', 1.0).
calculation_arc('mini_NetCashFlowFinancingActivities', 'mini_PaymentForDistributionsToOwner', -1.0).
calculation_arc('mini_NetCashFlow', 'mini_NetCashFlowInvestingActivities', 1.0).
calculation_arc('mini_NetCashFlowInvestingActivities', 'mini_PaymentForCapitalAdditionsOfPropertyPlantEquipment', -1.0).
calculation_arc('mini_CashAndCashEquivalents', 'mini_Cash', 1.0).
calculation_arc('mini_CashAndCashEquivalents', 'mini_CashEquivalents', 1.0).
calculation_arc('mini_Receivables', 'mini_TradeReceivables', 1.0).
calculation_arc('mini_Receivables', 'mini_OtherReceivables', 1.0).
calculation_arc('mini_Inventories', 'mini_FinishedGoods', 1.0).
calculation_arc('mini_Inventories', 'mini_WorkInProgress', 1.0).
calculation_arc('mini_Inventories', 'mini_RawMaterial', 1.0).
calculation_arc('mini_PropertyPlantAndEquipment', 'mini_PropertyPlantAndEquipmentGross', 1.0).
calculation_arc('mini_PropertyPlantAndEquipmentGross', 'mini_Land', 1.0).
calculation_arc('mini_PropertyPlantAndEquipmentGross', 'mini_Buildings', 1.0).
calculation_arc('mini_PropertyPlantAndEquipmentGross', 'mini_Equipment', 1.0).
calculation_arc('mini_PropertyPlantAndEquipment', 'mini_AccumulatedDepreciation', -1.0).
calculation_arc('mini_AccountsPayable', 'mini_TradePayables', 1.0).
calculation_arc('mini_AccountsPayable', 'mini_OtherPayables', 1.0).
calculation_arc('mini_LongtermDebt', 'mini_MortgageLoans', 1.0).
calculation_arc('mini_LongtermDebt', 'mini_OtherSecuredLoans', 1.0).
calculation_arc('mini_LongtermDebt', 'mini_MaturesInOneYear', 1.0).
calculation_arc('mini_LongtermDebt', 'mini_MaturesInTwoYears', 1.0).
calculation_arc('mini_LongtermDebt', 'mini_MaturesInThreeYears', 1.0).
calculation_arc('mini_LongtermDebt', 'mini_MaturesInFourYears', 1.0).
calculation_arc('mini_LongtermDebt', 'mini_MaturesInFiveYears', 1.0).
calculation_arc('mini_LongtermDebt', 'mini_MaturesThereafter', 1.0).
calculation_arc('mini_CheckSum', 'mini_CashAndCashEquivalents', 1.0).
calculation_arc('mini_CheckSum', 'mini_Receivables', 1.0).
calculation_arc('mini_CheckSum', 'mini_Inventories', 1.0).
calculation_arc('mini_CheckSum', 'mini_PropertyPlantAndEquipment', 1.0).
calculation_arc('mini_CheckSum', 'mini_AccountsPayable', -1.0).
calculation_arc('mini_CheckSum', 'mini_AccruedExpenses', -1.0).
calculation_arc('mini_CheckSum', 'mini_LongtermDebt', -1.0).
calculation_arc('mini_CheckSum', 'mini_PaidInCapital', -1.0).
calculation_arc('mini_CheckSum', 'mini_RetainedEarnings', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_ProceedsFromCollectionOfReceivables', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_ProceedsFromInvestmentsByOwner', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_PaymentForDistributionsToOwner', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_PaymentOfAccountsPayable', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_PaymentInterest', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_ProceedsFromAdditionalLongtermBorrowings', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_PaymentForReductionOfLongtermBorrowings', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_PaymentForCapitalAdditionsOfPropertyPlantEquipment', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_IncreaseInReceivablesFromSalesOnAccount', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_CollectionOfReceivables', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_AdditionsToAllowanceForBadDebts', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_BadDebtsWrittenOff', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_PurchasesOfInventoryForSale', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_DecreaseInInventoriesFromSales', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_InventoryWrittenOff', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_CapitalAdditionsPropertyPlantAndEquipment', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_DecreaseFromDepreciationAndAmortization', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_PropertyPlantAndEquipmentWrittenOff', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_PurchasesInventoryForSaleOnAccount', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_DecreaseFromPaymentAccountsPayable', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_InterestAccrued', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_DecreaseFromPaymentOfInterest', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_AdditionalLongtermBorrowings', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_RepaymentLongtermBorrowings', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_InvestmentsByOwner', -1.0).
calculation_arc('mini_CheckSumChanges', 'mini_DistributionsToOwner', 1.0).
calculation_arc('mini_CheckSumChanges', 'mini_NetIncomeLoss', -1.0).

% ============================================================================
% THE RECURSIVE ROLLUP ENGINE
% ============================================================================
% Base case: If it's a raw fact provided by the GL, return its value.
node_value(Node, Value) :-
    raw_fact(Node, Value).

% Recursive case: If it's a parent node, sum the weighted values of its children.
node_value(Parent, TotalValue) :-
    \+ raw_fact(Parent, _), % Only calculate if not a raw leaf
    findall(ChildVal, (
        calculation_arc(Parent, Child, Weight),
        node_value(Child, RawVal),
        ChildVal is RawVal * Weight
    ), Vals),
    Vals \= [], % Ensure it has children
    sum_list(Vals, TotalValue).

% Fallback for missing nodes (0.0)
node_value(_, 0.0).
