---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-non-current-liabilities-sample-001
ontological_class: FinancialFact
domain_tags:
- SBRM
- BalanceSheet
gist_equivalent: gist:Fact
content_hash: ef3836d76b00e3188fbc82b86acf73f53c3d53c9edaa6575d1f194b30d79a1c6
hypercube_context:
  primary_hypercube: StatementOfFinancialPosition
  arrangement_pattern: Hierarchy
integrity:
  source_uri: null
  content_hash: ef3836d76b00e3188fbc82b86acf73f53c3d53c9edaa6575d1f194b30d79a1c6
parameters_exposed: {}
fact_value: 50000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-non-current-liabilities
---

# Fact: Non-Current Liabilities
As of 2026, Non-Current Liabilities equal $50,000.00 AUD.