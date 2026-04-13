---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:39ea9fe5-91d9-4240-9aac-e0fef729c2c8
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
  content_hash: 4cc08311c4bcb120393a3250769ed9a08433273214a105aea9c4d6a329f9c7fb
value: 75000.0
edges:
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-cash-at-bank
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:period-2026
---
# Cash at Bank (Account: 1-1110)
Balance: 75000.0
Classification: CurrentAssets
Source: Legacy CSV Trial Balance Import
