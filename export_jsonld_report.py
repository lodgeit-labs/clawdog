def map_hierarchy(concept_id):
    """Maps flat SBRM concepts to their presentation layer hierarchy."""
    c = concept_id.lower()
    
    if c in ['section:total-assets', 'section:total-liabilities', 'section:total-equity', 'section:profit-loss']:
        return None 
        
    if 'cash' in c or 'receivable' in c or 'nab' in c: return "section:current-assets"
    if 'plant' in c or 'accumulated' in c: return "section:non-current-assets"
    if c == 'section:current-assets' or c == 'section:non-current-assets': return "section:total-assets"
    
    if 'payable' in c: return "section:current-liabilities"
    if c == 'section:current-liabilities' or c == 'section:non-current-liabilities': return "section:total-liabilities"
    
    if 'sales' in c or ('revenue' in c and c != 'section:revenue'): return "section:revenue"
    if c == 'section:revenue': return "section:profit-loss"
    
    if 'expense' in c: return "section:expenses"
    if c == 'section:expenses': return "section:profit-loss"
    
    if 'dividend' in c or 'capital' in c or 'retained' in c or 'opening-equity' in c or c == 'section:profit-loss': 
        return "section:total-equity"
        
    return None