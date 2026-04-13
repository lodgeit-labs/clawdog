---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:rule-div7a-myr"
ontological_class: "CalculationRule"
gist_equivalent: "gist:Directive"
domain_tags:
  - SBRM
  - Div7A
  - TaxLaw

integrity:
  source_uri: null
  content_hash: "8bff4936d92a1725f0be5822ab0f5b718ddae27819b8b3a608f11270b66f8470"

execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null

parameters_exposed:
  AmalgamatedLoan:
    sbrm_label: "urn:uuid:def-div7a-amalgamated-loan"
  BenchmarkRate:
    sbrm_label: "urn:uuid:def-div7a-benchmark-rate"
  TermYears:
    sbrm_label: "urn:uuid:def-div7a-term-years"

edges:
  - rel: gist:appliesTo
    target: "urn:uuid:def-sbrm-reporting-entity"
---

# ATO Div7A Rule: Minimum Yearly Repayment (MYR)

## Epistemological Definition (Logical English)
```logical-english
the Div7A MYR is valid if
    the fact set has an AmalgamatedLoan value
    and the fact set has a BenchmarkRate value
    and the fact set has a TermYears value
    and the MYR is exactly (AmalgamatedLoan * BenchmarkRate) / (1 - (1 + BenchmarkRate)^(-TermYears)).
```
