---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:asset-001-name"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:name"

temporal_context:
  type: "Instant" 
  as_at_date: "2015-01-30T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-dep-name"
  value: "Toyota"
  currency: "STR"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://Depreciation_Transforms/dep_assets.csv"
  content_hash: "48af90228eb05988dde32ab6600243a74ab44cce440281b779bb72b369192652"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# Depreciation Fact: name
This node represents an objective financial parameter extracted from the legacy Depreciation Ledger.
