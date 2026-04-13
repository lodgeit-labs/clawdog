---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:rule-sbrm-revenue-fanout
ontological_class: CalculationRule
domain_tags":
- SBRM
- IncomeStatement
- DimensionalAggregation
gist_equivalent: gist:Directive
integrity:
  source_uri: null
  content_hash: 9146073b5938e947db3fa0eb15ff17398f415ad24ba46ba7609c7e79660ddda4
execution_parameters:
  payload_format: Hybrid-LE-Prolog
parameters_exposed:
  TotalRevenue:
    sbrm_label: urn:uuid:def-sbr-revenue
  RevRed:
    sbrm_label: urn:uuid:def-sbr-revenue-red
  RevBlue:
    sbrm_label: urn:uuid:def-sbr-revenue-blue
  RevGreen:
    sbrm_label: urn:uuid:def-sbr-revenue-green
  RevYellow:
    sbrm_label: urn:uuid:def-sbr-revenue-yellow
edges:
- rel: gist:appliesTo
  target: urn:uuid:def-sbrm-reporting-entity
---

# SBRM Consistency Rule: Revenue Dimensional Fan-Out

## Epistemological Definition (Logical English)
```logical-english
the fact set is valid for dimensional aggregation if
    the fact set has a TotalRevenue value
    and the fact set has a RevRed value
    and the fact set has a RevBlue value
    and the fact set has a RevGreen value
    and the fact set has a RevYellow value
    and the TotalRevenue value is exactly the RevRed value + the RevBlue value + the RevGreen value + the RevYellow value.
```