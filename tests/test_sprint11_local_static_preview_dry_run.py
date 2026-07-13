from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint11.local_static_preview_dry_run import (
    LocalStaticPreviewDryRunStatus,
    build_local_static_preview_dry_run_request,
    dry_run_to_view_model,
    run_local_static_preview_dry_run,
)


def _safe_request():
    return build_local_static_preview_dry_run_request(
        branch="sprint-11-local-static-preview",
        commit="abc1234",
        git_status_clean=True,
        full_test_suite_passed=True,
    )


def _result():
    return run_local_static_preview_dry_run(_safe_request())


def test_local_static_preview_dry_run_completes_safe_local_review():
    result = _result()

    assert result.dry_run_id == "sprint11-local-static-preview-dry-run-001"
    assert result.status == LocalStaticPreviewDryRunStatus.COMPLETED_SAFE_LOCAL_REVIEW
    assert result.decision == "DO_NOT_DEPLOY_YET"
    assert result.manifest.manifest_id == "sprint11-local-static-preview-manifest-001"
    assert result.render_result.render_id == "sprint11-local-static-preview-render-001"
    assert result.bundle.bundle_id == "sprint11-local-static-preview-bundle-001"
    assert result.verification.verification_id == "sprint11-local-static-preview-verification-001"
    assert result.verification.failed_count == 0


def test_local_static_preview_dry_run_blocks_invalid_context():
    request = build_local_static_preview_dry_run_request(
        branch="main",
        commit="abc1234",
        git_status_clean=True,
        full_test_suite_passed=True,
    )

    result = run_local_static_preview_dry_run(request)

    assert result.status == LocalStaticPreviewDryRunStatus.BLOCKED_SAFETY_VERIFICATION
    assert result.decision == "DO_NOT_DEPLOY_YET"
    assert result.materialization_allowed is False
    assert result.cloud_deployment_allowed is False
    assert result.verification.failed_count > 0


def test_local_static_preview_dry_run_preserves_no_persistence_or_cloud_deployment():
    result = _result()

    assert result.files_persisted is False
    assert result.site_published is False
    assert result.server_started is False
    assert result.browser_opened is False
    assert result.cloud_resources_created is False
    assert result.materialization_allowed is False
    assert result.cloud_deployment_allowed is False


def test_local_static_preview_dry_run_preserves_disabled_integrations_and_runtime():
    result = _result()

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


def test_local_static_preview_dry_run_view_model_is_json_serializable():
    view_model = dry_run_to_view_model(_result())
    serialized = json.dumps(view_model, indent=2, default=str)

    assert "sprint11-local-static-preview-dry-run-001" in serialized
    assert "COMPLETED_SAFE_LOCAL_REVIEW" in serialized
    assert "DO_NOT_DEPLOY_YET" in serialized
    assert "sprint11-local-static-preview-manifest-001" in serialized
    assert "sprint11-local-static-preview-render-001" in serialized
    assert "sprint11-local-static-preview-bundle-001" in serialized
    assert "sprint11-local-static-preview-verification-001" in serialized
    assert "providers_enabled" in serialized
    assert "mcp_connectors_enabled" in serialized
    assert "cloud_deployment_allowed" in serialized


def test_local_static_preview_dry_run_source_has_no_external_execution_or_file_writes():
    source = Path("src/eaios/sprint11/local_static_preview_dry_run.py").read_text(
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
