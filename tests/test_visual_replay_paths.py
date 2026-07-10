from ui.demo_fixtures import build_demo_comparison_view_model
from ui.visual_replay_paths import (
    build_demo_story_contract,
    build_visual_paths_by_run,
)


def test_visual_replay_paths_export_exact_scenario_lengths():
    comparison = build_demo_comparison_view_model()

    paths = build_visual_paths_by_run(comparison)

    assert len(paths["run-no-memory"]) == 7
    assert len(paths["run-trusted-memory"]) == 3
    assert len(paths["run-drift-conflict"]) == 5


def test_visual_replay_paths_include_step_numbers_totals_and_run_ids():
    comparison = build_demo_comparison_view_model()

    paths = build_visual_paths_by_run(comparison)

    for run in comparison["runs"]:
        events = paths[run["run_id"]]

        assert [
            event["visual_step_number"]
            for event in events
        ] == list(range(1, len(events) + 1))

        assert {
            event["visual_step_total"]
            for event in events
        } == {len(events)}

        assert {
            event["run_id"]
            for event in events
        } == {run["run_id"]}


def test_visual_replay_paths_preserve_scenario_specific_endpoints():
    comparison = build_demo_comparison_view_model()

    paths = build_visual_paths_by_run(comparison)

    assert paths["run-no-memory"][-1]["label"] == "Human review package"
    assert paths["run-trusted-memory"][-1]["label"] == (
        "Targeted human validation"
    )
    assert paths["run-drift-conflict"][-1]["label"] == (
        "Human review package"
    )


def test_demo_story_contract_contains_same_alert_and_path_stories():
    story = build_demo_story_contract()

    assert story["same_alert"] == {
        "application": "Digital Checkout",
        "symptom": (
            "Payment authorization latency and elevated error rate"
        ),
    }

    assert story["path_story_by_scenario"]["First-time / no memory"][
        "title"
    ] == "Full due diligence"
    assert story["path_story_by_scenario"][
        "Trusted memory / validated pattern"
    ]["title"] == "Targeted validation"
    assert story["path_story_by_scenario"]["Drift or conflict"][
        "title"
    ] == "Expanded validation"


def test_replay_export_payload_contains_visual_paths_and_demo_story():
    from ui.replay_export import build_replay_export_payload

    payload = build_replay_export_payload()

    assert "demo_story" in payload
    assert "visual_paths_by_run" in payload
    assert payload["visual_event_count"] == 15
    assert len(payload["visual_paths_by_run"]["run-no-memory"]) == 7
    assert len(payload["visual_paths_by_run"]["run-trusted-memory"]) == 3
    assert len(payload["visual_paths_by_run"]["run-drift-conflict"]) == 5
