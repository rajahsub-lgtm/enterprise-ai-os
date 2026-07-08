\# ADR-015: Evidence Fusion Contract



\## Status



Accepted



\## Context



ADR-003 defines Enterprise Reasoning as a staged framework:



```text

Observation

&#x20;       ↓

Evidence

&#x20;       ↓

Evidence Fusion

&#x20;       ↓

Hypothesis Generation

&#x20;       ↓

Hypothesis Ranking

&#x20;       ↓

Operational Confidence

&#x20;       ↓

Execution Strategy

&#x20;       ↓

Recommendation

```



ADR-008 establishes that evidence must carry provenance.



ADR-009 separates source authorization from content safety.



ADR-011 defines reasoning as a pluggable architecture where LLMs, deterministic rules, scoring models, and human-assisted approaches may all become implementations.



ADR-014 establishes confidence-governed adaptive orchestration.



Sprint 2.5 requires a more explicit contract for Evidence Fusion because the synthetic ITIL application-health repository will include multiple evidence streams:



\* Monitoring events and alerts

\* Incidents

\* Problems

\* Known errors

\* Knowledge articles

\* Change requests

\* CMDB relationships

\* Business service mappings

\* Business impact assessments

\* Enterprise memory patterns

\* Governance decisions

\* Human feedback or review outcomes



The system must combine these streams without treating any single source as final truth.



\---



\## Decision



EAIOS will define Evidence Fusion as a first-class contract.



Evidence Fusion reconciles multiple governed evidence items, observations, memory patterns, and contextual signals into a structured fusion package.



Evidence Fusion does not produce final truth.



Evidence Fusion prepares the reasoning layer by organizing:



\* Supporting evidence

\* Weakening evidence

\* Conflicting evidence

\* Missing evidence

\* Evidence gaps

\* Uncertainty

\* Fusion confidence

\* Required review conditions



\---



\## Core Principle



```text

Evidence Fusion organizes evidence.



It does not independently decide the truth,

authorize action, or bypass human approval.

```



\---



\## Evidence Fusion Package



The minimum Evidence Fusion package is:



```json

{

&#x20; "fusion\_id": "FUSION-001",

&#x20; "case\_id": "CASE-001",

&#x20; "business\_outcome": "Maintain Application Health",

&#x20; "goal\_context": {

&#x20;   "goal\_category": "operational\_troubleshooting"

&#x20; },

&#x20; "hypothesis\_id": "HYP-001",

&#x20; "supporting\_evidence": \[],

&#x20; "weakening\_evidence": \[],

&#x20; "conflicting\_evidence": \[],

&#x20; "missing\_evidence": \[],

&#x20; "evidence\_gaps": \[],

&#x20; "fusion\_confidence": "MEDIUM",

&#x20; "requires\_human\_review": true,

&#x20; "required\_controls": \[],

&#x20; "created\_at": "2026-07-07T00:00:00Z",

&#x20; "created\_by": "evidence\_fusion\_agent"

}

```



\---



\## Evidence Categories



\### Supporting Evidence



Evidence that increases support for a hypothesis.



Example:



```text

A critical alert on CI-SRV-101 occurred during the same time window as checkout failures.

```



\### Weakening Evidence



Evidence that reduces support for a hypothesis.



Example:



```text

A suspected CI has no related alerts or incidents during the issue window.

```



\### Conflicting Evidence



Evidence that points to incompatible explanations or requires reconciliation.



Example:



```text

Alerts point to compute saturation, while recent changes point to an API deployment.

```



\### Missing Evidence



Expected evidence that was not found.



Example:



```text

No business service mapping exists for the impacted CI.

```



\### Evidence Gaps



Known limitations that affect reasoning confidence.



Example:



```text

Knowledge article is stale and has not been validated in the last 180 days.

```



\---



\## Fusion Confidence



Evidence Fusion produces a fusion confidence value.



Initial allowed values:



```text

HIGH

MEDIUM

LOW

UNKNOWN

```



Fusion confidence is based on:



\* Evidence quality

\* Source trust

\* Content safety outcome

\* Number of independent supporting sources

\* Presence of weakening evidence

\* Presence of conflicting evidence

\* Missing evidence

\* Business impact certainty

\* Memory validation state

\* Governance debt

\* Human validation state



Fusion confidence is not the same as final operational confidence.



Fusion confidence is one input into Operational Confidence.



\---



\## Fusion Confidence Rules



Initial deterministic rules:



| Condition                                                                      | Fusion Confidence                              |

| ------------------------------------------------------------------------------ | ---------------------------------------------- |

| Multiple authoritative supporting evidence items and no material conflict      | HIGH                                           |

| Some supporting evidence with minor gaps or only supporting-only evidence      | MEDIUM                                         |

| Weak support, stale content, unvalidated memory, or important missing evidence | LOW                                            |

| Required evidence cannot be evaluated                                          | UNKNOWN                                        |

| Conflicting evidence exists                                                    | LOW or UNKNOWN depending severity              |

| Unknown business impact exists                                                 | Cannot exceed MEDIUM                           |

