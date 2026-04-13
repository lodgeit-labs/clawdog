---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:registry-access-control-l402
ontological_class: AccessRegistry
gist_equivalent: gist:License
domain_tags:
- L402
- Lightning-Network
- Monetization
- API-Gateway
project_context:
  platform: LodgeiT / ClientRelay Global Fleet
  objective: Decentralized logic execution metering via cryptographically attenuated
    macaroons.
integrity:
  source_uri: internal://architect/03_registry/access-control
  content_hash: 80b90300620962241b484cbab4aa23a121e3f537d424bfd0ecb6ddeca94e2038
economics:
  payment_pointer: lnurlp:logic-fleet@clientrelay.node
  settlement_layer: Bitcoin Lightning Network
  base_currency: Sats
api_tiers:
  Foundational_Read:
    sbrm_scope: 01_Ontology
    cost_per_query_sats: 0
    macaroon_caveat: methods=GET, target=facts
  Standard_Proof:
    sbrm_scope: 02_Rules_Basic
    cost_per_query_sats: 50
    macaroon_caveat: methods=POST, target=equation_proofs
  Complex_Fanout:
    sbrm_scope: 02_Rules_Dimensional
    cost_per_query_sats: 150
    macaroon_caveat: methods=POST, target=dimensional_rollups
---

# Registry: L402 Access Control & Metering
This node governs the pricing for the LodgeiT global logic fleet.