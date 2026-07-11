from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint6.static_review_page import (
    StaticReviewPageMode,
    build_static_review_page_model,
    summarize_static_review_page_model,
    to_view_model,
)


def _page():
    return build_static_review_page_model()


def test_static_review_page_builds_from_export_plan():
    page = _page()

    assert page.page_id == "sprint6-static-review-page-001"
    assert page.mode == StaticReviewPageMode.RENDER_ONLY
    assert page.title == "EAIOS Portfolio Review Page"
    assert page.source_export_plan_id == "sprint6-artifact-export-plan-001"
    assert page.provenance == "static_review_page:model"


def test_static_review_page_has_expected_sections():
    page = _page()

    assert len(page.sections) == 5

    titles = tuple(section.title for section in page.sections)
    assert titles == (
        "Demo Story",
        "Operator Experience",
        "Cloud Readiness",
        "Package Plan",
        "Governance Boundaries",
    )

    for section in page.sections:
        assert section.provenance == "static_review_page:section"
        assert len(section.evidence_refs) >= 1


def test_static_review_page_html_contains_portfolio_content():
    page = _page()
    html = page.rendered_html

    assert "<!doctype html>" in html
    assert "<h1>EAIOS Portfolio Review Page</h1>" in html
    assert "Mode: RENDER_ONLY" in html
    assert "sprint6-artifact-export-plan-001" in html
    assert "benchmark-grounded governed AIOps" in html
    assert "REVIEW_READY_NOT_DEPLOYED" in html
    assert "GCP_READINESS_REVIEW_ONLY" in html
    assert "Human review required: true" in html


def test_static_review_page_blocked_actions_are_explicit():
    page = _page()

    assert page.blocked_actions == (
        "write_static_html_file",
        "create_export_folder",
        "copy_artifact_files",
        "create_archive",
        "run_shell_command",
        "create_cloud_resources",
        "load_secret_material",
        "call_real_provider",
        "call_real_connector",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_review_page",
        "enable_autonomous_remediation",
    )


def test_static_review_page_embeds_export_summary():
    page = _page()

    assert page.export_plan_summary["export_plan_id"] == "sprint6-artifact-export-plan-001"
    assert page.export_plan_summary["mode"] == "DRY_RUN_ONLY"
    assert page.export_plan_summary["files_copied"] is False
    assert page.export_plan_summary["human_review_required"] is True


def test_static_review_page_preserves_no_execution_boundaries():
    page = _page()

    assert page.html_file_written is False
    assert page.export_folder_created is False
    assert page.files_copied is False
    assert page.archive_created is False
    assert page.shell_commands_executed is False
    assert page.cloud_resources_created is False
    assert page.secrets_loaded is False
    assert page.provider_calls_performed is False
    assert page.real_connectors_called is False
    assert page.remediation_performed is False
    assert page.notifications_sent is False
    assert page.benchmark_scoring_performed is False
    assert page.autonomous_remediation_allowed is False
    assert page.human_review_required is True


def test_static_review_page_summary_is_view_ready():
    page = _page()

    assert summarize_static_review_page_model(page) == {
        "page_id": "sprint6-static-review-page-001",
        "mode": "RENDER_ONLY",
        "title": "EAIOS Portfolio Review Page",
        "source_export_plan_id": "sprint6-artifact-export-plan-001",
        "section_count": 5,
        "blocked_action_count": 13,
        "html_file_written": False,
        "export_folder_created": False,
        "files_copied": False,
        "archive_created": False,
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


def test_static_review_page_view_model_is_json_serializable():
    page = _page()

    serialized = json.dumps(to_view_model(page), indent=2)

    assert "sprint6-static-review-page-001" in serialized
    assert "EAIOS Portfolio Review Page" in serialized
    assert "score_benchmark_from_review_page" in serialized


def test_static_review_page_module_does_not_write_or_call_external_systems():
    source = Path("src/eaios/sprint6/static_review_page.py").read_text(
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
