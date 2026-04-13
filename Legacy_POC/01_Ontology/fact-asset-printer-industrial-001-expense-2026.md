---
"@context": "ipfs://bafkreifcontext...[Base_Context]"
"@id": "urn:uuid:fact-asset-printer-industrial-001-expense-001"
ontological_class: "FixedAssetDepreciationExpense"
gist_equivalent: "gist:Magnitude"
value: 20000.0
hypercube_context:
  primary_hypercube: "StatementOfComprehensiveIncome"
  arrangement_pattern: "RollUp"
edges:
  - rel: "sbrm:isInstanceOfConcept"
    target: "urn:uuid:def-sbr-asset-printer-industrial-001-expense"
  - rel: "sbrm:hasReportingEntity"
    target: "urn:uuid:def-sbrm-reporting-entity"
integrity:
  content_hash: "[SHA-256 injected at commit]"
---
# Industrial 3D Printer (Depreciation Expense)
Method: Diminishing Value
Rate: 0.25


