\# ADR-007: Human Approval Is a State Machine, Not a Boolean



\## Status



Accepted



\## Context



EAIOS 2 introduces runtime governance for agent actions. Some actions can be automatically approved, some must be denied, and some require human review before proceeding.



A simple Boolean approval model is insufficient because enterprise approval has lifecycle state, ownership, timeout behavior, delegation, rationale, and audit requirements.



For example, a governed action may be pending approval, approved by an authorized owner, denied by a reviewer, or expired because no decision was made within the required window.



In a Zero Trust governance model, expired or unresolved approval must not silently become permission.



\## Decision



EAIOS will model human approval as a state machine.



The initial approval states are:



```text

PENDING → APPROVED

PENDING → DENIED

PENDING → EXPIRED

```



Each approval request must carry:



\* approval request ID

\* request ID

\* requesting agent

\* target agent

\* requested capability

\* requested source or resource

\* Goal Context

\* risk tier

\* required approver or owner

\* delegate, if applicable

\* evidence package or rationale

\* created timestamp

\* expiration timestamp or SLA

\* final state

\* final decision timestamp

\* reviewer rationale, if provided



\## Default Behavior



Expired approvals fail closed.



If an approval is required and the approval state is not `APPROVED`, the governed action must not proceed.



Default behavior:



| Approval State | Runtime Behavior                       |

| -------------- | -------------------------------------- |

| `PENDING`      | Do not proceed                         |

| `APPROVED`     | Proceed only within policy constraints |

| `DENIED`       | Do not proceed                         |

| `EXPIRED`      | Do not proceed; fail closed            |



\## Sprint 1 Boundary



In EAIOS 2 Sprint 1, human approval is an Architectural Foundation.



Sprint 1 may define the approval state model and placeholder object, but does not implement a full approval workflow UI, notification flow, delegation workflow, or enterprise integration.



Sprint 1 governance decisions may return `ESCALATE` to indicate that human approval is required.



\## Consequences



This keeps governance explicit and auditable.



It prevents escalation from being treated as soft approval.



It also creates a clean foundation for later integration with workflow systems, approval queues, service owners, policy owners, and enterprise risk review.



\## Future Work



Future EAIOS releases may add:



\* approval queue

\* approval UI

\* owner and delegate resolution

\* SLA aging

\* notification integration

\* approval evidence package

\* approval analytics

\* separation-of-duties checks

\* recurring approval review

\* exception management



