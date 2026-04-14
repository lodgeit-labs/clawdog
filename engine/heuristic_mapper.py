def map_account_to_mini(acc_name):
    acc = acc_name.lower()
    
    if any(x in acc for x in ['telstra', 'rent', 'super', 'wages', 'office', 'qantas', 'xero', 'expense', 'supplies']):
        return 'mini_OperatingExpenses'
    elif any(x in acc for x in ['bank', 'nab', 'westpac', 'cba', 'anz', 'macquarie']):
        return 'mini_CashAndCashEquivalents'
    elif 'receivable' in acc or 'loan' in acc:
        return 'mini_Receivables'
    elif 'inventory' in acc:
        return 'mini_Inventories'
    elif 'equipment' in acc or 'vehicle' in acc or 'property' in acc or 'depreciation' in acc:
        return 'mini_PropertyPlantAndEquipment'
    elif 'payable' in acc or 'gst' in acc or 'payg' in acc or 'ato' in acc:
        return 'mini_AccountsPayable'
    elif 'hire purchase' in acc:
        return 'mini_LongtermDebt'
    elif 'share capital' in acc or 'corpus' in acc or 'settlement' in acc or ('partner' in acc and 'capital' in acc) or 'accumulation' in acc or 'pension' in acc:
        return 'mini_PaidInCapital'
    elif any(x in acc for x in ['retained', 'drawings', 'upe', 'distributions', 'dividend']):
        return 'mini_RetainedEarnings'
    elif 'sales' in acc or 'income' in acc or 'revenue' in acc or 'services' in acc or 'contracting' in acc or 'franked' in acc or 'employer contributions' in acc:
        return 'mini_Sales'
    elif 'bunnings' in acc or 'cost of sales' in acc:
        return 'mini_CostOfGoodsSold'
    elif 'penalties' in acc:
        return 'mini_NonoperatingIncomeExpense'
        
    return 'mini_OperatingExpenses'