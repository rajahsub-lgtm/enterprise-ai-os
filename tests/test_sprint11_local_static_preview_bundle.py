from dataclasses import replace
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint11.local_static_preview_manifest import (
    build_generation_context,
    build_local_static_preview_manifest,
)
from eaios.sprint11.local_static_preview_renderer import render_local_static_preview
from eaios.sprint11.local_static_preview_bundle import (
    LocalStaticPreviewBundleFileType,
    LocalStaticPreviewBundleStatus,
    assemble_local_static_preview_bundle,
    bundle_to_manifest_view,
    validate_bundle_is_in_memory_static_only,
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


def _bundle():
    return assemble_local_static_preview_bundle(manifest=_manifest())


def test_local_static_preview_bundle_assembles_in_memory():
    bundle = _bundle()

    assert bundle.bundle_id == "sprint11-local-static-preview-bundle-001"
    assert bundle.status == LocalStaticPreviewBundleStatus.ASSEMBLED_IN_MEMORY
    assert bundle.render_id == "sprint11-local-static-preview-render-001"
    assert bundle.manifest_id == "sprint11-local-static-preview-manifest-001"
    assert bundle.decision == "DO_NOT_DEPLOY_YET"
    assert bundle.file_count == 7
    assert bundle.total_byte_count > 0
    assert len(bundle.bundle_digest) == 64
    assert bundle.violations == ()


def test_local_static_preview_bundle_contains_expected_files():
    bundle = _bundle()

    output_paths = tuple(item.output_path for item in bundle.files)

    assert "preview/index.html" in output_paths
    assert "preview/architecture.html" in output_paths
    assert "preview/demo-storyboard.html" in output_paths
    assert "preview/real-enterprise-mapping.html" in output_paths
    assert "preview/interview-qa.html" in output_paths
    assert "preview/manifest.json" in output_paths
    assert output_paths.count("preview/manifest.json") >= 1


def test_local_static_preview_bundle_files_have_digests_and_sizes():
    bundle = _bundle()

    assert all(len(item.sha256_digest) == 64 for item in bundle.files)
    assert all(item.byte_count > 0 for item in bundle.files)
    assert all(item.persisted is False for item in bundle.files)
    assert any(item.file_type == LocalStaticPreviewBundleFileType.HTML for item in bundle.files)
    assert any(item.file_type == LocalStaticPreviewBundleFileType.JSON for item in bundle.files)


def test_local_static_preview_bundle_preserves_no_persistence_or_deployment():
    bundle = _bundle()

    assert bundle.files_persisted is False
    assert bundle.site_published is False
    assert bundle.server_started is False
    assert bundle.browser_opened is False
    assert bundle.cloud_resources_created is False


def test_local_static_preview_bundle_preserves_disabled_state():
    bundle = _bundle()

    assert bundle.providers_enabled is False
    assert bundle.mcp_connectors_enabled is False
    assert bundle.production_data_used is False
    assert bundle.credentials_required is False
    assert bundle.runtime_enabled is False
    assert bundle.writes_enabled is False
    assert bundle.notifications_enabled is False
    assert bundle.remediation_enabled is False
    assert bundle.benchmark_truth_mutation_enabled is False
    assert bundle.autonomous_action_enabled is False
    assert bundle.human_approval_required is True
    assert bundle.rollback_required is True



def test_local_static_preview_bundle_blocks_unsafe_render_result():
    unsafe_manifest = replace(
        _manifest(),
        providers_enabled=True,
        runtime_enabled=True,
        autonomous_action_enabled=True,
        human_approval_required=False,
    )
    unsafe_render = render_local_static_preview(unsafe_manifest)

    bundle = assemble_local_static_preview_bundle(
        manifest=unsafe_manifest,
        render_result=unsafe_render,
    )

    assert bundle.status == LocalStaticPreviewBundleStatus.BLOCKED_RENDER_NOT_SAFE
    assert bundle.file_count == 0
    assert bundle.files == ()
    assert "providers must remain disabled" in bundle.violations
    assert "runtime must not be enabled" in bundle.violations
    assert "autonomous action must remain disabled" in bundle.violations
    assert "human approval must remain required" in bundle.violations


def test_local_static_preview_bundle_manifest_view_is_json_serializable():
    view = bundle_to_manifest_view(_bundle())
    serialized = json.dumps(view, indent=2, default=str)

    assert "sprint11-local-static-preview-bundle-001" in serialized
    assert "ASSEMBLED_IN_MEMORY" in serialized
    assert "DO_NOT_DEPLOY_YET" in serialized
    assert "preview/index.html" in serialized
    assert "preview/manifest.json" in serialized
    assert "providers_enabled" in serialized
    assert "mcp_connectors_enabled" in serialized


def test_local_static_preview_bundle_validation_accepts_safe_bundle():
    valid, violations = validate_bundle_is_in_memory_static_only(_bundle())

    assert valid is True
    assert violations == ()


def test_local_static_preview_bundle_validation_blocks_drift():
    unsafe_bundle = replace(
        _bundle(),
        files_persisted=True,
        site_published=True,
        providers_enabled=True,
        mcp_connectors_enabled=True,
        runtime_enabled=True,
        autonomous_action_enabled=True,
        human_approval_required=False,
    )

    valid, violations = validate_bundle_is_in_memory_static_only(unsafe_bundle)

    assert valid is False
    assert "files must not be persisted" in violations
    assert "site must not be published" in violations
    assert "providers must remain disabled" in violations
    assert "MCP connectors must remain disabled" in violations
    assert "runtime must not be enabled" in violations
    assert "autonomous action must remain disabled" in violations
    assert "human approval must remain required" in violations


def test_local_static_preview_bundle_source_has_no_external_execution_or_file_writes():
    source = Path("src/eaios/sprint11/local_static_preview_bundle.py").read_text(
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
