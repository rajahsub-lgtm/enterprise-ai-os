\# ADR-009: Separate Source Authorization from Content Safety



\## Status



Accepted



\## Context



EAIOS 2 governs agent access to enterprise knowledge sources. However, authorization to access a source does not guarantee that the content retrieved from that source is safe to use.



A source may be authorized, approved, and owned, while still containing unsafe, stale, conflicting, poisoned, or instruction-like content.



For agentic AI systems, this distinction matters because retrieved content may influence reasoning, recommendations, tool calls, or future actions.



Examples include:



\* a trusted wiki page containing outdated instructions

\* a runbook containing unsafe operational commands

\* a support article containing conflicting remediation steps

\* a knowledge item with unknown freshness

\* a document containing prompt-injection-like instructions

\* a retrieved passage that attempts to override system governance

\* a source that is valid for reference but not authoritative for action



If EAIOS treats authorized access as equivalent to safe use, it creates a governance gap.



\## Decision



EAIOS will separate source authorization from content safety.



Source authorization answers:



```text

May this agent access this source for this Goal Context?

```



Content safety answers:



```text

Is the retrieved content safe to use in reasoning, recommendation, or action?

```



The Access Governance System and Governance Broker control source authorization.



A future Content Safety Gateway will evaluate retrieved content before it is passed into reasoning or action.



Content safety outcomes may include:



| Status               | Meaning                                                |

| -------------------- | ------------------------------------------------------ |

| `SAFE`               | Content may be used normally                           |

| `SAFE\_WITH\_CONTROLS` | Content may be used with required controls             |

| `SUPPORTING\_ONLY`    | Content may support reasoning but is not authoritative |

| `NEEDS\_HUMAN\_REVIEW` | Content requires human review before use               |

| `UNSAFE`             | Content must not be used                               |



\## Design Principle



Authorized source access does not imply safe content use.



No retrieved content should influence reasoning or action until it has either passed content safety checks or been explicitly restricted to a safe usage category.



\## Sprint 1 Boundary



In EAIOS 2 Sprint 1, source authorization is an Operational Capability for the governed Knowledge Agent access path.



Content safety is an Architectural Foundation.



Sprint 1 may define a Content Safety Gateway hook or placeholder, but does not implement full content inspection, prompt-injection detection, semantic safety analysis, stale-content detection, or conflicting-guidance resolution.



\## Consequences



This avoids overclaiming source governance.



It also prepares the architecture for agentic AI risks where the danger is not only unauthorized access, but unsafe use of authorized content.



This distinction supports later evidence quality scoring, knowledge quality scoring, GraphRAG safety, and governed reasoning.



\## Future Work



Future EAIOS releases may add:



\* content safety evaluator

\* prompt-injection detection

\* stale knowledge detection

\* conflicting guidance detection

\* unsafe command detection

\* source authority ranking

\* content usage restrictions

\* human review workflow for unsafe or ambiguous content

\* integration with evidence provenance and operational confidence



