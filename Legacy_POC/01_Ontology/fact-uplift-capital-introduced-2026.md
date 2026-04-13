---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:72f40714-e6c6-4e0d-a224-1c2ff9f98427
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
  primary_hypercube: StatementOfChangesInEquity
  arrangement_pattern: RollForward
integrity:
  source_uri: internal://ingestion/csv/trial_balance
  content_hash: 9da8fd59f0511a4fc7fdf77fa98324d15e95261e21c1f6dfd47189560fa607bb
value: 10000.0
edges:
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-capital-introduced
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:period-2026
---
# Capital Introduced (Account: 3-1100)
Balance: 10000.0
Classification: TotalEquity
Source: Legacy CSV Trial Balance Import
