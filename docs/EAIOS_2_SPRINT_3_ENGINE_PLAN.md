# EAIOS 2 Sprint 3-engine Plan

## Sprint Name

EAIOS 2 Sprint 3-engine — Governed Adaptive Orchestration Core

## Sprint North Star

Make the engine truthful before making the demo beautiful.

Sprint 3-engine builds the headless, test-backed core required for the future Sprint 3-UI demo.

The goal is not to build a polished UI yet.

The goal is to prove that EAIOS can perform governed, explainable, adaptive multi-agent orchestration where operational confidence determines the level of due diligence and governance remains mandatory.

## Starting Point

Sprint 2.5 is complete and tagged as:

```text
eaios-2-sprint-2.5-sprint3-ready
```

Sprint 2.5 delivered:

- Governed retrieval seam
- Synthetic ITIL application-health repository
- Domain adapter boundary
- Evidence fusion
- KT-lite reasoning explanation
- Operational confidence gate
- Recommendation candidate
- Human review package
- EAIOS 1 skeleton demo cleanup
- Current executable demo through `python app.py`
- Final verified baseline of 143 passing tests

Sprint 3-engine begins from that foundation.

## Sprint 3-engine Mission

Build the headless engine that proves:

```text
Every agent source access is registered and governed.
Every evidence item entering fusion came through the existing governed seam.
Unsafe and review-required content cannot enter reasoning.
Denied source access creates a traceable evidence gap.
CaseContext is validated by phase.
Operational confidence determines due-diligence depth.
Behavior is adaptive, explainable, and not random.
Governance is never optional.
Human approval remains required.
Autonomous production action remains disabled.
```

## Explicit Non-Goals

Sprint 3-engine does not include:

- Streamlit UI
- Polished demo screens
- Large 50k-record generated dataset
- Real writable enterprise memory store
- Human review workflow UI
- Production integrations
- Autonomous remediation or production action

The UI will come after the headless engine is green.

## Sprint 3-engine Build Sequence

```text
3E-0 Registry expansion
3E-1 Legacy deprecation boundary and seam reuse map
3E-2 CaseContext contract and validator
3E-3 Governed evidence package and seam-to-fusion unification
3E-4 Adaptive orchestrator and orchestration trace
3E-5 Operational-confidence adaptive depth
3E-6 Governance trace view-model
3E-7 Scenario and memory-state model
3E-8 End-to-end headless engine DoD
```

---

# 3E-0 — Registry Expansion for Sprint 3 Agents and Sources

## Purpose

Register Sprint 3 orchestration agents and governed sources before building the orchestrator.

The adaptive orchestrator cannot truthfully execute governed agent steps unless those agents and sources exist in the Governance Broker / AGS registry.

## Why This Comes First

If new agents are not registered, AGS should deny their requests.

If new sources are not registered, AGS should deny or escalate access unexpectedly.

Governed orchestration requires the registry to expand before orchestration code.

## Sprint 3 Agents to Register

Add these to `data/governance/agents.json`:

```text
adaptive_orchestrator_agent
memory_pattern_agent
incident_correlation_agent
cmdb_impact_agent
business_impact_agent
change_analysis_agent
knowledge_retrieval_agent
```

Each agent must include:

```text
agent_id
capabilities
allowed_target_agents
allowed_goal_categories
metadata_complete
```

## Sprint 3 Sources to Register

Add these to `data/governance/data_sources.json`:

```text
enterprise_memory
itil_incidents
itil_changes
itil_cmdb_topology
itil_business_impact_map
itil_operational_records
```

Important:

```text
support_knowledge already exists.
Reuse it.
Do not create a duplicate support knowledge source.
```

## Required Source Schema

Each source must satisfy the full AGS schema:

```text
source_id
allowed_capabilities
allowed_goal_categories
metadata_complete
high_impact_signals
required_controls
trust_level
classification
owner
```

## Trust-Level Guidance

Set trust deliberately because it affects evidence quality and fusion:

```text
itil_cmdb_topology          → APPROVED / HIGH trust
itil_business_impact_map    → APPROVED / HIGH trust
itil_incidents              → APPROVED / MEDIUM-HIGH trust
itil_changes                → APPROVED / MEDIUM-HIGH trust
itil_operational_records    → APPROVED / MEDIUM-HIGH trust
enterprise_memory           → CONDITIONAL trust
support_knowledge           → governed knowledge trust rules
```

## Planned Agent-to-Source Access

```text
memory_pattern_agent        → enterprise_memory
incident_correlation_agent  → itil_incidents
cmdb_impact_agent           → itil_cmdb_topology
business_impact_agent       → itil_business_impact_map
change_analysis_agent       → itil_changes
knowledge_retrieval_agent   → support_knowledge
adaptive_orchestrator_agent → orchestration coordination only
```

