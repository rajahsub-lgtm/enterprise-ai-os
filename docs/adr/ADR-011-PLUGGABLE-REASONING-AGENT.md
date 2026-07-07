\# ADR-011: ReasoningAgent Is Pluggable; LLMs Are Implementations, Not the Architecture



\## Status



Accepted



\## Context



EAIOS includes reasoning as part of the enterprise operating model. Reasoning transforms evidence, memory, context, and confidence signals into hypotheses and recommendation candidates.



However, EAIOS should not equate reasoning with a single LLM call.



A reliable enterprise architecture must support multiple reasoning implementations, including deterministic rules, scoring models, knowledge-based reasoning, domain-specific reasoning, human-assisted reasoning, and LLM-assisted reasoning.



EAIOS 2 should keep reasoning deterministic initially for repeatability, auditability, and testability while defining an interface that allows future implementations to be introduced safely.



\## Decision



EAIOS will define ReasoningAgent as an interface.



Initial implementation:



\* `DeterministicReasoningAgent`



Possible future implementations:



\* `LLMReasoningAgent`

\* `ScoringModelReasoningAgent`

\* `HumanAssistedReasoningAgent`

\* `DomainSpecificReasoningAgent`



All ReasoningAgent implementations must accept governed inputs and return structured outputs.



Governed inputs may include:



\* Goal Context

\* governed evidence

\* evidence quality

\* source quality

\* operational context

\* policy constraints

\* risk context



Structured outputs may include:



\* hypotheses

\* evidence references

\* confidence rationale

\* uncertainty statement

\* recommendation candidates

\* required controls

\* provenance metadata



LLM outputs must not bypass governance.



Any LLM output must enter EAIOS as one of the following governed objects:



\* Evidence

\* Hypothesis

\* RecommendationCandidate



These objects must carry provenance, quality scoring, and governance metadata.



\## Design Principle



LLMs are reasoning implementations, not the reasoning architecture.



The operating system governs reasoning. It does not outsource reasoning governance to the model.



\## Sprint 1 Boundary



In EAIOS 2 Sprint 1, ReasoningAgent is a Defined Interface.



Sprint 1 may define the ReasoningAgent contract, but real LLM reasoning is not part of the Sprint 1 runtime.



The governed Knowledge Agent access path must remain deterministic and testable.



\## Consequences



This prevents the architecture from becoming model-centric.



It also allows EAIOS to add LLM reasoning later without changing the governance boundary.



LLM-generated hypotheses can become useful demo artifacts later, but they must be evaluated like any other evidence or hypothesis.



\## Future Work



Future EAIOS releases may add:



\* deterministic reasoning implementation

\* LLM reasoning implementation

\* model selection policy

\* reasoning provenance

\* hypothesis quality scoring

\* comparison of deterministic and LLM-generated hypotheses

\* LLM output safety checks

\* human-assisted reasoning workflow



