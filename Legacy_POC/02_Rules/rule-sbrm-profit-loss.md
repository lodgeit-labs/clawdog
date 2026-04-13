---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:rule-sbrm-profit-loss
ontological_class: CalculationRule
gist_equivalent: gist:Directive
domain_tags:
- SBRM
- IncomeStatement
integrity:
  source_uri: null
  content_hash: 741a1eb9a90adf8d50346c1db163fa5410d5e61890bfa5b11a660434892d3173
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
parameters_exposed:
  Revenue:
    sbrm_label: urn:uuid:def-sbr-revenue
  Expenses:
    sbrm_label: urn:uuid:def-sbr-expenses
  ProfitLoss:
    sbrm_label: urn:uuid:def-sbr-profit-loss
edges:
- rel: gist:appliesTo
  target: urn:uuid:def-sbrm-reporting-entity
---

# SBRM Consistency Rule: Profit & Loss

## Epistemological Definition (Logical English)
```logical-english
the fact set is valid for profit and loss if
    the fact set has a Revenue value
    and the fact set has an Expenses value
    and the fact set has a ProfitLoss value
    and the ProfitLoss value is exactly the Revenue value - the Expenses value.
```