## Tests

Add:

```text
tests/test_sprint3_governance_registry_expansion.py
```

Core assertions:

```text
all Sprint 3 agents are registered
all Sprint 3 sources are registered
each planned source access has an allow policy
unregistered agent is denied
wrong-source access is denied
support_knowledge is reused and not duplicated
all sources satisfy full AGS schema
```

---

# 3E-1 — Legacy Deprecation Boundary and Seam Reuse Map

## Purpose

Prevent EAIOS 1 runtime concepts and EAIOS 2 Sprint 3 engine concepts from blending.

## Deliverables

```text
docs/EAIOS_2_LEGACY_DEPRECATION_MAP.md
tests/test_legacy_runtime_boundary.py
```

## Required Deprecation Map

The document must map:

```text
Old EAIOS 1 runtime module
→ Current status
→ Sprint 3 replacement or reason retained
```

## Required Seam Reuse Map

Sprint 3 must not create a second parallel governed retrieval stack.

The design must explicitly reuse the existing seam:

```text
Existing ActionRequest              → wrapped by SourceAccessRequest
Existing GovernedKnowledgeClient    → reused/delegated by GovernedEvidenceClient
Existing KnowledgeRepository        → extended as governed source adapter pattern
Existing EvidenceFactory            → remains evidence creation mechanism
Existing ContentSafetyGateway       → remains safety classification mechanism
Existing EvidenceStore              → remains evidence persistence mechanism
Existing GovernanceBroker / AGS     → remains access-control mechanism
```

## Key Rule

```text
Sprint 3 adds packaging and orchestration around the existing seam.
Sprint 3 does not fork governance, evidence, safety, or storage.
```

---

# 3E-2 — CaseContext Contract and Validator

## Purpose

The Sprint 3 orchestrator will assemble context incrementally.

Partial context is valid early in orchestration.

Downstream execution must require phase-appropriate validation.

## Deliverables

```text
src/contracts/case_context.py
src/contracts/case_context_validator.py
tests/test_case_context_contract.py
```

## Required Phases

```text
INITIAL_SIGNAL
PARTIAL_CONTEXT
GOVERNED_EVIDENCE_COLLECTED
FUSION_READY
REASONING_READY
RECOMMENDATION_READY
HUMAN_REVIEW_READY
```

## Validation Rules

```text
INITIAL_SIGNAL can be minimal.
PARTIAL_CONTEXT can be incomplete.
GOVERNED_EVIDENCE_COLLECTED requires a governed evidence package.
FUSION_READY requires governed, safety-classified evidence.
REASONING_READY requires a fusion result.
RECOMMENDATION_READY requires reasoning explanation.
HUMAN_REVIEW_READY requires recommendation candidate and approval boundary.
```

## Key Rule

```text
Partial context is allowed.
Invalid fusion-ready context is not allowed.
```

---

# 3E-3 — Governed Evidence Package and Seam-to-Fusion Unification

## Purpose

Make the demo actually governed by connecting source access, evidence creation, safety classification, evidence storage, and evidence fusion into one path.

## Current Gap

Sprint 2.5 has two partially separate paths:

```text
Path A:
Governed retrieval seam
Broker → EvidenceFactory → ContentSafetyGateway → EvidenceStore

Path B:
App-health concept path
Domain Adapter → Case Context → EvidenceFusionEngine → Reasoning → Recommendation
```

Sprint 3-engine must unify these paths.

## Target Flow

```text
Agent Source Request
→ Governance Broker
→ Governed Source Adapter
→ EvidenceFactory
→ ContentSafetyGateway
→ EvidenceStore
→ GovernedEvidencePackage
→ EvidenceFusionEngine
```

## Deliverables

```text
src/governance/source_access_request.py
src/governance/source_access_result.py
src/governance/governed_evidence_package.py
src/governance/governed_evidence_client.py
tests/test_governed_evidence_to_fusion_seam.py
```

## Seam Reuse Constraint

```text
SourceAccessRequest wraps existing ActionRequest.
GovernedEvidenceClient delegates to GovernedKnowledgeClient where possible.
GovernedEvidenceClient shapes outputs into GovernedEvidencePackage.
EvidenceFactory remains the source of evidence IDs.
Evidence IDs must preserve real EvidenceFactory format, such as ev-<hash>.
ContentSafetyGateway remains the safety classifier for free-text evidence.
EvidenceStore remains the persistence layer.
```

## Evidence Classes

Structured enterprise records and free-text knowledge do not have the same safety contract.

Sprint 3-engine must define two evidence classes.

### Free-Text Evidence

Examples:

```text
support knowledge
runbook-style knowledge
analyst notes
```

Safety rules:

```text
prompt-injection scan
staleness check
owner / validation check
trust classification
content safety classification
```

