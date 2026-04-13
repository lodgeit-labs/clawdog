---
'@context': https://schema.clientrelay.io/v1/context.jsonld
'@id': urn:uuid:registry-sbrm-master-ruleset
ontological_class: RuleRegistry
gist_equivalent: gist:Collection
domain_tags:
- SBRM
- OperativeLogic
- MasterIndex
execution_parameters:
  payload_format: null
  execution_context: null
  shacl_shape_ref: null
parameters_exposed: {}
edges:
- rel: gist:hasPart
  target: urn:uuid:rule-sbrm-accounting-equation
- rel: gist:hasPart
  target: urn:uuid:rule-sbrm-asset-rollup
- rel: gist:hasPart
  target: urn:uuid:rule-sbrm-equity-rollforward
- rel: gist:hasPart
  target: urn:uuid:rule-sbrm-fixed-assets-net
- rel: gist:hasPart
  target: urn:uuid:rule-sbrm-liability-rollup
- rel: gist:hasPart
  target: urn:uuid:rule-sbrm-profit-loss
- rel: gist:hasPart
  target: urn:uuid:rule-sbrm-revenue-fanout
- rel: gist:hasPart
  target: urn:uuid:rule-wp-crossref-bank
integrity:
  source_uri: internal://clientrelay/registry/master_ruleset
  content_hash: 06255f4e25a6f1cdbe9cce5c1f7e717a6641318f1325e6ce083f39ca0a1cb969
  validity_horizon: null
  staleness_flag: false
economics:
  author_id: System_Architect
  payment_pointer: null
  l402_rate: 0
  access_tier: public_infrastructure
---

# SBRM Master Rule Registry

## Ontological Commentary
This node acts as the definitive index of all operative calculation rules within the Open-Source SBRM hypercube. It does not contain executable payloads itself. Instead, the `edges` array cryptographically links to the atomic Markdown nodes residing in the `02_Rules` directory.

The Python-based universal logic engine must query this node first to retrieve the `@id` targets, subsequently loading only the required sub-graphs into active memory for deterministic execution.