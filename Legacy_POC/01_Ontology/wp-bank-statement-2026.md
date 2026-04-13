---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:wp-bank-statement-sample-001
ontological_class: WorkingPaperFact
domain_tags:
- SBRM
- AuditEvidence
- BankReconciliation
gist_equivalent: gist:Fact
hypercube_context:
  primary_hypercube: WorkingPaper_BankReconciliation
  arrangement_pattern: CrossReference
integrity:
  source_uri: null
  content_hash: 58a141142b071bf871d19eff8ea492e781b532d3fbb9aa6c3151b82c2d1f0a58
parameters_exposed: {}
fact_value: 50000.0
fact_unit: AUD
edges:
- rel: sbrm:hasReportingEntity
  target: urn:uuid:def-sbrm-reporting-entity
- rel: sbrm:hasReportingPeriod
  target: urn:uuid:def-sbrm-reporting-period-2026
- rel: sbrm:isInstanceOfConcept
  target: urn:uuid:def-wp-bank-statement-balance
- rel: prov:wasDerivedFrom
  target: ipfs://[CID_of_Scanned_Bank_Statement_PDF]
---

# Working Paper: Bank Statement Balance
Per the external bank statement provided by the institution, the balance is $50,000.00 AUD.