---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:def-sbrm-reporting-period
ontological_class: StatutoryDefinition
gist_equivalent: gist:TemporalRelation
domain_tags:
- SBRM
- OIM
- Time
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
parameters_exposed: {}
edges:
- rel: gist:isContainedIn
  target: ipfs://bafybeig...[SBRM_Report_Frame_CID]
- rel: gist:refersTo
  target: urn:uuid:def-sbrm-reporting-entity
hypercube_context:
  primary_hypercube: System_Ontology_Definition
  arrangement_pattern: SemanticLink
integrity:
  content_hash: c2554304d366f71117c8b9159710ebead78be26a6c1e3e2efb2bb813411b3689
  source_authority: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  source_uri: null
  validity_horizon: null
  staleness_flag: false
economics:
  author_id: nostr:pubkey:a1b2c3d4...[LodgeiT_Hex_Pubkey]
  payment_pointer: null
  l402_rate: 0
  access_tier: public_infrastructure
---

# SBRM: Reporting Period

## 1. Raw Source Text
A **Reporting Period** is the specific time interval or point-in-time to which a financial fact applies. In SBRM, this typically distinguishes between "Instant" facts (e.g., Balance Sheet items at a specific date) and "Duration" facts (e.g., Income Statement items over a year).

## 2. Ontological Commentary
This node provides the temporal context for the **Report Frame**. It allows the logic engine to distinguish between different iterations of the same concept (e.g., Total Assets for 2025 vs. 2026). In the Gist ontology, this maps to `gist:TemporalRelation`, ensuring that the period is treated as a first-class dimensional object rather than a simple string.

## 3. Epistemological Definition (Logical English)
```logical-english
a period is a reporting period if
    the period is a gist temporal relation
    and the period has a start date
    and the period has an end date
    and the period is associated with a financial report frame.

an instant is a reporting period if
    the instant is a gist temporal relation
    and the instant has a single point in time.
```