---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-current-assets-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:MonetaryAmount
domain_tags:
- SBRM
- BalanceSheet
execution_parameters: {}
parameters_exposed: {}
fact_value: 50000.0
fact_unit: AUD
fact_decimals: 2
fact_rounding: inf
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-current-assets
hypercube_context:
  primary_hypercube: StatementOfFinancialPosition
  arrangement_pattern: Hierarchy
integrity:
  source_authority: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  staleness_flag: false
  source_uri: null
  content_hash: f8b413994a205b54548df7a614db251ee2f595602a48679ae783c3135c5d2547
value: 160000.0
---





# Fact: Current Assets
As of the 2026 reporting period, the entity holds Current Assets valued at $50,000.00 AUD.