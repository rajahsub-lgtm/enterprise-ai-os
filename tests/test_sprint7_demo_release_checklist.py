from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.demo_release_checklist import (
    DemoReleaseChecklistMode,
    DemoReleaseItemStatus,
    DemoReleaseReadinessStatus,
    build_demo_release_checklist,
    summarize_demo_release_checklist,
    to_view_model,
)


def _checklist():
    return build_demo_release_checklist()


def test_demo_release_checklist_builds_review_only_model():
    checklist = _checklist()

    assert checklist.checklist_id == "sprint7-demo-release-checklist-001"
    assert checklist.mode == DemoReleaseChecklistMode.REVIEW_ONLY_RELEASE_CHECKLIST
    assert checklist.readiness_status == (
        DemoReleaseReadinessStatus.BLOCKED_PENDING_RELEASE_APPROVAL
    )
    assert checklist.title == "EAIOS Sprint 7 Demo Release Checklist"
    assert checklist.source_human_approval_workflow_id == (
        "sprint7-human-approval-workflow-001"
    )
    assert checklist.provenance == "demo_release_checklist:model"


def test_demo_release_checklist_items_are_declared():
    checklist = _checklist()

    assert len(checklist.items) == 9

    item_ids = tuple(item.item_id for item in checklist.items)
    assert item_ids == (
        "release-item-001-package-manifest",
        "release-item-002-web-review-surface",
        "release-item-003-cloud-preflight",
        "release-item-004-provider-validator",
        "release-item-005-connector-classifier",
        "release-item-006-audit-envelope",
        "release-item-007-human-approval",
        "release-item-008-benchmark-boundary",
        "release-item-009-release-approval",
    )

    assert all(item.provenance == "demo_release_checklist:item" for item in checklist.items)
    assert all(item.evidence_refs for item in checklist.items)


def test_demo_release_checklist_item_statuses_are_explicit():
    checklist = _checklist()

    statuses = tuple(item.status for item in checklist.items)

    assert statuses == (
        DemoReleaseItemStatus.SATISFIED_BY_DESIGN,
        DemoReleaseItemStatus.SATISFIED_BY_DESIGN,
        DemoReleaseItemStatus.BLOCKING,
        DemoReleaseItemStatus.REQUIRED,
        DemoReleaseItemStatus.REQUIRED,
        DemoReleaseItemStatus.REQUIRED,
        DemoReleaseItemStatus.BLOCKING,
        DemoReleaseItemStatus.REQUIRED,
        DemoReleaseItemStatus.BLOCKING,
    )


def test_demo_release_checklist_required_reviews_are_derived_from_items():
    checklist = _checklist()

    assert checklist.required_reviews == (
        "package_manifest_review",
        "web_review_surface_review",
        "cloud_release_readiness_review",
        "provider_output_validation_review",
        "connector_permission_release_review",
        "audit_trace_release_review",
        "human_approval_release_review",
        "benchmark_truth_release_review",
        "final_release_approval_review",
    )



def test_demo_release_checklist_blocked_actions_are_explicit():
    checklist = _checklist()

    assert checklist.blocked_actions == (
        "create_release_archive",
        "publish_static_site",
        "build_container_image",
        "push_container_image",
        "deploy_to_cloud",
        "enable_real_provider",
        "enable_real_connector",
        "persist_approval_record_to_external_store",
        "execute_approved_action",
        "send_notification",
        "execute_remediation",
        "load_secret_material",
        "access_external_network",
        "score_benchmark_from_release",
        "update_benchmark_truth_from_release",
        "enable_autonomous_remediation",
    )


def test_demo_release_checklist_preserves_no_release_or_execution_boundaries():
    checklist = _checklist()

    assert checklist.checklist_built is True
    assert checklist.release_created is False
    assert checklist.archive_created is False
    assert checklist.static_site_published is False
    assert checklist.container_built is False
    assert checklist.container_pushed is False
    assert checklist.cloud_deployed is False
    assert checklist.provider_enabled is False
    assert checklist.connector_enabled is False
    assert checklist.approval_records_persisted is False
    assert checklist.remediation_performed is False
    assert checklist.notifications_sent is False
    assert checklist.benchmark_scoring_performed is False
    assert checklist.benchmark_truth_updated is False
    assert checklist.autonomous_remediation_allowed is False
    assert checklist.human_review_required is True


def test_demo_release_checklist_embeds_human_approval_workflow_summary():
    checklist = _checklist()

    assert checklist.human_approval_workflow_summary["workflow_id"] == (
        "sprint7-human-approval-workflow-001"
    )
    assert checklist.human_approval_workflow_summary["mode"] == "REVIEW_ONLY_WORKFLOW"
    assert checklist.human_approval_workflow_summary["approvals_granted"] is False
    assert checklist.human_approval_workflow_summary["human_review_required"] is True


def test_demo_release_checklist_summary_is_view_ready():
    checklist = _checklist()

    assert summarize_demo_release_checklist(checklist) == {
        "checklist_id": "sprint7-demo-release-checklist-001",
        "mode": "REVIEW_ONLY_RELEASE_CHECKLIST",
        "readiness_status": "BLOCKED_PENDING_RELEASE_APPROVAL",
        "title": "EAIOS Sprint 7 Demo Release Checklist",
        "source_human_approval_workflow_id": "sprint7-human-approval-workflow-001",
        "item_count": 9,
        "blocking_item_count": 3,
        "required_review_count": 9,
        "blocked_action_count": 16,
        "checklist_built": True,
        "release_created": False,
        "archive_created": False,
        "static_site_published": False,
        "container_built": False,
        "container_pushed": False,
        "cloud_deployed": False,
        "provider_enabled": False,
        "connector_enabled": False,
        "approval_records_persisted": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "benchmark_truth_updated": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_demo_release_checklist_view_model_is_json_serializable():
    checklist = _checklist()

    serialized = json.dumps(to_view_model(checklist), indent=2)

    assert "sprint7-demo-release-checklist-001" in serialized
    assert "BLOCKED_PENDING_RELEASE_APPROVAL" in serialized
    assert "final_release_approval_review" in serialized
    assert "score_benchmark_from_release" in serialized


def test_demo_release_checklist_module_does_not_release_or_call_external_systems():
    source = Path("src/eaios/sprint7/demo_release_checklist.py").read_text(
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
