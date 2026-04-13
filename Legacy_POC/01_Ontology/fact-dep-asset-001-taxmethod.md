---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:asset-001-taxmethod"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:method"

temporal_context:
  type: "Instant" 
  as_at_date: "2015-01-30T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-dep-tax-method"
  value: "dv"
  currency: "ENUM"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://Depreciation_Transforms/dep_assets.csv"
  content_hash: "9230ae9678de6661a0b8ed92c9437158e310903f7bb2c5a65af1c365699805aa"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# Depreciation Fact: method
This node represents an objective financial parameter extracted from the legacy Depreciation Ledger.
