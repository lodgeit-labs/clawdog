---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:registry-namespaces-core
ontological_class: RegistryIndex
gist_equivalent: gist:Category
domain_tags:
- SBRM
- System
- Namespaces
integrity:
  source_uri: null
  content_hash: 378f57234719362cb980ada4599c32145e660390bd5280cbc1f821a593eb914d
parameters_exposed: {}
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
namespaces:
- prefix: sbrm
  uri: http://www.xbrl.org/wg/sbrm/core#
  description: Standard Business Reporting Model core vocabulary
- prefix: gist
  uri: https://ontologies.semanticarts.com/gist#
  description: Gist minimal upper ontology for enterprise semantic models
- prefix: oim
  uri: http://www.xbrl.org/wg/oim/core#
  description: Open Information Model vocabulary
---

# Core Namespace Registry

This registry index explicitly defines the base URIs for all semantic prefixes used within the SBRM hypercube. By maintaining this registry locally, agents can dynamically resolve shorthand prefixes into their full, globally addressable URIs.