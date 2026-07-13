from dataclasses import replace
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint11.local_static_preview_manifest import (
    build_generation_context,
    build_local_static_preview_manifest,
)
from eaios.sprint11.local_static_preview_renderer import (
    LocalStaticPreviewPageKind,
    LocalStaticPreviewRenderStatus,
    build_local_static_preview_pages,
    render_local_static_preview,
    render_result_to_view_model,
)


def _manifest():
    return build_local_static_preview_manifest(
        build_generation_context(
            branch="sprint-11-local-static-preview",
            commit="abc1234",
            git_status_clean=True,
            full_test_suite_passed=True,
        )
    )


def test_local_static_preview_renderer_renders_in_memory():
    result = render_local_static_preview(_manifest())

    assert result.render_id == "sprint11-local-static-preview-render-001"
    assert result.status == LocalStaticPreviewRenderStatus.RENDERED_IN_MEMORY
    assert result.manifest_id == "sprint11-local-static-preview-manifest-001"
    assert result.decision == "DO_NOT_DEPLOY_YET"
    assert result.page_count == 6
    assert result.violations == ()


def test_local_static_preview_renderer_creates_expected_page_kinds():
    pages = build_local_static_preview_pages(_manifest())

    kinds = tuple(page.kind for page in pages)
    output_paths = tuple(page.output_path for page in pages)

    assert LocalStaticPreviewPageKind.LANDING in kinds
    assert LocalStaticPreviewPageKind.ARCHITECTURE in kinds
    assert LocalStaticPreviewPageKind.DEMO_STORYBOARD in kinds
    assert LocalStaticPreviewPageKind.ENTERPRISE_MAPPING in kinds
    assert LocalStaticPreviewPageKind.INTERVIEW_QA in kinds
    assert LocalStaticPreviewPageKind.MANIFEST in kinds

    assert "preview/index.html" in output_paths
    assert "preview/architecture.html" in output_paths
    assert "preview/demo-storyboard.html" in output_paths
    assert "preview/real-enterprise-mapping.html" in output_paths
    assert "preview/interview-qa.html" in output_paths
    assert "preview/manifest.json" in output_paths


def test_local_static_preview_renderer_pages_are_not_persisted():
    result = render_local_static_preview(_manifest())

    assert result.files_persisted is False
    assert result.site_published is False
    assert result.server_started is False
    assert result.browser_opened is False
    assert result.cloud_resources_created is False

    assert all(page.rendered_in_memory is True for page in result.pages)
    assert all(page.persisted is False for page in result.pages)


def test_local_static_preview_renderer_embeds_safety_banner():
    result = render_local_static_preview(_manifest())
    landing = next(page for page in result.pages if page.kind == LocalStaticPreviewPageKind.LANDING)

    assert "<section id=\"safety-banner\">" in landing.html
    assert "Decision: DO_NOT_DEPLOY_YET" in landing.html
    assert "Preview type: STATIC_REVIEW_PREVIEW" in landing.html
    assert "Providers enabled: False" in landing.html
    assert "MCP connectors enabled: False" in landing.html
    assert "Production data used: False" in landing.html
    assert "Human approval required: True" in landing.html


def test_local_static_preview_renderer_preserves_disabled_state():
    result = render_local_static_preview(_manifest())

    assert result.providers_enabled is False
    assert result.mcp_connectors_enabled is False
    assert result.production_data_used is False
    assert result.credentials_required is False
    assert result.runtime_enabled is False
    assert result.writes_enabled is False
    assert result.notifications_enabled is False
    assert result.remediation_enabled is False
    assert result.benchmark_truth_mutation_enabled is False
    assert result.autonomous_action_enabled is False
    assert result.human_approval_required is True
    assert result.rollback_required is True



def test_local_static_preview_renderer_blocks_manifest_violations():
    unsafe_manifest = replace(
        _manifest(),
        providers_enabled=True,
        mcp_connectors_enabled=True,
        runtime_enabled=True,
        autonomous_action_enabled=True,
        human_approval_required=False,
    )

    result = render_local_static_preview(unsafe_manifest)

    assert result.status == LocalStaticPreviewRenderStatus.BLOCKED_MANIFEST_VIOLATIONS
    assert result.page_count == 0
    assert result.pages == ()
    assert "providers must remain disabled" in result.violations
    assert "MCP connectors must remain disabled" in result.violations
    assert "runtime must not be enabled" in result.violations
    assert "autonomous action must remain disabled" in result.violations
    assert "human approval must remain required" in result.violations


def test_local_static_preview_renderer_view_model_is_json_serializable():
    view_model = render_result_to_view_model(render_local_static_preview(_manifest()))
    serialized = json.dumps(view_model, indent=2, default=str)

    assert "sprint11-local-static-preview-render-001" in serialized
    assert "RENDERED_IN_MEMORY" in serialized
    assert "DO_NOT_DEPLOY_YET" in serialized
    assert "preview/index.html" in serialized
    assert "providers_enabled" in serialized
    assert "mcp_connectors_enabled" in serialized


def test_local_static_preview_renderer_includes_key_story_points():
    result = render_local_static_preview(_manifest())
    html = "\n".join(page.html for page in result.pages)

    assert "Synthetic execution, real enterprise architecture." in html
    assert "Cloud deployment remains not approved." in html
    assert "Business Outcome -&gt; Capability -&gt; Skill" in html
    assert "HIGH evidence with LOW operational confidence" in html
    assert "Providers and MCP connectors remain disabled." in html
    assert "Decision remains DO_NOT_DEPLOY_YET." in html


def test_local_static_preview_renderer_source_has_no_external_execution_or_file_writes():
    source = Path("src/eaios/sprint11/local_static_preview_renderer.py").read_text(
        encoding="utf-8"
    ).lower()

    for forbidden in [
        "subprocess",
        "os.system",
        "requests.",
        "httpx.",
        "urllib",
        "socket",
        "api_key",
        "password",
        "bearer ",
        "client_secret",
        "private_key",
        "secret_value",
        "secret_key",
        "write_text(",
        "mkdir(",
        "open(",
        "startfile",
        "webbrowser",
        "execute_tool(",
        "restart_service(",
    ]:
        assert forbidden not in source
