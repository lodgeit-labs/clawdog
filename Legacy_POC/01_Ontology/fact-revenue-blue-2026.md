---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-revenue-blue-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:Measurement
domain_tags:
- SBRM
- IncomeStatement
- Revenue
- Dimension:Blue
content_hash: 98a6ac6768c58ece74f826ea34c932d99ee0bd09ea6faaae0a3b095bad3e3e8b
hypercube_context:
  primary_hypercube: StatementOfComprehensiveIncome
  arrangement_pattern: RollUp
integrity:
  source_uri: null
  content_hash: 98a6ac6768c58ece74f826ea34c932d99ee0bd09ea6faaae0a3b095bad3e3e8b
parameters_exposed: {}
fact_value: 25000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026-duration
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-revenue-blue
---

# Fact: Revenue (Blue Dimension)
Revenue attributed to the Blue segment for 2026 is $25,000.00 AUD.