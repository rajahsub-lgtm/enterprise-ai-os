# Historical Note

This document is retained as an earlier EAIOS 2 sprint planning artifact.

Current Sprint 2.5 status is captured in:

- `README.md`
- `docs/EAIOS_2_SPRINT_2_5_COMPLETION_SUMMARY.md`
- `docs/EAIOS_2_REPOSITORY_HOUSEKEEPING_STATUS.md`

The current executable demo is `python app.py`.

---
\# EAIOS 2 Sprint Plan



\## Version Theme



EAIOS 1 proved enterprise reasoning can run.



EAIOS 2 proves enterprise reasoning can be trusted.



\## Sprint Discipline



EAIOS 2 has a broad architecture, but Sprint 1 has a controlled implementation scope.



The goal is to explicitly separate:



\* What is operational in Sprint 1

\* What is architecturally prepared

\* What is defined as an interface

\* What is intentionally deferred to EAIOS 3 or later



This prevents overclaiming and keeps the build testable.



\---



\# Implementation Maturity Levels



| Maturity Label           | Meaning                                                      | Sprint Interpretation                        |

| ------------------------ | ------------------------------------------------------------ | -------------------------------------------- |

| Operational Capability   | Working code, automated tests, observable behavior           | Built and validated in Sprint 1              |

| Architectural Foundation | Data model, hook, placeholder, or lightweight implementation | Structurally prepared, not fully implemented |

| Defined Interface        | Stable contract for future implementations                   | Boundary defined, implementation deferred    |

| Roadmap Capability       | Recognized capability outside Sprint 1 scope                 | Future EAIOS 3+ work                         |



\---



\# Sprint 0 â€” Hygiene and Build Readiness



Before Sprint 1 governance coding proceeds, the EAIOS 1 spine must be stable.



\## Sprint 0 Objective



Ensure the existing runtime can be built, tested, and run from a clean checkout before adding the governance layer.



\## Sprint 0 Acceptance Criteria



Sprint 0 is complete when:



1\. The EnterpriseMemory crash is fixed.

2\. The project runs from a clean checkout.

3\. Runtime dependencies are pinned.

4\. `pytest` is available.

5\. A baseline smoke test exists for the EAIOS 1 spine.

6\. A repeatable test command exists.



Minimum required command:



```text

python -m pytest

```



Sprint 1 should not proceed until the baseline test command runs successfully.



\---



\# Sprint 1 â€” Zero Trust Knowledge Access Governance



\## Sprint 1 Objective



Prove that a Knowledge Agent action can be governed before execution using Goal Context, Agent Registry, Data Source Registry, Policy Registry, AGS/PDP, Broker/PEP, default-deny behavior, governance debt tracking, and audit.



\## Sprint 1 Core Question



Can EAIOS prevent, deny, escalate, or fail closed on unsafe knowledge access before enterprise knowledge is retrieved or used?



\---



\# Sprint 1 Runtime Flow



```text

Application Health Agent

â†“

requests Knowledge Agent support

â†“

ActionRequest created with Goal Context

â†“

Knowledge Agent uses GovernedKnowledgeClient

â†“

GovernanceBroker intercepts the request

â†“

AccessGovernanceSystem evaluates policy

â†“

Decision returned:

APPROVED\_WITH\_CONTROLS / DENIED / ESCALATE / FAIL\_CLOSED

â†“

Broker enforces decision

â†“

Audit record written or access blocked fail-closed

```



\---



\# Sprint 1 Identity Assumption



In Sprint 1, caller identity is asserted in the `ActionRequest` and verified by the Governance Broker against the Agent Registry.



This is not production identity federation.



It is a controlled Sprint 1 identity boundary that proves unregistered callers are denied before source authorization proceeds.



Production identity, signed agent tokens, workload identity, IAM, mTLS, and attestation are Roadmap Capabilities.



\---



\# Sprint 1 Build Scope by Implementation Maturity



\## Operational Capabilities



These are implemented in working code and validated by automated tests in Sprint 1.



| Capability                    | Sprint 1 Implementation                                                                               |

| ----------------------------- | ----------------------------------------------------------------------------------------------------- |

| Agent Registry                | `agents.json` defines registered agents, owners, capabilities, and risk tier                          |

| Data Source Registry          | `data\_sources.json` defines governed knowledge sources, classification, trust, metadata, and controls |

| Policy Registry               | `policies.json` defines source, capability, goal-context, and risk rules                              |

