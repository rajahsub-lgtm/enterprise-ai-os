from tests.test_ui_view_models import build_sample_run

from ui.story_mode import (
    EVENT_CONFIDENCE_UPDATED,
    EVENT_DUE_DILIGENCE_SELECTED,
    EVENT_EVIDENCE_EXCLUDED,
    EVENT_EVIDENCE_GAP_CREATED,
    EVENT_EVIDENCE_TOKEN_MOVED,
    EVENT_GOVERNANCE_GATE_STAMPED,
    EVENT_HUMAN_REVIEW_REQUIRED,
    EVENT_NODE_ACTIVATED,
    attach_animation_events,
    build_animation_events,
)


def test_story_mode_builds_deterministic_animation_events_from_run_view_model():
    run = build_sample_run()

    events = build_animation_events(run)

    assert events[0]["event_id"] == "run-trusted-EVT-001"
    assert events[0]["timestamp_offset_ms"] == 0
    assert events[0]["event_type"] == EVENT_NODE_ACTIVATED
    assert events[0]["node_id"] == "joint_goal"

    assert [
        event["event_id"]
        for event in events
    ] == [
        f"run-trusted-EVT-{index:03d}"
        for index in range(1, len(events) + 1)
    ]


def test_story_mode_preserves_governance_decisions_and_audit_ids():
    run = build_sample_run()

    events = build_animation_events(run)

    gate_events = [
        event
        for event in events
        if event["event_type"] == EVENT_GOVERNANCE_GATE_STAMPED
    ]

    assert [
        event["decision"]
        for event in gate_events
    ] == ["ALLOW", "DENY"]

    assert [
        event["audit_id"]
        for event in gate_events
    ] == ["AUDIT-001", "AUDIT-002"]


def test_story_mode_moves_only_reasoning_eligible_evidence_to_fusion():
    run = build_sample_run()

    events = build_animation_events(run)

    moved_events = [
        event
        for event in events
        if event["event_type"] == EVENT_EVIDENCE_TOKEN_MOVED
    ]

    assert len(moved_events) == 1
    assert moved_events[0]["evidence_id"] == "EVIDENCE-001"
    assert moved_events[0]["to_node"] == "evidence_fusion"
    assert moved_events[0]["allowed_for_reasoning"] is True


def test_story_mode_excludes_review_required_evidence_instead_of_fusing_it():
    run = build_sample_run()

    events = build_animation_events(run)

    excluded_events = [
        event
        for event in events
        if event["event_type"] == EVENT_EVIDENCE_EXCLUDED
    ]

    assert len(excluded_events) == 1
    assert excluded_events[0]["evidence_id"] == "EVIDENCE-EXCLUDED-001"
    assert excluded_events[0]["content_safety_status"] == "REVIEW_REQUIRED"
    assert excluded_events[0]["allowed_for_reasoning"] is False
    assert excluded_events[0]["to_node"] == "excluded_evidence"


def test_story_mode_creates_visible_gap_events_for_denied_access_and_gaps():
    run = build_sample_run()

    events = build_animation_events(run)

    gap_events = [
        event
        for event in events
        if event["event_type"] == EVENT_EVIDENCE_GAP_CREATED
    ]

    assert len(gap_events) >= 1

    assert any(
        event.get("audit_id") == "AUDIT-002"
        and event.get("source_id") == "itil_business_impact_map"
        for event in gap_events
    )


def test_story_mode_uses_engine_confidence_and_due_diligence_values():
    run = build_sample_run()

    events = build_animation_events(run)

    confidence_event = next(
        event
        for event in events
        if event["event_type"] == EVENT_CONFIDENCE_UPDATED
    )
    diligence_event = next(
        event
        for event in events
        if event["event_type"] == EVENT_DUE_DILIGENCE_SELECTED
    )

    assert confidence_event["confidence"] == run["operational_confidence"]
    assert confidence_event["confidence_direction"] == run["confidence_direction"]
    assert confidence_event["pattern_maturity"] == run["pattern_maturity"]
    assert diligence_event["due_diligence"] == run["selected_due_diligence_level"]


def test_story_mode_stops_at_human_review_with_autonomous_action_disabled():
    run = build_sample_run()

    events = build_animation_events(run)

    final_event = events[-1]

    assert final_event["event_type"] == EVENT_HUMAN_REVIEW_REQUIRED
    assert final_event["governance_required"] is True
    assert final_event["human_approval_required"] is True
    assert final_event["autonomous_action_allowed"] is False


def test_attach_animation_events_returns_copy_without_mutating_original():
    run = build_sample_run()

    updated = attach_animation_events(run)

    assert run["animation_events"] == []
    assert updated["animation_events"]
    assert updated is not run
