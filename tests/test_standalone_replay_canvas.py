from pathlib import Path


HTML = Path("ui_static/replay_canvas/index.html")
CSS = Path("ui_static/replay_canvas/replay_canvas.css")
JS = Path("ui_static/replay_canvas/replay_canvas.js")


def test_standalone_replay_canvas_files_exist():
    assert HTML.exists()
    assert CSS.exists()
    assert JS.exists()


def test_standalone_replay_canvas_uses_one_way_json_export():
    text = JS.read_text(encoding="utf-8")

    assert "../../ui_replay_exports/eaios_sprint3_replay.json" in text
    assert "fetch(REPLAY_JSON_PATH)" in text


def test_standalone_replay_canvas_has_story_controls():
    text = HTML.read_text(encoding="utf-8")

    assert "EAIOS 2 Control Room" in text
    assert "Governed adaptive orchestration replay" in text
    assert 'id="play-pause"' in text
    assert 'id="next-event"' in text
    assert 'id="reset"' in text
    assert 'id="run-selector"' in text


def test_standalone_replay_canvas_renders_core_nodes():
    text = HTML.read_text(encoding="utf-8")

    assert 'data-node-id="joint_goal"' in text
    assert 'data-node-id="evidence_fusion"' in text
    assert 'data-node-id="operational_confidence"' in text
    assert 'data-node-id="due_diligence"' in text
    assert 'data-node-id="human_review"' in text


def test_standalone_replay_canvas_animates_event_types():
    text = JS.read_text(encoding="utf-8")

    assert 'event.event_type === "EVIDENCE_TOKEN_MOVED"' in text
    assert 'event.event_type === "EVIDENCE_EXCLUDED"' in text
    assert 'event.event_type === "EVIDENCE_GAP_CREATED"' in text
    assert 'event.event_type === "CONFIDENCE_UPDATED"' in text
    assert 'event.event_type === "DUE_DILIGENCE_SELECTED"' in text
    assert 'event.event_type === "HUMAN_REVIEW_REQUIRED"' in text


def test_standalone_replay_canvas_has_governance_boundary_language():
    text = HTML.read_text(encoding="utf-8")

    assert "Governance: Mandatory" in text
    assert "Human approval: Required" in text
    assert "Autonomous action: Off" in text
    assert "Memory: Evidence, not truth" in text


def test_standalone_replay_canvas_styles_allow_deny_review_and_excluded_states():
    text = CSS.read_text(encoding="utf-8")

    assert "--allow" in text
    assert "--deny" in text
    assert "--review" in text
    assert ".node.allow" in text
    assert ".node.deny" in text
    assert ".token.eligible.visible" in text
    assert ".token.excluded.visible" in text
    assert ".gap-token.visible" in text


def test_standalone_replay_canvas_documents_local_server_fallback():
    text = JS.read_text(encoding="utf-8")

    assert "python -m http.server 8765" in text
    assert "http://localhost:8765/ui_static/replay_canvas/index.html" in text


def test_standalone_replay_canvas_has_traceability_footer():
    text = HTML.read_text(encoding="utf-8")

    assert "Replay contract" in text
    assert "Execution trace" in text
    assert "Provenance summary" in text
    assert 'id="renderer-contract"' in text
    assert 'id="schema-version"' in text
    assert 'id="event-counter"' in text
    assert 'id="animation-event-count"' in text
    assert 'id="provenance-summary"' in text


def test_standalone_replay_canvas_updates_traceability_footer_from_export_payload():
    text = JS.read_text(encoding="utf-8")

    assert "function renderTraceabilityFooter()" in text
    assert "payload.schema_version" in text
    assert "payload.animation_event_count" in text
    assert "payload.renderer_contract.direction" in text
    assert "payload.renderer_contract.python_owns_decisions" in text
    assert "payload.renderer_contract.renderer_owns_playhead" in text
    assert "payload.renderer_contract.renderer_must_not_invent_decisions" in text
    assert "payload.provenance_summary.audit_ids.length" in text
    assert "payload.provenance_summary.evidence_ids.length" in text
    assert "payload.provenance_summary.governance_decisions.join" in text
    assert "payload.provenance_summary.approval_states.join" in text


