from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint11.local_static_preview_generator import (
    LocalStaticPreviewMode,
    LocalStaticPreviewStatus,
    LocalStaticPreviewType,
    build_local_static_preview_generator_contract,
    summarize_local_static_preview_generator_contract,
    to_view_model,
)


def _contract():
    return build_local_static_preview_generator_contract()


def test_local_static_preview_generator_contract_builds():
    contract = _contract()

    assert contract.contract_id == "sprint11-local-static-preview-generator-contract-001"
    assert contract.mode == LocalStaticPreviewMode.LOCAL_CONTRACT_ONLY
    assert contract.status == LocalStaticPreviewStatus.CONTRACT_READY_NOT_MATERIALIZED
    assert contract.preview_type == LocalStaticPreviewType.STATIC_REVIEW_PREVIEW
    assert contract.title == "EAIOS Local Static Preview Generator Contract"
    assert contract.decision == "DO_NOT_DEPLOY_YET"


def test_local_static_preview_generator_contract_sources_are_review_artifacts():
    contract = _contract()

    paths = tuple(source.path for source in contract.source_artifacts)

    assert "README.md" in paths
    assert "docs/EAIOS_2_SPRINT_8_DEMO_STORYBOARD.md" in paths
    assert "docs/EAIOS_2_SPRINT_9_ARCHITECTURE_NARRATIVE.md" in paths
    assert "docs/EAIOS_2_SPRINT_9_REAL_ENTERPRISE_MAPPING.md" in paths
    assert "docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md" in paths
    assert "docs/EAIOS_2_SPRINT_10_STATIC_PREVIEW_DECISION_RECORD.md" in paths
    assert all(source.required is True for source in contract.source_artifacts)


def test_local_static_preview_generator_contract_plans_artifacts_without_materializing():
    contract = _contract()

    outputs = tuple(artifact.output_path for artifact in contract.planned_artifacts)

    assert "preview/index.html" in outputs
    assert "preview/architecture.html" in outputs
    assert "preview/demo-storyboard.html" in outputs
    assert "preview/real-enterprise-mapping.html" in outputs
    assert "preview/interview-qa.html" in outputs
    assert "preview/manifest.json" in outputs
    assert all(artifact.materialized is False for artifact in contract.planned_artifacts)


def test_local_static_preview_manifest_contract_preserves_disabled_state():
    manifest = _contract().manifest_contract

    assert manifest.preview_id == "eaios-local-static-preview-contract-001"
    assert manifest.preview_type == LocalStaticPreviewType.STATIC_REVIEW_PREVIEW
    assert manifest.mode == LocalStaticPreviewMode.LOCAL_CONTRACT_ONLY
    assert manifest.providers_enabled is False
    assert manifest.provider_runtime_enabled is False
    assert manifest.provider_credentials_present is False
    assert manifest.provider_invocation_allowed is False
    assert manifest.mcp_connectors_enabled is False
    assert manifest.connector_runtime_enabled is False
    assert manifest.connector_credentials_present is False
    assert manifest.connector_invocation_allowed is False
    assert manifest.human_approval_required is True
    assert manifest.rollback_required is True



def test_local_static_preview_generator_contract_blocks_cloud_runtime_and_integrations():
    contract = _contract()

    for expected in [
        "materialize_preview_files",
        "publish_static_site",
        "deploy_to_cloud",
        "create_cloud_resources",
        "create_iam_roles",
        "create_service_accounts",
        "configure_billing",
        "start_runtime",
        "start_server",
        "open_browser",
        "call_provider",
        "call_mcp_connector",
        "load_secrets",
        "read_production_data",
        "write_production_records",
        "send_notifications",
        "execute_remediation",
        "mutate_benchmark_truth",
        "approve_release",
        "enable_autonomous_action",
    ]:
        assert expected in contract.blocked_actions


def test_local_static_preview_generator_contract_allows_only_review_planning():
    contract = _contract()

    assert contract.allowed_actions == (
        "read_approved_repository_docs",
        "plan_local_static_artifacts",
        "build_disabled_state_manifest_contract",
        "validate_no_cloud_scope",
    )


def test_local_static_preview_generator_contract_summary_is_safe():
    summary = summarize_local_static_preview_generator_contract(_contract())

    assert summary["contract_id"] == "sprint11-local-static-preview-generator-contract-001"
    assert summary["mode"] == "LOCAL_CONTRACT_ONLY"
    assert summary["status"] == "CONTRACT_READY_NOT_MATERIALIZED"
    assert summary["preview_type"] == "STATIC_REVIEW_PREVIEW"
    assert summary["source_artifact_count"] == 6
    assert summary["planned_artifact_count"] == 6
    assert summary["cloud_deployment_approved"] is False
    assert summary["static_preview_approved"] is False
    assert summary["implementation_approved"] is False
    assert summary["files_materialized"] is False
    assert summary["providers_enabled"] is False
    assert summary["mcp_connectors_enabled"] is False
    assert summary["production_data_used"] is False
    assert summary["secrets_required"] is False
    assert summary["decision"] == "DO_NOT_DEPLOY_YET"


def test_local_static_preview_generator_view_model_is_json_serializable():
    view_model = to_view_model(_contract())
    serialized = json.dumps(view_model, indent=2, default=str)

    assert "sprint11-local-static-preview-generator-contract-001" in serialized
    assert "STATIC_REVIEW_PREVIEW" in serialized
    assert "DO_NOT_DEPLOY_YET" in serialized
    assert "deploy_to_cloud" in serialized
    assert "providers_enabled" in serialized
    assert "mcp_connectors_enabled" in serialized


def test_local_static_preview_generator_contract_does_not_create_side_effects():
    contract = _contract()

    assert contract.cloud_deployment_approved is False
    assert contract.static_preview_approved is False
    assert contract.implementation_approved is False
    assert contract.files_materialized is False
    assert contract.cloud_resources_created is False
    assert contract.runtime_started is False
    assert contract.server_started is False
    assert contract.browser_opened is False
    assert contract.providers_enabled is False
    assert contract.mcp_connectors_enabled is False
    assert contract.production_data_used is False
    assert contract.secrets_required is False
    assert contract.writes_enabled is False
    assert contract.notifications_enabled is False
    assert contract.remediation_enabled is False
    assert contract.benchmark_truth_mutation_enabled is False
    assert contract.autonomous_action_enabled is False
    assert contract.human_approval_required is True


def test_local_static_preview_generator_source_has_no_external_execution_or_file_writes():
    source = Path("src/eaios/sprint11/local_static_preview_generator.py").read_text(
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
