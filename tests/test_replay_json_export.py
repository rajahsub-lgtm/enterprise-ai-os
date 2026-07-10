import json
from pathlib import Path

from ui.demo_fixtures import build_demo_comparison_view_model
from ui.replay_export import (
    EXPORT_SCHEMA_VERSION,
    build_replay_export_payload,
    write_replay_export,
)


def test_replay_export_payload_declares_one_way_renderer_contract():
    payload = build_replay_export_payload()

    assert payload["schema_version"] == EXPORT_SCHEMA_VERSION
    assert payload["export_purpose"] == "standalone_replay_renderer"
    assert payload["source_of_truth"] == (
        "Sprint 3 tested headless view-model outputs"
    )
    assert payload["renderer_contract"] == {
        "direction": "one_way_json",
        "python_owns_decisions": True,
        "renderer_owns_playhead": True,
        "renderer_must_not_invent_decisions": True,
    }


def test_replay_export_payload_contains_comparison_runs_and_animation_events():
    payload = build_replay_export_payload()

    assert payload["comparison"]["comparison_label"] == (
        "Same alert, different memory states"
    )
    assert [
        run["scenario_label"]
        for run in payload["runs"]
    ] == [
        "First-time / no memory",
        "Trusted memory / validated pattern",
        "Drift or conflict",
    ]

    assert payload["animation_event_count"] == sum(
        len(run["animation_events"])
        for run in payload["runs"]
    )

    for run in payload["runs"]:
        assert run["animation_events"]


def test_replay_export_preserves_constant_safety_boundaries():
    payload = build_replay_export_payload()

    assert payload["safety_boundaries"] == {
        "governance_required_values": [True],
        "human_approval_required_values": [True],
        "autonomous_action_allowed_values": [False],
    }


def test_replay_export_preserves_provenance_values_from_view_models():
    comparison = build_demo_comparison_view_model()
    payload = build_replay_export_payload(comparison)

    expected_audit_ids = sorted(
        audit_id
        for run in comparison["runs"]
        for audit_id in run["provenance"]["audit_ids"]
    )

    expected_evidence_ids = sorted(
        evidence_id
        for run in comparison["runs"]
        for evidence_id in run["provenance"]["evidence_ids"]
    )

    assert payload["provenance_summary"]["audit_ids"] == expected_audit_ids
    assert payload["provenance_summary"]["evidence_ids"] == expected_evidence_ids
    assert payload["provenance_summary"]["governance_decisions"] == [
        "ALLOW",
        "DENY",
    ]
    assert payload["provenance_summary"]["approval_states"] == [
        "BLOCKED",
        "PENDING_HUMAN_REVIEW",
    ]
    assert payload["provenance_summary"]["operational_confidence_values"] == [
        "HIGH",
        "LOW",
        "MEDIUM",
    ]
    assert payload["provenance_summary"]["due_diligence_values"] == [
        "EXPANDED_VALIDATION",
        "FULL_DUE_DILIGENCE",
        "TARGETED_VALIDATION",
    ]


def test_replay_export_is_valid_json_round_trip(tmp_path):
    output = tmp_path / "replay.json"

    write_replay_export(output)

    loaded = json.loads(output.read_text(encoding="utf-8"))

    assert loaded["schema_version"] == EXPORT_SCHEMA_VERSION
    assert loaded["comparison"]["comparison_id"] == (
        "comparison-same-alert-memory-states"
    )
    assert loaded["runs"][0]["run_id"] == "run-no-memory"


def test_export_script_points_to_default_replay_json_location():
    script = Path("scripts/export_sprint3_ui_replay_json.py")

    assert script.exists()

    text = script.read_text(encoding="utf-8")

    assert '"ui_replay_exports"' in text
    assert '"eaios_sprint3_replay.json"' in text
    assert "write_replay_export" in text
