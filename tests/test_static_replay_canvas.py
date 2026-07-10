from pathlib import Path

from ui.components.replay_canvas import replay_canvas_model
from ui.demo_fixtures import build_demo_comparison_view_model


STREAMLIT_APP = Path("ui/streamlit_app.py")


def selected_run():
    comparison = build_demo_comparison_view_model()
    return comparison["runs"][0]


def test_replay_canvas_model_builds_nodes_and_edges_from_animation_events():
    canvas = replay_canvas_model(selected_run())

    assert canvas["run_id"] == "run-no-memory"
    assert canvas["scenario_label"] == "First-time / no memory"

    node_ids = {
        node["node_id"]
        for node in canvas["nodes"]
    }

    assert "joint_goal" in node_ids
    assert "evidence_fusion" in node_ids
    assert "operational_confidence" in node_ids
    assert "due_diligence" in node_ids
    assert "human_review" in node_ids
    assert "excluded_evidence" in node_ids


def test_replay_canvas_shows_governance_gate_decisions():
    canvas = replay_canvas_model(selected_run())

    gate_nodes = [
        node
        for node in canvas["nodes"]
        if node["node_id"].startswith("gate::")
    ]

    labels = {
        node["label"]
        for node in gate_nodes
    }

    assert any("Gate: ALLOW" in label for label in labels)
    assert any("Gate: DENY" in label for label in labels)


def test_replay_canvas_routes_reasoning_evidence_to_fusion():
    canvas = replay_canvas_model(selected_run())

    assert {
        "from_node": "evidence::run-no-memory-EVIDENCE-001",
        "to_node": "evidence_fusion",
        "label": "eligible",
        "color": "green",
    } in canvas["edges"]


def test_replay_canvas_routes_review_required_evidence_to_excluded_bucket():
    canvas = replay_canvas_model(selected_run())

    assert {
        "from_node": "evidence::run-no-memory-EVIDENCE-EXCLUDED-001",
        "to_node": "excluded_evidence",
        "label": "excluded",
        "color": "red",
    } in canvas["edges"]


def test_replay_canvas_creates_visible_gap_edge_for_denied_source_access():
    canvas = replay_canvas_model(selected_run())

    assert any(
        edge["label"] == "gap created"
        and edge["color"] == "red"
        and edge["to_node"].startswith("gap::business_impact_agent::")
        for edge in canvas["edges"]
    )


def test_replay_canvas_dot_contains_control_room_flow():
    canvas = replay_canvas_model(selected_run())
    dot = canvas["dot"]

    assert "digraph EAIOSReplay" in dot
    assert "Joint Goal" in dot
    assert "Evidence Fusion" in dot
    assert "Operational Confidence" in dot
    assert "Human Review Required" in dot
    assert "Gate: ALLOW" in dot
    assert "Gate: DENY" in dot


def test_streamlit_app_renders_orchestration_replay_canvas():
    text = STREAMLIT_APP.read_text(encoding="utf-8")

    assert "replay_canvas_model" in text
    assert "Orchestration replay canvas" in text
    assert "st.graphviz_chart" in text
