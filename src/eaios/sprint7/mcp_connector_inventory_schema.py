"""Sprint 7 MCP connector inventory schema.

Review-only structured inventory for future MCP connectors.
No connector calls, tool execution, writes, secrets, network access, remediation,
notifications, benchmark scoring, benchmark truth updates, or autonomous action.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint7.provider_output_validator import (
    summarize_provider_output_validation,
    validate_provider_output,
)


class MCPConnectorInventoryMode(str, Enum):
    REVIEW_ONLY_INVENTORY_SCHEMA = "REVIEW_ONLY_INVENTORY_SCHEMA"


class ConnectorRiskTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKED = "BLOCKED"


class ConnectorPermissionClass(str, Enum):
    READ_ONLY = "READ_ONLY"
    READ_WITH_FILTERED_DATA = "READ_WITH_FILTERED_DATA"
    READ_WITH_SENSITIVE_DATA = "READ_WITH_SENSITIVE_DATA"
    WRITE_NON_PRODUCTION = "WRITE_NON_PRODUCTION"
    WRITE_PRODUCTION_REQUIRES_APPROVAL = "WRITE_PRODUCTION_REQUIRES_APPROVAL"
    WRITE_PRODUCTION_BLOCKED = "WRITE_PRODUCTION_BLOCKED"
    ADMIN_OPERATION_BLOCKED = "ADMIN_OPERATION_BLOCKED"


class ConnectorOperationClass(str, Enum):
    SAFE_READ_OPERATION = "safe_read_operation"
    SENSITIVE_READ_OPERATION = "sensitive_read_operation"
    NON_PRODUCTION_WRITE_OPERATION = "non_production_write_operation"
    PRODUCTION_WRITE_OPERATION = "production_write_operation"
    NOTIFICATION_OPERATION = "notification_operation"
    REMEDIATION_OPERATION = "remediation_operation"
    IDENTITY_OR_ACCESS_OPERATION = "identity_or_access_operation"
    BENCHMARK_SCORING_OPERATION = "benchmark_scoring_operation"
    BENCHMARK_TRUTH_UPDATE_OPERATION = "benchmark_truth_update_operation"


@dataclass(frozen=True)
class MCPConnectorInventoryEntry:
    connector_id: str
    connector_name: str
    connector_type: str
    owning_service: str
    service_owner: str
    business_owner: str
    technical_owner: str
    data_domain: str
    data_classification: str
    permission_class: ConnectorPermissionClass
    allowed_operations: tuple[ConnectorOperationClass, ...]
    disallowed_operations: tuple[ConnectorOperationClass, ...]
    environment_scope: str
    approval_status: str
    risk_tier: ConnectorRiskTier
    audit_required: bool
    rollback_or_disable_switch: bool
    human_review_required: bool
    real_connector_call_performed: bool
    external_write_performed: bool
    provenance: str


@dataclass(frozen=True)
class MCPConnectorInventorySchema:
    schema_id: str
    mode: MCPConnectorInventoryMode
    title: str
    source_provider_validation_id: str
    entries: tuple[MCPConnectorInventoryEntry, ...]
    required_fields: tuple[str, ...]
    permission_classes: tuple[str, ...]
    operation_classes: tuple[str, ...]
    required_reviews: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    provider_validation_summary: dict[str, object]
    schema_built: bool
    real_connector_calls_performed: bool
    external_writes_performed: bool
    production_records_modified: bool
    infrastructure_changed: bool
    secrets_loaded: bool
    network_access_performed: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    benchmark_truth_updated: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_mcp_connector_inventory_schema() -> MCPConnectorInventorySchema:
    provider_validation = validate_provider_output(
        {
            "response_id": "provider-response-for-connector-inventory",
            "request_schema_id": "sprint7-provider-request-schema-001",
            "summary": "Connector inventory remains review-only and permission-gated.",
            "evidence_refs": ["docs/EAIOS_2_SPRINT_6_MCP_CONNECTOR_PERMISSION_MODEL.md"],
            "risk_flags": ["connector_calls_disabled"],
            "confidence_statement": "Governance summary only; no connector call performed.",
            "human_review_required": True,
            "blocked_actions": ["call_real_connector", "perform_external_write"],
        }
    )
    provider_summary = summarize_provider_output_validation(provider_validation)

    entries = (
        MCPConnectorInventoryEntry(
            connector_id="mcp-connector-servicenow-incident-read-001",
            connector_name="ServiceNow Incident Read Connector",
            connector_type="ITSM_RECORD_READ",
            owning_service="Incident Management",
            service_owner="service_owner_required",
            business_owner="business_owner_required",
            technical_owner="technical_owner_required",
            data_domain="incident_records",
            data_classification="synthetic_or_approved_internal_metadata",
            permission_class=ConnectorPermissionClass.READ_ONLY,
            allowed_operations=(ConnectorOperationClass.SAFE_READ_OPERATION,),
            disallowed_operations=(
                ConnectorOperationClass.PRODUCTION_WRITE_OPERATION,
                ConnectorOperationClass.NOTIFICATION_OPERATION,
                ConnectorOperationClass.REMEDIATION_OPERATION,
                ConnectorOperationClass.BENCHMARK_SCORING_OPERATION,
                ConnectorOperationClass.BENCHMARK_TRUTH_UPDATE_OPERATION,
            ),
            environment_scope="sandbox_or_read_only_review",
            approval_status="PENDING_CONNECTOR_INVENTORY_REVIEW",
            risk_tier=ConnectorRiskTier.MEDIUM,
            audit_required=True,
            rollback_or_disable_switch=True,
            human_review_required=True,
            real_connector_call_performed=False,
            external_write_performed=False,
            provenance="mcp_connector_inventory_schema:entry",
        ),
        MCPConnectorInventoryEntry(
            connector_id="mcp-connector-observability-alert-read-001",
            connector_name="Observability Alert Read Connector",
            connector_type="OBSERVABILITY_READ",
            owning_service="Application Health Monitoring",
            service_owner="service_owner_required",
            business_owner="business_owner_required",
            technical_owner="technical_owner_required",
            data_domain="alerts_and_telemetry",
            data_classification="synthetic_or_approved_internal_metadata",
            permission_class=ConnectorPermissionClass.READ_WITH_FILTERED_DATA,
            allowed_operations=(ConnectorOperationClass.SAFE_READ_OPERATION,),
            disallowed_operations=(
                ConnectorOperationClass.PRODUCTION_WRITE_OPERATION,
                ConnectorOperationClass.NOTIFICATION_OPERATION,
                ConnectorOperationClass.REMEDIATION_OPERATION,
                ConnectorOperationClass.IDENTITY_OR_ACCESS_OPERATION,
                ConnectorOperationClass.BENCHMARK_SCORING_OPERATION,
                ConnectorOperationClass.BENCHMARK_TRUTH_UPDATE_OPERATION,
            ),
            environment_scope="sandbox_or_read_only_review",
            approval_status="PENDING_CONNECTOR_INVENTORY_REVIEW",
            risk_tier=ConnectorRiskTier.MEDIUM,
            audit_required=True,
            rollback_or_disable_switch=True,
            human_review_required=True,
            real_connector_call_performed=False,
            external_write_performed=False,
            provenance="mcp_connector_inventory_schema:entry",
        ),
        MCPConnectorInventoryEntry(
            connector_id="mcp-connector-change-write-001",
            connector_name="Change Record Write Connector",
            connector_type="ITSM_RECORD_WRITE",
            owning_service="Change Management",
            service_owner="service_owner_required",
            business_owner="business_owner_required",
            technical_owner="technical_owner_required",
            data_domain="change_records",
            data_classification="production_control_metadata",
            permission_class=ConnectorPermissionClass.WRITE_PRODUCTION_BLOCKED,
            allowed_operations=(),
            disallowed_operations=(
                ConnectorOperationClass.NON_PRODUCTION_WRITE_OPERATION,
                ConnectorOperationClass.PRODUCTION_WRITE_OPERATION,
                ConnectorOperationClass.NOTIFICATION_OPERATION,
                ConnectorOperationClass.REMEDIATION_OPERATION,
                ConnectorOperationClass.IDENTITY_OR_ACCESS_OPERATION,
                ConnectorOperationClass.BENCHMARK_SCORING_OPERATION,
                ConnectorOperationClass.BENCHMARK_TRUTH_UPDATE_OPERATION,
            ),
            environment_scope="blocked_until_human_approval_workflow",
            approval_status="BLOCKED_PENDING_PERMISSION_MODEL_REVIEW",
            risk_tier=ConnectorRiskTier.BLOCKED,
            audit_required=True,
            rollback_or_disable_switch=True,
            human_review_required=True,
            real_connector_call_performed=False,
            external_write_performed=False,
            provenance="mcp_connector_inventory_schema:entry",
        ),
    )

    required_fields = (
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

    return MCPConnectorInventorySchema(
        schema_id="sprint7-mcp-connector-inventory-schema-001",
        mode=MCPConnectorInventoryMode.REVIEW_ONLY_INVENTORY_SCHEMA,
        title="EAIOS MCP Connector Inventory Schema",
        source_provider_validation_id=str(provider_summary["validation_id"]),
        entries=entries,
        required_fields=required_fields,
        permission_classes=tuple(item.value for item in ConnectorPermissionClass),
        operation_classes=tuple(item.value for item in ConnectorOperationClass),
        required_reviews=(
            "connector_inventory_review",
            "permission_model_review",
            "read_write_classification_review",
            "sandbox_boundary_review",
            "secret_handling_review",
            "network_access_review",
            "audit_trace_review",
            "rollback_disable_switch_review",
            "human_approval_workflow_review",
        ),
        blocked_actions=(
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
        ),
        provider_validation_summary=provider_summary,
        schema_built=True,
        real_connector_calls_performed=False,
        external_writes_performed=False,
        production_records_modified=False,
        infrastructure_changed=False,
        secrets_loaded=False,
        network_access_performed=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        benchmark_truth_updated=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="mcp_connector_inventory_schema:model",
    )


def summarize_mcp_connector_inventory_schema(
    schema: MCPConnectorInventorySchema,
) -> dict[str, object]:
    return {
        "schema_id": schema.schema_id,
        "mode": schema.mode.value,
        "title": schema.title,
        "source_provider_validation_id": schema.source_provider_validation_id,
        "entry_count": len(schema.entries),
        "required_field_count": len(schema.required_fields),
        "permission_class_count": len(schema.permission_classes),
        "operation_class_count": len(schema.operation_classes),
        "required_review_count": len(schema.required_reviews),
        "blocked_action_count": len(schema.blocked_actions),
        "schema_built": schema.schema_built,
        "real_connector_calls_performed": schema.real_connector_calls_performed,
        "external_writes_performed": schema.external_writes_performed,
        "production_records_modified": schema.production_records_modified,
        "infrastructure_changed": schema.infrastructure_changed,
        "secrets_loaded": schema.secrets_loaded,
        "network_access_performed": schema.network_access_performed,
        "remediation_performed": schema.remediation_performed,
        "notifications_sent": schema.notifications_sent,
        "benchmark_scoring_performed": schema.benchmark_scoring_performed,
        "benchmark_truth_updated": schema.benchmark_truth_updated,
        "autonomous_remediation_allowed": schema.autonomous_remediation_allowed,
        "human_review_required": schema.human_review_required,
    }


def to_view_model(schema: MCPConnectorInventorySchema) -> dict[str, Any]:
    return {
        "summary": summarize_mcp_connector_inventory_schema(schema),
        "entries": [
            {
                "connector_id": entry.connector_id,
                "connector_name": entry.connector_name,
                "connector_type": entry.connector_type,
                "owning_service": entry.owning_service,
                "data_domain": entry.data_domain,
                "data_classification": entry.data_classification,
                "permission_class": entry.permission_class.value,
                "allowed_operations": [item.value for item in entry.allowed_operations],
                "disallowed_operations": [item.value for item in entry.disallowed_operations],
                "environment_scope": entry.environment_scope,
                "approval_status": entry.approval_status,
                "risk_tier": entry.risk_tier.value,
                "audit_required": entry.audit_required,
                "rollback_or_disable_switch": entry.rollback_or_disable_switch,
                "human_review_required": entry.human_review_required,
                "real_connector_call_performed": entry.real_connector_call_performed,
                "external_write_performed": entry.external_write_performed,
                "provenance": entry.provenance,
            }
            for entry in schema.entries
        ],
        "required_fields": list(schema.required_fields),
        "permission_classes": list(schema.permission_classes),
        "operation_classes": list(schema.operation_classes),
        "required_reviews": list(schema.required_reviews),
        "blocked_actions": list(schema.blocked_actions),
        "provider_validation_summary": schema.provider_validation_summary,
        "provenance": schema.provenance,
    }
