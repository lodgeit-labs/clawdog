---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:6c44b760-f1f9-43d3-8cbb-38654f92cc7a
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
  content_hash: 0c3d1325e62326c50dbda1777bdbf85c2a27cf02be673484275348e41d2dc60c
value: 45000.0
edges:
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-retained-earnings
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:period-2026
---
# Retained Earnings (Account: 3-1000)
Balance: 45000.0
Classification: TotalEquity
Source: Legacy CSV Trial Balance Import
