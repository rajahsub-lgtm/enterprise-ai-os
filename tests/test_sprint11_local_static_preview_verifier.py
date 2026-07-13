from dataclasses import replace
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint11.local_static_preview_manifest import (
    build_generation_context,
    build_local_static_preview_manifest,
)
from eaios.sprint11.local_static_preview_bundle import assemble_local_static_preview_bundle
from eaios.sprint11.local_static_preview_verifier import (
    LocalStaticPreviewCheckCategory,
    LocalStaticPreviewVerificationStatus,
    verification_to_view_model,
    verify_local_static_preview_bundle_safety,
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


def _verification():
    return verify_local_static_preview_bundle_safety(_bundle())


def test_local_static_preview_verifier_accepts_safe_bundle():
    result = _verification()

    assert result.verification_id == "sprint11-local-static-preview-verification-001"
    assert result.status == LocalStaticPreviewVerificationStatus.VERIFIED_SAFE_FOR_LOCAL_REVIEW
    assert result.bundle_id == "sprint11-local-static-preview-bundle-001"
    assert result.decision == "DO_NOT_DEPLOY_YET"
    assert result.violations == ()
    assert result.check_count == 11
    assert result.passed_count == 11
    assert result.failed_count == 0


def test_local_static_preview_verifier_preserves_no_materialization_or_cloud_approval():
    result = _verification()

    assert result.files_persisted is False
    assert result.site_published is False
    assert result.server_started is False
    assert result.browser_opened is False
    assert result.cloud_resources_created is False
    assert result.materialization_allowed is False
    assert result.cloud_deployment_allowed is False


def test_local_static_preview_verifier_preserves_disabled_integrations_and_runtime():
    result = _verification()

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


def test_local_static_preview_verifier_has_expected_check_categories():
    result = _verification()

    categories = {check.category for check in result.checks}

    assert LocalStaticPreviewCheckCategory.BUNDLE_STATE in categories
    assert LocalStaticPreviewCheckCategory.CONTENT_BOUNDARY in categories
    assert LocalStaticPreviewCheckCategory.DECISION_BOUNDARY in categories
    assert LocalStaticPreviewCheckCategory.INTEGRATION_BOUNDARY in categories
    assert LocalStaticPreviewCheckCategory.RUNTIME_BOUNDARY in categories
    assert LocalStaticPreviewCheckCategory.APPROVAL_BOUNDARY in categories


def test_local_static_preview_verifier_blocks_unsafe_bundle_drift():
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

    result = verify_local_static_preview_bundle_safety(unsafe_bundle)

    assert result.status == LocalStaticPreviewVerificationStatus.BLOCKED_SAFETY_VIOLATIONS
    assert result.failed_count > 0
    assert any("files must not be persisted" in item for item in result.violations)
    assert any("providers must remain disabled" in item for item in result.violations)
    assert any("MCP connectors must remain disabled" in item for item in result.violations)
    assert any("runtime must not be enabled" in item for item in result.violations)
    assert any("autonomous action must remain disabled" in item for item in result.violations)
    assert any("human approval must remain required" in item for item in result.violations)
    assert result.materialization_allowed is False
    assert result.cloud_deployment_allowed is False


def test_local_static_preview_verifier_view_model_is_json_serializable():
    view_model = verification_to_view_model(_verification())
    serialized = json.dumps(view_model, indent=2, default=str)

    assert "sprint11-local-static-preview-verification-001" in serialized
    assert "VERIFIED_SAFE_FOR_LOCAL_REVIEW" in serialized
    assert "DO_NOT_DEPLOY_YET" in serialized
    assert "providers_enabled" in serialized
    assert "mcp_connectors_enabled" in serialized
    assert "materialization_allowed" in serialized
    assert "cloud_deployment_allowed" in serialized


def test_local_static_preview_verifier_source_has_no_external_execution_or_file_writes():
    source = Path("src/eaios/sprint11/local_static_preview_verifier.py").read_text(
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
