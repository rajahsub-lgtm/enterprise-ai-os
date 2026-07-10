# EAIOS 2 Legacy Deprecation Map

## Purpose

This document defines the boundary between EAIOS 1 legacy runtime artifacts and the EAIOS 2 Sprint 3-engine architecture.

Sprint 3-engine must not blend old skeleton runtime behavior with the new governed adaptive orchestration engine.

## Current Status

EAIOS 1 skeleton demo artifacts have been retired:

- `demo.py` removed
- hard-coded application-health example files removed
- old Sprint 0 smoke test removed
- `app.py` now runs the EAIOS 2 application-health concept path

Some `src/eaios/runtime` modules remain temporarily because existing architecture contract tests still validate business-outcome-first concepts.

These retained modules are not the Sprint 3 orchestration runtime.

## Legacy Runtime Boundary

| Legacy module | Current status | Sprint 3 replacement / disposition |
|---|---|---|
| `src/eaios/runtime/business_outcome_manager.py` | Temporarily retained | Business outcome concept remains, but Sprint 3 orchestration should use EAIOS 2 contracts and orchestrator modules. |
| `src/eaios/runtime/capability_assessor.py` | Temporarily retained | Future EAIOS 2 capability evaluation should move behind contracts/orchestration modules. |
| `src/eaios/runtime/task_planner.py` | Temporarily retained | Replaced conceptually by Sprint 3 adaptive orchestrator and agent-step planning. |
| `src/eaios/runtime/skill_matcher.py` | Temporarily retained | Future skill matching should be modeled explicitly as a governed orchestration capability. |
| `src/eaios/runtime/agent_orchestrator.py` | Temporarily retained | Replaced by Sprint 3 `src/orchestration/adaptive_orchestrator.py`. |
| `src/eaios/runtime/enterprise_memory.py` | Legacy memory implementation | Not used as Sprint 3 writable enterprise memory. Sprint 3-engine uses simulated memory-state fixtures. |
| `src/eaios/runtime/execution_logger.py` | Legacy execution logging | Sprint 3 uses structured orchestration trace and governance trace view-models. |
| `src/eaios/runtime/learning_engine.py` | Legacy learning concept | Real writable governed learning store is deferred to Sprint 3.1 / v1.2. |
| `src/eaios/runtime/pattern.py` | Legacy pattern support | Sprint 3 uses simulated memory-state model and governed evidence records. |

## Sprint 3 Engine Boundary

Sprint 3-engine core packages are:

```text
src/governance
src/contracts
src/orchestration
src/views
```

These packages must not import from the old `src.eaios.runtime` namespace.

The current `tests/test_business_outcome_entry_point.py` may continue to import legacy runtime modules until a future migration replaces that contract.

## Seam Reuse Map

Sprint 3 must not create a second parallel governed retrieval stack.

Sprint 3 extends and packages the existing seam.

| Existing seam element | Sprint 3 usage |
|---|---|
| `ActionRequest` | Wrapped by `SourceAccessRequest`. |
| `GovernedKnowledgeClient` | Reused or delegated by `GovernedEvidenceClient`. |
| `KnowledgeRepository` | Extended as the governed source adapter pattern. |
| `EvidenceFactory` | Remains the evidence creation mechanism. |
| `ContentSafetyGateway` | Remains the safety classifier for free-text evidence. |
| `EvidenceStore` | Remains the evidence persistence layer. |
| `GovernanceBroker / AGS` | Remains the access-control mechanism. |

## Key Rule

```text
Sprint 3 adds packaging and orchestration around the existing governed seam.
Sprint 3 does not fork governance, evidence creation, content safety, or evidence storage.
```

## Structured vs Free-Text Evidence Reminder

Sprint 3 must distinguish:

```text
free-text evidence
structured-record evidence
```

Free-text evidence uses content safety scanning.

Structured records use governed provenance, source trust, schema validation, and freshness checks.

Structured records are not automatically truth.

They are only eligible for reasoning when governed, trusted, schema-valid, and fresh enough.

## Deferred Work

A real writable governed enterprise memory store is deferred to:

```text
Sprint 3.1 / v1.2
```

Sprint 3-engine uses simulated memory-state fixtures for deterministic demo behavior.

## Sprint 3-UI Dependency

Sprint 3-UI must not invent runtime state.

It should render tested Sprint 3-engine view-models only.
