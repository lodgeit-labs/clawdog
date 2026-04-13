---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:loan-L001-principal"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:def-div7a-amalgamated-loan"

temporal_context:
  type: "Instant" 
  as_at_date: "2024-07-01T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-div7a-amalgamated-loan"
  value: 100000
  currency: "AUD"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://Div7A_Calculator/loan_params.csv"
  content_hash: "22da1bddfe4d2b6eaabe9d61425bb68a1c2a9239bf2cfc583afd8d666f0dbf17"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# Div7A Fact: def-div7a-amalgamated-loan
This node represents an objective financial parameter extracted from the Div7A loan parameters CSV.
