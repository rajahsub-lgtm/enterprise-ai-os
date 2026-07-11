"""Sprint 6 local demo package manifest.

This module defines a local, read-only packaging manifest for the EAIOS demo.

It does not write package artifacts, deploy cloud resources, load secrets, call
providers, connect real tools, execute remediation, send notifications, score
benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint5.gcp_readiness_checklist import (
    build_gcp_readiness_checklist,
    summarize_gcp_readiness_checklist,
)


class DemoPackageMode(str, Enum):
    LOCAL_MANIFEST_ONLY = "LOCAL_MANIFEST_ONLY"


class DemoPackageArtifactType(str, Enum):
    DOCUMENT = "DOCUMENT"
    SOURCE_CONTRACT = "SOURCE_CONTRACT"
    TEST_CONTRACT = "TEST_CONTRACT"
    VIEW_MODEL = "VIEW_MODEL"


@dataclass(frozen=True)
class DemoPackageArtifact:
    artifact_id: str
    artifact_type: DemoPackageArtifactType
    path: str
    purpose: str
    required: bool
    read_only: bool
    provenance: str


@dataclass(frozen=True)
class DemoPackageManifest:
    manifest_id: str
    mode: DemoPackageMode
    title: str
    source_readiness_checklist_id: str
    artifacts: tuple[DemoPackageArtifact, ...]
    package_sections: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    readiness_summary: dict[str, object]
    package_files_written: bool
    external_files_written: bool
    shell_commands_executed: bool
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


def build_demo_package_manifest() -> DemoPackageManifest:
    readiness = build_gcp_readiness_checklist()
    readiness_summary = summarize_gcp_readiness_checklist(readiness)

    artifacts = (
        DemoPackageArtifact(
            artifact_id="artifact-demo-narrative-001",
            artifact_type=DemoPackageArtifactType.DOCUMENT,
            path="docs/EAIOS_2_SPRINT_5_DEMO_NARRATIVE.md",
            purpose="Operator-facing demo story and talk track.",
            required=True,
            read_only=True,
            provenance="demo_package:artifact",
        ),
        DemoPackageArtifact(
            artifact_id="artifact-sprint5-closeout-001",
            artifact_type=DemoPackageArtifactType.DOCUMENT,
            path="docs/EAIOS_2_SPRINT_5_CLOSEOUT.md",
            purpose="Sprint 5 architecture checkpoint.",
            required=True,
            read_only=True,
            provenance="demo_package:artifact",
        ),
        DemoPackageArtifact(
            artifact_id="artifact-scenario-command-001",
            artifact_type=DemoPackageArtifactType.SOURCE_CONTRACT,
            path="src/eaios/sprint5/scenario_command.py",
            purpose="Single read-only application-health scenario command contract.",
            required=True,
            read_only=True,
            provenance="demo_package:artifact",
        ),
        DemoPackageArtifact(
            artifact_id="artifact-operator-review-screen-001",
            artifact_type=DemoPackageArtifactType.SOURCE_CONTRACT,
            path="src/eaios/sprint5/operator_review_screen.py",
            purpose="Operator review screen and disabled decision controls.",
            required=True,
            read_only=True,
            provenance="demo_package:artifact",
        ),
        DemoPackageArtifact(
            artifact_id="artifact-gcp-readiness-001",
            artifact_type=DemoPackageArtifactType.SOURCE_CONTRACT,
            path="src/eaios/sprint5/gcp_readiness_checklist.py",
            purpose="GCP readiness checklist and deployment gates.",
            required=True,
            read_only=True,
            provenance="demo_package:artifact",
        ),
        DemoPackageArtifact(
            artifact_id="artifact-sprint5-tests-001",
            artifact_type=DemoPackageArtifactType.TEST_CONTRACT,
            path="tests/test_sprint5_closeout.py",
            purpose="Closeout tests proving read-only governance boundaries.",
            required=True,
            read_only=True,
            provenance="demo_package:artifact",
        ),
    )

    return DemoPackageManifest(
        manifest_id="sprint6-demo-package-manifest-001",
        mode=DemoPackageMode.LOCAL_MANIFEST_ONLY,
        title="EAIOS Portfolio Demo Package Manifest",
        source_readiness_checklist_id=str(readiness_summary["checklist_id"]),
        artifacts=artifacts,
        package_sections=(
            "demo_story",
            "operator_experience",
            "governance_boundaries",
            "cloud_readiness",
            "test_evidence",
            "next_steps",
        ),
        blocked_actions=(
            "write_package_artifacts",
            "write_external_files",
            "run_shell_packaging_command",
            "create_cloud_resources",
            "load_secret_material",
            "call_real_provider",
            "call_real_connector",
            "execute_remediation",
            "send_notification",
            "score_benchmark_from_package",
            "enable_autonomous_remediation",
        ),
        readiness_summary=readiness_summary,
        package_files_written=False,
        external_files_written=False,
        shell_commands_executed=False,
        cloud_resources_created=False,
        secrets_loaded=False,
        provider_calls_performed=False,
        real_connectors_called=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="demo_package:manifest",
    )


def summarize_demo_package_manifest(manifest: DemoPackageManifest) -> dict[str, object]:
    return {
        "manifest_id": manifest.manifest_id,
        "mode": manifest.mode.value,
        "title": manifest.title,
        "source_readiness_checklist_id": manifest.source_readiness_checklist_id,
        "artifact_count": len(manifest.artifacts),
        "required_artifact_count": len([item for item in manifest.artifacts if item.required]),
        "package_section_count": len(manifest.package_sections),
        "blocked_action_count": len(manifest.blocked_actions),
        "package_files_written": manifest.package_files_written,
        "external_files_written": manifest.external_files_written,
        "shell_commands_executed": manifest.shell_commands_executed,
        "cloud_resources_created": manifest.cloud_resources_created,
        "secrets_loaded": manifest.secrets_loaded,
        "provider_calls_performed": manifest.provider_calls_performed,
        "real_connectors_called": manifest.real_connectors_called,
        "remediation_performed": manifest.remediation_performed,
        "notifications_sent": manifest.notifications_sent,
        "benchmark_scoring_performed": manifest.benchmark_scoring_performed,
        "autonomous_remediation_allowed": manifest.autonomous_remediation_allowed,
        "human_review_required": manifest.human_review_required,
    }


def to_view_model(manifest: DemoPackageManifest) -> dict[str, Any]:
    return {
        "summary": summarize_demo_package_manifest(manifest),
        "artifacts": [
            {
                "artifact_id": item.artifact_id,
                "artifact_type": item.artifact_type.value,
                "path": item.path,
                "purpose": item.purpose,
                "required": item.required,
                "read_only": item.read_only,
                "provenance": item.provenance,
            }
            for item in manifest.artifacts
        ],
        "package_sections": list(manifest.package_sections),
        "blocked_actions": list(manifest.blocked_actions),
        "readiness_summary": manifest.readiness_summary,
        "provenance": manifest.provenance,
    }


def render_demo_package_manifest_text(manifest: DemoPackageManifest) -> str:
    artifact_lines = "\n".join(
        f"- {item.artifact_id}: {item.path}" for item in manifest.artifacts
    )
    blocked_lines = "\n".join(f"- {item}" for item in manifest.blocked_actions)

    return (
        "# EAIOS Portfolio Demo Package Manifest\n\n"
        f"Manifest: {manifest.manifest_id}\n"
        f"Mode: {manifest.mode.value}\n"
        f"Source readiness checklist: {manifest.source_readiness_checklist_id}\n\n"
        "## Artifacts\n"
        f"{artifact_lines}\n\n"
        "## Blocked Actions\n"
        f"{blocked_lines}\n\n"
        "Human review required: true\n"
    )