### Structured-Record Evidence

Examples:

```text
itil_incidents
itil_changes
itil_cmdb_topology
itil_business_impact_map
itil_operational_records
enterprise_memory
```

Safety rules:

```text
approved provenance
source trust
schema validation
freshness
classification
```

Structured records are not prompt-injection scanned as if they were free-text knowledge.

## Important Rule

```text
Structured records are not automatically truth.
They are SAFE-by-approved-provenance only if the source is governed,
trusted, schema-valid, and fresh enough.
```

## Source-to-Evidence-Class Map

```text
itil_incidents              → structured_record_evidence
itil_changes                → structured_record_evidence
itil_cmdb_topology          → structured_record_evidence
itil_business_impact_map    → structured_record_evidence
itil_operational_records    → structured_record_evidence
enterprise_memory           → structured_record_evidence / conditional memory evidence
support_knowledge           → free_text_knowledge_evidence
```

## Fusion Contract

EvidenceFusionEngine must consume governed evidence.

It must not rely on pre-baked safety flags from the domain adapter.

Rules:

```text
Allowed + safe evidence may support reasoning.
Denied source access creates an evidence gap.
Unsafe evidence is excluded from reasoning.
Review-required evidence is excluded from reasoning and flagged.
Low-trust evidence may weaken confidence.
Raw ungoverned records must be rejected for fusion-ready execution.
```

## Tests

```text
allowed source access creates stored evidence
denied source access creates evidence gap
unsafe content is excluded from reasoning
review-required content is excluded from reasoning
structured records use approved-provenance safety rules
free-text knowledge uses content safety rules
fusion rejects raw ungoverned records
fusion includes audit linkage
```

---

# 3E-4 — Adaptive Orchestrator and Orchestration Trace

## Purpose

Choose the next governed step based on operational confidence, memory maturity, evidence quality, conflicts, and impact uncertainty.

This is the heart of Sprint 3-engine.

## Deliverables

```text
src/orchestration/adaptive_orchestrator.py
src/orchestration/orchestration_trace.py
src/orchestration/agent_step.py
tests/test_adaptive_orchestrator.py
```

## Behavior Rules

```text
LOW confidence        → full diligence
MEDIUM confidence     → targeted retrieval / targeted validation
HIGH confidence       → validate-only path
DECREASING confidence → expanded diligence
UNKNOWN impact        → escalation
CONFLICTING evidence  → hypothesis expansion
GOVERNANCE denial     → trace + evidence gap
UNSAFE content        → excluded from reasoning
```

## Trace Must Show

```text
trace_id
joint_goal
case_id
current_phase
selected_due_diligence_level
agent steps
governed source requests
access decisions
audit ids
evidence ids
reasoning eligibility
why the path was selected
```

## Key Rule

```text
The orchestrator never calls raw source repositories directly.
It issues governed source requests and consumes governed evidence packages.
```

---

# 3E-5 — Operational-Confidence Adaptive Depth

## Purpose

Make OperationalConfidenceGate directly consumable by the orchestrator.

## Deliverables

```text
src/governance/operational_confidence.py
tests/test_operational_confidence_adaptive_depth.py
```

## Required Output Fields

```text
operational_confidence
confidence_direction
pattern_maturity
selected_due_diligence_level
knowledge_retrieval_required
required_agent_steps
prohibited_shortcuts
why
governance_required
human_approval_required
autonomous_action_allowed
```

## Fixture Requirement

`data/domain/it_application_health/sprint3_demo_memory_states.json` must include:

```text
prior_confidence
outcome_history
successful_uses
failed_uses
similarity
freshness
validation_state
```

This makes `confidence_direction` deterministic without a writable memory store.

## Key Rule

```text
Operational confidence determines due-diligence depth.
It does not determine whether governance applies.
Governance always applies.
```

---

# 3E-6 — Governance Trace View-Model

## Purpose

Create the headless object Sprint 3-UI will render.

No Streamlit logic belongs here.

## Deliverables

```text
src/views/governance_trace_view.py
tests/test_governance_trace_view.py
```

## Required View-Model Fields

```text
agent_id
source_id
source_access_purpose
governance_decision
audit_id
evidence_id
content_safety_status
allowed_for_reasoning
required_controls
approval_state
autonomous_action_allowed
reason
```

## Key Rule

```text
The UI will render this view-model later.
The UI must not invent governance state.
```

---

# 3E-7 — Scenario and Memory-State Model

## Purpose

Support same-alert / different-memory-state behavior.

## Deliverables

```text
data/domain/it_application_health/sprint3_demo_scenarios.json
data/domain/it_application_health/sprint3_demo_memory_states.json
tests/test_sprint3_scenario_memory_model.py
```

## Required Scenarios

