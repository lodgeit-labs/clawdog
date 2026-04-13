---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-revenue-red-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:Fact
domain_tags:
- SBRM
- IncomeStatement
- Revenue
- Dimension:Red
hypercube_context:
  primary_hypercube: StatementOfComprehensiveIncome
  arrangement_pattern: RollUp
integrity:
  source_uri: null
  content_hash: a10724cee82b50efb174c72ecc85f94a034f968f274a4ff6666a4a7f9248e135
parameters_exposed: {}
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
fact_value: 25000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026-duration
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-revenue-red
---

# Fact: Revenue (Red Dimension)
Revenue attributed to the Red segment for 2026 is $25,000.00 AUD.