| Goal Context                  | Required input for every governed action                                                              |

| ActionRequest                 | Runtime object carrying caller, target, capability, requested sources, and context                    |

| AGS / PDP                     | Access Governance System evaluates request and returns a decision                                     |

| Governance Broker / PEP       | Broker verifies identity, calls AGS, enforces decision before knowledge access                        |

| Governed Knowledge Client     | Only approved path for Knowledge Agent source access                                                  |

| Default Deny / Escalate       | Unknown, unauthorized, missing-context, and unsafe requests do not proceed                            |

| Governance Debt Detection     | Unknown or incomplete metadata is escalated and tracked                                               |

| Basic Audit Logging           | Every completed governance decision creates an audit record                                           |

| Fail-Closed for Audit Failure | Audit failure on governed access blocks access and returns `FAIL\_CLOSED`                              |



\## Architectural Foundations



These are introduced structurally, but not fully implemented in Sprint 1.



| Capability                            | Sprint 1 Boundary                                                    |

| ------------------------------------- | -------------------------------------------------------------------- |

| Human Approval State Model            | Define `PENDING / APPROVED / DENIED / EXPIRED`; no full workflow UI  |

| Append-Only Audit Design              | Hash-chain design or lightweight hook; production immutability later |

| Evidence Provenance Model             | Define provenance fields; full evidence graph later                  |

| Content Safety Gateway Hook           | Boundary between source authorization and content safety             |

| AgentOps Metrics Hooks                | Simple structured metrics/logs; full Command Center later            |

| Broader Fail-Closed Platform Handling | Core governed access path only in Sprint 1                           |



\## Defined Interfaces



These contracts are defined now to avoid rework later.



| Interface                                    | Sprint 1 Boundary                                                 |

| -------------------------------------------- | ----------------------------------------------------------------- |

| ReasoningAgent Interface                     | Deterministic reasoning remains default; LLM implementation later |

| LLMReasoningAgent Contract                   | Optional future implementation, not Sprint 1 runtime              |

| Evidence / Hypothesis Object Contract        | Future reasoning outputs enter governance as structured objects   |

| Operational Confidence Calibration Interface | Outcome comparison structure defined; no calibration engine yet   |

| Red-Team Scenario Format                     | Scenario schema defined; full regression runner later             |



\## Roadmap Capabilities



These are explicitly out of Sprint 1.



| Capability                                | Deferred To                     |

| ----------------------------------------- | ------------------------------- |

| Full Enterprise Command Center UI         | EAIOS 3+                        |

| Real LLM Reasoning Demo                   | Later EAIOS 2 sprint or EAIOS 3 |

| Full Content Safety Detection             | EAIOS 3+                        |

| Full Human Approval Workflow Integration  | EAIOS 3+                        |

| Full Red-Team Regression Runner           | EAIOS 3+                        |

| Production IAM Integration                | EAIOS 3+                        |

| Full NIST / ISO / COBIT Compliance Engine | Future                          |

| Autonomous Remediation                    | Future                          |

| Full Agent Marketplace / Catalog UI       | Future                          |



\---



\# Standard Taxonomy



Policies must key off exact strings. Sprint 1 uses the following controlled taxonomy.



\## Goal Categories



```text

operational\_troubleshooting

self\_help

hr\_support

```



\## Capabilities



```text

retrieve\_best\_knowledge

retrieve\_identity\_context

write\_validated\_learning

```



\## Source IDs



```text

support\_knowledge

self\_help\_knowledge

wiki\_knowledge

human\_resources\_knowledge

employee\_identification\_knowledge

validated\_learning\_store

```



\---



\# Sprint 1 Data Files



```text

data/governance/

&#x20; agents.json

&#x20; data\_sources.json

&#x20; policies.json

&#x20; audit\_log.json

&#x20; governance\_debt.json

```



\---



\# Sprint 1 Core Code Files



```text

src/governance/

&#x20; \_\_init\_\_.py

&#x20; registry\_loader.py

&#x20; action\_request.py

&#x20; access\_governance\_system.py

&#x20; governance\_broker.py

&#x20; governed\_knowledge\_client.py

&#x20; audit\_logger.py

&#x20; governance\_debt\_logger.py

```



\---



\# Sprint 1 Foundation / Interface Files



These files may be lightweight. They exist to protect the architecture, not to overbuild.



