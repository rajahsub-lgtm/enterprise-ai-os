# EAIOS 2 Sprint 3-UI Architecture Checkpoint

## Status

Sprint 3-UI replay is ready.

This checkpoint covers:

- Streamlit control room shell.
- Headless UI view models.
- Story-mode animation events.
- Evidence workbench.
- Reasoning detective board.
- Recommendation review.
- One-way replay JSON export.
- Standalone animated replay canvas.
- Presenter mode.
- Traceability footer.
- Export-driven visual replay paths.

## Architecture Principle

The UI must not become the decision engine.

The architecture boundary is:

```text
Sprint 3 engine outputs
? ReplayRunViewModel
? ComparisonViewModel
? JSON export contract
? standalone renderer

```

The renderer may own:

- Play / pause / reset.
- Current event index.
- Visual highlighting.
- Layout.
- Presenter mode navigation.

The renderer must not own:

- Operational confidence decisions.
- Due-diligence selection.
- Governance gate decisions.
- Evidence eligibility.
- Evidence exclusion.
- Evidence gap creation.
- Human approval boundary.
- Scenario path length.

## Export Contract

The replay export contains:

```text
schema_version
renderer_contract
comparison
runs
demo_story
visual_paths_by_run
visual_event_count
animation_event_count
safety_boundaries
provenance_summary
```

The key rule is:

```text
Python owns decisions.
Renderer owns play-head.
Renderer must not invent decisions.
Renderer must not invent replay paths.
```

## Visual Path Contract

Visual replay paths are exported by Python in:

```text
ui/visual_replay_paths.py
```

The browser consumes:

```text
payload.visual_paths_by_run[currentRun.run_id]
payload.demo_story.path_story_by_scenario
payload.demo_story.same_alert
```

The browser must not define:

```text
const VISUAL_PATHS_BY_SCENARIO
const PATH_STORY_BY_SCENARIO
```

## Scenario Path Lengths

The current demo path lengths are:

```text
run-no-memory        ? 7 visual events
run-trusted-memory   ? 3 visual events
run-drift-conflict   ? 5 visual events
```

These lengths are not cosmetic. They demonstrate adaptive due diligence:

```text
LOW confidence + no memory        ? FULL_DUE_DILIGENCE
HIGH confidence + trusted memory  ? TARGETED_VALIDATION
MEDIUM confidence + drift/conflict ? EXPANDED_VALIDATION
```

## Governance Boundary

Governance is constant across all scenarios:

```text
governance_required = True
human_approval_required = True
autonomous_action_allowed = False
```

This is the enterprise control story.

Behavior adapts. Governance does not relax.

## Evidence Boundary

Evidence remains governed:

- Reasoning-eligible evidence enters fusion.
- Review-required evidence is excluded.
- Denied access creates an evidence gap.
- Structured records use approved provenance.
- Free text uses content-safety semantics.
- Memory is evidence, not truth.

## Current Demo Commands

Run tests:

```powershell
python -m pytest --basetemp .pytest_tmp
```

Regenerate replay JSON:

```powershell
python scripts\export_sprint3_ui_replay_json.py
```

Launch standalone replay:

```powershell
python -m http.server 8765
```

Open:

```text
http://localhost:8765/ui_static/replay_canvas/index.html
```

## Checkpoint Meaning

This checkpoint proves that EAIOS can present an enterprise-safe agentic replay:

```text
Same alert.
Different enterprise memory.
Different due-diligence depth.
Same governance.
Same human approval boundary.
No autonomous production action.
```
