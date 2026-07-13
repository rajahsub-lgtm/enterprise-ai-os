from dataclasses import replace
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint11.local_static_preview_manifest import (
    LocalStaticPreviewDecision,
    LocalStaticPreviewManifestStatus,
    build_generation_context,
    build_local_static_preview_manifest,
    manifest_to_dict,
    summarize_manifest,
    validate_manifest_is_static_review_only,
)


def _valid_context():
    return build_generation_context(
        branch="sprint-11-local-static-preview",
        commit="abc1234",
        git_status_clean=True,
        full_test_suite_passed=True,
    )


def _manifest():
    return build_local_static_preview_manifest(_valid_context())


def test_local_static_preview_manifest_builds_ready_in_memory():
    manifest = _manifest()

    assert manifest.manifest_id == "sprint11-local-static-preview-manifest-001"
    assert manifest.preview_id == "eaios-local-static-preview-contract-001"
    assert manifest.preview_type.value == "STATIC_REVIEW_PREVIEW"
    assert manifest.mode.value == "LOCAL_CONTRACT_ONLY"
    assert manifest.status == LocalStaticPreviewManifestStatus.READY_IN_MEMORY
    assert manifest.decision == LocalStaticPreviewDecision.DO_NOT_DEPLOY_YET
    assert manifest.branch == "sprint-11-local-static-preview"
    assert manifest.commit == "abc1234"


def test_local_static_preview_manifest_blocks_invalid_context():
    context = build_generation_context(
        branch="main",
        commit="abc1234",
        git_status_clean=True,
        full_test_suite_passed=True,
    )

    manifest = build_local_static_preview_manifest(context)

    assert manifest.status == LocalStaticPreviewManifestStatus.BLOCKED_INVALID_CONTEXT
    assert manifest.decision == LocalStaticPreviewDecision.DO_NOT_DEPLOY_YET
    assert manifest.static_preview_approved is False


def test_local_static_preview_manifest_includes_contract_sources_and_planned_artifacts():
    manifest = _manifest()

    assert "README.md" in manifest.source_artifacts
    assert "docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md" in manifest.source_artifacts
    assert "docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md" in manifest.source_artifacts
    assert "docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_DECISION_RECORD.md" in manifest.source_artifacts

    output_paths = tuple(artifact.output_path for artifact in manifest.planned_artifacts)

    assert "preview/index.html" in output_paths
    assert "preview/architecture.html" in output_paths
    assert "preview/demo-storyboard.html" in output_paths
    assert "preview/manifest.json" in output_paths
    assert all(artifact.materialized is False for artifact in manifest.planned_artifacts)
    assert all(artifact.included is True for artifact in manifest.planned_artifacts)


def test_local_static_preview_manifest_preserves_non_approval():
    manifest = _manifest()

    assert manifest.cloud_deployment_approved is False
    assert manifest.static_preview_approved is False
    assert manifest.implementation_approved is False
    assert manifest.approval_record_created is False
    assert manifest.release_created is False
    assert manifest.decision.value == "DO_NOT_DEPLOY_YET"


def test_local_static_preview_manifest_preserves_no_materialization_or_runtime():
    manifest = _manifest()

    assert manifest.files_materialized is False
    assert manifest.cloud_resources_created is False
    assert manifest.runtime_enabled is False
    assert manifest.server_started is False
    assert manifest.browser_opened is False



def test_local_static_preview_manifest_preserves_provider_disabled_state():
    manifest = _manifest()

    assert manifest.providers_enabled is False
    assert manifest.provider_runtime_enabled is False
    assert manifest.provider_credentials_present is False
    assert manifest.provider_invocation_allowed is False
    assert manifest.provider_cost_enabled is False


def test_local_static_preview_manifest_preserves_mcp_connector_disabled_state():
    manifest = _manifest()

    assert manifest.mcp_connectors_enabled is False
    assert manifest.connector_runtime_enabled is False
    assert manifest.connector_credentials_present is False
    assert manifest.connector_invocation_allowed is False
    assert manifest.connector_write_allowed is False
    assert manifest.connector_notification_allowed is False
    assert manifest.connector_remediation_allowed is False
    assert manifest.connector_benchmark_mutation_allowed is False
    assert manifest.connector_cost_enabled is False


def test_local_static_preview_manifest_preserves_data_action_and_benchmark_boundaries():
    manifest = _manifest()

    assert manifest.production_data_used is False
    assert manifest.credentials_required is False
    assert manifest.writes_enabled is False
    assert manifest.notifications_enabled is False
    assert manifest.remediation_enabled is False
    assert manifest.benchmark_truth_mutation_enabled is False
    assert manifest.autonomous_action_enabled is False
    assert manifest.human_approval_required is True
    assert manifest.rollback_required is True


def test_local_static_preview_manifest_summary_is_safe():
    summary = summarize_manifest(_manifest())

    assert summary["manifest_id"] == "sprint11-local-static-preview-manifest-001"
    assert summary["status"] == "READY_IN_MEMORY"
    assert summary["decision"] == "DO_NOT_DEPLOY_YET"
    assert summary["source_artifact_count"] == 6
    assert summary["planned_artifact_count"] == 6
    assert summary["cloud_deployment_approved"] is False
    assert summary["static_preview_approved"] is False
    assert summary["implementation_approved"] is False
    assert summary["files_materialized"] is False
    assert summary["providers_enabled"] is False
    assert summary["mcp_connectors_enabled"] is False
    assert summary["production_data_used"] is False
    assert summary["credentials_required"] is False
    assert summary["human_approval_required"] is True
    assert summary["rollback_required"] is True


def test_local_static_preview_manifest_to_dict_is_json_serializable():
    as_dict = manifest_to_dict(_manifest())
    serialized = json.dumps(as_dict, indent=2, default=str)

    assert "sprint11-local-static-preview-manifest-001" in serialized
    assert "STATIC_REVIEW_PREVIEW" in serialized
    assert "LOCAL_CONTRACT_ONLY" in serialized
    assert "DO_NOT_DEPLOY_YET" in serialized
    assert "providers_enabled" in serialized
    assert "mcp_connectors_enabled" in serialized


def test_local_static_preview_manifest_validator_accepts_safe_manifest():
    valid, violations = validate_manifest_is_static_review_only(_manifest())

    assert valid is True
    assert violations == ()


def test_local_static_preview_manifest_validator_blocks_runtime_or_integration_drift():
    unsafe_manifest = replace(
        _manifest(),
        providers_enabled=True,
        mcp_connectors_enabled=True,
        runtime_enabled=True,
        autonomous_action_enabled=True,
        human_approval_required=False,
    )

    valid, violations = validate_manifest_is_static_review_only(unsafe_manifest)

    assert valid is False
    assert "providers must remain disabled" in violations
    assert "MCP connectors must remain disabled" in violations
    assert "runtime must not be enabled" in violations
    assert "autonomous action must remain disabled" in violations
    assert "human approval must remain required" in violations


def test_local_static_preview_manifest_source_has_no_external_execution_or_file_writes():
    source = Path("src/eaios/sprint11/local_static_preview_manifest.py").read_text(
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
