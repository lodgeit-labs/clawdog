---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-accumulated-depreciation-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:Fact
domain_tags:
- SBRM
- FixedAssets
- ContraAsset
fact_value: 25000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-accumulated-depreciation
hypercube_context:
  primary_hypercube: StatementOfFinancialPosition
  arrangement_pattern: Hierarchy
integrity:
  source_uri: null
  content_hash: 5b668f41bbc359974a89ea84a54dac129d1ea4f3326d766af423962988344325
parameters_exposed: {}
---

# Fact: Accumulated Depreciation
The accumulated depreciation against the Plant & Equipment is $25,000.00 AUD.