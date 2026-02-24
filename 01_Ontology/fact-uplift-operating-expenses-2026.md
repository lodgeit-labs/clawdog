---
"@context": "ipfs://bafkreifcontext...[Base_Context]"
"@id": "urn:uuid:86b31237-d57b-48d8-8a22-65ce3c62cda3"
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
  primary_hypercube: "StatementOfComprehensiveIncome"
  arrangement_pattern: "RollUp"

integrity:
  source_uri: "internal://ingestion/csv/trial_balance"
  content_hash: "bc464a8857581685712e1aca8c5e45413514028fe20faf62824e03272292a279"
---

# Operating Expenses (Account: 5-1000)
Balance: 75000.0
Classification: Expenses
Source: Legacy CSV Trial Balance Import
