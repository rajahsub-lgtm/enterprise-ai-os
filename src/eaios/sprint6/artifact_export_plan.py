"""Sprint 6 dry-run artifact export plan.

This module defines the portfolio export folder plan without writing files.

It does not copy files, create folders, run shell commands, deploy cloud
resources, load secrets, call providers, connect real tools, execute
remediation, send notifications, score benchmarks, or enable autonomous
remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint6.demo_package import (
    DemoPackageManifest,
    build_demo_package_manifest,
    summarize_demo_package_manifest,
)


class ExportPlanMode(str, Enum):
    DRY_RUN_ONLY = "DRY_RUN_ONLY"


class ExportArtifactState(str, Enum):
    PLANNED_NOT_WRITTEN = "PLANNED_NOT_WRITTEN"


@dataclass(frozen=True)
class ExportArtifactPlan:
    plan_id: str
    source_path: str
    export_path: str
    section: str
    state: ExportArtifactState
    required: bool
    copied: bool
    provenance: str


@dataclass(frozen=True)
class ArtifactExportPlan:
    export_plan_id: str
    mode: ExportPlanMode
    source_manifest_id: str
    export_root: str
    artifact_plans: tuple[ExportArtifactPlan, ...]
    planned_sections: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    manifest_summary: dict[str, object]
    export_folder_created: bool
    files_copied: bool
    archive_created: bool
    shell_commands_executed: bool
    external_files_written: bool
    cloud_resources_created: bool
    secrets_loaded: bool
    provider_calls_performed: bool
    real_connectors_called: bool
    remediation_performed: bool
    notifications_sent: bool
    benchmark_scoring_performed: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_artifact_export_plan(
    manifest: DemoPackageManifest | None = None,
) -> ArtifactExportPlan:
    if manifest is None:
        manifest = build_demo_package_manifest()

    artifact_plans = tuple(
        ExportArtifactPlan(
            plan_id=f"export-plan::{artifact.artifact_id}",
            source_path=artifact.path,
            export_path=f"artifacts/eaios-demo/{artifact.path}",
            section=_section_for_path(artifact.path),
            state=ExportArtifactState.PLANNED_NOT_WRITTEN,
            required=artifact.required,
            copied=False,
            provenance="artifact_export_plan:artifact_plan",
        )
        for artifact in manifest.artifacts
    )

    return ArtifactExportPlan(
        export_plan_id="sprint6-artifact-export-plan-001",
        mode=ExportPlanMode.DRY_RUN_ONLY,
        source_manifest_id=manifest.manifest_id,
        export_root="artifacts/eaios-demo",
        artifact_plans=artifact_plans,
        planned_sections=(
            "docs",
            "source_contracts",
            "test_contracts",
            "rendered_views",
            "governance_summary",
        ),
        blocked_actions=(
            "create_export_folder",
            "copy_artifact_files",
            "create_archive",
            "run_shell_export_command",
            "write_external_files",
            "create_cloud_resources",
            "load_secret_material",
            "call_real_provider",
            "call_real_connector",
            "execute_remediation",
            "send_notification",
            "score_benchmark_from_export",
            "enable_autonomous_remediation",
        ),
        manifest_summary=summarize_demo_package_manifest(manifest),
        export_folder_created=False,
        files_copied=False,
        archive_created=False,
        shell_commands_executed=False,
        external_files_written=False,
        cloud_resources_created=False,
        secrets_loaded=False,
        provider_calls_performed=False,
        real_connectors_called=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="artifact_export_plan:dry_run",
    )


def summarize_artifact_export_plan(plan: ArtifactExportPlan) -> dict[str, object]:
    return {
        "export_plan_id": plan.export_plan_id,
        "mode": plan.mode.value,
        "source_manifest_id": plan.source_manifest_id,
        "export_root": plan.export_root,
        "artifact_plan_count": len(plan.artifact_plans),
        "planned_section_count": len(plan.planned_sections),
        "blocked_action_count": len(plan.blocked_actions),
        "export_folder_created": plan.export_folder_created,
        "files_copied": plan.files_copied,
        "archive_created": plan.archive_created,
        "shell_commands_executed": plan.shell_commands_executed,
        "external_files_written": plan.external_files_written,
        "cloud_resources_created": plan.cloud_resources_created,
        "secrets_loaded": plan.secrets_loaded,
        "provider_calls_performed": plan.provider_calls_performed,
        "real_connectors_called": plan.real_connectors_called,
        "remediation_performed": plan.remediation_performed,
        "notifications_sent": plan.notifications_sent,
        "benchmark_scoring_performed": plan.benchmark_scoring_performed,
        "autonomous_remediation_allowed": plan.autonomous_remediation_allowed,
        "human_review_required": plan.human_review_required,
    }


def to_view_model(plan: ArtifactExportPlan) -> dict[str, Any]:
    return {
        "summary": summarize_artifact_export_plan(plan),
        "artifact_plans": [
            {
                "plan_id": item.plan_id,
                "source_path": item.source_path,
                "export_path": item.export_path,
                "section": item.section,
                "state": item.state.value,
                "required": item.required,
                "copied": item.copied,
                "provenance": item.provenance,
            }
            for item in plan.artifact_plans
        ],
        "planned_sections": list(plan.planned_sections),
        "blocked_actions": list(plan.blocked_actions),
        "manifest_summary": plan.manifest_summary,
        "provenance": plan.provenance,
    }


def render_artifact_export_plan_text(plan: ArtifactExportPlan) -> str:
    artifact_lines = "\n".join(
        f"- {item.source_path} -> {item.export_path} [{item.state.value}]"
        for item in plan.artifact_plans
    )
    blocked_lines = "\n".join(f"- {item}" for item in plan.blocked_actions)

    return (
        "# EAIOS Dry-Run Artifact Export Plan\n\n"
        f"Export plan: {plan.export_plan_id}\n"
        f"Mode: {plan.mode.value}\n"
        f"Export root: {plan.export_root}\n\n"
        "## Planned Artifacts\n"
        f"{artifact_lines}\n\n"
        "## Blocked Actions\n"
        f"{blocked_lines}\n\n"
        "Files copied: false\n"
        "Human review required: true\n"
    )


def _section_for_path(path: str) -> str:
    if path.startswith("docs/"):
        return "docs"
    if path.startswith("tests/"):
        return "test_contracts"
    if path.startswith("src/"):
        return "source_contracts"
    return "other"
