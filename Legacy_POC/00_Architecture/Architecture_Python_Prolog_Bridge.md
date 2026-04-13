---

"@id": "urn:uuid:architecture-python-prolog-bridge"

ontological\_class: "Documentation"

gist\_equivalent: "gist:SystemArchitecture"

---



\# Architecture: The Python-Prolog Neurosymbolic Bridge



The LodgeiT Global engine relies on a strict division of labor to maintain a "Zero Hallucination" environment. We decouple the \*\*State\*\* (SBRM Facts) from the \*\*Logic\*\* (Prolog Rules). 



To connect these two domains without permanently hardcoding data into the logic scripts, we utilize an \*\*In-Memory Dynamic Injection Bridge\*\*.







\## 1. The Division of Labor



\### Python (The Orchestrator \& Compiler)

SWI-Prolog does not natively understand Markdown, Git, YAML frontmatter, or JSON-LD. Python serves as the sensory organ and translator for the system. 

\* It scans the `01\_Ontology` vault.

\* It parses the cryptographically verified Markdown nodes.

\* It translates the YAML dictionaries into formal Prolog syntax (e.g., minting Arity-6 `sbrm\_fact/6` and `sbrm\_edge/4` statements).



\### SWI-Prolog (The Reasoner)

Prolog is the deterministic brain. It does not read files from the hard drive at runtime; it only knows what Python explicitly tells it. 

\* It holds the immutable rules (`02\_Rules/sbrm\_kb.pl` and `gst\_tax\_rules.pl`).

\* It evaluates deterministic proofs (like the Fundamental Accounting Equation or the ATO IAWO rules) within the highly specific, conflict-free closed world that Python just built for it.



\## 2. The Evolution: In-Memory vs. Temporary Files

In legacy versions of this architecture, Python physically extracted the YAML data, wrote a temporary `sbrm\_kb.pl` file to the hard drive, forced Prolog to read it, and then deleted it. 



\*\*This approach has been deprecated.\*\* It was slow and risked leaving stale data on the disk if a process crashed.



\*\*The Current State (Dynamic Injection):\*\*

We now use true in-memory execution. In the master `02\_Rules/sbrm\_kb.pl` file, we declare dynamic predicates at the very top:

`:- dynamic sbrm\_edge/4.`

`:- dynamic sbrm\_fact/6.`



This tells the Prolog engine: \*"The rules are permanent, but the data will be injected directly into your RAM at runtime."\*



\## 3. The Execution Pipeline (Step-by-Step)

When a query hits the system (e.g., via the L402 Gateway or `prolog\_app.py`), the following sequence occurs:



1\. \*\*Extraction:\*\* Python reads the required `.md` files from `01\_Ontology`.

2\. \*\*Injection:\*\* Python connects to a background SWI-Prolog subprocess and uses `assertz/1` to dynamically push the facts (`sbrm\_fact`) and relationships (`sbrm\_edge`) directly into Prolog's active memory.

3\. \*\*Execution:\*\* Python fires the target query (e.g., `calculate\_iawo\_deduction`). Prolog evaluates the query against the freshly injected data and the static rules.

4\. \*\*Stateless Teardown:\*\* Prolog returns the calculated ground truth (e.g., `Deduction = 1.0e+05`) back to Python. The Prolog subprocess is immediately flushed and killed, ensuring the system remains pristine, stateless, and ready for the next query.

