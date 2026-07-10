# EAIOS 2 UI View-Model Contract Map

## Purpose

This document maps Sprint 3-UI presentation objects to Sprint 3-engine source-of-truth objects.

The UI must render engine state.

The UI must not invent runtime state.

## Source-of-Truth Engine Objects

The UI may compose from:

```text
OperationalConfidenceGate output
AdaptiveOrchestrator output
OrchestrationTrace
AgentStep
GovernedEvidencePackage
EvidenceFusionEngine output
GovernanceTraceView
Scenario and memory-state fixtures
ReplayRunViewModel
ComparisonViewModel
AnimationEvent
Presentation Objects

Sprint 3-UI introduces presentation-layer objects:

ReplayRunViewModel
ComparisonViewModel
AnimationEvent

These are not new decision engines.

They are renderable compositions of tested headless outputs.

ReplayRunViewModel Contract

A ReplayRunViewModel must derive its key values from engine objects.

View-model field    Source of truth
run_id    UI composition identifier
scenario_id    scenario fixture
scenario_label    scenario fixture
business_outcome    CaseContext / scenario fixture
joint_goal    CaseContext / scenario fixture
current_alert    CaseContext / scenario fixture
operational_confidence    OperationalConfidenceGate output
confidence_direction    OperationalConfidenceGate output
pattern_maturity    OperationalConfidenceGate output
selected_due_diligence_level    OperationalConfidenceGate output
why    OperationalConfidenceGate output
orchestration_trace    OrchestrationTrace
governance_trace_view    GovernanceTraceView
evidence_for_reasoning    GovernedEvidencePackage
excluded_evidence    GovernedEvidencePackage
evidence_gaps    GovernedEvidencePackage
safety_boundaries    engine safety boundary output
animation_events    deterministic projection from trace and governance view
Provenance Invariants

The UI must not invent:

audit_id
evidence_id
governance_decision
content_safety_status
allowed_for_reasoning
approval_state
operational_confidence
confidence_direction
pattern_maturity
selected_due_diligence_level
autonomous_action_allowed

Every value above must be traceable to a headless engine object.

ComparisonViewModel Contract

A ComparisonViewModel is a collection of ReplayRunViewModel instances.

Example:

First-time / no memory
Trusted memory / validated pattern
Drift or conflict

The comparison layer may calculate display-only summaries such as:

number of agent steps
number of evidence items
number of evidence gaps
number of denied source accesses

It must not calculate new governance or confidence decisions.

AnimationEvent Contract

Animation events are deterministic projections from engine outputs.

They may contain:

event_id
event_type
run_id
node_id
from_node
to_node
agent_id
source_id
audit_id
evidence_id
decision
caption
timestamp_offset_ms

The event stream may add display-only timing.

The event stream must not alter the underlying decision.

Core vs Presentation Naming

src/views is core.

It contains neutral headless view-models such as GovernanceTraceView.

ui is presentation.

It contains app-health replay rendering and UI composition.

The two are intentionally separate.

app.py Reconciliation

The canonical Sprint 3-UI entrypoint is:

ui/streamlit_app.py

Any root-level app.py must be clearly marked as deprecated or quarantined if it references legacy runtime behavior.

No reviewer should accidentally run a deprecated root app and think it is EAIOS 2 Sprint 3-UI.

Renderer Strategy

The initial renderer may be Streamlit.

The rich animation renderer should use one-way JSON export:

Python engine → replay JSON → standalone React Flow / HTML replay

The React replay canvas owns animation timing and play-head.

Python remains the source of truth for data and decisions.

The root-level `app.py` entrypoint must not be treated as the canonical Sprint 3-UI entrypoint.
