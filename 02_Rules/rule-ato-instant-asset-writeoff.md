---
'@context': ipfs://bafkreifcontext...[Base_Context]
'@id': urn:uuid:rule-ato-instant-asset-writeoff
ontological_class: JurisdictionalDirective
gist_equivalent: gist:Directive
domain_tags:
- SBRM
- Tax-Logic
- ATO
jurisdictional_context:
  required_namespace: urn:uuid:registry-namespace-au
  authority: Australian Taxation Office
parameters_exposed:
  AssetCost:
    sbrm_label: urn:uuid:def-sbr-plant-at-cost
  ThresholdLimit:
    static_value: 20000.0
  TaxDeduction:
    sbrm_label: urn:uuid:def-ato-tax-deduction-amount
edges:
- rel: gist:appliesTo
  target: urn:uuid:def-sbrm-reporting-entity
- rel: gist:isGovernedBy
  target: urn:uuid:registry-namespace-au
integrity:
  source_uri: internal://architect/02_rules/ato_iawo
  content_hash: ecd4c7d437cee5232f97684753d5f22b22ffb6b9230b51d2a1a57514f17beb8e
  validity_horizon: Perpetual
  staleness_flag: false
---

# RULE: ATO INSTANT ASSET WRITE-OFF (IAWO)

## 1. Ontological Purpose
This directive computes the allowable tax deduction for a fixed asset under the Australian Taxation Office (ATO) Instant Asset Write-Off provisions.

## 2. Deterministic Logic (Logical English)
* IF the Reporting Entity is governed by the `AU` Jurisdictional Namespace
* AND the `AssetCost` is less than or equal to the `ThresholdLimit` (e.g., $20,000 AUD)
* THEN the `TaxDeduction` equals the total `AssetCost`.
* ELSE the `TaxDeduction` falls back to the standard SBRM GAAP depreciation schedule.

## 3. Prolog Execution Mapping
This node exposes the parameters required for `jurisdictional_router.pl` to evaluate the asset against the local tax threshold, overriding the base multidimensional rollup where applicable.