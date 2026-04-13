---

"@id": "urn:uuid:architecture-rules-and-execution-layer"

ontological\_class: "Documentation"

gist\_equivalent: "gist:SystemArchitecture"

---



\# Architecture: The Rules \& Execution Layer (`02\_Rules`)



The `02\_Rules` directory is the core neurosymbolic engine of the LodgeiT Global platform. It deliberately utilizes a \*\*Dual-State Architecture\*\*, splitting the repository into two distinct file types to strictly separate the "Immutable Truth" from the "Active Reasoning."



\## 1. The Ontological Nodes (`rule-\*.md`)

\*\*Role:\*\* The Static World-Model \& Epistemic Truth

\*\*Format:\*\* Markdown with strictly typed YAML frontmatter.



These files represent the Standard Business Reporting Model (SBRM) constructs. They are human-readable, machine-parsable, and cryptographically hashed. 



\* \*\*The Gatekeeper:\*\* These nodes are permanently monitored by the GitOps pre-commit hook (`audit\_ontology\_v2.py`). 

\* \*\*Zero Hallucination:\*\* They establish the mathematical and dimensional boundaries of the financial world (e.g., `rule-sbrm-accounting-equation.md`). They do not \*execute\* logic; they \*define\* the reality that the logic must adhere to.

\* \*\*Integrity:\*\* If a parameter is altered without authorization, the SHA-256 hash fails, and the system rejects the truth decay.



\## 2. The Logic Engines (`\*.pl`)

\*\*Role:\*\* The Active Reasoning \& Cross-Domain Inference

\*\*Format:\*\* SWI-Prolog scripts (`sbrm\_kb.pl`, `gst\_tax\_rules.pl`)



While the Markdown files define the universe, the Prolog files are the active brains that traverse it. 



\* \*\*Stateless Execution:\*\* These files are never run in a continuous loop. They are spun up as stateless, invisible subprocesses by the Python frontend, execute a specific query, return a deterministic output (e.g., `Deduction = 1.0e+05`), and immediately shut down to prevent memory leaks.

\* \*\*Cross-Domain Inference:\*\* The Prolog layer contains the semantic bridges. For example, it maps the global SBRM UUID of an entity to the local jurisdictional tax logic (like the ATO Instant Asset Write-Off), querying the SBRM graph for the turnover fact, computing the threshold, and returning the result.



\## Strategic Imperative: The End of "Brittle Scenarios"

Historically, logic engines required engineers to manually craft temporary "scenarios" (fact assertions) to test rules. In this architecture, \*\*the SBRM Graph is the scenario.\*\* Prolog engineers (including the Logical English team) must write rules that dynamically query the persistent SBRM Markdown nodes for their facts, rather than hardcoding assumptions.

