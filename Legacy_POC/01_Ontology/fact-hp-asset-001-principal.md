---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:asset-001-principal"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:principal"

temporal_context:
  type: "Instant" 
  as_at_date: "2021-04-06T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-hp-principal"
  value: 252450
  currency: "AUD"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://HP_Calculator/HP_Input.csv"
  content_hash: "bd15f79b4beee81532b2b14f25bcb56579b37f753ac02cd2ca2e3b2f2eda6917"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# HP Fact: principal
This node represents an objective financial parameter extracted from the HP Loan parameters CSV.
