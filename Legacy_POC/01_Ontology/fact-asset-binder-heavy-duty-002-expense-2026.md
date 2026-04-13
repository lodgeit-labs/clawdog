---
"@context": "ipfs://bafkreifcontext...[Base_Context]"
"@id": "urn:uuid:fact-asset-binder-heavy-duty-002-expense-001"
ontological_class: "FixedAssetDepreciationExpense"
gist_equivalent: "gist:Magnitude"
value: 5000.0
hypercube_context:
  primary_hypercube: "StatementOfComprehensiveIncome"
  arrangement_pattern: "RollUp"
edges:
  - rel: "sbrm:isInstanceOfConcept"
    target: "urn:uuid:def-sbr-asset-binder-heavy-duty-002-expense"
  - rel: "sbrm:hasReportingEntity"
    target: "urn:uuid:def-sbrm-reporting-entity"
integrity:
  content_hash: "[SHA-256 injected at commit]"
---
# Heavy Duty Thermal Binder (Depreciation Expense)
Method: Diminishing Value
Rate: 0.25


