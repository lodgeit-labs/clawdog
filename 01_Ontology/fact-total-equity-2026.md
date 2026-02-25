---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-total-equity-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:InformationElement
domain_tags:
- SBRM
- BalanceSheet
- Equity
fact_value: 45000.0
fact_unit: AUD
fact_decimals: 2
fact_rounding: inf
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-total-equity
hypercube_context:
  primary_hypercube: StatementOfChangesInEquity
  arrangement_pattern: RollForward
integrity:
  source_uri: null
  source_authority: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  staleness_flag: false
  content_hash: 114d1672cc23db726c2be25bbddb3994b2cba22a857afdb2b50c92cf3a755800
parameters_exposed: {}
value: 125000.0
---





# Fact: Total Equity
As of the 2026 reporting period, the entity holds Total Equity valued at $45,000.00 AUD.