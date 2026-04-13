---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-revenue-yellow-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:Fact
domain_tags:
- SBRM
- IncomeStatement
- Revenue
- Dimension:Yellow
fact_value: 25000.0
fact_unit: AUD
hypercube_context:
  primary_hypercube: StatementOfComprehensiveIncome
  arrangement_pattern: RollUp
integrity:
  source_uri: null
  content_hash: 050b6c49e8011d7bc4d42ef077a12252f20017b03d8eaa8689b3867de1b09ebe
parameters_exposed: {}
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026-duration
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-revenue-yellow
---

# Fact: Revenue (Yellow Dimension)
Revenue attributed to the Yellow segment for 2026 is $25,000.00 AUD.