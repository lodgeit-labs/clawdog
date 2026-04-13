---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:asset-001-cost"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:cost"

temporal_context:
  type: "Instant" 
  as_at_date: "2015-01-30T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-dep-cost"
  value: 26255
  currency: "AUD"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://Depreciation_Transforms/dep_assets.csv"
  content_hash: "66967a40b31956587dbcbf6d0705a1fc8f526c436d13bcd7f44cc49f268dcb6e"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# Depreciation Fact: cost
This node represents an objective financial parameter extracted from the legacy Depreciation Ledger.
