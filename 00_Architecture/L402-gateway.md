---

## 🏗️ System Architecture

The architecture consists of three primary layers:
1.  **The Client Relay (Engagement Node):** Initiates requests and handles Lightning Network invoice payments.
2.  **The L402 Gateway (Middleware):** Intercepts requests, issues HTTP 402 invoices, verifies cryptographic preimages, and orchestrates the backend logic.
3.  **The SWI-Prolog Engine (Reasoner):** A deterministic multidimensional logic engine that evaluates standard business reports across multiple layers of integrity (OIM fidelity, Hypercube roll-ups, and core accounting equations).

### The Machine-to-Machine Flow
1.  **Request:** Client requests an SBRM proof.
2.  **Intercept (HTTP 402):** Gateway rejects unauthenticated requests, returning an HTTP 402 status, a Lightning Invoice, and a locked Macaroon.
3.  **Settlement:** Client pays the invoice via the Lightning Network, unlocking the cryptographic Preimage.
4.  **Verification:** Client resubmits the request with the `Macaroon:Preimage` token.
5.  **Execution (HTTP 200):** Gateway verifies the token, boots the SWI-Prolog engine, and returns the evaluated JSON-LD payload to the client.

---

## 📂 Core File Inventory

* **`l402_middleware.py`**
    * *Role:* The API Gateway and L402 Server.
    * *Function:* Listens on Port 8021. Manages the authorization headers, issues mock Lightning invoices, verifies payment tokens, and triggers the backend Prolog engine upon successful settlement.
* **`client_relay_ping.py`**
    * *Role:* The simulated remote client.
    * *Function:* Pings the gateway, handles the 402 rejection, simulates the payment of 1000 sats, parses the Macaroon, appends the Preimage, and successfully retrieves the final SBRM proof.
* **`evaluate_oim_report.py`**
    * *Role:* The core computational logic engine.
    * *Function:* A deterministic script (interfacing with SWI-Prolog) that evaluates multidimensional hypercubes. It validates Layer A (OIM Fidelity), Layer B (Hypercube Roll-Up Integrity), and Layer C (Multidimensional Accounting Logic).

---

## 🚀 Execution Instructions

To simulate the machine-to-machine micro-transactional flow locally, you require two terminal windows running simultaneously.

**Step 1: Initialize the Gateway**
Open Terminal 1 and start the L402 server. It will hang and listen on Port 8021.
> `python l402_middleware.py`

**Step 2: Trigger the Client Relay**
Open Terminal 2, navigate to the same directory, and execute the client request.
> `python client_relay_ping.py`

**Expected Output:**
Terminal 1 will log the issuance of the invoice, the verification of the payment, and the booting of the engine. Terminal 2 will log the HTTP 402 rejection, the simulated payment, and finally output the decrypted multidimensional evaluation (HTTP 200).

---

## 🔮 Future Scope (Next Phases)
* **Live Lightning Node Integration:** Transition from mock invoices/macaroons to a live LND or Core Lightning node to process real Satoshi transactions.
* **Dynamic Pricing:** Adjust the "1000 sats" cost dynamically based on the computational weight of the requested hypercube evaluation.
* **Expanded SBRM Rulesets:** Introduce Layer D (Jurisdictional Tax Logic) into the SWI-Prolog engine.