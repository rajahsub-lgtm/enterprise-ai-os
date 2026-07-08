\# ADR-014: Confidence-Governed Adaptive Orchestration



\## Status



Accepted



\## Context



ADR-001 establishes EAIOS as an Enterprise AI Operating System centered on business outcomes, enterprise capabilities, enterprise skills, enterprise memory, operational confidence, enterprise reasoning, governed execution, and enterprise learning.



ADR-002 establishes Business Outcome First architecture.



ADR-003 establishes the Enterprise Reasoning Framework, including evidence fusion, hypothesis generation, hypothesis ranking, operational confidence, execution strategy, and recommendation.



ADR-004 establishes Business Outcome Driven Capability Orchestration.



ADR-012 establishes that Operational Confidence must be outcome-calibrated.



However, Sprint 2.5 requires a clearer runtime contract for how orchestration behavior changes when confidence, risk, evidence quality, business impact, and uncertainty vary.



The orchestrator must not behave as a fixed linear workflow.



It must also not behave randomly or autonomously without governance.



EAIOS requires policy-bounded adaptive orchestration.



\---



\## Decision



EAIOS will use Confidence-Governed Adaptive Orchestration.



The orchestrator may adapt the next capability, skill, or agent invocation based on:



\* Goal Context

\* Business outcome

\* Business impact

\* Evidence quality

\* Content safety

\* Operational confidence

\* Governance decision

\* Governance debt

\* Conflicting evidence

\* Missing evidence

\* Human approval requirements

\* Risk tier

\* Prior validated memory patterns



Adaptive orchestration must remain bounded by governance.



The orchestrator may choose different next steps, but it must not bypass:



\* Governance Broker / Policy Enforcement Point

\* Access Governance System / Policy Decision Point

\* Source authorization

\* Content safety

\* Evidence creation

\* Audit logging

\* Evidence provenance

\* Human approval boundaries



\---



\## Core Principle



```text

The orchestrator is adaptive, not autonomous.



It may change the investigation path based on confidence and evidence,

but it may not bypass governance or execute unsafe actions.

```



\---



\## Adaptive Behavior Rules



| Situation                                | Required Orchestrator Behavior                                           |

| ---------------------------------------- | ------------------------------------------------------------------------ |

| High confidence and low risk             | Continue targeted investigation                                          |

| High confidence and high business impact | Continue targeted investigation, but preserve human review               |

| Medium confidence                        | Gather additional corroborating evidence                                 |

| Low confidence                           | Invoke broader investigation capabilities                                |

| Conflicting evidence                     | Trigger evidence fusion and human review                                 |

| Missing evidence                         | Record evidence gap and gather additional evidence where allowed         |

| Unknown business impact                  | Escalate for business impact assessment                                  |

| High business impact with low confidence | Escalate; do not downgrade priority                                      |

| Governance debt exists                   | Preserve debt, restrict action, and require review where policy requires |

| Unsafe content                           | Block use or require human review according to content safety result     |

| Stale or low-trust memory                | Treat as supporting evidence only                                        |

| Proposed remediation                     | Produce recommendation candidate only; do not execute autonomously       |



\---



\## Orchestration Model



```text

Business Outcome

&#x20;       ↓

Goal Context

&#x20;       ↓

Capability Assessment

&#x20;       ↓

Skill / Capability Candidate Selection

&#x20;       ↓

Governance Check

&#x20;       ↓

Evidence Collection

&#x20;       ↓

Content Safety

&#x20;       ↓

Evidence Quality

&#x20;       ↓

Operational Confidence Evaluation

&#x20;       ↓

Adaptive Next-Step Selection

&#x20;       ↓

Evidence Fusion

&#x20;       ↓

Reasoning

&#x20;       ↓

Recommendation Candidate

&#x20;       ↓

Human Approval Boundary

```



\---



\## Determinism and Non-Determinism



EAIOS does not require every orchestration path to be identical.



Different evidence, confidence, risk, impact, or governance conditions may cause the orchestrator to select different next steps.



This is acceptable only when the variability is:



\* Policy-bounded

\* Explainable

\* Auditable

\* Testable

\* Governed by confidence and risk

\* Traceable to evidence and Goal Context



This is not free-form agent autonomy.



It is governed adaptive orchestration.



\---



\## Operational Confidence Effects



Operational Confidence influences orchestration depth.



| Confidence | Meaning                                               | Orchestration Effect                               |

| ---------- | ----------------------------------------------------- | -------------------------------------------------- |

| HIGH       | Current evidence strongly matches a validated pattern | Use targeted validation; do not skip governance    |

| MEDIUM     | Evidence partially supports a known path              | Gather additional evidence                         |

| LOW        | Evidence is weak, incomplete, or conflicting          | Expand investigation and require review            |

| UNKNOWN    | Confidence cannot be determined                       | Escalate uncertainty and prevent autonomous action |



Operational Confidence must not be used as a shortcut around human approval, audit, or governance controls.



\---



\## Business Impact Effects



Business impact influences urgency and required controls.



Known low business impact may reduce urgency.



Known high business impact increases urgency and review requirements.



Unknown business impact must not be treated as low business impact.



```text

Unknown impact is not low impact.

```



When business impact is unknown, EAIOS must:



\* Preserve the uncertainty

\* Create governance debt or evidence gap

\* Require business-owner or human review where appropriate

\* Prevent autonomous remediation



\---



\## Relationship to Collective Intelligence



Collective Intelligence may inform orchestration through:



\* Validated memory patterns

\* Historical outcomes

\* Human feedback

\* Prior governance decisions

\* Known errors

\* Successful resolutions

\* Failed resolutions

\* Capability performance

\* Skill performance

\* Implementation performance



However, Collective Intelligence is not direct authority.



It must enter orchestration through governed evidence, memory validation, confidence evaluation, or policy-approved metadata.



\---



\## Relationship to Enterprise Memory



Enterprise Memory may affect orchestration by increasing or decreasing confidence.



For example, a validated prior pattern may support targeted investigation.



A stale, unvalidated, or miscalibrated pattern may require broader investigation.



Memory is evidence.



Memory is not truth.



Memory must not directly authorize action.



\---



\## Sprint 2.5 Boundary



Sprint 2.5 will implement this ADR as a concept contract and regression-tested behavior where practical.



Sprint 2.5 may include deterministic rules for:



\* High / medium / low / unknown confidence

\* Unknown business impact

\* Conflicting evidence

\* Missing evidence

\* Governance debt

\* Recommendation candidate boundaries



Sprint 2.5 does not implement a full autonomous planning engine.



Sprint 2.5 does not implement LLM-driven orchestration.



Sprint 2.5 does not implement production workflow execution.



\---



\## Consequences



\### Benefits



\* Prevents hardcoded linear demo orchestration

\* Preserves business-outcome-first architecture

\* Makes operational confidence actionable

\* Supports richer multi-agent behavior

\* Keeps adaptive orchestration governed and auditable

\* Enables production-ready concept transfer without unsafe autonomy



\### Trade-offs



\* Requires explicit orchestration contracts

\* Requires confidence and evidence metadata

\* Adds complexity to testing

\* Requires clear separation between adaptive investigation and autonomous action



\---



\## Decision Summary



EAIOS orchestration is adaptive but bounded.



Operational confidence, evidence quality, business impact, governance decisions, and memory patterns may influence the next step.



No adaptive orchestration path may bypass governance, evidence provenance, content safety, audit, or human approval.



The orchestrator may change the investigation path.



It may not become an ungoverned actor.



