---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-profit-loss-sample-001
ontological_class: FinancialFact
domain_tags:
- SBRM
- Equity
- IncomeStatement
gist_equivalent: gist:Event
content_hash: 9f7c298e53689bcf23b6eb0cdaac3531ae279429615732f72f21e876834c353f
hypercube_context:
  primary_hypercube: StatementOfComprehensiveIncome
  arrangement_pattern: RollUp
integrity:
  source_uri: null
  content_hash: 8df75cc0d5e58dec35037bcee77dce0d9acadcb39241dc70499290c5533ff771
parameters_exposed: {}
fact_value: 20000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026-duration
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-profit-loss
value: 45000.0
---







# Fact: Profit & Loss (2026 Duration)
For the 2026 duration, the entity generated a Net Profit of $20,000.00 AUD.