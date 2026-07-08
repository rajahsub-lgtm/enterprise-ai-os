\# ADR-017: Synthetic Domain Repository as Architecture Test Harness



\## Status



Accepted



\## Context



EAIOS began with an IT application-health walking skeleton that demonstrated business-outcome-driven reasoning, agent orchestration, enterprise memory, operational confidence, strategy selection, recommendation generation, and human approval boundaries.



EAIOS 2 then introduced governed access, Governance Broker enforcement, Access Governance System decisions, audit logging, governance debt, evidence creation, content safety, evidence quality, and evidence-to-audit linkage.



Sprint 2.5 requires a richer application-health operating model that can exercise the major EAIOS concepts together:



\* Business Outcome First architecture

\* Capability and skill orchestration

\* Governed access

\* Goal Context

\* Source authorization

\* Content safety

\* Evidence creation

\* Evidence quality

\* Evidence fusion

\* Operational confidence

\* Enterprise memory

\* Collective intelligence

\* Business impact analysis

\* Governance debt

\* Human approval

\* Domain adapter separation



Public datasets may support individual parts of this story, such as telemetry, root-cause analysis, incidents, or ITSM records, but they rarely provide all of the relationships required to test the full EAIOS architecture.



Therefore, Sprint 2.5 will use a synthetic IT application-health repository.



\---



\## Decision



EAIOS will use synthetic domain repositories as architecture and orchestration test harnesses.



A synthetic domain repository is a deterministic, controlled, domain-specific dataset designed to test EAIOS concepts, contracts, boundaries, and orchestration behavior.



A synthetic repository may include realistic-looking domain records, but it must not be presented as proof of real-world operational accuracy.



It is a test harness.



It is not a production benchmark.



\---



\## Core Principle



```text

Synthetic data can prove architectural behavior.



Synthetic data cannot prove real-world operational accuracy.

```



\---



\## Purpose



The synthetic IT application-health repository exists to test whether EAIOS can:



\* Start from a business outcome

\* Identify required capabilities and skills

\* Traverse multi-agent orchestration paths

\* Govern access to domain data

\* Convert domain records into core-facing observations and evidence

\* Preserve provenance and source metadata

\* Apply content safety and evidence quality rules

\* Fuse evidence from multiple sources

\* Use memory patterns safely

\* Reason under uncertainty

\* Identify business impact and unknown impact

\* Produce recommendation candidates

\* Preserve human approval boundaries

\* Record governance debt and evidence gaps

\* Keep IT domain concepts out of EAIOS Core



\---



\## Repository Scope



The Sprint 2.5 synthetic IT application-health repository may include:



```text

cmdb\_topology

business\_services

service\_ci\_mappings

monitoring\_events

incidents

problems

knowledge\_base

change\_requests

memory\_patterns

governance\_metadata

golden\_scenarios

```



Target scale:



```text

24 CMDB CIs

6 business services

5,000 monitoring events / alerts

2,400 incidents

16–24 problems

20–40 knowledge articles

16–24 change requests

6 deterministic golden scenarios

```



The exact record counts may evolve, but the repository must include enough scale to separate meaningful signal from operational noise.



\---



\## Golden Scenarios



Synthetic repositories must contain deterministic golden scenarios.



Golden scenarios are hand-controlled records designed to test specific architectural concepts.



Sprint 2.5 golden scenarios should include:



| Scenario                                         | Purpose                                                                                                            |

| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |

| Tier-0 checkout degradation                      | Tests business impact, CMDB traversal, incidents, alerts, knowledge, evidence fusion, and recommendation candidate |

| Known error reuse                                | Tests memory patterns, known errors, confidence, and targeted validation                                           |

| Recent change correlation                        | Tests change analysis, causal hypothesis, and approval boundary                                                    |

| High technical severity with low business impact | Tests technical severity versus business impact                                                                    |

| Unknown business impact                          | Tests governance debt and escalation                                                                               |

| Conflicting evidence                             | Tests evidence fusion, uncertainty, and human review                                                               |



Golden scenarios must be deterministic so regression tests can validate expected behavior.



\---



\## Background Noise



Synthetic repositories may include generated background records.



Background noise exists to test:



\* Filtering

\* Correlation

\* Prioritization

\* Signal-to-noise handling

\* Agent focus

\* Scalability of the repository structure

\* Robustness of deterministic scenario selection



Background noise must not interfere with golden scenario determinism.



Golden scenario records should be explicitly marked or discoverable through stable scenario IDs.



\---



\## Governance Metadata



Synthetic repository records should include governance-relevant metadata where applicable.



Examples:



```text

source\_id

source\_owner

item\_owner

item\_last\_validated

classification

trust\_level

risk\_tier

business\_owner

allowed\_goal\_categories

metadata\_complete

high\_impact\_signals

usage\_constraints

```



This allows Sprint 2.5 to test governance concepts without connecting to real enterprise systems.



\---



\## Domain Adapter Boundary



Synthetic domain repository records are domain-specific.



For Sprint 2.5, the repository belongs to the IT application-health domain adapter.



IT-domain terms such as the following must remain outside EAIOS Core:



```text

incident

alert

problem

change

CMDB CI

business service

runbook

known error

outage

application health

service degradation

host migration

pod eviction

```



The domain adapter translates these terms into core-facing concepts:



| IT Domain Concept                         | Core Concept                         |

| ----------------------------------------- | ------------------------------------ |

| Business service / CI                     | Entity                               |

| Alert / incident / event                  | Observation                          |

| Problem / known error / knowledge article | Evidence source or memory pattern    |

