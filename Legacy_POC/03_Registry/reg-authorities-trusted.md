---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:registry-authorities-trusted
ontological_class: RegistryIndex
gist_equivalent: gist:Category
domain_tags:
- SBRM
- System
- Cryptography
- Trust
integrity:
  source_uri: null
  content_hash: 9ea635216e1c5156799ab5906fd998d50e5db89a982bea6cace2bf1632644f7d
parameters_exposed: {}
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
trusted_publishers:
- id: urn:uuid:auth-publisher-001
  cryptographic_uri: nostr:pubkey:a1b2c3d4e5f6g7h8i9j0
  human_readable_name: Open Source SBRM Working Group
  role: Core Ontology Maintainer
- id: urn:uuid:auth-publisher-002
  cryptographic_uri: nostr:pubkey:x9y8z7w6v5u4t3s2r1q0
  human_readable_name: Reporting Entity A
  role: Financial Fact Publisher
---

# Trusted Authority Registry

This registry maps decentralized cryptographic identifiers (such as Nostr public keys or DID documents) to known network participants. Logic engines must reference this index to verify the `source_authority` of incoming Fact Nodes before permitting them to bind to the hypercube.