---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:rule-sbrm-fixed-assets-net
ontological_class: CalculationRule
gist_equivalent: gist:Directive
domain_tags:
- SBRM
- FixedAssets
- NetBookValue
content_hash: febb658e2319c2d1fa9c4e7a3a39f06bb526f69fa7df860e78ede0c6e006773e
integrity:
  source_uri: null
  content_hash: ec883f6fc0076210d76e6c15677d07dfcd305732323b2a217de93030a42d1ccc
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
parameters_exposed:
  PlantAtCost:
    sbrm_label: urn:uuid:def-sbr-plant-at-cost
  AccumulatedDep:
    sbrm_label: urn:uuid:def-sbr-accumulated-depreciation
  NonCurrentAssets:
    sbrm_label: urn:uuid:def-sbr-non-current-assets
edges:
- rel: gist:appliesTo
  target: urn:uuid:def-sbrm-reporting-entity
---

# SBRM Consistency Rule: Net Fixed Assets

## Epistemological Definition (Logical English)
```logical-english
the fact set is valid for net fixed assets if
    the fact set has a PlantAtCost value
    and the fact set has an AccumulatedDep value
    and the fact set has a NonCurrentAssets value
    and the NonCurrentAssets value is exactly the PlantAtCost value - the AccumulatedDep value.
```