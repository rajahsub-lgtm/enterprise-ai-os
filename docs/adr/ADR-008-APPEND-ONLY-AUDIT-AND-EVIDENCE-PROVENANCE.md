\# ADR-008: Audit Is Append-Only and Tamper-Evident; Evidence Carries Provenance



\## Status



Accepted



\## Context



EAIOS 2 governs agent actions at runtime. Governance decisions must be explainable, reviewable, and auditable.



A normal mutable log is not sufficient for governance because later changes could obscure what was known, decided, approved, denied, or escalated at the time of action.



EAIOS also depends on evidence. Evidence may come from telemetry, incidents, knowledge sources, wiki pages, runbooks, user reports, system alerts, reasoning agents, or future LLM outputs. Evidence is only useful if its provenance is known.



The system must be able to answer:



\* What evidence supported this decision?

\* Where did the evidence come from?

\* Who or what collected it?

\* When was it collected?

\* What was the source classification and trust level?

\* Which policies were applied?

\* What decision was made?

\* Was the audit trail modified later?



\## Decision



EAIOS audit records will be append-only and tamper-evident.



Each audit record must include:



\* audit ID

\* request ID

\* timestamp

\* caller agent

\* target agent

\* requested capability

\* requested source or resource

\* Goal Context reference

\* policy references

\* decision

\* required controls

\* risk tier

\* evidence references, when available

\* previous record hash

\* current record hash



Corrections, reversals, new approvals, or updated conclusions must be appended as new audit records. Existing audit records must not be overwritten.



EAIOS evidence objects must carry provenance metadata.



Each evidence object should include:



\* evidence ID

\* source ID

\* source owner

\* source type

\* classification

\* trust level

\* collection time

\* collecting agent

\* collection method

\* content hash or signature where available

\* attribution

\* quality signals

\* policy or usage constraints



\## Design Principle



Evidence and audit records together form a chain of custody from signal to decision.



Governance should not merely record the final answer. It should preserve the path from observed evidence, to interpretation, to policy evaluation, to decision, to action or non-action.



\## Sprint 1 Boundary



In EAIOS 2 Sprint 1, basic audit logging is an Operational Capability.



The audit logger must write a record for each completed governance decision.



A lightweight hash-chain implementation or hook may be included as an Architectural Foundation. Production-grade immutable storage, external ledger integration, write-once storage, and advanced tamper detection are deferred.



Evidence provenance is an Architectural Foundation in Sprint 1. The evidence object and provenance fields may be defined, but full evidence fusion and provenance graph behavior are deferred.



\## Consequences



This improves trust, reviewability, and enterprise defensibility.



It also prevents EAIOS from treating reasoning outputs, including future LLM outputs, as ungrounded assertions.



The system becomes able to explain not only what it decided, but why the decision was justified at the time.



\## Future Work



Future EAIOS releases may add:



\* JSONL append-only audit files

\* audit-chain verification tool

\* external immutable storage

\* evidence graph

\* provenance visualization

\* policy-to-evidence traceability

\* audit export

\* compliance reporting

\* tamper detection alerts



