---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:asset-001-term"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:months"

temporal_context:
  type: "Instant" 
  as_at_date: "2021-04-06T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-hp-term-months"
  value: 59
  currency: "MONTHS"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://HP_Calculator/HP_Input.csv"
  content_hash: "35e2933554b54ddf9213072d7d18a78e884ff49359cd6e5ae32fc2faa1d33052"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# HP Fact: months
This node represents an objective financial parameter extracted from the HP Loan parameters CSV.