```text

src/governance/

&#x20; human\_approval.py

&#x20; evidence.py

&#x20; content\_safety\_gateway.py

&#x20; agentops\_metrics.py

&#x20; reasoning\_agent.py

```



\---



\# Sprint 1 Test Files



Automated tests are first-class Sprint 1 scope.



```text

tests/

&#x20; test\_sprint0\_smoke.py

&#x20; test\_scenarios.py

```



Governance validation must not rely on eyeballing demo output.



\---



\# Policy-as-Data Example



The following policy produces the expected denial in Scenario 3.



```json

{

&#x20; "policy\_id": "POL-KNOWLEDGE-HR-001",

&#x20; "name": "Restrict Human Resources Knowledge to HR Goal Contexts",

&#x20; "owner": "enterprise\_governance",

&#x20; "risk\_tier": "high",

&#x20; "subject": {

&#x20;   "target\_agent\_id": "knowledge\_agent",

&#x20;   "capability": "retrieve\_best\_knowledge"

&#x20; },

&#x20; "condition": {

&#x20;   "requested\_source": "human\_resources\_knowledge",

&#x20;   "allowed\_goal\_categories": \[

&#x20;     "hr\_support"

&#x20;   ]

&#x20; },

&#x20; "effect": {

&#x20;   "when\_goal\_category\_not\_in\_allowed\_list": "DENY"

&#x20; },

&#x20; "controls": \[

&#x20;   "log\_denied\_access",

&#x20;   "record\_policy\_reference",

&#x20;   "notify\_source\_owner\_if\_repeated"

&#x20; ],

&#x20; "nist\_trace": {

&#x20;   "govern": "Policy owner and HR source restriction",

&#x20;   "map": "Goal Context compared to requested HR source",

&#x20;   "measure": "Risk tier high due to confidential HR source",

&#x20;   "manage": "Deny non-HR access"

&#x20; }

}

```



Scenario tests must prove that outcomes are policy-driven, not hidden hardcoded branches.



\---



\# Controls Boundary



In Sprint 1, `APPROVED\_WITH\_CONTROLS` means the AGS returns required controls and the broker attaches them to the decision and audit record.



Sprint 1 does not fully enforce every named control.



Control execution, validation, and evidence-backed control effectiveness move to later sprints.



Use the label:



```text

required\_controls

```



not language that implies full runtime enforcement.



\---



\# Retrieval Boundary



In Sprint 1, `retrieve\_best\_knowledge` is governed as a requested capability, but the system does not perform real retrieval ranking.



Sprint 1 proves whether retrieval is allowed.



Actual knowledge ranking, source quality scoring, GraphRAG, and content selection move to Sprint 2+.



The governed client may return mock approved-source results.



\---



\# Governance Debt Boundary



In Sprint 1, governance debt is recorded in two places:



1\. The audit record for the decision.

2\. `data/governance/governance\_debt.json` as a lightweight queue.



Full workflow, ownership assignment, aging, SLA, and remediation are later capabilities.



Example governance debt record:



```json

{

&#x20; "debt\_id": "gd-001",

&#x20; "request\_id": "req-007",

&#x20; "debt\_type": "unknown\_source",

&#x20; "missing\_item": "unknown\_knowledge\_source",

&#x20; "decision": "ESCALATE",

&#x20; "created\_by": "access\_governance\_system",

&#x20; "status": "OPEN"

}

```



\---



\# Ambiguous Risk vs. High-Risk Uncertainty



Risk behavior should be policy-driven and metadata-driven, not hardcoded.



\## Ambiguous Risk



```text

Missing or conflicting governance information

\+

No high-impact signal detected

=

ESCALATE

```



Examples:



```text

unknown source owner

missing freshness metadata

missing source quality score

conflicting policy mapping

unknown source trust level

```



\## High-Risk Uncertainty



```text

Missing or conflicting governance information

\+

one or more high-impact signals detected

=

DENY

```



High-impact signals can come from:



```text

source classification

capability type

Goal Context

risk context

data sensitivity

environment

business impact

```



Examples:



```text

PII source with missing privacy control

production action with missing approval

identity access without complete justification

write action with missing owner

high-severity context with missing source trust

```



\---



\# Sprint 1 Automated Scenarios



All scenarios must be implemented as automated assertions in `tests/test\_scenarios.py`.



|  # | Scenario                                  | Expected Decision        |

| -: | ----------------------------------------- | ------------------------ |

|  1 | Operational troubleshooting source access | `APPROVED\_WITH\_CONTROLS` |

