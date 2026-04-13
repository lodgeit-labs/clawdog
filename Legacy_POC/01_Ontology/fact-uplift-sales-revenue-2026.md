---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:08fcb05b-1688-4723-a0a8-cf9e07f07f44
ontological_class: FinancialFact
gist_equivalent: gist:Magnitude
domain_tags:
- SBRM
- Trial-Balance-Ingestion
- Uplifted-Fact
project_context:
  reporting_entity: urn:uuid:entity-lodgeit-demo
  reporting_period: urn:uuid:period-2026
hypercube_context:
  primary_hypercube: StatementOfComprehensiveIncome
  arrangement_pattern: RollUp
integrity:
  source_uri: internal://ingestion/csv/trial_balance
  content_hash: 715c39fd7d3b92182e078869d200f05e4124889973cf73dbdc8a3aba97f3e6f2
value: 100000.0
edges:
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-sales-revenue
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:period-2026
---
# Sales Revenue (Account: 4-1000)
Balance: 100000.0
Classification: TotalRevenue
Source: Legacy CSV Trial Balance Import
