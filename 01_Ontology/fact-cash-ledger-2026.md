---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:fact-cash-ledger-sample-001
ontological_class: FinancialFact
domain_tags:
- SBRM
- TrialBalance
- Asset
gist_equivalent: gist:Fact
hypercube_context:
  primary_hypercube: StatementOfFinancialPosition
  arrangement_pattern: Hierarchy
integrity:
  source_uri: urn:uuid:fact-cash-ledger-sample-001
  content_hash: 41a4e696a623be07234369f061487d0ee888be98e7da00820ed56c4dea114ab1
parameters_exposed: {}
fact_value: 50000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-sbr-cash-at-bank
value: 50000.0
content_hash: fb81a1375d425611d9639e04b5935a2a79095fdd607cefb0634b6c0c8b94de6a
---





# Fact: Cash at Bank (Ledger)
Per the internal trial balance, the Cash at Bank account holds $50,000.00 AUD.