def test_standalone_replay_canvas_event_counter_advances_with_playhead():
    text = JS.read_text(encoding="utf-8")

    assert "currentEventIndex + 1" in text
    assert "currentRun.animation_events.length" in text
    assert "renderTraceabilityFooter();" in text


def test_standalone_replay_canvas_has_presenter_mode_panel():
    text = HTML.read_text(encoding="utf-8")

    assert "Presenter mode" in text
    assert "Guided narrative: same alert, adaptive due diligence" in text
    assert 'id="presenter-headline"' in text
    assert 'id="presenter-act-buttons"' in text
    assert 'id="presenter-act-label"' in text
    assert 'id="presenter-scenario-label"' in text
    assert 'id="presenter-demo-cue"' in text
    assert 'id="presenter-talking-points"' in text
    assert 'id="presenter-closing-line"' in text


def test_standalone_replay_canvas_presenter_mode_defines_three_acts():
    text = JS.read_text(encoding="utf-8")

    assert "const PRESENTER_ACTS" in text
    assert "Act 1 ? First-time alert" in text
    assert "Act 2 ? Trusted memory" in text
    assert "Act 3 ? Drift or conflict" in text
    assert "First-time / no memory" in text
    assert "Trusted memory / validated pattern" in text
    assert "Drift or conflict" in text


def test_standalone_replay_canvas_presenter_mode_selects_run_and_resets_replay():
    text = JS.read_text(encoding="utf-8")

    assert "function renderPresenterMode()" in text
    assert "function setPresenterAct(act)" in text
    assert "payload.runs.find" in text
    assert "candidate.scenario_label === act.run_label" in text
    assert "currentRun = run" in text
    assert "selector.value = run.run_id" in text
    assert "resetReplay()" in text


def test_standalone_replay_canvas_presenter_mode_tells_governance_story():
    text = JS.read_text(encoding="utf-8")

    assert "Same alert" in text or "same alert" in text
    assert "Memory influences confidence, but memory is still evidence, not truth." in text
    assert "Governance gates still stamp source access before evidence can move." in text
    assert "Review-required evidence is excluded from reasoning." in text
    assert "human review, not autonomous remediation" in text
    assert "does not lower governance" in text


def test_standalone_replay_canvas_styles_presenter_mode():
    text = CSS.read_text(encoding="utf-8")

    assert ".presenter-mode" in text
    assert ".presenter-header" in text
    assert ".act-buttons" in text
    assert ".act-button.active" in text
    assert ".presenter-grid" in text
    assert ".presenter-script" in text
    assert ".closing-line" in text


def test_standalone_replay_canvas_renders_run_specific_agent_step_lane():
    text = JS.read_text(encoding="utf-8")

    assert "function agentStepsForCurrentRun()" in text
    assert "currentRun.agent_steps" in text
    assert "currentRun.orchestration_steps" in text
    assert "currentRun.orchestration_trace?.agent_steps" in text
    assert "agentSteps.forEach" in text
    assert "Visual path steps" in text


def test_standalone_replay_canvas_groups_governance_gates_under_agent_steps():
    text = JS.read_text(encoding="utf-8")

    assert "function governanceGateEventsByAgent()" in text
    assert "GOVERNANCE_GATE_STAMPED" in text
    assert "gateEventsByAgent.get(step.agent_id)" in text
    assert "gateEvents.shift()" in text


def test_standalone_replay_canvas_styles_path_step_nodes():
    text = CSS.read_text(encoding="utf-8")

    assert ".path-step" in text
    assert ".path-step small" in text
    assert ".path-step strong" in text
    assert ".path-step em" in text

