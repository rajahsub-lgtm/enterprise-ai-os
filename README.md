# Enterprise AI Operating System — EAIOS 2

EAIOS is an enterprise AI operating model and executable architecture for governed, observable, evidence-based, human-bounded multi-agent orchestration.

The repo has moved beyond the original EAIOS 1 skeleton demo. The current foundation is EAIOS 2 Sprint 2.5: a test-backed application-health governance concept path.

## Current Architecture Path

```text
Business Outcome
→ Domain Repository
→ Case Context
→ Evidence Fusion
→ Reasoning Explanation
→ Recommendation Candidate
→ Human Review Package
```

With the operational confidence gate enabled, the architecture also includes:

```text
Case Context + Memory + Evidence State
→ Operational Confidence Gate
→ Due Diligence Decision
```

## Current Demo

Run:

```powershell
python app.py
```

This runs the current EAIOS 2 application-health concept demo using the synthetic ITIL repository.

## Current Domain Repository

The active demo data is here:

```text
data/domain/it_application_health/
```

It includes:

- `golden_scenarios.json`
- `business_impact_map.json`
- `cmdb_topology.json`
- `operational_records.json`

These replace the old hard-coded EAIOS 1 application-health example files.

## Governance Principles

EAIOS enforces these principles:

1. Business outcome is the entry point.
2. Governance is mandatory for source access.
3. Evidence must preserve provenance.
4. Content safety gates determine what can reach reasoning.
5. Memory is evidence, not truth.
6. Evidence fusion separates supporting, weakening, conflicting, and missing evidence.
7. Reasoning explains hypotheses before recommendation.
8. Operational confidence determines due-diligence depth.
9. Human approval is required for production-impacting recommendations.
10. Autonomous production action is disabled.

## Run Tests

```powershell
python -m pytest
```

Expected Sprint 2.5 baseline after reasoning explanation:

```text
135 passed
```

Expected Sprint 2.5 baseline after operational confidence gate:

```text
143 passed
```

## Sprint 3 Direction

Sprint 3 will build a peer-reviewable demo showing explainable adaptive multi-agent orchestration under strict governance using expanded synthetic app-health data.

Core Sprint 3 message:

```text
Operational confidence determines the level of due diligence.
Governance is never optional.
```

## EAIOS 2 Sprint 3 Demo

Sprint 3 demonstrates governed orchestration replay for enterprise-safe agentic AI.

Core story:

```text
Same alert.
Different enterprise memory.
Different due-diligence depth.
Same governance.
Same human approval boundary.
No autonomous production action.
```

Run the replay export:

```powershell
python scripts\export_sprint3_ui_replay_json.py
```

Launch the standalone replay:

```powershell
python -m http.server 8765
```

Open:

```text
http://localhost:8765/ui_static/replay_canvas/index.html
```

Demo package:

- `docs/EAIOS_2_SPRINT_3_CLOSEOUT.md`
- `docs/EAIOS_2_SPRINT_3_UI_DEMO_WALKTHROUGH.md`
- `docs/EAIOS_2_SPRINT_3_UI_ARCHITECTURE_CHECKPOINT.md`

Architecture rule:

```text
Python owns decisions.
Renderer owns play-head.
Renderer must not invent replay paths.
```
