---
"@context": "ipfs://bafkreifcontext_base"
"@id": "urn:uuid:asset-001-date"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"

inherits_from_seed: "urn:sbrm:concept:date"

temporal_context:
  type: "Instant" 
  as_at_date: "2015-01-30T00:00:00Z"

parameters_exposed:
  concept: "urn:uuid:def-dep-purchase-date"
  value: "2015-01-30T00:00:00Z"
  currency: "DATE"
  arrangement_pattern: "Hierarchy"

cryptographic_anchor:
  source_file: "local://Depreciation_Transforms/dep_assets.csv"
  content_hash: "5129008ba2edc5ec7d9feeda0183d9dc0c86fed23bb16c5b42bbc496aaadc595"

cybernetic_state:
  status: "resolved" 
  prolog_trace_id: null
  error_vector: null
  helm_trigger: "autonomous-triage"
  human_override_required: false

helm_mutations: []
---

# Depreciation Fact: date
This node represents an objective financial parameter extracted from the legacy Depreciation Ledger.
