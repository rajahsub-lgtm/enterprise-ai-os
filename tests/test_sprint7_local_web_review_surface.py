from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.local_web_review_surface import (
    LocalWebPageKind,
    LocalWebReviewMode,
    build_local_web_review_surface,
    summarize_local_web_review_surface,
    to_view_model,
)


def _surface():
    return build_local_web_review_surface()


def test_local_web_review_surface_builds_model_only_surface():
    surface = _surface()

    assert surface.surface_id == "sprint7-local-web-review-surface-001"
    assert surface.mode == LocalWebReviewMode.SURFACE_MODEL_ONLY
    assert surface.title == "EAIOS Local Web Review Surface"
    assert surface.source_container_contract_id == "sprint7-container-packaging-contract-001"
    assert surface.provenance == "local_web_review_surface:model"


def test_local_web_review_surface_pages_are_declared():
    surface = _surface()

    assert len(surface.pages) == 6

    titles = tuple(page.title for page in surface.pages)
    assert titles == (
        "Overview",
        "Governance Boundaries",
        "Container Package Contract",
        "Cloud Readiness",
        "Provider Integration",
        "MCP Connector Permissions",
    )

    routes = tuple(page.route for page in surface.pages)
    assert routes == (
        "/review/overview",
        "/review/governance",
        "/review/package",
        "/review/cloud",
        "/review/provider",
        "/review/connector",
    )


def test_local_web_review_surface_page_kinds_are_explicit():
    surface = _surface()

    assert tuple(page.page_kind for page in surface.pages) == (
        LocalWebPageKind.OVERVIEW,
        LocalWebPageKind.GOVERNANCE,
        LocalWebPageKind.PACKAGE,
        LocalWebPageKind.CLOUD,
        LocalWebPageKind.PROVIDER,
        LocalWebPageKind.CONNECTOR,
    )


def test_local_web_review_surface_pages_have_evidence_and_disabled_controls():
    surface = _surface()

    for page in surface.pages:
        assert page.summary
        assert len(page.evidence_refs) >= 1
        assert len(page.disabled_controls) >= 3
        assert page.provenance == "local_web_review_surface:page"


def test_local_web_review_surface_blocked_actions_are_explicit():
    surface = _surface()

    assert surface.blocked_actions == (
        "start_local_server",
        "open_browser",
        "write_static_html_file",
        "build_container_image",
        "run_container",
        "push_container_image",
        "create_cloud_resources",
        "load_secret_material",
        "call_real_provider",
        "call_real_connector",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_web_output",
        "update_benchmark_truth_from_web_output",
        "enable_autonomous_remediation",
    )


def test_local_web_review_surface_html_contains_review_content():
    html = _surface().rendered_html

    assert "<!doctype html>" in html
    assert "<h1>EAIOS Local Web Review Surface</h1>" in html
    assert "Mode: SURFACE_MODEL_ONLY" in html
    assert "/review/overview" in html
    assert "/review/governance" in html
    assert "/review/package" in html
    assert "/review/cloud" in html
    assert "/review/provider" in html
    assert "/review/connector" in html
    assert "Human review required: true" in html
    assert "score_benchmark_from_web_output" in html


def test_local_web_review_surface_preserves_no_execution_boundaries():
    surface = _surface()

    assert surface.server_started is False
    assert surface.browser_opened is False
    assert surface.files_written is False
    assert surface.shell_commands_executed is False
    assert surface.cloud_resources_created is False
    assert surface.secrets_loaded is False
    assert surface.provider_calls_performed is False
    assert surface.real_connectors_called is False
    assert surface.remediation_performed is False
    assert surface.notifications_sent is False
    assert surface.benchmark_scoring_performed is False
    assert surface.autonomous_remediation_allowed is False
    assert surface.human_review_required is True


def test_local_web_review_surface_embeds_container_contract_summary():
    surface = _surface()

    assert surface.container_contract_summary["contract_id"] == (
        "sprint7-container-packaging-contract-001"
    )
    assert surface.container_contract_summary["mode"] == "REVIEW_ONLY_CONTRACT"
    assert surface.container_contract_summary["build_performed"] is False
    assert surface.container_contract_summary["human_review_required"] is True


def test_local_web_review_surface_summary_is_view_ready():
    surface = _surface()

    assert summarize_local_web_review_surface(surface) == {
        "surface_id": "sprint7-local-web-review-surface-001",
        "mode": "SURFACE_MODEL_ONLY",
        "title": "EAIOS Local Web Review Surface",
        "source_container_contract_id": "sprint7-container-packaging-contract-001",
        "page_count": 6,
        "navigation_count": 6,
        "blocked_action_count": 15,
        "server_started": False,
        "browser_opened": False,
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


def test_local_web_review_surface_view_model_is_json_serializable():
    surface = _surface()

    serialized = json.dumps(to_view_model(surface), indent=2)

    assert "sprint7-local-web-review-surface-001" in serialized
    assert "EAIOS Local Web Review Surface" in serialized
    assert "start_local_server" in serialized
    assert "score_benchmark_from_web_output" in serialized


def test_local_web_review_surface_module_does_not_start_server_or_call_external_systems():
    source = Path("src/eaios/sprint7/local_web_review_surface.py").read_text(
        encoding="utf-8"
    ).lower()

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "socket" not in source
    assert "uvicorn" not in source
    assert "flask" not in source
    assert "fastapi" not in source
    assert "streamlit" not in source
    assert "webbrowser" not in source
    assert "write_text(" not in source
    assert "mkdir(" not in source
    assert "requests.post" not in source
    assert "httpx.post" not in source
    assert "gcloud run deploy" not in source
    assert "terraform apply" not in source
    assert "docker build" not in source
    assert "docker run" not in source
    assert "docker push" not in source
    assert "openai" not in source
    assert "anthropic" not in source
