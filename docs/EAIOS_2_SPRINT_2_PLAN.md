# EAIOS 2 Sprint 2 Plan

## Sprint Name

Governed Evidence and Content Safety

## Version Theme

Sprint 1 proved that EAIOS can govern whether an agent may access a source for a given Goal Context.

Sprint 2 proves that authorized knowledge does not automatically become trusted evidence.

## Sprint 2 Objective

Prove that after source access is approved, retrieved knowledge is converted into structured Evidence with provenance, deterministic quality signals, content-safety status, usage constraints, and linkage back to the governed access decision.

## Core Question

Authorized source access does not mean safe content use.

Can EAIOS prevent unsafe, stale, low-quality, low-trust, or non-authoritative content from influencing reasoning?

---

# Sprint 2 Start Gate

Sprint 2 starts only after the existing baseline remains green.

Required command:

```text
python -m pytest
```

Expected current baseline:

```text
13 passed
```

Sprint 2 must not begin if Sprint 0 or Sprint 1 tests are failing.

---

# Sprint 2 Architectural Principle

Source authorization is a gate before retrieval.

Content safety is a gate before reasoning.

Sprint 1 answered:

```text
May this agent access this source for this Goal Context?
```

Sprint 2 answers:

```text
Is the retrieved content safe and trustworthy enough to become evidence?
```

---

# Sprint 2 Flow

```text
Knowledge Agent requests access
↓
GovernanceBroker / PEP intercepts
↓
AGS / PDP evaluates policy
↓
Access-decision audit record is written
↓
Broker returns approved sources + audit_id
↓
GovernedKnowledgeClient retrieves mock knowledge items
↓
EvidenceFactory creates Evidence objects
↓
Evidence carries request_id + access_decision_audit_id
↓
EvidenceQualityScorer scores evidence quality
↓
ContentSafetyGateway classifies content safety
↓
EvidenceStore records evidence
↓
Only safe, controlled, or supporting evidence can proceed
```

---

# Audit Linkage Rule

Audit records are append-only.

The Sprint 1 access-decision audit record is written before retrieval and must not be mutated after Evidence is created.

Therefore, Evidence points back to the access-decision audit record.

Each Evidence object must include:

* request_id
* access_decision_audit_id
* source_id
* source owner
* collection timestamp
* collecting agent
* collection method
* content hash
* provenance metadata

If evidence creation itself needs to be audited, EAIOS must append a second audit event. It must not update the original access-decision audit record.

Design principle:

```text
Audit records are append-only.
Evidence points back to the audit decision that authorized retrieval.
Later lifecycle events append new audit records; they do not rewrite old ones.
```

---

# Sprint 2 Implementation Maturity

## Operational Capabilities

These are built and tested in Sprint 2.

| Capability                | Sprint 2 Implementation                                                           |
| ------------------------- | --------------------------------------------------------------------------------- |
| Evidence object           | Structured Evidence with identity, source, provenance, quality, safety, and usage |
| EvidenceFactory           | Converts governed retrieval results into Evidence                                 |
| Evidence provenance       | Source ID, source owner, collection time, collecting agent, method, content hash  |
| EvidenceQualityScorer     | Deterministic quality scoring from metadata and content signals                   |
| ContentSafetyGateway      | Classifies content before it can enter reasoning                                  |
| EvidenceStore             | Records created Evidence objects                                                  |
| Evidence-to-audit linkage | Evidence carries request_id and access_decision_audit_id                          |
| Reasoning eligibility     | Evidence includes content_safety.allowed_for_reasoning                            |
| Authority marking         | Evidence includes usage.authoritative and usage.level                             |
| Safe evidence boundary    | Unsafe or review-required content cannot proceed to reasoning                     |

## Architectural Foundations

These are structurally prepared but not fully implemented.

| Capability                     | Sprint 2 Boundary                                     |
| ------------------------------ | ----------------------------------------------------- |
| Full provenance graph          | Evidence references exist; graph representation later |
| Prompt-injection detection     | Basic deterministic patterns only                     |
| Stale-content detection        | Metadata-based only                                   |
| Conflicting guidance detection | Basic placeholder or simple deterministic rule        |
| Evidence fusion                | Not full hypothesis ranking yet                       |
| GraphRAG                       | Not implemented; prepared as future source type       |

## Defined Interfaces

These contracts are defined now for future expansion.

| Interface             | Sprint 2 Boundary                                      |
| --------------------- | ------------------------------------------------------ |
| EvidenceQualityScorer | Deterministic implementation now; richer scoring later |
| ContentSafetyGateway  | Rule-based implementation now; ML/LLM evaluators later |
| EvidenceStore         | File-backed or in-memory now; persistent graph later   |

