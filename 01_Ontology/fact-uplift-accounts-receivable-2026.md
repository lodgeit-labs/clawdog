---
"@context": "ipfs://bafkreifcontext...[Base_Context]"
"@id": "urn:uuid:7a461d6c-cb64-4d54-ba1d-b9e51b0dac85"
ontological_class: "FinancialFact"
gist_equivalent: "gist:Magnitude"
domain_tags:
  - "SBRM"
  - "Trial-Balance-Ingestion"
  - "Uplifted-Fact"

project_context:
  reporting_entity: "urn:uuid:entity-lodgeit-demo"
  reporting_period: "urn:uuid:period-2026"

hypercube_context:
  primary_hypercube: "StatementOfFinancialPosition"
  arrangement_pattern: "Hierarchy"

integrity:
  source_uri: "internal://ingestion/csv/trial_balance"
  content_hash: "7a522f7af2c7f0a7b9dfc9d2bc744625bac7879a573c6e0c738c2253d16c7952"
---

# Accounts Receivable (Account: 1-1200)
Balance: 25000.0
Classification: CurrentAssets
Source: Legacy CSV Trial Balance Import
