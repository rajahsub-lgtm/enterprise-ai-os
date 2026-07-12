from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.mcp_connector_permission_classifier import (
    ConnectorPermissionDecision,
    ConnectorPermissionReasonCode,
    MCPConnectorPermissionClassifierMode,
    classify_mcp_connector_permissions,
    summarize_mcp_connector_permission_classifier_report,
    to_view_model,
)


def _report():
    return classify_mcp_connector_permissions()


def test_mcp_connector_permission_classifier_builds_review_only_report():
    report = _report()

    assert report.classifier_id == "sprint7-mcp-connector-permission-classifier-001"
    assert report.mode == MCPConnectorPermissionClassifierMode.REVIEW_ONLY_CLASSIFIER
    assert report.title == "EAIOS MCP Connector Permission Classifier"
    assert report.source_inventory_schema_id == (
        "sprint7-mcp-connector-inventory-schema-001"
    )
    assert report.provenance == "mcp_connector_permission_classifier:report"


def test_mcp_connector_permission_classifier_classifies_inventory_entries():
    report = _report()

    assert len(report.classifications) == 3

    connector_ids = tuple(item.connector_id for item in report.classifications)
    assert connector_ids == (
        "mcp-connector-servicenow-incident-read-001",
        "mcp-connector-observability-alert-read-001",
        "mcp-connector-change-write-001",
    )

    assert all(
        item.provenance == "mcp_connector_permission_classifier:classification"
        for item in report.classifications
    )


def test_mcp_connector_permission_classifier_decisions_are_explicit():
    report = _report()

    decisions = tuple(item.decision for item in report.classifications)

    assert decisions == (
        ConnectorPermissionDecision.ALLOW_READ_ONLY_REVIEW,
        ConnectorPermissionDecision.ALLOW_READ_ONLY_REVIEW,
        ConnectorPermissionDecision.BLOCK_PRODUCTION_WRITE,
    )


def test_mcp_connector_permission_classifier_reason_codes_are_explicit():
    report = _report()

    first, second, third = report.classifications

    assert first.reason_codes == (
        ConnectorPermissionReasonCode.SAFE_READ_ONLY,
        ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
        ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
    )

    assert second.reason_codes == (
        ConnectorPermissionReasonCode.FILTERED_READ_ONLY,
        ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
        ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
    )

    assert third.reason_codes == (
        ConnectorPermissionReasonCode.PRODUCTION_WRITE_BLOCKED,
        ConnectorPermissionReasonCode.WRITE_PERMISSION_BLOCKED,
        ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
        ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
    )


def test_mcp_connector_permission_classifier_read_only_and_blocked_flags_are_correct():
    report = _report()

    first, second, third = report.classifications

    assert first.allowed_for_read_only_review is True
    assert second.allowed_for_read_only_review is True
    assert third.allowed_for_read_only_review is False

    assert first.write_blocked is False
    assert second.write_blocked is False
    assert third.write_blocked is True

    assert first.admin_or_identity_blocked is False
    assert second.admin_or_identity_blocked is False
    assert third.admin_or_identity_blocked is False

    assert first.benchmark_operation_blocked is False
    assert second.benchmark_operation_blocked is False
    assert third.benchmark_operation_blocked is False


def test_mcp_connector_permission_classifier_blocked_actions_are_explicit():
    report = _report()

    assert report.blocked_actions == (
        "call_real_connector",
        "execute_tool_action",
        "perform_external_write",
        "modify_production_record",
        "change_infrastructure",
        "send_notification",
        "load_secret_material",
        "access_external_network",
        "score_benchmark_from_connector_output",
        "update_benchmark_truth_from_connector_output",
        "enable_autonomous_remediation",
        "bypass_human_review",
    )


def test_mcp_connector_permission_classifier_preserves_no_execution_boundaries():
    report = _report()

    assert report.classification_performed is True
    assert report.real_connector_calls_performed is False
    assert report.external_writes_performed is False
    assert report.production_records_modified is False
    assert report.infrastructure_changed is False
    assert report.secrets_loaded is False
    assert report.network_access_performed is False
    assert report.remediation_performed is False
    assert report.notifications_sent is False
    assert report.benchmark_scoring_performed is False
    assert report.benchmark_truth_updated is False
    assert report.autonomous_remediation_allowed is False
    assert report.human_review_required is True

    for item in report.classifications:
        assert item.real_connector_call_performed is False
        assert item.external_write_performed is False
        assert item.human_review_required is True


def test_mcp_connector_permission_classifier_embeds_inventory_summary():
    report = _report()

    assert report.inventory_summary["schema_id"] == (
        "sprint7-mcp-connector-inventory-schema-001"
    )
    assert report.inventory_summary["mode"] == "REVIEW_ONLY_INVENTORY_SCHEMA"
    assert report.inventory_summary["real_connector_calls_performed"] is False
    assert report.inventory_summary["human_review_required"] is True


def test_mcp_connector_permission_classifier_summary_is_view_ready():
    report = _report()

    assert summarize_mcp_connector_permission_classifier_report(report) == {
        "classifier_id": "sprint7-mcp-connector-permission-classifier-001",
        "mode": "REVIEW_ONLY_CLASSIFIER",
        "title": "EAIOS MCP Connector Permission Classifier",
        "source_inventory_schema_id": "sprint7-mcp-connector-inventory-schema-001",
        "classification_count": 3,
        "allowed_for_read_only_review_count": 2,
        "blocked_count": 1,
        "blocked_action_count": 12,
        "classification_performed": True,
        "real_connector_calls_performed": False,
        "external_writes_performed": False,
        "production_records_modified": False,
        "infrastructure_changed": False,
        "secrets_loaded": False,
        "network_access_performed": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "benchmark_truth_updated": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_mcp_connector_permission_classifier_view_model_is_json_serializable():
    report = _report()

    serialized = json.dumps(to_view_model(report), indent=2)

    assert "sprint7-mcp-connector-permission-classifier-001" in serialized
    assert "ALLOW_READ_ONLY_REVIEW" in serialized
    assert "BLOCK_PRODUCTION_WRITE" in serialized
    assert "score_benchmark_from_connector_output" in serialized


def test_mcp_connector_permission_classifier_module_does_not_call_connectors_or_network():
    source = Path("src/eaios/sprint7/mcp_connector_permission_classifier.py").read_text(
        encoding="utf-8"
    ).lower()

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "requests.post" not in source
    assert "httpx.post" not in source
    assert "api_key" not in source
    assert "password" not in source
    assert "bearer " not in source
    assert "curl " not in source
    assert "write_text(" not in source
    assert "mkdir(" not in source
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
