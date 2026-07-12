from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.human_approval_workflow import (
    ApprovalActionCategory,
    ApprovalRequestStatus,
    ApprovalRiskLevel,
    HumanApprovalWorkflowMode,
    build_human_approval_workflow,
    summarize_human_approval_workflow,
    to_view_model,
)


def _workflow():
    return build_human_approval_workflow()


def test_human_approval_workflow_builds_review_only_model():
    workflow = _workflow()

    assert workflow.workflow_id == "sprint7-human-approval-workflow-001"
    assert workflow.mode == HumanApprovalWorkflowMode.REVIEW_ONLY_WORKFLOW
    assert workflow.title == "EAIOS Sprint 7 Human Approval Workflow"
    assert workflow.source_audit_envelope_id == "sprint7-audit-event-envelope-001"
    assert workflow.provenance == "human_approval_workflow:model"


def test_human_approval_workflow_creates_requests_from_review_events():
    workflow = _workflow()

    assert len(workflow.requests) == 3

    assert tuple(request.request_id for request in workflow.requests) == (
        "human-approval-request-001",
        "human-approval-request-002",
        "human-approval-request-003",
    )

    assert tuple(request.source_event_id for request in workflow.requests) == (
        "audit-event-001-governance-boundary",
        "audit-event-004-mcp-connector-change-write-001",
        "audit-event-999-human-review-required",
    )

    assert all(
        request.provenance == "human_approval_workflow:request"
        for request in workflow.requests
    )
    assert all(request.human_review_required is True for request in workflow.requests)


def test_human_approval_workflow_statuses_and_risk_levels_are_explicit():
    workflow = _workflow()

    assert tuple(request.status for request in workflow.requests) == (
        ApprovalRequestStatus.PENDING_HUMAN_REVIEW,
        ApprovalRequestStatus.BLOCKED_UNTIL_APPROVED,
        ApprovalRequestStatus.PENDING_HUMAN_REVIEW,
    )

    assert tuple(request.risk_level for request in workflow.requests) == (
        ApprovalRiskLevel.HIGH,
        ApprovalRiskLevel.BLOCKING,
        ApprovalRiskLevel.HIGH,
    )


def test_human_approval_workflow_action_categories_and_approvers_are_explicit():
    workflow = _workflow()

    assert tuple(request.action_category for request in workflow.requests) == (
        ApprovalActionCategory.GOVERNANCE_REVIEW,
        ApprovalActionCategory.CONNECTOR_WRITE_REVIEW,
        ApprovalActionCategory.HUMAN_REVIEW_BOUNDARY,
    )

    assert tuple(request.required_approvers for request in workflow.requests) == (
        ("governance_reviewer", "architecture_owner"),
        ("service_owner", "technical_owner", "governance_reviewer"),
        ("governance_reviewer", "risk_owner"),
    )



def test_human_approval_workflow_requests_are_not_approved_or_executed():
    workflow = _workflow()

    for request in workflow.requests:
        assert request.approved is False
        assert request.rejected is False
        assert request.expired is False
        assert request.action_executed is False
        assert request.evidence_refs
        assert request.blocked_actions


def test_human_approval_workflow_decision_policy_is_explicit():
    workflow = _workflow()

    assert workflow.decision_policy == (
        "human_approval_required_for_write_operations",
        "human_approval_required_for_remediation",
        "human_approval_required_for_notifications",
        "human_approval_required_for_benchmark_scoring",
        "human_approval_required_for_benchmark_truth_updates",
        "human_approval_required_for_connector_enablement",
        "human_approval_required_for_provider_output_acceptance",
        "human_approval_required_for_cloud_deployment",
    )


def test_human_approval_workflow_reviews_and_blocks_are_explicit():
    workflow = _workflow()

    assert workflow.required_reviews == (
        "approval_workflow_schema_review",
        "segregation_of_duties_review",
        "risk_acceptance_review",
        "audit_trace_review",
        "rollback_disable_switch_review",
        "benchmark_truth_isolation_review",
    )

    assert workflow.blocked_actions == (
        "approve_without_human",
        "reject_without_human",
        "persist_approval_record_to_external_store",
        "execute_approved_action",
        "call_real_connector",
        "execute_tool_action",
        "perform_external_write",
        "modify_production_record",
        "change_infrastructure",
        "send_notification",
        "load_secret_material",
        "access_external_network",
        "score_benchmark_from_approval",
        "update_benchmark_truth_from_approval",
        "enable_autonomous_remediation",
        "bypass_human_review",
    )


def test_human_approval_workflow_preserves_no_execution_boundaries():
    workflow = _workflow()

    assert workflow.workflow_built is True
    assert workflow.approval_records_persisted is False
    assert workflow.approvals_granted is False
    assert workflow.rejections_recorded is False
    assert workflow.actions_executed is False
    assert workflow.real_connector_calls_performed is False
    assert workflow.external_writes_performed is False
    assert workflow.production_records_modified is False
    assert workflow.infrastructure_changed is False
    assert workflow.secrets_loaded is False
    assert workflow.network_access_performed is False
    assert workflow.remediation_performed is False
    assert workflow.notifications_sent is False
    assert workflow.benchmark_scoring_performed is False
    assert workflow.benchmark_truth_updated is False
    assert workflow.autonomous_remediation_allowed is False
    assert workflow.human_review_required is True



def test_human_approval_workflow_embeds_audit_envelope_summary():
    workflow = _workflow()

    assert workflow.audit_envelope_summary["envelope_id"] == (
        "sprint7-audit-event-envelope-001"
    )
    assert workflow.audit_envelope_summary["mode"] == "REVIEW_ONLY_AUDIT_ENVELOPE"
    assert workflow.audit_envelope_summary["audit_events_persisted"] is False
    assert workflow.audit_envelope_summary["human_review_required"] is True


def test_human_approval_workflow_summary_is_view_ready():
    workflow = _workflow()

    assert summarize_human_approval_workflow(workflow) == {
        "workflow_id": "sprint7-human-approval-workflow-001",
        "mode": "REVIEW_ONLY_WORKFLOW",
        "title": "EAIOS Sprint 7 Human Approval Workflow",
        "source_audit_envelope_id": "sprint7-audit-event-envelope-001",
        "request_count": 3,
        "blocking_request_count": 1,
        "decision_policy_count": 8,
        "required_review_count": 6,
        "blocked_action_count": 16,
        "workflow_built": True,
        "approval_records_persisted": False,
        "approvals_granted": False,
        "rejections_recorded": False,
        "actions_executed": False,
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


def test_human_approval_workflow_view_model_is_json_serializable():
    workflow = _workflow()

    serialized = json.dumps(to_view_model(workflow), indent=2)

    assert "sprint7-human-approval-workflow-001" in serialized
    assert "PENDING_HUMAN_REVIEW" in serialized
    assert "BLOCKED_UNTIL_APPROVED" in serialized
    assert "score_benchmark_from_approval" in serialized


def test_human_approval_workflow_module_does_not_approve_or_call_external_systems():
    source = Path("src/eaios/sprint7/human_approval_workflow.py").read_text(
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
