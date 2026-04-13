---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:def-sbrm-reporting-entity
ontological_class: StatutoryDefinition
gist_equivalent: gist:LegalEntity
domain_tags:
- SBRM
- OIM
- Governance
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
parameters_exposed: {}
edges:
- rel: gist:isContainedIn
  target: ipfs://bafybeig...[SBRM_Report_Frame_CID]
- rel: gist:hasPart
  target: urn:uuid:def-sbrm-entity-identifier
hypercube_context:
  primary_hypercube: System_Ontology_Definition
  arrangement_pattern: SemanticLink
integrity:
  source_authority: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  source_uri: urn:uuid:def-sbrm-reporting-entity
  validity_horizon: null
  staleness_flag: false
  content_hash: abb52ee94afd41530fd1172ac2c399f5c7772c63b0bab9aae56e3b51f714945d
economics:
  author_id: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  payment_pointer: null
  l402_rate: 0
  access_tier: public_infrastructure
---

# SBRM: Reporting Entity

## 1. Raw Source Text
A **Reporting Entity** (or Economic Entity) is a specific organizational unit for which a financial report is prepared. It serves as the primary identifier dimension in the OIM (Open Information Model), ensuring that every fact is uniquely attributed to a legal or economic body.

## 2. Ontological Commentary
In the Seattle Method, the Reporting Entity is the anchor of the **Report Frame**. It provides the context required to disambiguate facts that share the same Concept and Period. For example, "Total Assets" is only a valid fact when bound to a specific Reporting Entity. Under the Gist Upper Ontology, this maps to `gist:LegalEntity` (or `gist:Organization` for non-legal units), providing a domain-agnostic link to broader enterprise ontologies.

## 3. Epistemological Definition (Logical English)
```logical-english
% Epistemic Definition: Reporting Entity

a unit is a reporting entity if
    the unit is a gist organization
    and the unit has a unique identifier
    and the unit is the subject of a financial report frame.

a unit is a legal entity if
    the unit is a reporting entity
    and the unit is recognized by a statutory authority.
```