|  2 | Self-help source access                   | `APPROVED\_WITH\_CONTROLS` |

|  3 | HR source from non-HR context             | `DENIED`                 |

|  4 | Identity source through generic retrieval | `DENIED`                 |

|  5 | Identity access with justification        | `ESCALATE`               |

|  6 | Knowledge write                           | `ESCALATE`               |

|  7 | Unknown source governance debt            | `ESCALATE`               |

|  8 | Missing Goal Context                      | `DENIED`                 |

|  9 | High-risk uncertainty                     | `DENIED`                 |

| 10 | Unregistered caller agent                 | `DENIED`                 |

| 11 | Audit failure on governed action          | `FAIL\_CLOSED`            |

| 12 | Goal-category spoofing by unauthorized caller | `DENIED` |



\---



\# Scenario Details



\## Scenario 1 â€” Approved Operational Troubleshooting



```text

Caller:

application\_health\_agent



Target:

knowledge\_agent



Goal category:

operational\_troubleshooting



Requested capability:

retrieve\_best\_knowledge



Requested sources:

support\_knowledge

wiki\_knowledge

self\_help\_knowledge



Expected decision:

APPROVED\_WITH\_CONTROLS

```



Purpose:



Proves normal governed knowledge access works.



\---



\## Scenario 2 â€” Approved Self-Help



```text

Caller:

self\_help\_agent



Target:

knowledge\_agent



Goal category:

self\_help



Requested capability:

retrieve\_best\_knowledge



Requested sources:

self\_help\_knowledge

wiki\_knowledge



Expected decision:

APPROVED\_WITH\_CONTROLS

```



Purpose:



Proves the same Knowledge Agent can be reused under a different Goal Context.



\---



\## Scenario 3 â€” Denied HR Source From Non-HR Context



```text

Caller:

application\_health\_agent



Target:

knowledge\_agent



Goal category:

operational\_troubleshooting



Requested capability:

retrieve\_best\_knowledge



Requested source:

human\_resources\_knowledge



Expected decision:

DENIED

```



Purpose:



Proves source access is purpose-aware, not just agent-aware.



\---



\## Scenario 4 â€” Denied Identity Source Through Generic Retrieval



```text

Caller:

self\_help\_agent



Target:

knowledge\_agent



Goal category:

self\_help



Requested capability:

retrieve\_best\_knowledge



Requested source:

employee\_identification\_knowledge



Expected decision:

DENIED

```



Purpose:



Proves sensitive identity sources cannot be reached through generic knowledge retrieval.



\---



\## Scenario 5 â€” Escalated Identity Access With Justification



```text

Caller:

hr\_support\_agent



Target:

knowledge\_agent



Goal category:

hr\_support



Requested capability:

retrieve\_identity\_context



Requested source:

employee\_identification\_knowledge



Business justification:

provided



Expected decision:

ESCALATE

```



Purpose:



Proves high-sensitivity access requires review even when the request appears legitimate.



\---



\## Scenario 6 â€” Escalated Knowledge Write



```text

Caller:

application\_health\_agent



Target:

knowledge\_agent



Requested capability:

write\_validated\_learning



Requested source:

validated\_learning\_store



Expected decision:

ESCALATE

```



Purpose:



Proves enterprise memory updates require human governance.



\---



\## Scenario 7 â€” Governance Debt



```text

Caller:

application\_health\_agent



Target:

knowledge\_agent



Requested source:

unknown\_knowledge\_source



Expected decision:

ESCALATE

```



Purpose:



Proves missing metadata is treated as governance debt, not implicit approval.



\---



\## Scenario 8 â€” Missing Goal Context



```text

Caller:

application\_health\_agent



Target:

knowledge\_agent



Goal Context:

missing



Expected decision:

DENIED

```



Purpose:



Proves Goal Context is mandatory for governed action.



\---



\## Scenario 9 â€” High-Risk Uncertainty



```text

Caller:

application\_health\_agent



Target:

knowledge\_agent



Requested source:

restricted or high-impact source



Required control:

missing



Expected decision:

DENIED

```



Purpose:



Proves uncertainty attached to high-impact action or sensitive data is denied by default.



\---



\## Scenario 10 â€” Unregistered Caller Agent



```text

Caller:

unregistered\_agent



Target:

knowledge\_agent



Requested capability:

retrieve\_best\_knowledge



Requested source:

support\_knowledge



Expected decision:

DENIED

```



Purpose:



