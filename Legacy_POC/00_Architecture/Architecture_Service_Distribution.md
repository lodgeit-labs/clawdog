---
"@id": "urn:uuid:service-distribution-layer-lodgeit-global"
ontological_class: "Documentation"
gist_equivalent: "gist:Service"
service_type: "Logic-as-a-Service (LaaS)"
access_protocol: "L402 / Lightning Network"
integrity:
  content_hash: "[SHA-256 injected at commit]"
---

# Service Distribution: LodgeiT Global Logic Fleet

## 1. The Consumption Model
External consumers do not need to understand SBRM or Prolog. They simply "POST" a JSON-LD payload to the LodgeiT Fleet and receive a validated, logically-proven result.

### Endpoint Architecture
* **Ingestion:** API Gateway (AWS) accepts JSON-LD facts.
* **Processing:** Warm-start SWI-Prolog Lambda functions.
* **Caching:** Results stored in the Global SBRM Caching Tier for rapid re-validation.

## 2. Monetization & Access (L402)
To ensure this is a "Global Fleet," access is governed by the **L402 protocol** (formerly LSAT):
* **Authentication:** Macaroons used for decentralized authorization.
* **Payment:** Micropayments per logic-inference or per-kilobyte of proof.
* **Tiers:** * *Standard:* General accounting equation validation.
  * *Premium:* Cross-jurisdictional tax optimization logic.

## 3. The "Plug" for External Epistemologies
Third-party developers can "Subscribe" to specific **Registries** (from `03_Registry`) to interpret their own data through the LodgeiT lens.