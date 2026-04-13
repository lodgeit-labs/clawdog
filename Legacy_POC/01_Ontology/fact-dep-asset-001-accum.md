---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:asset-001-accum"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:dep"

temporal_context:
  type: "Instant" 
  as_at_date: "2015-01-30T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-dep-accum-dep"
  value: 24934.04
  currency: "AUD"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://Depreciation_Transforms/dep_assets.csv"
  content_hash: "f7266a4c461539604b43bd03fdc9099bbce2f0f199416a62b5c973627540bb55"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# Depreciation Fact: dep
This node represents an objective financial parameter extracted from the legacy Depreciation Ledger.
