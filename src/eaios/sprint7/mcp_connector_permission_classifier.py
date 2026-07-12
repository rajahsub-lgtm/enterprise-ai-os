"""Sprint 7 MCP connector permission classifier.

Review-only classifier for MCP connector inventory entries.

It does not call connectors, execute tools, perform writes, load secrets, access
external networks, execute remediation, send notifications, score benchmarks,
update benchmark truth, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint7.mcp_connector_inventory_schema import (
    ConnectorOperationClass,
    ConnectorPermissionClass,
    MCPConnectorInventoryEntry,
    MCPConnectorInventorySchema,
    build_mcp_connector_inventory_schema,
    summarize_mcp_connector_inventory_schema,
)


class MCPConnectorPermissionClassifierMode(str, Enum):
    REVIEW_ONLY_CLASSIFIER = "REVIEW_ONLY_CLASSIFIER"


class ConnectorPermissionDecision(str, Enum):
    ALLOW_READ_ONLY_REVIEW = "ALLOW_READ_ONLY_REVIEW"
    BLOCK_SENSITIVE_READ_PENDING_REVIEW = "BLOCK_SENSITIVE_READ_PENDING_REVIEW"
    BLOCK_WRITE_PENDING_APPROVAL = "BLOCK_WRITE_PENDING_APPROVAL"
    BLOCK_PRODUCTION_WRITE = "BLOCK_PRODUCTION_WRITE"
    BLOCK_ADMIN_OR_IDENTITY = "BLOCK_ADMIN_OR_IDENTITY"
    BLOCK_BENCHMARK_OPERATION = "BLOCK_BENCHMARK_OPERATION"


class ConnectorPermissionReasonCode(str, Enum):
    SAFE_READ_ONLY = "SAFE_READ_ONLY"
    FILTERED_READ_ONLY = "FILTERED_READ_ONLY"
    SENSITIVE_READ_REQUIRES_REVIEW = "SENSITIVE_READ_REQUIRES_REVIEW"
    WRITE_PERMISSION_BLOCKED = "WRITE_PERMISSION_BLOCKED"
    PRODUCTION_WRITE_BLOCKED = "PRODUCTION_WRITE_BLOCKED"
    ADMIN_OPERATION_BLOCKED = "ADMIN_OPERATION_BLOCKED"
    BENCHMARK_OPERATION_BLOCKED = "BENCHMARK_OPERATION_BLOCKED"
    CONNECTOR_CALL_DISABLED = "CONNECTOR_CALL_DISABLED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


@dataclass(frozen=True)
class ConnectorPermissionClassification:
    classification_id: str
    connector_id: str
    connector_name: str
    permission_class: str
    risk_tier: str
    decision: ConnectorPermissionDecision
    reason_codes: tuple[ConnectorPermissionReasonCode, ...]
    allowed_for_read_only_review: bool
    write_blocked: bool
    admin_or_identity_blocked: bool
    benchmark_operation_blocked: bool
    real_connector_call_performed: bool
    external_write_performed: bool
    human_review_required: bool
    provenance: str


@dataclass(frozen=True)
class MCPConnectorPermissionClassifierReport:
    classifier_id: str
    mode: MCPConnectorPermissionClassifierMode
    title: str
    source_inventory_schema_id: str
    classifications: tuple[ConnectorPermissionClassification, ...]
    blocked_actions: tuple[str, ...]
    inventory_summary: dict[str, object]
    classification_performed: bool
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


def classify_mcp_connector_permissions(
    schema: MCPConnectorInventorySchema | None = None,
) -> MCPConnectorPermissionClassifierReport:
    inventory_schema = schema or build_mcp_connector_inventory_schema()
    inventory_summary = summarize_mcp_connector_inventory_schema(inventory_schema)

    classifications = tuple(
        _classify_entry(entry=entry, index=index)
        for index, entry in enumerate(inventory_schema.entries, start=1)
    )

    return MCPConnectorPermissionClassifierReport(
        classifier_id="sprint7-mcp-connector-permission-classifier-001",
        mode=MCPConnectorPermissionClassifierMode.REVIEW_ONLY_CLASSIFIER,
        title="EAIOS MCP Connector Permission Classifier",
        source_inventory_schema_id=inventory_schema.schema_id,
        classifications=classifications,
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
        inventory_summary=inventory_summary,
        classification_performed=True,
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
        provenance="mcp_connector_permission_classifier:report",
    )


def summarize_mcp_connector_permission_classifier_report(
    report: MCPConnectorPermissionClassifierReport,
) -> dict[str, object]:
    allowed_count = sum(
        1 for item in report.classifications if item.allowed_for_read_only_review
    )

    return {
        "classifier_id": report.classifier_id,
        "mode": report.mode.value,
        "title": report.title,
        "source_inventory_schema_id": report.source_inventory_schema_id,
        "classification_count": len(report.classifications),
        "allowed_for_read_only_review_count": allowed_count,
        "blocked_count": len(report.classifications) - allowed_count,
        "blocked_action_count": len(report.blocked_actions),
        "classification_performed": report.classification_performed,
        "real_connector_calls_performed": report.real_connector_calls_performed,
        "external_writes_performed": report.external_writes_performed,
        "production_records_modified": report.production_records_modified,
        "infrastructure_changed": report.infrastructure_changed,
        "secrets_loaded": report.secrets_loaded,
        "network_access_performed": report.network_access_performed,
        "remediation_performed": report.remediation_performed,
        "notifications_sent": report.notifications_sent,
        "benchmark_scoring_performed": report.benchmark_scoring_performed,
        "benchmark_truth_updated": report.benchmark_truth_updated,
        "autonomous_remediation_allowed": report.autonomous_remediation_allowed,
        "human_review_required": report.human_review_required,
    }


def to_view_model(report: MCPConnectorPermissionClassifierReport) -> dict[str, Any]:
    return {
        "summary": summarize_mcp_connector_permission_classifier_report(report),
        "classifications": [
            {
                "classification_id": item.classification_id,
                "connector_id": item.connector_id,
                "connector_name": item.connector_name,
                "permission_class": item.permission_class,
                "risk_tier": item.risk_tier,
                "decision": item.decision.value,
                "reason_codes": [reason.value for reason in item.reason_codes],
                "allowed_for_read_only_review": item.allowed_for_read_only_review,
                "write_blocked": item.write_blocked,
                "admin_or_identity_blocked": item.admin_or_identity_blocked,
                "benchmark_operation_blocked": item.benchmark_operation_blocked,
                "real_connector_call_performed": item.real_connector_call_performed,
                "external_write_performed": item.external_write_performed,
                "human_review_required": item.human_review_required,
                "provenance": item.provenance,
            }
            for item in report.classifications
        ],
        "blocked_actions": list(report.blocked_actions),
        "inventory_summary": report.inventory_summary,
        "provenance": report.provenance,
    }


def _classify_entry(
    entry: MCPConnectorInventoryEntry,
    index: int,
) -> ConnectorPermissionClassification:
    allowed_operations = set(entry.allowed_operations)
    permission_class = entry.permission_class

    decision = ConnectorPermissionDecision.BLOCK_WRITE_PENDING_APPROVAL
    reason_codes: tuple[ConnectorPermissionReasonCode, ...] = (
        ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
        ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
    )

    if _has_benchmark_operation(allowed_operations):
        decision = ConnectorPermissionDecision.BLOCK_BENCHMARK_OPERATION
        reason_codes = (
            ConnectorPermissionReasonCode.BENCHMARK_OPERATION_BLOCKED,
            ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
            ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
        )
    elif ConnectorOperationClass.IDENTITY_OR_ACCESS_OPERATION in allowed_operations:
        decision = ConnectorPermissionDecision.BLOCK_ADMIN_OR_IDENTITY
        reason_codes = (
            ConnectorPermissionReasonCode.ADMIN_OPERATION_BLOCKED,
            ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
            ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
        )
    elif permission_class == ConnectorPermissionClass.ADMIN_OPERATION_BLOCKED:
        decision = ConnectorPermissionDecision.BLOCK_ADMIN_OR_IDENTITY
        reason_codes = (
            ConnectorPermissionReasonCode.ADMIN_OPERATION_BLOCKED,
            ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
            ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
        )
    elif permission_class == ConnectorPermissionClass.WRITE_PRODUCTION_BLOCKED:
        decision = ConnectorPermissionDecision.BLOCK_PRODUCTION_WRITE
        reason_codes = (
            ConnectorPermissionReasonCode.PRODUCTION_WRITE_BLOCKED,
            ConnectorPermissionReasonCode.WRITE_PERMISSION_BLOCKED,
            ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
            ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
        )
    elif permission_class in {
        ConnectorPermissionClass.WRITE_NON_PRODUCTION,
        ConnectorPermissionClass.WRITE_PRODUCTION_REQUIRES_APPROVAL,
    }:
        decision = ConnectorPermissionDecision.BLOCK_WRITE_PENDING_APPROVAL
        reason_codes = (
            ConnectorPermissionReasonCode.WRITE_PERMISSION_BLOCKED,
            ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
            ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
        )
    elif permission_class == ConnectorPermissionClass.READ_WITH_SENSITIVE_DATA:
        decision = ConnectorPermissionDecision.BLOCK_SENSITIVE_READ_PENDING_REVIEW
        reason_codes = (
            ConnectorPermissionReasonCode.SENSITIVE_READ_REQUIRES_REVIEW,
            ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
            ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
        )
    elif permission_class == ConnectorPermissionClass.READ_WITH_FILTERED_DATA:
        decision = ConnectorPermissionDecision.ALLOW_READ_ONLY_REVIEW
        reason_codes = (
            ConnectorPermissionReasonCode.FILTERED_READ_ONLY,
            ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
            ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
        )
    elif permission_class == ConnectorPermissionClass.READ_ONLY:
        decision = ConnectorPermissionDecision.ALLOW_READ_ONLY_REVIEW
        reason_codes = (
            ConnectorPermissionReasonCode.SAFE_READ_ONLY,
            ConnectorPermissionReasonCode.CONNECTOR_CALL_DISABLED,
            ConnectorPermissionReasonCode.HUMAN_REVIEW_REQUIRED,
        )

    return ConnectorPermissionClassification(
        classification_id=f"mcp-connector-permission-classification-{index:03d}",
        connector_id=entry.connector_id,
        connector_name=entry.connector_name,
        permission_class=entry.permission_class.value,
        risk_tier=entry.risk_tier.value,
        decision=decision,
        reason_codes=reason_codes,
        allowed_for_read_only_review=decision == ConnectorPermissionDecision.ALLOW_READ_ONLY_REVIEW,
        write_blocked=decision
        in {
            ConnectorPermissionDecision.BLOCK_WRITE_PENDING_APPROVAL,
            ConnectorPermissionDecision.BLOCK_PRODUCTION_WRITE,
        },
        admin_or_identity_blocked=decision
        == ConnectorPermissionDecision.BLOCK_ADMIN_OR_IDENTITY,
        benchmark_operation_blocked=decision
        == ConnectorPermissionDecision.BLOCK_BENCHMARK_OPERATION,
        real_connector_call_performed=False,
        external_write_performed=False,
        human_review_required=True,
        provenance="mcp_connector_permission_classifier:classification",
    )


def _has_benchmark_operation(
    operations: set[ConnectorOperationClass],
) -> bool:
    return bool(
        {
            ConnectorOperationClass.BENCHMARK_SCORING_OPERATION,
            ConnectorOperationClass.BENCHMARK_TRUTH_UPDATE_OPERATION,
        }
        & operations
    )