Proves the broker validates caller identity against the Agent Registry before source authorization.



\---



\## Scenario 11 â€” Audit Failure on Governed Action



```text

Condition:

Audit logger fails during governed source access.



Expected decision:

FAIL\_CLOSED

```



Purpose:



Proves the broker does not allow governed access when mandatory auditability cannot be established.



\---


## Scenario 12 â€” Goal-Category Spoofing

```text
Caller:
application_health_agent

Claimed Goal Category:
hr_support

Requested capability:
retrieve_best_knowledge

Requested source:
human_resources_knowledge

Expected decision:
DENIED

\# Sprint 1 Acceptance Criteria



Sprint 1 is complete when:



1\. Sprint 0 smoke tests pass.

2\. All 12 governance scenarios pass in `tests/test\_scenarios.py`.

3\. Each scenario asserts the expected decision.

4\. Each scenario asserts the relevant policy reference or denial/escalation reason.

5\. Each scenario asserts an audit record is written, except the audit-failure scenario, which asserts `FAIL\_CLOSED` and no source access.

6\. Unregistered callers are denied before source authorization.

7\. Missing Goal Context is denied.

8\. Unknown or incomplete metadata creates governance debt.

9\. Ambiguous non-high-risk uncertainty escalates.

10\. High-risk uncertainty denies.

11\. `APPROVED\_WITH\_CONTROLS` decisions include `required\_controls` in the decision and audit record.

12\. Denied, escalated, and fail-closed decisions do not allow source access.

13\. The NIST trace is present on decisions where policy evaluation completes.

14\. The implementation maturity map is documented so operational capabilities are not confused with foundations, interfaces, or roadmap capabilities.

15\. Goal-category spoofing is denied when a caller asserts a Goal Context category it is not entitled to use.

\---



\# Sprint 1 Non-Goals



Sprint 1 explicitly does not include:



\* Real LLM reasoning

\* Autonomous remediation

\* Full Enterprise Command Center UI

\* Full content safety detection engine

\* Full human approval workflow

\* Full red-team regression runner

\* Production IAM integration

\* Complex policy language

\* Full compliance claim

\* Broad multi-agent runtime

\* Real knowledge ranking or GraphRAG retrieval



\---



\# Sprint 2 Preview â€” Governed Evidence and Content Safety



\## Maturity Shift



```text

Evidence Provenance:

Architectural Foundation â†’ Operational Capability



Content Safety Gateway:

Architectural Foundation â†’ Operational Capability

```



\## Build



```text

Evidence object

Evidence provenance

Content safety evaluation

SAFE / SAFE\_WITH\_CONTROLS / SUPPORTING\_ONLY / NEEDS\_HUMAN\_REVIEW / UNSAFE

```



\---



\# Sprint 3 Preview â€” Derived Operational Confidence



\## Maturity Shift



```text

Operational Confidence Calibration:

Defined Interface â†’ Architectural Foundation / partial Operational Capability

```



\## Build



```text

derived confidence scoring

knowledge quality scoring

source trust scoring

risk-context weighting

confidence explanation

```



\---



\# Sprint 4 Preview â€” Outcome-Calibrated Learning



\## Maturity Shift



```text

Operational Confidence Calibration:

Architectural Foundation â†’ Operational Capability

```



\## Build



```text

governed action outcome records

confidence-vs-outcome comparison

calibration error

miscalibration review flags

threshold adjustment recommendation

```



\---



\# Sprint 5 Preview â€” Red-Team Governance Regression



\## Maturity Shift



```text

Red-Team Scenario Format:

Defined Interface â†’ Operational Capability

```



\## Build



```text

red\_team\_scenarios.json

scenario runner

expected-vs-actual decision comparison

audit-chain verification

governance regression report

```



\---



\# Final Sprint 1 Boundary Statement



EAIOS 2 Sprint 1 implements and tests the runtime governance path for Knowledge Agent access.



It operationalizes Agent Registry, Data Source Registry, Policy Registry, Goal Context, ActionRequest, AGS/PDP, Broker/PEP, governed knowledge access, caller identity validation against the registry, default-deny behavior, governance debt recording, basic audit, caller goal-category entitlement validation and fail-closed behavior for audit failure on the governed access path.



It introduces human approval, evidence provenance, content safety, AgentOps metrics, reasoning interfaces, operational confidence calibration, and red-team testing as architectural foundations or defined interfaces, without claiming they are fully implemented yet.




