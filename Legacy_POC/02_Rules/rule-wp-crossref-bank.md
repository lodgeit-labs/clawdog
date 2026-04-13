---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:rule-wp-crossref-bank
ontological_class: CalculationRule
gist_equivalent: gist:Directive
domain_tags:
- SBRM
- AuditRule
- CrossReference
integrity:
  source_uri: null
  content_hash: 6de11b38d470eb2843cce41ce37e110a75561381fc74858b516176609fb46e60
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
parameters_exposed:
  LedgerCash:
    sbrm_label: urn:uuid:def-sbr-cash-at-bank
  StatementCash:
    sbrm_label: urn:uuid:def-wp-bank-statement-balance
edges:
- rel: gist:appliesTo
  target: urn:uuid:def-sbrm-reporting-entity
---

# SBRM Working Paper Rule: Bank Reconciliation Cross-Reference

## Epistemological Definition (Logical English)
```logical-english
the working paper set is valid for bank cross-reference if
    the fact set has a LedgerCash value
    and the working paper set has a StatementCash value
    and the LedgerCash value is exactly the StatementCash value.
```