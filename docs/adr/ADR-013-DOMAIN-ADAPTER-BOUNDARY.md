\# ADR-013: Domain Adapter Boundary



\## Status



Accepted



\## Context



EAIOS began with an IT application-health scenario. The first working version demonstrated that enterprise reasoning could run over application health signals, produce recommendations, and preserve a human approval boundary.



EAIOS 2 then added core governance capabilities:



\* Governance Broker / Policy Enforcement Point

\* Access Governance System / Policy Decision Point

\* Goal Context

\* Agent identity validation

\* Source authorization

\* Governance debt

\* Audit logging

\* Evidence creation

\* Content safety

\* Evidence quality

\* Usage constraints

\* Reasoning eligibility



As EAIOS expands, it must avoid becoming tightly coupled to a single domain such as IT application health.



The platform should support multiple domains, including:



\* IT application health

\* Financial AML investigation

\* Healthcare safety

\* Supply chain risk

\* Other governed reasoning domains



The core architecture should remain stable while domain-specific agents, vocabulary, data sources, mappings, and presentation logic vary by domain.



\## Decision



EAIOS will use a domain adapter architecture.



EAIOS Core owns the domain-neutral governance and reasoning contracts.



Domain adapters own domain-specific terminology, data ingestion, feature extraction, agents, safety vocabulary, and presentation templates.



The core code must remain domain-neutral.



Agents and domains may change.



Governance, evidence, audit, content safety, KT framing, hypothesis, recommendation, and human approval contracts remain stable.



\## Core Responsibilities



EAIOS Core includes:



\* Governance Broker / Policy Enforcement Point

\* Access Governance System / Policy Decision Point

\* ActionRequest

\* Goal Context

\* Agent Registry structure

\* Data Source Registry structure

\* Policy Registry structure

\* Audit logging

\* Governance debt logging

\* Evidence object

\* EvidenceFactory

\* EvidenceQualityScorer

\* ContentSafetyGateway framework

\* EvidenceStore

\* CaseContext contract

\* Entity contract

\* Observation contract

\* KT Case Frame contract

\* Hypothesis contract

\* RecommendationCandidate contract

\* Human approval boundary



Core vocabulary should use domain-neutral concepts:



\* case

\* goal

\* entity

\* observation

\* evidence

\* hypothesis

\* risk

\* control

\* recommendation candidate

\* approval

\* audit



Core code must not depend on IT-specific vocabulary such as:



\* application

\* incident

\* alert

\* outage

\* runbook

\* major incident

\* service health

\* remediation



Nor should it depend on financial-specific vocabulary such as:



\* transaction

\* account

\* counterparty

\* laundering

\* SAR

\* mule account

\* structuring

\* layering



Those terms belong in domain adapters.



\## Domain Adapter Responsibilities



Domain adapters include:



\* Domain-specific data loaders

\* Domain-specific source mappings

\* Domain-specific entity mappings

\* Domain-specific observation mappings

\* Domain-specific KT case frame mappings

\* Domain-specific agents

\* Domain-specific safety tokens and policy extensions

\* Domain-specific presentation templates

\* Domain-specific demo scripts



Domain adapters translate domain concepts into EAIOS Core contracts.



A domain adapter may extend policy or safety rules, but it must not bypass:



\* Governance Broker

\* Access Governance System

\* EvidenceFactory

\* ContentSafetyGateway

\* Audit logging

\* Evidence-to-audit linkage

\* Human approval boundaries



\## IT Application Health Adapter



The IT application-health adapter owns terms such as:



\* application

\* service

\* incident

\* alert

\* event cluster

\* telemetry

\* runbook

\* known error

\* major incident

\* service health

\* remediation candidate



The IT adapter maps these terms into core concepts:



| IT Domain Concept     | Core Concept                     |

| --------------------- | -------------------------------- |

| Application / service | Entity                           |

| Incident / alert      | Observation                      |

| Event cluster         | Observation cluster              |

| Runbook / known error | Evidence source / knowledge item |

| Business impact       | Risk / impact                    |

| Root cause candidate  | Hypothesis                       |

| Remediation proposal  | RecommendationCandidate          |

| Change approval       | Human approval                   |



\## Financial AML Adapter



The financial AML adapter owns terms such as:



\* transaction

\* account

\* customer

\* counterparty

\* transaction cluster

\* laundering label

\* structuring

\* layering

\* mule account

\* suspicious activity

\* investigator review



The financial AML adapter maps these terms into core concepts:



| AML Domain Concept                     | Core Concept                       |

| -------------------------------------- | ---------------------------------- |

| Account / customer / counterparty      | Entity                             |

| Transaction                            | Observation                        |

| Transaction cluster                    | Observation cluster                |

| Laundering label                       | Ground-truth / validation signal   |

| Suspicious pattern                     | Risk signal                        |

| Structuring / layering / mule behavior | Hypothesis                         |

| Investigator review                    | Human approval                     |

| SAR or enforcement action              | Out of scope for autonomous action |



\## File Classification Rule



Every new source file should include a short classification header.



Examples:



```python

"""

Classification: EAIOS Core



This module defines a domain-neutral contract used across all domain adapters.

"""

```



```python

"""

Classification: IT Application Health Domain Adapter



This module converts IT application-health records into EAIOS generic

CaseContext, Entity, Observation, and Evidence-compatible structures.

"""

```



```python

"""

Classification: Financial AML Domain Adapter



This module converts AML transaction records into EAIOS generic

CaseContext, Entity, Observation, and Evidence-compatible structures.

"""

```



\## Runtime Data Rule



Runtime data files generated by demos or executions are domain-specific unless they are explicitly part of the core audit/evidence infrastructure.



For EAIOS 1, runtime memory files such as application-health memory and execution history are treated as IT application-health domain runtime artifacts.



They should not be used as the model for cross-domain core memory without review.



\## Consequences



This decision allows EAIOS to complete a strong IT application-health story without contaminating the core architecture.



It also prepares EAIOS to prove domain independence later using financial AML data.



The next priority is to complete the IT application-health story with real external RCA-style data, while keeping all new IT-specific code inside the IT domain adapter boundary.



\## Decision Summary



EAIOS Core remains stable and domain-neutral.



Domain adapters change by use case.



Agents may change by domain.



No domain adapter may bypass governance, evidence creation, content safety, audit linkage, or human approval.



