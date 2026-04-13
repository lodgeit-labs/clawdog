---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:3e1651b3-65d3-41b3-8bb3-31c38ca18371
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
  primary_hypercube: StatementOfFinancialPosition
  arrangement_pattern: Hierarchy
integrity:
  source_uri: internal://ingestion/csv/trial_balance
  content_hash: c4aafeadee051d1873898c928a46ce03bf29028bf336cdb06f76e2220f6ca906
value: 30000.0
edges:
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-accounts-payable
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:period-2026
---
# Accounts Payable (Account: 2-2100)
Balance: 30000.0
Classification: CurrentLiabilities
Source: Legacy CSV Trial Balance Import
