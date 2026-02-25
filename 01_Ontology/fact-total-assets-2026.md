---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-total-assets-sample-001
ontological_class: FinancialFact
gist_equivalent: gist:MonetaryAmount
domain_tags:
- SBRM
- OIM
- BalanceSheet
parameters_exposed: {}
execution_parameters: null
fact_value: 125000.0
fact_unit: AUD
fact_decimals: 2
fact_rounding: inf
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-total-assets
hypercube_context:
  primary_hypercube: StatementOfFinancialPosition
  arrangement_pattern: Hierarchy
integrity:
  content_hash: 09bfd78d206b87a9cb112d3734f3d5113dc5127e25ebd7f49d1b7a58ff5d2d0b
  source_authority: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  validity_horizon: '2027-10-31'
  staleness_flag: false
  source_uri: null
economics:
  author_id: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  payment_pointer: null
  l402_rate: 0
  access_tier: private_ledger
value: 235000.0
---





# Fact: Total Assets (Sample)

## 1. Raw Source Text
As of the 2026 reporting period, the entity holds Total Assets valued at **$125,000.00 AUD**.

## 2. Ontological Commentary
This node represents a single point in the SBRM hypercube. It is not a rule; it is an assertion of reality. By linking to both the Entity and Period nodes, it inherits the context required for high-speed AI reasoning. If the Entity's legal status changes or the Period is redefined, this fact node remains cryptographically tied to its original context, preventing "context drift" in your accounting records.

## 3. Epistemological Definition (Logical English)
```logical-english
the fact 001 asserts that 
    the reporting entity has total assets of 125000.00 AUD
    at the reporting period 2026.
```