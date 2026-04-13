---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-non-current-assets-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:MonetaryAmount
domain_tags:
- SBRM
- BalanceSheet
execution_parameters: {}
parameters_exposed: null
fact_value: 75000.0
fact_unit: AUD
fact_decimals: 2
fact_rounding: inf
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-non-current-assets
hypercube_context:
  primary_hypercube: StatementOfFinancialPosition
  arrangement_pattern: Hierarchy
integrity:
  source_authority: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  staleness_flag: false
  source_uri: null
  content_hash: "[SHA-256 injected at commit]"
---

# Fact: Non-Current Assets
As of the 2026 reporting period, the entity holds Non-Current Assets valued at $75,000.00 AUD.