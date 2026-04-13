---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:asset-001-rate"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:rate"

temporal_context:
  type: "Instant" 
  as_at_date: "2021-04-06T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-hp-annual-rate"
  value: 0.0399
  currency: "RATE"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://HP_Calculator/HP_Input.csv"
  content_hash: "57de8bff0716240784f747496ad9be7d282b67d0e9eed36999a1adfa221df6d4"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# HP Fact: rate
This node represents an objective financial parameter extracted from the HP Loan parameters CSV.
