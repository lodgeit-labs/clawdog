---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:rule-sbrm-accounting-equation
ontological_class: CalculationRule
gist_equivalent: gist:Directive
domain_tags:
- SBRM
- AccountingEquation
integrity:
  source_uri: null
  content_hash: 2b68eaa10b5450c4cfc9b095c46962ffd54f0d2e985ea34172b5d4af5c4c22f9
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
parameters_exposed:
  TotalAssets:
    sbrm_label: urn:uuid:def-sbr-total-assets
  TotalLiabilities:
    sbrm_label: urn:uuid:def-sbr-total-liabilities
  TotalEquity:
    sbrm_label: urn:uuid:def-sbr-total-equity
edges:
- rel: gist:appliesTo
  target: urn:uuid:def-sbrm-reporting-entity
- rel: gist:appliesTo
  target: urn:uuid:def-sbrm-reporting-period
---

# SBRM Consistency Rule: Fundamental Accounting Equation

## Epistemological Definition (Logical English)
```logical-english
the fact set is valid for the accounting equation if
    the fact set has a TotalAssets value
    and the fact set has a TotalLiabilities value
    and the fact set has a TotalEquity value
    and the TotalAssets value is exactly the TotalLiabilities value + the TotalEquity value.
```