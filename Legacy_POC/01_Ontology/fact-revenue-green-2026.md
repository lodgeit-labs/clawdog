---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-revenue-green-sample-001
ontological_class: FinancialFact
domain_tags:
- SBRM
- IncomeStatement
- Revenue
- Dimension:Green
gist_equivalent: gist:Information
hypercube_context:
  primary_hypercube: StatementOfComprehensiveIncome
  arrangement_pattern: RollUp
integrity:
  source_uri: null
  content_hash: 03ad9eed3a08cf727bd5269864e8a454991654300aa98ff6a6a78be63b05a472
parameters_exposed: {}
fact_value: 25000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026-duration
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-revenue-green
---

# Fact: Revenue (Green Dimension)
Revenue attributed to the Green segment for 2026 is $25,000.00 AUD.