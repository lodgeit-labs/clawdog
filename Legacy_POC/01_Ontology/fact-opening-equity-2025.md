---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-opening-equity-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:Fact
domain_tags":
- SBRM
- Equity
- RollForward
hypercube_context:
  primary_hypercube: StatementOfChangesInEquity
  arrangement_pattern: RollForward
integrity:
  source_uri: null
  content_hash: 6bc25281bbd058c42391679304673083770a9aafa2a6cbbe9f1a0c7ea3d15a64
parameters_exposed: {}
fact_value: 30000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2025
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-opening-equity
---

# Fact: Opening Equity (2025)
As of the 2025 reporting period, the entity held Opening Equity valued at $30,000.00 AUD.