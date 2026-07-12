"""Sprint 7 demo release checklist.

Review-only release checklist for the EAIOS portfolio demo.

It does not create a release, create an archive, publish a site, build a
container, deploy cloud resources, enable providers, enable connectors, persist
approvals, send notifications, execute remediation, score benchmarks, update
benchmark truth, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint7.human_approval_workflow import (
    build_human_approval_workflow,
    summarize_human_approval_workflow,
)


class DemoReleaseChecklistMode(str, Enum):
    REVIEW_ONLY_RELEASE_CHECKLIST = "REVIEW_ONLY_RELEASE_CHECKLIST"


class DemoReleaseReadinessStatus(str, Enum):
    BLOCKED_PENDING_RELEASE_APPROVAL = "BLOCKED_PENDING_RELEASE_APPROVAL"


class DemoReleaseItemStatus(str, Enum):
    SATISFIED_BY_DESIGN = "SATISFIED_BY_DESIGN"
    REQUIRED = "REQUIRED"
    BLOCKING = "BLOCKING"


class DemoReleaseItemCategory(str, Enum):
    PACKAGE = "PACKAGE"
    WEB_REVIEW = "WEB_REVIEW"
    CLOUD = "CLOUD"
    PROVIDER = "PROVIDER"
    CONNECTOR = "CONNECTOR"
    AUDIT = "AUDIT"
    APPROVAL = "APPROVAL"
    BENCHMARK = "BENCHMARK"
    SAFETY = "SAFETY"


@dataclass(frozen=True)
class DemoReleaseChecklistItem:
    item_id: str
    category: DemoReleaseItemCategory
    name: str
    status: DemoReleaseItemStatus
    evidence_refs: tuple[str, ...]
    blocking_reason: str
    required_review: str
    provenance: str


@dataclass(frozen=True)
class DemoReleaseChecklist:
    checklist_id: str
    mode: DemoReleaseChecklistMode
    readiness_status: DemoReleaseReadinessStatus
    title: str
    source_human_approval_workflow_id: str
    items: tuple[DemoReleaseChecklistItem, ...]
    required_reviews: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    human_approval_workflow_summary: dict[str, object]
    checklist_built: bool
    release_created: bool
    archive_created: bool
    static_site_published: bool
    container_built: bool
    container_pushed: bool
    cloud_deployed: bool
    provider_enabled: bool
    connector_enabled: bool
    approval_records_persisted: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    benchmark_truth_updated: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_demo_release_checklist() -> DemoReleaseChecklist:
    workflow = build_human_approval_workflow()
    workflow_summary = summarize_human_approval_workflow(workflow)

    items = (
        DemoReleaseChecklistItem(
            item_id="release-item-001-package-manifest",
            category=DemoReleaseItemCategory.PACKAGE,
            name="Local package manifest reviewed",
            status=DemoReleaseItemStatus.SATISFIED_BY_DESIGN,
            evidence_refs=("src/eaios/sprint6/demo_package.py",),
            blocking_reason="Package is manifest-only and does not write release artifacts.",
            required_review="package_manifest_review",
            provenance="demo_release_checklist:item",
        ),
        DemoReleaseChecklistItem(
            item_id="release-item-002-web-review-surface",
            category=DemoReleaseItemCategory.WEB_REVIEW,
            name="Local web review surface modeled",
            status=DemoReleaseItemStatus.SATISFIED_BY_DESIGN,
            evidence_refs=("src/eaios/sprint7/local_web_review_surface.py",),
            blocking_reason="Surface is model-only and no server or browser is started.",
            required_review="web_review_surface_review",
            provenance="demo_release_checklist:item",
        ),
        DemoReleaseChecklistItem(
            item_id="release-item-003-cloud-preflight",
            category=DemoReleaseItemCategory.CLOUD,
            name="Cloud deployment preflight remains blocked",
            status=DemoReleaseItemStatus.BLOCKING,
            evidence_refs=("src/eaios/sprint7/cloud_deploy_preflight.py",),
            blocking_reason="Cloud deployment remains blocked pending architecture, secret, provider, and connector reviews.",
            required_review="cloud_release_readiness_review",
            provenance="demo_release_checklist:item",
        ),
        DemoReleaseChecklistItem(
            item_id="release-item-004-provider-validator",
            category=DemoReleaseItemCategory.PROVIDER,
            name="Provider output validator available",
            status=DemoReleaseItemStatus.REQUIRED,
            evidence_refs=("src/eaios/sprint7/provider_output_validator.py",),
            blocking_reason="Provider output is not accepted without validation and human review.",
            required_review="provider_output_validation_review",
            provenance="demo_release_checklist:item",
        ),
        DemoReleaseChecklistItem(
            item_id="release-item-005-connector-classifier",
            category=DemoReleaseItemCategory.CONNECTOR,
            name="MCP connector permissions classified",
            status=DemoReleaseItemStatus.REQUIRED,
            evidence_refs=("src/eaios/sprint7/mcp_connector_permission_classifier.py",),
            blocking_reason="Real connector calls remain disabled by default.",
            required_review="connector_permission_release_review",
            provenance="demo_release_checklist:item",
        ),
    )

    items = items + (
        DemoReleaseChecklistItem(
            item_id="release-item-006-audit-envelope",
            category=DemoReleaseItemCategory.AUDIT,
            name="Audit event envelope modeled",
            status=DemoReleaseItemStatus.REQUIRED,
            evidence_refs=("src/eaios/sprint7/audit_event_envelope.py",),
            blocking_reason="Audit events are not persisted to an external store.",
            required_review="audit_trace_release_review",
            provenance="demo_release_checklist:item",
        ),
        DemoReleaseChecklistItem(
            item_id="release-item-007-human-approval",
            category=DemoReleaseItemCategory.APPROVAL,
            name="Human approval workflow remains pending",
            status=DemoReleaseItemStatus.BLOCKING,
            evidence_refs=("src/eaios/sprint7/human_approval_workflow.py",),
            blocking_reason="No approval records are persisted and no actions are approved.",
            required_review="human_approval_release_review",
            provenance="demo_release_checklist:item",
        ),
        DemoReleaseChecklistItem(
            item_id="release-item-008-benchmark-boundary",
            category=DemoReleaseItemCategory.BENCHMARK,
            name="Benchmark truth isolation preserved",
            status=DemoReleaseItemStatus.REQUIRED,
            evidence_refs=("docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",),
            blocking_reason="Runtime, provider, connector, audit, and release output must not define benchmark truth.",
            required_review="benchmark_truth_release_review",
            provenance="demo_release_checklist:item",
        ),
        DemoReleaseChecklistItem(
            item_id="release-item-009-release-approval",
            category=DemoReleaseItemCategory.SAFETY,
            name="Release approval required",
            status=DemoReleaseItemStatus.BLOCKING,
            evidence_refs=("src/eaios/sprint7/human_approval_workflow.py",),
            blocking_reason="A release cannot be created without explicit human approval.",
            required_review="final_release_approval_review",
            provenance="demo_release_checklist:item",
        ),
    )

    return DemoReleaseChecklist(
        checklist_id="sprint7-demo-release-checklist-001",
        mode=DemoReleaseChecklistMode.REVIEW_ONLY_RELEASE_CHECKLIST,
        readiness_status=DemoReleaseReadinessStatus.BLOCKED_PENDING_RELEASE_APPROVAL,
        title="EAIOS Sprint 7 Demo Release Checklist",
        source_human_approval_workflow_id=str(workflow_summary["workflow_id"]),
        items=items,
        required_reviews=tuple(item.required_review for item in items),
        blocked_actions=(
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
        ),
        human_approval_workflow_summary=workflow_summary,
        checklist_built=True,
        release_created=False,
        archive_created=False,
        static_site_published=False,
        container_built=False,
        container_pushed=False,
        cloud_deployed=False,
        provider_enabled=False,
        connector_enabled=False,
        approval_records_persisted=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        benchmark_truth_updated=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="demo_release_checklist:model",
    )


def summarize_demo_release_checklist(
    checklist: DemoReleaseChecklist,
) -> dict[str, object]:
    blocking_count = sum(
        1 for item in checklist.items if item.status == DemoReleaseItemStatus.BLOCKING
    )

    return {
        "checklist_id": checklist.checklist_id,
        "mode": checklist.mode.value,
        "readiness_status": checklist.readiness_status.value,
        "title": checklist.title,
        "source_human_approval_workflow_id": checklist.source_human_approval_workflow_id,
        "item_count": len(checklist.items),
        "blocking_item_count": blocking_count,
        "required_review_count": len(checklist.required_reviews),
        "blocked_action_count": len(checklist.blocked_actions),
        "checklist_built": checklist.checklist_built,
        "release_created": checklist.release_created,
        "archive_created": checklist.archive_created,
        "static_site_published": checklist.static_site_published,
        "container_built": checklist.container_built,
        "container_pushed": checklist.container_pushed,
        "cloud_deployed": checklist.cloud_deployed,
        "provider_enabled": checklist.provider_enabled,
        "connector_enabled": checklist.connector_enabled,
        "approval_records_persisted": checklist.approval_records_persisted,
        "remediation_performed": checklist.remediation_performed,
        "notifications_sent": checklist.notifications_sent,
        "benchmark_scoring_performed": checklist.benchmark_scoring_performed,
        "benchmark_truth_updated": checklist.benchmark_truth_updated,
        "autonomous_remediation_allowed": checklist.autonomous_remediation_allowed,
        "human_review_required": checklist.human_review_required,
    }


def to_view_model(checklist: DemoReleaseChecklist) -> dict[str, Any]:
    return {
        "summary": summarize_demo_release_checklist(checklist),
        "items": [
            {
                "item_id": item.item_id,
                "category": item.category.value,
                "name": item.name,
                "status": item.status.value,
                "evidence_refs": list(item.evidence_refs),
                "blocking_reason": item.blocking_reason,
                "required_review": item.required_review,
                "provenance": item.provenance,
            }
            for item in checklist.items
        ],
        "required_reviews": list(checklist.required_reviews),
        "blocked_actions": list(checklist.blocked_actions),
        "human_approval_workflow_summary": checklist.human_approval_workflow_summary,
        "provenance": checklist.provenance,
    }
