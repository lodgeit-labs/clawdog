---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:loan-L001-rate"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:def-div7a-benchmark-rate"

temporal_context:
  type: "Instant" 
  as_at_date: "2024-07-01T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-div7a-benchmark-rate"
  value: 0.0877
  currency: "RATE"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://Div7A_Calculator/loan_params.csv"
  content_hash: "d10a821d798543bfb89d4a48bc8ec22e507b01340acdcf1ffb39c9a067bf4ba1"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# Div7A Fact: def-div7a-benchmark-rate
This node represents an objective financial parameter extracted from the Div7A loan parameters CSV.
