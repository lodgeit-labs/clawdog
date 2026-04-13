---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:registry-namespace-au
ontological_class: JurisdictionalNamespace
gist_equivalent: gist:GeographicRegion
domain_tags:
- SBRM
- Jurisdiction
- ATO
- Australia
execution_parameters: null
parameters_exposed: null
edges:
- rel: gist:isContainedIn
  target: urn:uuid:reg-namespaces-core
- rel: gist:isGovernedBy
  target: urn:uuid:reg-authorities-trusted
integrity:
  source_uri: internal://architect/03_registry/namespace_au
  content_hash: 487e0e77423e8ecca874a4321ba9deb5bdb56153fe1f3b45519f0a19da340958
  validity_horizon: Perpetual
  staleness_flag: false
economics:
  author_id: The_Ontologist
  payment_pointer: null
  l402_rate: 0
  access_tier: foundational_infrastructure
---

# REGISTRY: AUSTRALIAN JURISDICTIONAL NAMESPACE (AU)

## 1. Ontological Boundary
This node establishes the `AU` jurisdictional namespace for the SBRM hypercube. It acts as a semantic boundary for evaluating localized taxation and corporate compliance rules governed by the Australian Taxation Office (ATO) and the Australian Securities & Investments Commission (ASIC).

## 2. Dimensional Routing Parameters
When the SWI-Prolog inference engine detects an entity or reporting period tagged with this namespace, it MUST execute the AU-specific deductive predicates alongside the universal base SBRM rules.

* **Base Currency:** `AUD`
* **Governing Authority:** Australian Taxation Office (ATO)
* **Namespace Prefix:** `sbrm-au:`

## 3. Associated Rule Sets
This namespace governs the execution of divergent tax treatments, including but not limited to:
* Instant Asset Write-Off (ATO Specific)
* R&D Tax Incentive Offsets
* GST/BAS Roll-ups