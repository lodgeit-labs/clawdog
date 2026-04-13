---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-other-expenses-001
ontological_class: FinancialFact
gist_equivalent: gist:Fact
domain_tags:
- SBRM
- IncomeStatement
- Expenses
hypercube_context:
  primary_hypercube: StatementOfComprehensiveIncome
  arrangement_pattern: RollUp
integrity:
  source_uri: null
  content_hash: "[SHA-256 injected at commit]"
parameters_exposed: {}
fact_value: 80000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026-duration
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-other-expenses
value: 55000.0
content_hash: 757df495d86f5e1bdd9715e6f172d3b2f76e1c256fbf56c0560c8a880b04a9b2
---
# Other Base Expenses
Base: 55000.0 (80k original base - 25k sub-ledger depreciation)
