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
