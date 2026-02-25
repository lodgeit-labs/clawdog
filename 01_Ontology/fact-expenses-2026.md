---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-expenses-sample-001
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
  content_hash: b2b0bc492c57a6132512366355f112708d900a3668f4956a8fd6c3c4a91860c5
parameters_exposed: {}
fact_value: 80000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026-duration
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-expenses
value: 155000.0
content_hash: c158bd4770b71be9d89935c8122e16f8ee9b0946990c6f6fd20d7101166d9d4b
---







# Fact: Expenses (2026 Duration)
For the 2026 duration, the entity incurred Expenses of $80,000.00 AUD.