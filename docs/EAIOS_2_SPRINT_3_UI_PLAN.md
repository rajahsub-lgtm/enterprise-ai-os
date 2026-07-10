# EAIOS 2 Sprint 3-UI Plan

## North Star

Do not build a dashboard.

Build a governed orchestration replay.

A dashboard shows state.
A replay shows behavior changing.

The EAIOS 2 UI must make one thesis obvious:

```text
Same alert.
Different enterprise memory.
Different operational confidence.
Different due-diligence depth.
Same governance.
Same human approval boundary.
Autonomous action remains disabled.
```

## Product Concept

```text
EAIOS 2 Control Room
Governed Adaptive Orchestration Replay
```

## Primary Story

The UI demonstrates that EAIOS adapts the level of due diligence based on memory, evidence quality, confidence, and governance, while never relaxing enterprise controls.

The UI must show:

```text
Behavior adapts.
Governance does not relax.
```

## Design Principle

The UI is a renderer over tested Sprint 3-engine outputs.

It must not recreate business logic.

It must not invent:

```text
audit IDs
evidence IDs
governance decisions
allowed_for_reasoning values
approval states
confidence values
due-diligence levels
autonomous action permissions
```

## Architecture

Sprint 3-UI uses a layered presentation architecture:

```text
Sprint 3-engine outputs
→ ReplayRunViewModel
→ ComparisonViewModel
→ animation_events
→ renderer
```

The renderer may be Streamlit, React Flow, D3, or another visual layer.

The source of truth remains the tested headless engine.

## One-Way Visualization Strategy

The default rich visualization strategy is one-way JSON export.

Python builds and exports:

```text
ReplayRunViewModel
ComparisonViewModel
animation_events
```

A standalone React/HTML replay canvas may consume the JSON and manage its own play-head.

This avoids bidirectional Streamlit component complexity during the demo sprint.

A true bidirectional Streamlit component is optional future polish, not the default path.

## Core vs Presentation Boundary

There are two different meanings of "view":

```text
src/views
```

is the headless, domain-neutral, tested core view-model layer.

```text
ui
```

is the domain-aware presentation layer for the app-health replay demo.

The `ui` package is not part of the Sprint 3 core boundary and must not be added to core vocabulary-boundary tests.

The `ui` layer may render app-health scenarios, but it must remain pure presentation and composition.

## UI Composition Guardrails

`ui/view_models.py` must be pure composition.

It may collect, reshape, and package tested engine outputs.

It must not make new governance, confidence, evidence eligibility, or approval decisions.

JSX / React rendering must be positional and visual.

It may place nodes, animate events, and display passports.

It must not create business decisions.

## ReplayRunViewModel

A ReplayRunViewModel represents one engine run for one scenario and memory state.

Required conceptual fields:

```text
run_id
scenario_id
scenario_label
business_outcome
joint_goal
current_alert
operational_confidence
confidence_direction
pattern_maturity
selected_due_diligence_level
why
orchestration_trace
governance_trace_view
governed_evidence_package
fusion_result
reasoning_explanation
recommendation_candidate
safety_boundaries
animation_events
```

## ComparisonViewModel

A ComparisonViewModel represents a side-by-side replay.

It is a collection of ReplayRunViewModel instances.

Example:

```text
ComparisonViewModel
  - First-time / no memory
  - Trusted memory / validated pattern
  - Drift or conflict
```

The side-by-side renderer must not recompute decisions.

It only renders the run view-models.

## Animation Event Model

The animation event stream is deterministic and testable.

Supported event types include:

```text
NODE_ACTIVATED
GOVERNANCE_GATE_STAMPED
EVIDENCE_TOKEN_MOVED
EVIDENCE_EXCLUDED
EVIDENCE_GAP_CREATED
CONFIDENCE_UPDATED
DUE_DILIGENCE_SELECTED
RECOMMENDATION_CREATED
HUMAN_REVIEW_REQUIRED
```

The renderer uses these events to replay the orchestration.

Story Mode and Explore Mode use the same event model.

## Story Mode

Story Mode is a scripted deterministic replay.

It advances through events with captions.

It exists for demos, interviews, and executive storytelling.

## Explore Mode

Explore Mode lets a reviewer manually select scenarios and inspect outputs.

It uses the same underlying view-model and event stream.

## Three-Act Demo Narrative

### Act 1 — First-Time Alert

The alert has no reliable memory.

Expected story:

```text
Operational confidence is low.
Full due diligence is selected.
More agent steps are invoked.
Governance gates every source access.
Human approval is required.
Autonomous action remains disabled.
```

### Act 2 — Trusted Memory

The same alert has a trusted validated memory pattern.

Expected story:

```text
Operational confidence is high.
Targeted validation is selected.
Fewer agent steps are invoked.
Governance remains mandatory.
Human approval is still required.
Autonomous action remains disabled.
```

### Act 3 — Drift, Conflict, Denial, Unsafe Evidence

The same alert encounters degraded trust, conflicting evidence, restricted source access, or unsafe/review-required evidence.

Expected story:

```text
Confidence decreases or escalation occurs.
Due diligence expands.
Denied access creates an evidence gap.
Unsafe evidence is excluded from reasoning.
The audit trail grows.
Human approval remains required.
```

## Visual Experience

The primary screen is a control-room replay, not a multi-tab dashboard.

Persistent header, sentence case:

```text
Business outcome: Maintain Application Health
Joint goal: Maintain service health while preserving controls
Governance: Mandatory
Human approval: Required
Autonomous action: Off
Memory: Evidence, not truth
```

## Hero Visual

The hero visual is a live orchestration graph:

```text
Joint Goal
→ Agent Step
→ Governance Gate
→ Evidence
→ Evidence Fusion
→ Operational Confidence
→ Recommendation
→ Human Review
```

Governance gates visibly stamp:

```text
Allow
Escalate
Deny
Excluded
Review required
```

Evidence tokens may flow into the fusion node.

Unsafe or denied evidence may divert to:

```text
Evidence gap created
Audit logged
Not eligible for reasoning
```

## Mid-Sprint Demo Checkpoint

Before React or D3 polish, Sprint 3-UI should ship a credible Streamlit checkpoint:

```text
Headless ReplayRunViewModel
Story Mode event stream
Streamlit shell
Static side-by-side comparison
Governance passport panel
Confidence / due-diligence panel
Human review boundary
```

This proves the story before investing in richer animation.

## Rich Visualization Checkpoint

After the Streamlit checkpoint, build the high-polish replay canvas.

Default approach:

```text
Python exports JSON
Standalone React Flow replay page consumes JSON
React Flow owns play-head and animation
```

Optional later approach:

```text
Embed the React Flow replay as a Streamlit iframe or custom component
```

## Definition of Done

Sprint 3-UI is not done until:

```text
UI renders tested headless outputs.
Side-by-side replay shows adaptive due-diligence contrast.
Governance remains constant across runs.
Human approval boundary is visible.
Autonomous action remains disabled.
Animation events are deterministic and tested.
UI provenance invariants are enforced by tests.
Deprecated app.py ambiguity is resolved.
```