## Roadmap Capabilities

These are explicitly out of Sprint 2.

* Real GraphRAG
* Vector search
* LLM content safety evaluation
* Full evidence fusion
* Full reasoning / hypothesis ranking
* Full Enterprise Command Center UI
* Production document ingestion
* Autonomous remediation
* Production security integration

---

# Sprint 2 Data Files

```text
data/governance/
  mock_knowledge_items.json
  evidence_log.json
```

---

# Sprint 2 Code Files

New files:

```text
src/governance/
  evidence.py
  evidence_factory.py
  evidence_quality_scorer.py
  content_safety_gateway.py
  evidence_store.py
```

Modified Sprint 1 files:

```text
src/governance/
  governance_broker.py
  governed_knowledge_client.py
```

Reason for modifying Sprint 1 files:

```text
GovernanceBroker and GovernedKnowledgeClient must surface approved sources, mock retrieval items, request_id, and access_decision_audit_id into the evidence creation path.
```

---

# Sprint 2 Test Files

```text
tests/
  test_evidence_safety.py
```

Sprint 2 validation must be automated. It must not rely on manual demo review.

---

# Evidence Object Contract

Example shape:

```json
{
  "evidence_id": "ev-001",
  "request_id": "req-001",
  "access_decision_audit_id": "audit-req-001-20260707120000",
  "source_id": "support_knowledge",
  "source_owner": "Enterprise Support Operations",
  "classification": "internal",
  "trust_level": "approved",
  "collected_by": "knowledge_agent",
  "collection_method": "governed_mock_retrieval",
  "collected_at": "2026-07-07T12:00:00",
  "content_summary": "Known timeout pattern for payment connector.",
  "content_hash": "sha256...",
  "quality": {
    "score": 0.88,
    "level": "HIGH",
    "signals": [
      "approved_source",
      "owner_present",
      "last_validated_present",
      "fresh_content"
    ]
  },
  "usage": {
    "level": "authoritative",
    "authoritative": true,
    "reason": "Approved support knowledge with owner and freshness metadata."
  },
  "content_safety": {
    "status": "SAFE_WITH_CONTROLS",
    "allowed_for_reasoning": true,
    "reason": "Operational content from approved source requires validation before action.",
    "required_controls": [
      "human_validation",
      "check_recent_changes"
    ]
  }
}
```

The `source_owner` value must come from the Data Source Registry. It should not be hardcoded independently in the EvidenceFactory.

---

# Content Safety Statuses

| Status               | Meaning                                                |
| -------------------- | ------------------------------------------------------ |
| `SAFE`               | Content may be used normally                           |
| `SAFE_WITH_CONTROLS` | Content may be used with required controls             |
| `SUPPORTING_ONLY`    | Content may support reasoning but is not authoritative |
| `NEEDS_HUMAN_REVIEW` | Content requires human review before use               |
| `UNSAFE`             | Content must not be used                               |

---

# Reasoning Eligibility by Content-Safety Status

| Status               | allowed_for_reasoning | Authoritative? | Meaning                                           |
| -------------------- | --------------------: | -------------: | ------------------------------------------------- |
| `SAFE`               |                  true |           true | May be used normally                              |
| `SAFE_WITH_CONTROLS` |                  true |           true | May be used with required controls                |
| `SUPPORTING_ONLY`    |                  true |          false | May support reasoning but cannot be authoritative |
| `NEEDS_HUMAN_REVIEW` |                 false |          false | Must not enter reasoning until reviewed           |
| `UNSAFE`             |                 false |          false | Must not enter reasoning                          |

---

# Deterministic Sprint 2 Content-Safety Rules

Sprint 2 uses deterministic metadata and content-pattern rules.

These rules are intentionally simple so tests and implementation agree on the contract.

| Rule                                        | Conditions                                                                                                                   | Status               | Usage                  |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------- | ---------------------- |
| Approved operational source                 | `trust_level == approved`, owner present, `last_validated` present and fresh, operational action content                     | `SAFE_WITH_CONTROLS` | authoritative          |
| Conditional source with owner and freshness | `trust_level == conditional`, owner present, `last_validated` present and fresh                                              | `SUPPORTING_ONLY`    | supporting             |
| Missing owner                               | owner missing or blank                                                                                                       | `NEEDS_HUMAN_REVIEW` | not authoritative      |
| Stale content with owner                    | `last_validated` older than stale threshold, owner present                                                                   | `SUPPORTING_ONLY`    | supporting             |
| Prompt-injection pattern                    | content contains instruction-like override such as “ignore previous instructions”, “bypass policy”, or “override governance” | `UNSAFE`             | blocked                |
| Unsafe operational command                  | content recommends destructive or production-impacting command without validation language                                   | `NEEDS_HUMAN_REVIEW` | blocked pending review |
| Low-trust content                           | `trust_level` below approved or conditional                                                                                  | `SUPPORTING_ONLY`    | supporting only        |

