---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:rule-depreciation-audit"
ontological_class: "CalculationRule"
gist_equivalent: "gist:Directive"
domain_tags:
  - SBRM
  - Depreciation
  - Assets

integrity:
  source_uri: null
  content_hash: "3366983b18b64461251f2ab44897a66c3262b88c02c4147c60543894a47d1f34"

execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null

edges:
  - rel: gist:appliesTo
    target: "urn:uuid:def-sbrm-reporting-entity"
---

# SBRM Depreciation Rule: Asset Audit & Variance Detection

## Epistemological Definition (Logical English)
```logical-english
the Depreciation Audit is valid if
    the fact set has an OriginalCost value
    and the fact set has a PurchaseDate value
    and the fact set has a CurrentAccumDep value
    and the TargetAccumDep matches the simulated Straight-Line WDV to the transition date.
```
