---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-total-liabilities-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:MonetaryAmount
domain_tags:
- SBRM
- BalanceSheet
execution_parameters: {}
parameters_exposed: {}
fact_value: 80000.0
fact_unit: AUD
fact_decimals: 2
fact_rounding: inf
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-total-liabilities
hypercube_context:
  primary_hypercube: StatementOfFinancialPosition
  arrangement_pattern: Hierarchy
integrity:
  source_uri: null
  source_authority: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  staleness_flag: false
  content_hash: 29c0b805cbebffdbc6b077c9fc0c2179780d790f8f710c650b82fa2fd4b11d83
value: 110000.0
content_hash: 367f19850cbbd1b2128f1d238d57f887eb4a968a195075fcaf2eea4fd89a1cf1
---







# Fact: Total Liabilities
As of the 2026 reporting period, the entity holds Total Liabilities valued at $80,000.00 AUD.