| Change request                            | Observation, context, or risk signal |

| Business impact                           | Risk / impact signal                 |

| Root-cause candidate                      | Hypothesis                           |

| Remediation proposal                      | RecommendationCandidate              |

| Approval path                             | Human approval boundary              |



No synthetic repository or domain adapter may bypass:



\* Governance Broker

\* Access Governance System

\* EvidenceFactory

\* ContentSafetyGateway

\* Audit logging

\* Evidence-to-audit linkage

\* Human approval boundary



\---



\## Unknown and Missing Data



Synthetic repositories should intentionally include incomplete data to test governance behavior.



Examples:



\* Missing business impact mapping

\* Missing source owner

\* Missing item owner

\* Stale knowledge article

\* Conflicting problem record

\* Ambiguous CI ownership

\* Unknown source metadata

\* Unvalidated memory pattern

\* Unapproved change

\* Missing dependency mapping



These cases must not be silently treated as safe or low risk.



```text

Unknown is not low.

Missing is not safe.

Unvalidated is not truth.

```



\---



\## Business Impact Rule



Synthetic business impact mappings must preserve this default:



```text

Unknown business impact is not low business impact.

```



When business impact is unknown, EAIOS must:



\* Preserve uncertainty

\* Create an evidence gap or governance debt

\* Prevent autonomous remediation

\* Escalate for business impact assessment where required



\---



\## Memory Rule



Synthetic repositories may include prior memory patterns.



Memory patterns must include:



\* Validation state

\* Owner

\* Provenance

\* Freshness

\* Outcome history

\* Usage constraints



Memory may support reasoning and confidence.



Memory must not authorize action.



```text

Memory is evidence, not truth.

```



\---



\## Evidence Fusion Rule



Synthetic repositories must support evidence fusion.



At minimum, golden scenarios should provide records that can be classified as:



\* Supporting evidence

\* Weakening evidence

\* Conflicting evidence

\* Missing evidence

\* Evidence gaps



Evidence fusion must preserve provenance and uncertainty.



Evidence fusion must not produce autonomous action.



\---



\## Recommendation Candidate Rule



Synthetic scenarios may produce recommendation candidates.



Recommendation candidates must include:



\* Summary

\* Supporting evidence

\* Weakening or missing evidence

\* Risk level

\* Required controls

\* Human approval requirement

\* Prohibited autonomous actions



Recommendation candidates must not execute remediation.



\---



\## Test Harness Requirements



Synthetic repositories must be deterministic.



The generator must use a stable seed or static golden fixtures.



Tests should verify:



\* Repository generation is deterministic

\* Required record counts exist

\* Golden scenarios exist

\* Golden scenario relationships are valid

\* CMDB traversal works

\* Business impact mapping works

\* Unknown business impact escalates

\* Memory patterns have validation metadata

\* Evidence fusion input categories exist

\* No autonomous remediation path exists

\* Domain terms remain in the domain adapter

\* Core contracts remain domain-neutral



\---



\## Relationship to Real Datasets



Real datasets may be added later for validation, benchmarking, or realism.



Examples may include:



\* Observability datasets

\* Root-cause-analysis datasets

\* ITSM datasets

\* Service management exports

\* Incident/problem/change records

\* CMDB exports



Real datasets can improve realism, but they are not required to establish the Sprint 2.5 architecture contract.



Synthetic repositories are useful because they can intentionally exercise edge cases, governance debt, uncertainty, and safety boundaries.



\---



\## Overclaiming Boundary



EAIOS must not claim that synthetic repository results prove production accuracy.



Acceptable claims:



```text

The architecture supports governed orchestration across ITIL-style records.

The domain adapter can translate IT records into core-facing structures.

The governance and evidence contracts can be tested against deterministic scenarios.

The system preserves uncertainty, provenance, and human approval boundaries.

```



Unacceptable claims:



```text

The system proves real-world root-cause accuracy.

The synthetic data proves production performance.

The generated incidents represent actual enterprise incident distributions.

The recommendations are operationally safe in real production environments.

```



\---



\## Sprint 2.5 Boundary



Sprint 2.5 will use a synthetic IT application-health repository to implement and test production-ready concepts.



Sprint 2.5 may include:



\* Synthetic repository generator

\* Golden scenarios

\* Background alerts and incidents

\* Business service mappings

\* Memory patterns

\* Governance metadata

\* IT application-health domain adapter

\* Evidence fusion package generation

\* Recommendation candidate generation



Sprint 2.5 will not include:



\* Real ServiceNow integration

\* Real CMDB integration

\* Real observability platform integration

\* Real production remediation

\* Production-grade simulation of enterprise incident distributions

\* Real-world accuracy claims

\* Autonomous action execution



\---



\## Consequences



\### Benefits



\* Allows full EAIOS concept transfer without waiting for perfect public datasets

\* Enables deterministic regression tests

\* Supports business-outcome-first demos

\* Exercises governance, evidence, memory, confidence, and approval together

\* Keeps domain data separate from core architecture

\* Prevents overclaiming by defining the test harness boundary



\### Trade-offs



\* Synthetic data requires careful design

\* Synthetic data can create false confidence if overclaimed

\* Golden scenarios require maintenance

\* Real-world validation remains future work

\* Generated scale does not equal production realism



\---



\## Decision Summary



EAIOS will use synthetic domain repositories as deterministic architecture test harnesses.



Sprint 2.5 will use a synthetic IT application-health repository to test governed orchestration, evidence fusion, memory patterns, business impact, and recommendation candidate boundaries.



Synthetic repositories prove architectural behavior.



They do not prove real-world operational accuracy.



