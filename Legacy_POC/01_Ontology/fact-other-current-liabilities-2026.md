---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-other-curr-liab-001
ontological_class: FinancialFact
gist_equivalent: gist:Fact
domain_tags:
- SBRM
- BalanceSheet
hypercube_context:
  primary_hypercube: StatementOfFinancialPosition
  arrangement_pattern: Hierarchy
integrity:
  source_uri: null
  content_hash: "[SHA-256 injected at commit]"
parameters_exposed: {}
fact_value: 30000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-other-current-liabilities
value: 30000.0
content_hash: a0072abe6f42e3bd1aeb9dbde3f0d18e377e7b48e31c6c774aecb54def01ea4d
---
# Other Current Liabilities
Base: 30000.0
