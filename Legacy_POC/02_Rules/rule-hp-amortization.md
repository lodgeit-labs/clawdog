---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:rule-hp-amortization"
ontological_class: "CalculationRule"
gist_equivalent: "gist:Directive"
domain_tags:
  - SBRM
  - HirePurchase
  - Finance

integrity:
  source_uri: null
  content_hash: "79a43283e57722de40514c4cfff0f04ca9534e9e119f5a16d8c69345948f3177"

execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null

parameters_exposed:
  PrincipalAmount:
    sbrm_label: "urn:uuid:def-hp-principal"
  AnnualInterestRate:
    sbrm_label: "urn:uuid:def-hp-annual-rate"
  TermMonths:
    sbrm_label: "urn:uuid:def-hp-term-months"

edges:
  - rel: gist:appliesTo
    target: "urn:uuid:def-sbrm-reporting-entity"
---

# SBRM Hire Purchase Rule: Full Amortization Schedule

## Epistemological Definition (Logical English)
```logical-english
the HP Amortization Schedule is valid if
    the fact set has a PrincipalAmount value
    and the fact set has an AnnualInterestRate value
    and the fact set has a TermMonths value
    and the Schedule reflects exactly the regular PMT reduction plus balloon impacts.
```
