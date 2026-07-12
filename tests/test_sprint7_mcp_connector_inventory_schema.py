from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.mcp_connector_inventory_schema import (
    ConnectorPermissionClass,
    ConnectorRiskTier,
    MCPConnectorInventoryMode,
    build_mcp_connector_inventory_schema,
    summarize_mcp_connector_inventory_schema,
    to_view_model,
)


def _schema():
    return build_mcp_connector_inventory_schema()


def test_mcp_connector_inventory_schema_builds_review_only_schema():
    schema = _schema()

    assert schema.schema_id == "sprint7-mcp-connector-inventory-schema-001"
    assert schema.mode == MCPConnectorInventoryMode.REVIEW_ONLY_INVENTORY_SCHEMA
    assert schema.title == "EAIOS MCP Connector Inventory Schema"
    assert schema.source_provider_validation_id == "sprint7-provider-output-validation-001"
    assert schema.provenance == "mcp_connector_inventory_schema:model"


def test_mcp_connector_inventory_schema_entries_are_declared():
    schema = _schema()

    assert len(schema.entries) == 3

    connector_ids = tuple(entry.connector_id for entry in schema.entries)
    assert connector_ids == (
        "mcp-connector-servicenow-incident-read-001",
        "mcp-connector-observability-alert-read-001",
        "mcp-connector-change-write-001",
    )

    assert all(entry.provenance == "mcp_connector_inventory_schema:entry" for entry in schema.entries)
    assert all(entry.audit_required is True for entry in schema.entries)
    assert all(entry.rollback_or_disable_switch is True for entry in schema.entries)
    assert all(entry.human_review_required is True for entry in schema.entries)


def test_mcp_connector_inventory_schema_permission_and_risk_classes_are_explicit():
    schema = _schema()

    permission_classes = tuple(entry.permission_class for entry in schema.entries)
    risk_tiers = tuple(entry.risk_tier for entry in schema.entries)

    assert permission_classes == (
        ConnectorPermissionClass.READ_ONLY,
        ConnectorPermissionClass.READ_WITH_FILTERED_DATA,
        ConnectorPermissionClass.WRITE_PRODUCTION_BLOCKED,
    )

    assert risk_tiers == (
        ConnectorRiskTier.MEDIUM,
        ConnectorRiskTier.MEDIUM,
        ConnectorRiskTier.BLOCKED,
    )


def test_mcp_connector_inventory_schema_required_fields_are_explicit():
    schema = _schema()

    assert schema.required_fields == (
        "connector_id",
        "connector_name",
        "connector_type",
        "owning_service",
        "service_owner",
        "business_owner",
        "technical_owner",
        "data_domain",
        "data_classification",
        "permission_class",
        "allowed_operations",
        "disallowed_operations",
        "environment_scope",
        "approval_status",
        "risk_tier",
        "audit_required",
        "rollback_or_disable_switch",
        "human_review_required",
        "real_connector_call_performed",
        "external_write_performed",
    )


def test_mcp_connector_inventory_schema_classes_are_complete():
    schema = _schema()

    assert schema.permission_classes == (
        "READ_ONLY",
        "READ_WITH_FILTERED_DATA",
        "READ_WITH_SENSITIVE_DATA",
        "WRITE_NON_PRODUCTION",
        "WRITE_PRODUCTION_REQUIRES_APPROVAL",
        "WRITE_PRODUCTION_BLOCKED",
        "ADMIN_OPERATION_BLOCKED",
    )

    assert "safe_read_operation" in schema.operation_classes
    assert "production_write_operation" in schema.operation_classes
    assert "notification_operation" in schema.operation_classes
    assert "remediation_operation" in schema.operation_classes
    assert "benchmark_scoring_operation" in schema.operation_classes
    assert "benchmark_truth_update_operation" in schema.operation_classes


def test_mcp_connector_inventory_schema_reviews_and_blocks_are_explicit():
    schema = _schema()

    assert schema.required_reviews == (
        "connector_inventory_review",
        "permission_model_review",
        "read_write_classification_review",
        "sandbox_boundary_review",
        "secret_handling_review",
        "network_access_review",
        "audit_trace_review",
        "rollback_disable_switch_review",
        "human_approval_workflow_review",
    )

    assert schema.blocked_actions == (
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


def test_mcp_connector_inventory_schema_preserves_no_execution_boundaries():
    schema = _schema()

    assert schema.schema_built is True
    assert schema.real_connector_calls_performed is False
    assert schema.external_writes_performed is False
    assert schema.production_records_modified is False
    assert schema.infrastructure_changed is False
    assert schema.secrets_loaded is False
    assert schema.network_access_performed is False
    assert schema.remediation_performed is False
    assert schema.notifications_sent is False
    assert schema.benchmark_scoring_performed is False
    assert schema.benchmark_truth_updated is False
    assert schema.autonomous_remediation_allowed is False
    assert schema.human_review_required is True

    for entry in schema.entries:
        assert entry.real_connector_call_performed is False
        assert entry.external_write_performed is False


def test_mcp_connector_inventory_schema_embeds_provider_validation_summary():
    schema = _schema()

    assert schema.provider_validation_summary["validation_id"] == (
        "sprint7-provider-output-validation-001"
    )
    assert schema.provider_validation_summary["mode"] == "REVIEW_ONLY_VALIDATOR"
    assert schema.provider_validation_summary["provider_call_performed"] is False
    assert schema.provider_validation_summary["human_review_required"] is True


def test_mcp_connector_inventory_schema_summary_is_view_ready():
    schema = _schema()

    assert summarize_mcp_connector_inventory_schema(schema) == {
        "schema_id": "sprint7-mcp-connector-inventory-schema-001",
        "mode": "REVIEW_ONLY_INVENTORY_SCHEMA",
        "title": "EAIOS MCP Connector Inventory Schema",
        "source_provider_validation_id": "sprint7-provider-output-validation-001",
        "entry_count": 3,
        "required_field_count": 20,
        "permission_class_count": 7,
        "operation_class_count": 9,
        "required_review_count": 9,
        "blocked_action_count": 12,
        "schema_built": True,
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


def test_mcp_connector_inventory_schema_view_model_is_json_serializable():
    schema = _schema()

    serialized = json.dumps(to_view_model(schema), indent=2)

    assert "sprint7-mcp-connector-inventory-schema-001" in serialized
    assert "ServiceNow Incident Read Connector" in serialized
    assert "WRITE_PRODUCTION_BLOCKED" in serialized
    assert "score_benchmark_from_connector_output" in serialized


def test_mcp_connector_inventory_schema_module_does_not_call_connectors_or_network():
    source = Path("src/eaios/sprint7/mcp_connector_inventory_schema.py").read_text(
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