## Staleness Definition

For Sprint 2, content is stale when:

```text
last_validated is more than 180 days before collected_at
```

This threshold is policy-configurable in future sprints, but fixed in Sprint 2 tests.

## Low-Trust Definition

For Sprint 2:

```text
approved      = high trust
conditional   = usable as supporting evidence
unverified    = low trust
unknown/null  = low trust
```

Low-trust content cannot be authoritative and cannot independently drive a recommendation.

---

# Quality Scoring Rules

Sprint 2 quality scoring is deterministic and intentionally simple.

The quality score is not a production model. It is a testable starting point.

## Quality Signals

| Signal                 | Effect                               |
| ---------------------- | ------------------------------------ |
| approved source        | increases quality                    |
| conditional source     | moderate quality                     |
| owner present          | increases quality                    |
| owner missing          | lowers quality and triggers review   |
| last_validated present | increases quality                    |
| fresh content          | increases quality                    |
| stale content          | lowers quality                       |
| content hash present   | increases quality                    |
| low-trust source       | lowers quality                       |
| unsafe content pattern | quality does not make content usable |

## Quality Levels

|   Score Range | Level    |
| ------------: | -------- |
| `0.80 - 1.00` | `HIGH`   |
| `0.50 - 0.79` | `MEDIUM` |
| `0.00 - 0.49` | `LOW`    |

Quality is not the same as safety.

A high-quality item may still be blocked if content safety is `UNSAFE`.

---

# Sprint 2 Automated Scenarios

All scenarios must be implemented as automated assertions in `tests/test_evidence_safety.py`.

|  # | Scenario                                                            | Expected                                         |
| -: | ------------------------------------------------------------------- | ------------------------------------------------ |
|  1 | Approved support knowledge becomes evidence                         | `SAFE_WITH_CONTROLS`                             |
|  2 | Wiki knowledge with owner and freshness becomes supporting evidence | `SUPPORTING_ONLY`                                |
|  3 | Wiki knowledge missing owner requires review                        | `NEEDS_HUMAN_REVIEW`                             |
|  4 | Stale content with owner is not authoritative                       | `SUPPORTING_ONLY`                                |
|  5 | Prompt-injection-like content is blocked                            | `UNSAFE`                                         |
|  6 | Unsafe operational command requires review                          | `NEEDS_HUMAN_REVIEW`                             |
|  7 | Low-trust content cannot drive recommendation                       | `SUPPORTING_ONLY`                                |
|  8 | Evidence record includes provenance and content hash                | Required fields asserted                         |
|  9 | Evidence links back to access decision audit ID                     | request_id and access_decision_audit_id asserted |
| 10 | Unsafe content does not proceed to reasoning                        | `allowed_for_reasoning == false`                 |

---

# Scenario Details

## Scenario 1 — Approved Support Knowledge Becomes Evidence

```text
Source:
support_knowledge

trust_level:
approved

owner:
Enterprise Support Operations

last_validated:
fresh

Content:
operational support content with recommended validation controls

Expected content safety:
SAFE_WITH_CONTROLS

Expected usage:
authoritative

Expected allowed_for_reasoning:
true
```

Purpose:

Proves that approved support knowledge can become governed evidence, but operational action content still carries controls.

---

## Scenario 2 — Wiki Knowledge With Owner and Freshness Becomes Supporting Evidence

```text
Source:
wiki_knowledge

trust_level:
conditional

owner:
Enterprise Knowledge Operations

last_validated:
fresh

Expected content safety:
SUPPORTING_ONLY

Expected usage:
supporting

Expected authoritative:
false

Expected allowed_for_reasoning:
true
```

Purpose:

Proves conditional knowledge may support reasoning but cannot be authoritative.

---

## Scenario 3 — Wiki Knowledge Missing Owner Requires Review

```text
Source:
wiki_knowledge

trust_level:
conditional

owner:
missing

Expected content safety:
NEEDS_HUMAN_REVIEW

Expected usage:
not authoritative

Expected allowed_for_reasoning:
false
```

Purpose:

Proves missing ownership prevents content from entering reasoning.

---

## Scenario 4 — Stale Content With Owner Is Not Authoritative

