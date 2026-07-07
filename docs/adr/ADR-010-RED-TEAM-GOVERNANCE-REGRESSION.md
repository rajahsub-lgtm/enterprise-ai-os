\# ADR-010: Governance Must Be Proven Through Red-Team Regression Scenarios



\## Status



Accepted



\## Context



EAIOS 2 introduces runtime governance for agentic AI. Architecture diagrams and positive-path demos are not enough to prove that governance works.



A trustworthy governance layer must be tested against failure, misuse, missing metadata, unsafe access attempts, policy violations, and adversarial scenarios.



For EAIOS, the important question is not only:



```text

Can the happy path work?

```



It is also:



```text

Does the system deny, escalate, or fail closed when trust cannot be established?

```



\## Decision



EAIOS will maintain a red-team governance regression library.



The library will define scenarios with:



\* scenario ID

\* scenario name

\* caller agent

\* target agent

\* requested capability

\* requested source or resource

\* Goal Context

\* risk context

\* injected failure or adversarial condition

\* expected decision

\* expected policy reference or reason

\* expected audit behavior

\* expected governance debt behavior, if applicable



Initial red-team scenario categories include:



\* unregistered caller agent

\* rogue source access

\* unknown source metadata

\* missing Goal Context

\* HR source access from non-HR context

\* identity access without proper capability

\* identity access without business justification

\* knowledge write without approval

\* expired approval

\* broker bypass attempt

\* audit failure

\* evidence without provenance

\* stale knowledge

\* prompt-injected knowledge

\* poisoned knowledge

\* unsafe operational command

\* policy conflict

\* missing source owner

\* missing data classification



\## Design Principle



Trustworthiness is demonstrated through repeatable governance regression tests, not asserted through architecture diagrams.



\## Sprint 1 Boundary



In EAIOS 2 Sprint 1, red-team testing is a Defined Interface.



Sprint 1 must include automated scenario tests for the governed Knowledge Agent access path.



The full red-team scenario library and reusable regression runner may be deferred, but the scenario format should be clear enough to evolve into a first-class governance test suite.



Sprint 1 scenario tests must include:



\* approved operational troubleshooting access

\* approved self-help access

\* denied HR source from non-HR context

\* denied identity source through generic retrieval

\* escalated identity access with justification

\* escalated knowledge write

\* governance debt for unknown source

\* denied missing Goal Context

\* denied high-risk uncertainty

\* denied unregistered caller

\* fail-closed audit failure



\## Consequences



This makes governance testable and defensible.



It also prevents EAIOS from relying on demos or manual inspection to validate safety behavior.



The system becomes easier to extend because each new governance capability can be accompanied by a regression scenario.



\## Future Work



Future EAIOS releases may add:



\* `data/governance/red\_team\_scenarios.json`

\* reusable scenario runner

\* expected-vs-actual decision report

\* audit-chain verification in tests

\* content safety red-team tests

\* prompt injection test library

\* policy conflict tests

\* regression dashboard

\* governance maturity scoring