```text
same alert + no memory
same alert + emerging memory
same alert + trusted memory
same alert + trusted but drifting memory
same alert + conflicting evidence
same alert + unknown impact
same alert + simulated outcome feedback
```

## Simulated Memory-State Decision

Sprint 3-engine uses simulated state-swap memory.

This is intentional.

```text
sprint3_demo_memory_states.json represents controlled memory maturity states.
It is not production persistence.
It is not a real writable enterprise memory store.
```

A real writable governed memory store is deferred to:

```text
Sprint 3.1 / v1.2
```

## Required Memory-State Fields

```text
memory_state_id
pattern_maturity
prior_confidence
outcome_history
successful_uses
failed_uses
similarity
freshness
validation_state
expected_confidence_direction
expected_due_diligence_level
```

## KT-Lite Contrast Data

KT-lite reasoning needs deterministic contrast data.

`sprint3_demo_scenarios.json` must include:

```text
affected_entities
unaffected_entities
present_symptoms
absent_symptoms
changed_conditions
unchanged_conditions
candidate_hypotheses
expected_is_statements
expected_is_not_statements
```

This allows the reasoning engine to populate:

```text
Is
Is Not
Distinctions
Changes
Possible causes
```

without inventing contrast data.

---

# 3E-8 — End-to-End Headless Engine Definition of Done

## Purpose

Prove the engine before UI begins.

## Deliverable

```text
tests/test_sprint3_headless_engine_e2e.py
```

## Required Green Cases

```text
same alert + no memory
→ full diligence

same alert + trusted memory
→ targeted validation

same alert + trusted memory + conflict
→ expanded validation

same alert + unknown impact
→ escalation

real broker DENY
→ no evidence-for-reasoning and evidence gap created

unsafe content
→ excluded from reasoning

review-required content
→ excluded from reasoning and flagged for review

same alert + drifting memory
→ confidence decreases and diligence expands
```

## DENY vs ESCALATE Rule

The engine must test both denial and escalation.

```text
ESCALATE:
The request requires additional review, missing context, or elevated approval.

DENY:
The requesting agent is not entitled to the source or capability.
No evidence-for-reasoning is created.
A governance trace and evidence gap are created.
```

Example DENY scenario:

```text
memory_pattern_agent requests itil_business_impact_map
→ DENY
→ audit record created
→ no reasoning evidence
→ evidence gap added
→ trace shows blocked access
```

---

# Expanded Core Vocabulary Boundary

Sprint 3-engine defines EAIOS 2 core as:

```text
src/governance
src/contracts
src/orchestration
src/views
```

Update:

```text
tests/test_core_domain_vocabulary_boundary.py
```

The boundary test should scan all EAIOS 2 core packages.

## Boundary Rule

Domain-flavored source IDs are allowed in governance registry data.

Examples:

```text
itil_incidents
itil_cmdb_topology
itil_business_impact_map
```

Governance policy can legitimately name domain sources.

The boundary rule applies to EAIOS 2 core code, not governed configuration or domain adapter data.

---

# Reasoning Scope

KT-lite reasoning is in scope for Sprint 3-engine.

The existing reasoning package must emit the structure the future UI needs:

```text
Situation
Is
Is Not
Distinctions
Possible hypotheses
Selected hypothesis
Why-chain
Limits
```

No UI should invent reasoning structure.

Strengthen:

```text
tests/test_reasoning_explanation_contract.py
```

---

# Sprint 3-engine Final DoD

Sprint 3-engine is complete when:

```powershell
python -m pytest
```

is green and the headless system proves:

```text
Scenario
→ CaseContext validation
→ Adaptive orchestration
→ Governed source access
→ Safety-classified evidence
→ Evidence fusion
→ Operational confidence depth decision
→ Reasoning explanation
→ Recommendation candidate
→ Governance trace view-model
```

With these guarantees:

```text
Every agent source access is registered and governed.
Every evidence item entering fusion came through the existing governed seam.
Unsafe and review-required content cannot enter reasoning.
Denied source access creates traceable evidence gaps.
CaseContext is validated by phase.
Operational confidence determines due-diligence depth.
Behavior is adaptive, explainable, and not random.
Governance is never optional.
Human approval remains required.
Autonomous production action remains disabled.
```

## Sprint 3-engine Tag

When complete, tag:

```text
eaios-2-sprint-3-engine-ready
```

---

# Sprint 3-UI Dependency

Sprint 3-UI starts only after Sprint 3-engine is green.

Sprint 3-UI will render tested headless view-models:

```text
Control Room
Scenario Selector
Orchestration Timeline
Operational Confidence Panel
Governance Trace Panel
Evidence Workbench
Reasoning Panel
Recommendation / Human Review Panel
```

The UI must not invent orchestration, governance, reasoning, or confidence state.

It renders what the tested engine emits.
