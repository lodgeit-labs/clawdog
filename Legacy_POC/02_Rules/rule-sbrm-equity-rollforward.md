---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:rule-sbrm-equity-rollforward
ontological_class: CalculationRule
domain_tags:
- SBRM
- EquityStatement
gist_equivalent: gist:Directive
integrity:
  source_uri: null
  content_hash: d969d1efe729f866b5d1270ed6aaf3d3c29eb5bdcb7dfd3b6ea18f6416f94d26
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
parameters_exposed:
  OpeningEquity:
    sbrm_label: urn:uuid:def-sbr-opening-equity
  ProfitLoss:
    sbrm_label: urn:uuid:def-sbr-profit-loss
  Dividends:
    sbrm_label: urn:uuid:def-sbr-dividends-paid
  ClosingEquity:
    sbrm_label: urn:uuid:def-sbr-total-equity
edges:
- rel: gist:appliesTo
  target: urn:uuid:def-sbrm-reporting-entity
---

# SBRM Consistency Rule: Equity Roll-Forward

## Epistemological Definition (Logical English)
```logical-english
the fact set is valid for equity roll-forward if
    the fact set has an OpeningEquity value
    and the fact set has a ProfitLoss value
    and the fact set has a Dividends value
    and the fact set has a ClosingEquity value
    and the ClosingEquity value is exactly the OpeningEquity value + the ProfitLoss value - the Dividends value.
```