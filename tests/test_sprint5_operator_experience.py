from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint5.operator_experience import (
    OperatorExperienceMode,
    OperatorReviewSection,
    build_operator_dashboard_export,
    render_operator_dashboard_markdown,
    summarize_operator_dashboard_export,
    to_view_model,
)


def _export():
    return build_operator_dashboard_export()


def test_operator_dashboard_export_builds_from_sprint4_learning_dashboard():
    export = _export()

    assert export.export_id == "sprint5-operator-dashboard-export-001"
    assert export.source_dashboard_snapshot_id == (
        "governed-learning-dashboard::composition-structural-001"
    )
    assert export.mode == OperatorExperienceMode.READ_ONLY_DEMO
    assert export.title == "EAIOS Operator Dashboard Export"
    assert export.provenance == "operator_experience:dashboard_export"


def test_operator_dashboard_export_has_safety_banner():
    export = _export()

    assert "READ ONLY" in export.safety_banner
    assert "no remediation" in export.safety_banner
    assert "no real tools" in export.safety_banner
    assert "no provider calls" in export.safety_banner
    assert "no benchmark scoring" in export.safety_banner
    assert "no dashboard changes applied" in export.safety_banner


def test_operator_dashboard_export_contains_five_cards():
    export = _export()

    assert len(export.cards) == 5

    sections = tuple(card.section for card in export.cards)

    assert sections == (
        OperatorReviewSection.INCIDENT_CONTEXT,
        OperatorReviewSection.RESTORATION_STATUS,
        OperatorReviewSection.APPROVAL_DECISION,
        OperatorReviewSection.LEARNING_FEEDBACK,
        OperatorReviewSection.IMPROVEMENT_QUEUE,
    )


def test_operator_dashboard_export_cards_are_review_required():
    export = _export()

    for card in export.cards:
        assert card.review_required is True
        assert card.provenance.startswith("operator_experience:")


def test_operator_dashboard_export_marks_blocked_cards():
    export = _export()

    blocked_cards = tuple(card.card_id for card in export.cards if card.blocked)

    assert blocked_cards == (
        "operator-card-restoration-status-001",
        "operator-card-approval-decision-001",
        "operator-card-improvement-queue-001",
    )


def test_operator_dashboard_export_preserves_review_queue():
    export = _export()

    assert export.review_queue == (
        "improvement-dashboard-conflict-staleness-001",
        "improvement-service-owner-risk-prompt-001",
        "improvement-denied-tool-degraded-mode-001",
    )


def test_operator_dashboard_export_blocks_unsafe_actions():
    export = _export()

    assert "benchmark_truth_update" in export.blocked_actions
    assert "benchmark_score_update" in export.blocked_actions
    assert "autonomous_remediation_policy_change" in export.blocked_actions
    assert "real_tool_execution" in export.blocked_actions
    assert "production_knowledge_auto_approval" in export.blocked_actions
    assert "execute_remediation" in export.blocked_actions
    assert "restart_service" in export.blocked_actions
    assert "score_benchmark_from_operator_export" in export.blocked_actions
    assert "apply_dashboard_changes_automatically" in export.blocked_actions


def test_operator_dashboard_export_preserves_no_execution_boundaries():
    export = _export()

    assert export.real_tool_execution_performed is False
    assert export.autonomous_remediation_allowed is False
    assert export.dashboard_changes_applied is False
    assert export.benchmark_scoring_allowed_from_export is False
    assert export.human_review_required is True


def test_operator_dashboard_export_embeds_sprint4_dashboard_view():
    export = _export()

    assert export.dashboard_view["summary"]["snapshot_id"] == (
        "governed-learning-dashboard::composition-structural-001"
    )
    assert export.dashboard_view["summary"]["dashboard_changes_applied"] is False
    assert export.dashboard_view["summary"]["benchmark_scoring_allowed_from_dashboard"] is False


def test_operator_dashboard_export_formats_are_stable():
    export = _export()

    assert export.export_formats == (
        "json_view_model",
        "markdown_summary",
        "cli_text",
    )


def test_operator_dashboard_summary_is_view_ready():
    export = _export()

    assert summarize_operator_dashboard_export(export) == {
        "export_id": "sprint5-operator-dashboard-export-001",
        "source_dashboard_snapshot_id": (
            "governed-learning-dashboard::composition-structural-001"
        ),
        "mode": "READ_ONLY_DEMO",
        "card_count": 5,
        "blocked_card_count": 3,
        "review_required_card_count": 5,
        "blocked_action_count": 16,
        "review_queue_count": 3,
        "export_format_count": 3,
        "real_tool_execution_performed": False,
        "autonomous_remediation_allowed": False,
        "dashboard_changes_applied": False,
        "benchmark_scoring_allowed_from_export": False,
        "human_review_required": True,
    }


def test_operator_dashboard_markdown_is_operator_readable():
    export = _export()

    markdown = render_operator_dashboard_markdown(export)

    assert "# EAIOS Operator Dashboard Export" in markdown
    assert "Safety: READ ONLY" in markdown
    assert "## Operator Cards" in markdown
    assert "Application health scenario is ready for operator review" in markdown
    assert "Restoration remains blocked from autonomous execution" in markdown
    assert "## Blocked Actions" in markdown
    assert "execute_remediation" in markdown
    assert "## Review Queue" in markdown
    assert "improvement-dashboard-conflict-staleness-001" in markdown


def test_operator_dashboard_view_model_is_json_serializable():
    export = _export()

    serialized = json.dumps(to_view_model(export), indent=2)

    assert "sprint5-operator-dashboard-export-001" in serialized
    assert "READ_ONLY_DEMO" in serialized
    assert "operator-card-incident-context-001" in serialized
    assert "markdown_summary" in serialized
    assert "benchmark_scoring_allowed_from_export" in serialized


def test_operator_experience_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint5/operator_experience.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
