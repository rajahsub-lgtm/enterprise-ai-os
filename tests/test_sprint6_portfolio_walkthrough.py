from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint6.portfolio_walkthrough import (
    PortfolioWalkthroughAudience,
    PortfolioWalkthroughMode,
    build_portfolio_walkthrough,
    summarize_portfolio_walkthrough,
    to_view_model,
)


def _walkthrough():
    return build_portfolio_walkthrough()


def test_portfolio_walkthrough_builds_from_static_review_page():
    walkthrough = _walkthrough()

    assert walkthrough.walkthrough_id == "sprint6-portfolio-walkthrough-001"
    assert walkthrough.mode == PortfolioWalkthroughMode.READ_ONLY_SCRIPT
    assert walkthrough.audience == PortfolioWalkthroughAudience.ARCHITECTURE_REVIEWER
    assert walkthrough.title == "EAIOS Portfolio Walkthrough"
    assert walkthrough.source_static_review_page_id == "sprint6-static-review-page-001"
    assert walkthrough.provenance == "portfolio_walkthrough:script"


def test_portfolio_walkthrough_steps_are_ordered():
    walkthrough = _walkthrough()

    assert len(walkthrough.steps) == 8
    assert tuple(step.order for step in walkthrough.steps) == tuple(range(1, 9))

    titles = tuple(step.title for step in walkthrough.steps)
    assert titles == (
        "North Star",
        "Application-Health Scenario",
        "Operator Experience",
        "Cloud Readiness",
        "Provider and Connector Seams",
        "Portfolio Package Plan",
        "Governance Boundaries",
        "Close",
    )


def test_portfolio_walkthrough_steps_have_talk_tracks_and_evidence():
    walkthrough = _walkthrough()

    for step in walkthrough.steps:
        assert step.talk_track
        assert step.safety_message
        assert len(step.evidence_refs) >= 1
        assert step.duration_minutes >= 2
        assert step.provenance == "portfolio_walkthrough:step"


def test_portfolio_walkthrough_mentions_core_demo_story():
    text = _walkthrough().rendered_markdown

    assert "# EAIOS Portfolio Walkthrough" in text
    assert "benchmark-grounded application-health evidence" in text
    assert "The operator sees context" in text
    assert "GCP readiness checklist" in text
    assert "Provider and MCP connector seams" in text
    assert "local package manifest" in text
    assert "safety boundaries explicit" in text
    assert "Human review required: true" in text


def test_portfolio_walkthrough_supports_audience_override():
    walkthrough = build_portfolio_walkthrough(
        audience=PortfolioWalkthroughAudience.HIRING_MANAGER
    )

    assert walkthrough.audience == PortfolioWalkthroughAudience.HIRING_MANAGER
    assert "Audience: HIRING_MANAGER" in walkthrough.rendered_markdown


def test_portfolio_walkthrough_blocked_actions_are_explicit():
    walkthrough = _walkthrough()

    assert walkthrough.blocked_actions == (
        "write_walkthrough_file",
        "run_shell_command",
        "create_export_folder",
        "copy_artifact_files",
        "create_cloud_resources",
        "load_secret_material",
        "call_real_provider",
        "call_real_connector",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_walkthrough",
        "enable_autonomous_remediation",
    )


def test_portfolio_walkthrough_embeds_static_review_summary():
    walkthrough = _walkthrough()

    assert walkthrough.static_review_summary["page_id"] == "sprint6-static-review-page-001"
    assert walkthrough.static_review_summary["mode"] == "RENDER_ONLY"
    assert walkthrough.static_review_summary["html_file_written"] is False
    assert walkthrough.static_review_summary["human_review_required"] is True


def test_portfolio_walkthrough_preserves_no_execution_boundaries():
    walkthrough = _walkthrough()

    assert walkthrough.files_written is False
    assert walkthrough.shell_commands_executed is False
    assert walkthrough.cloud_resources_created is False
    assert walkthrough.secrets_loaded is False
    assert walkthrough.provider_calls_performed is False
    assert walkthrough.real_connectors_called is False
    assert walkthrough.remediation_performed is False
    assert walkthrough.notifications_sent is False
    assert walkthrough.benchmark_scoring_performed is False
    assert walkthrough.autonomous_remediation_allowed is False
    assert walkthrough.human_review_required is True


def test_portfolio_walkthrough_summary_is_view_ready():
    walkthrough = _walkthrough()

    assert summarize_portfolio_walkthrough(walkthrough) == {
        "walkthrough_id": "sprint6-portfolio-walkthrough-001",
        "mode": "READ_ONLY_SCRIPT",
        "audience": "ARCHITECTURE_REVIEWER",
        "title": "EAIOS Portfolio Walkthrough",
        "source_static_review_page_id": "sprint6-static-review-page-001",
        "step_count": 8,
        "total_duration_minutes": 24,
        "transition_prompt_count": 4,
        "blocked_action_count": 12,
        "files_written": False,
        "shell_commands_executed": False,
        "cloud_resources_created": False,
        "secrets_loaded": False,
        "provider_calls_performed": False,
        "real_connectors_called": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_portfolio_walkthrough_view_model_is_json_serializable():
    walkthrough = _walkthrough()

    serialized = json.dumps(to_view_model(walkthrough), indent=2)

    assert "sprint6-portfolio-walkthrough-001" in serialized
    assert "EAIOS Portfolio Walkthrough" in serialized
    assert "score_benchmark_from_walkthrough" in serialized


def test_portfolio_walkthrough_module_does_not_write_or_call_external_systems():
    source = Path("src/eaios/sprint6/portfolio_walkthrough.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "write_text(" not in source
    assert "mkdir(" not in source
    assert "shutil" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "google.cloud" not in source.lower()
    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