```text
Source:
wiki_knowledge

trust_level:
conditional

owner:
present

last_validated:
older than 180 days before collected_at

Expected content safety:
SUPPORTING_ONLY

Expected usage:
supporting

Expected authoritative:
false

Expected allowed_for_reasoning:
true
```

Purpose:

Proves stale but owned content may support investigation but cannot be authoritative.

---

## Scenario 5 — Prompt-Injection-Like Content Is Blocked

```text
Content includes:
ignore previous instructions
bypass policy
override governance

Expected content safety:
UNSAFE

Expected usage:
blocked

Expected allowed_for_reasoning:
false
```

Purpose:

Proves instruction-like content cannot enter reasoning.

---

## Scenario 6 — Unsafe Operational Command Requires Review

```text
Content includes:
restart production service immediately
delete records
disable monitoring
without validation language

Expected content safety:
NEEDS_HUMAN_REVIEW

Expected usage:
blocked pending review

Expected allowed_for_reasoning:
false
```

Purpose:

Proves destructive or production-impacting operational commands require human review.

---

## Scenario 7 — Low-Trust Content Cannot Drive Recommendation

```text
trust_level:
unverified or unknown

Expected content safety:
SUPPORTING_ONLY

Expected usage:
supporting only

Expected authoritative:
false

Expected allowed_for_reasoning:
true
```

Purpose:

Proves low-trust content may provide context but cannot independently drive a recommendation.

---

## Scenario 8 — Evidence Record Includes Provenance and Content Hash

Required assertions:

```text
evidence_id exists
request_id exists
access_decision_audit_id exists
source_id exists
source_owner exists
collected_by exists
collection_method exists
collected_at exists
content_hash exists
quality exists
content_safety exists
usage exists
```

Purpose:

Proves Evidence is not just content; it is content with provenance and governance metadata.

---

## Scenario 9 — Evidence Links Back to Access Decision Audit ID

Required assertions:

```text
Evidence.request_id == governed request ID
Evidence.access_decision_audit_id == access decision audit ID returned by Broker
```

Purpose:

Proves Evidence points back to the audit decision that authorized retrieval without mutating the original audit record.

---

## Scenario 10 — Unsafe Content Does Not Proceed to Reasoning

Required assertions:

```text
content_safety.status == UNSAFE
content_safety.allowed_for_reasoning == false
usage.authoritative == false
```

Purpose:

Proves unsafe content is blocked before reasoning.

---

# Sprint 2 Acceptance Criteria

Sprint 2 is complete when:

1. Sprint 0 smoke test still passes.
2. All Sprint 1 governance scenario tests still pass.
3. All Sprint 2 evidence and content-safety tests pass.
4. Approved source access returns governed mock knowledge items.
5. Each retrieved item is converted into an Evidence object.
6. Each Evidence object includes provenance.
7. Each Evidence object includes a deterministic quality score.
8. Each Evidence object includes content safety status.
9. `UNSAFE` and `NEEDS_HUMAN_REVIEW` evidence has `content_safety.allowed_for_reasoning == false`.
10. `SUPPORTING_ONLY` evidence has `content_safety.allowed_for_reasoning == true` and `usage.authoritative == false`.
11. `SAFE` and `SAFE_WITH_CONTROLS` evidence has `content_safety.allowed_for_reasoning == true`.
12. Each Evidence object includes `request_id` and `access_decision_audit_id`.
13. The original Sprint 1 access-decision audit record is not mutated.
14. No retrieved content enters reasoning without Evidence creation and content-safety classification.
15. Deterministic content-safety rules are documented and covered by automated tests.
16. The implementation maturity map is documented so operational capabilities are not confused with foundations, interfaces, or roadmap capabilities.

---

# Sprint 2 Non-Goals

Sprint 2 explicitly does not include:

* Real GraphRAG
* Real vector retrieval
* Real LLM reasoning
* Real LLM content-safety review
* Full evidence fusion
* Full hypothesis ranking
* Full Enterprise Command Center UI
* Production document ingestion
* Autonomous remediation
* Production security integration
* Production immutable audit storage
* Production policy engine

---

# Final Sprint 2 Boundary Statement

EAIOS 2 Sprint 2 operationalizes governed evidence creation and content safety for approved knowledge access.

It extends the Sprint 1 Zero Trust access path by converting retrieved knowledge into Evidence with provenance, deterministic quality signals, content-safety status, usage constraints, reasoning eligibility, and linkage back to the access-decision audit record.

It does not implement full GraphRAG, real enterprise retrieval, LLM reasoning, full evidence fusion, production content safety, or production compliance automation.
