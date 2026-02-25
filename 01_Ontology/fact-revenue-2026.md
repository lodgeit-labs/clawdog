---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-revenue-sample-001
ontological_class: FinancialFact
domain_tags:
- SBRM
- IncomeStatement
- Revenue
gist_equivalent: gist:Fact
hypercube_context:
  primary_hypercube: StatementOfComprehensiveIncome
  arrangement_pattern: RollUp
integrity:
  source_uri: '[INJECT_SOURCE_URI_HERE]'
  content_hash: fc5c494fb8e7e293480404c7bd7f9d454c73c762d11c937d073b95c8ad8d812e
parameters_exposed: {}
fact_value: 100000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026-duration
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-revenue
value: 200000.0
content_hash: e5c3db61c402ca81ef9a744186e1e7da226a00f80ca909f69274271a2d1e3a58
---







# Fact: Revenue (2026 Duration)
For the 2026 duration, the entity generated Revenue of $100,000.00 AUD.