| Unsafe content exists                                                          | Must not contribute to positive confidence     |

| Governance debt exists                                                         | Cannot be treated as HIGH without human review |



\---



\## Evidence Eligibility



Only evidence or observations that preserve provenance may enter an Evidence Fusion package.



The fusion process may consume:



\* Governed Evidence objects

\* Domain observations converted into core-facing observation structures

\* Human review notes with attribution

\* Enterprise memory patterns with validation metadata

\* Business impact assessments with ownership metadata

\* Governance decisions and debt records

\* Prior outcome records



The fusion process must not consume:



\* Raw unaudited model output as final evidence

\* Retrieved content that failed content safety

\* Data without source attribution

\* Memory without validation state

\* Domain records that bypass source authorization where authorization is required



\---



\## Relationship to Content Safety



Content Safety determines whether retrieved content may be used.



Evidence Fusion must respect content safety outcomes.



| Content Safety Status | Fusion Use                                          |

| --------------------- | --------------------------------------------------- |

| SAFE                  | May be used as authoritative evidence               |

| SAFE\_WITH\_CONTROLS    | May be used with controls                           |

| SUPPORTING\_ONLY       | May support reasoning but cannot be authoritative   |

| NEEDS\_HUMAN\_REVIEW    | Must not support automated reasoning until reviewed |

| UNSAFE                | Must be excluded from fusion                        |



\---



\## Relationship to Enterprise Memory



Enterprise Memory may contribute to Evidence Fusion only as governed memory evidence.



Memory may be classified as:



\* Human-validated memory

\* Outcome-calibrated memory

\* Stale memory

\* Unvalidated memory

\* Conflicting memory

\* Retired memory



Memory can support or weaken a hypothesis.



Memory cannot authorize action.



Memory cannot replace current evidence.



\---



\## Relationship to Business Impact



Business impact assessments may contribute to fusion.



Known high business impact increases urgency and may increase required controls.



Known low business impact may reduce urgency but does not remove governance.



Unknown business impact must be recorded as missing evidence or an evidence gap.



```text

Unknown business impact is not low business impact.

```



Unknown impact prevents fusion confidence from being treated as HIGH unless a human review or policy exception resolves the gap.



\---



\## Relationship to Hypothesis Generation



Evidence Fusion prepares inputs for Hypothesis Generation.



A Hypothesis should reference the fusion package or the evidence items organized within it.



The Hypothesis layer may produce statements such as:



```text

CI-SRV-101 is a likely contributing cause of checkout degradation.

```



Evidence Fusion itself should not produce final causal declarations.



\---



\## Relationship to Recommendation Candidates



Recommendation Candidates must reference evidence fusion outputs where applicable.



A recommendation candidate should state:



\* Which evidence supports it

\* Which evidence weakens it

\* Which evidence is missing

\* Which controls are required

\* Whether human approval is required

\* Which autonomous actions are prohibited



Evidence Fusion does not authorize remediation.



\---



\## Audit and Traceability



Each Evidence Fusion package must preserve traceability to the evidence it used.



At minimum, each evidence reference should include:



\* Evidence ID or observation ID

\* Source ID

\* Source owner

\* Item owner, where available

\* Content safety status, where applicable

\* Evidence quality level, where applicable

\* Audit ID or provenance reference, where available



Future versions may add:



\* Fusion audit event

\* Fusion graph

\* Evidence lineage visualization

\* Fusion confidence calibration



\---



\## Sprint 2.5 Boundary



Sprint 2.5 will implement Evidence Fusion as a lightweight contract and deterministic test-backed behavior.



Sprint 2.5 may include:



\* Evidence Fusion package dataclass or dictionary contract

\* Deterministic classification into supporting, weakening, conflicting, and missing evidence

\* Fusion confidence rules

\* Unknown-impact evidence gap handling

\* Memory-as-evidence handling

\* Tests using synthetic ITIL golden scenarios



Sprint 2.5 will not implement:



\* Full probabilistic inference

\* Full causal graph reasoning

\* LLM-based fusion

\* Production evidence graph database

\* Automated remediation

\* Enterprise-grade calibration dashboard



\---



\## Consequences



\### Benefits



\* Makes enterprise reasoning explainable

\* Prevents single-source final-answer behavior

\* Supports multi-agent collective intelligence

\* Preserves uncertainty

\* Enables confidence-governed orchestration

\* Provides a bridge between evidence and hypotheses

\* Supports safer recommendation candidates



\### Trade-offs



\* Requires more structured evidence metadata

\* Requires tests for evidence classification

\* Requires explicit handling of missing and conflicting evidence

\* Adds another contract between evidence collection and reasoning



\---



\## Decision Summary



Evidence Fusion is a first-class EAIOS contract.



It organizes governed evidence into supporting, weakening, conflicting, missing, and gap categories.



It produces fusion confidence but not final truth.



It informs reasoning, operational confidence, and recommendation candidates.



It does not authorize action.



It must preserve provenance, content safety, evidence quality, governance constraints, and human approval boundaries.



