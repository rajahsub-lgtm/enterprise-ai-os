"""Sprint 7 container packaging contract.

This module defines a review-only container packaging contract for EAIOS.

It does not build images, run containers, push images, create cloud resources,
load secrets, call providers, call connectors, execute remediation, send
notifications, score benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ContainerPackagingMode(str, Enum):
    REVIEW_ONLY_CONTRACT = "REVIEW_ONLY_CONTRACT"


class ContainerArtifactType(str, Enum):
    SOURCE_MODULE = "SOURCE_MODULE"
    TEST_MODULE = "TEST_MODULE"
    DOCUMENTATION = "DOCUMENTATION"
    CONFIG_TEMPLATE = "CONFIG_TEMPLATE"


@dataclass(frozen=True)
class ContainerArtifact:
    path: str
    artifact_type: ContainerArtifactType
    required: bool
    purpose: str
    provenance: str


@dataclass(frozen=True)
class ContainerPackagingContract:
    contract_id: str
    mode: ContainerPackagingMode
    title: str
    source_sprint: str
    image_name: str
    image_tag_policy: str
    runtime_entrypoint: str
    artifacts: tuple[ContainerArtifact, ...]
    required_reviews: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    environment_variables_allowed: tuple[str, ...]
    environment_variables_blocked: tuple[str, ...]
    build_performed: bool
    container_run_performed: bool
    image_push_performed: bool
    registry_write_performed: bool
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


def build_container_packaging_contract() -> ContainerPackagingContract:
    artifacts = (
        ContainerArtifact(
            path="src/eaios/sprint6/local_cli.py",
            artifact_type=ContainerArtifactType.SOURCE_MODULE,
            required=True,
            purpose="Read-only CLI contract that a future image may expose.",
            provenance="container_packaging_contract:artifact",
        ),
        ContainerArtifact(
            path="src/eaios/sprint6/static_review_page.py",
            artifact_type=ContainerArtifactType.SOURCE_MODULE,
            required=True,
            purpose="In-memory static review page model for future web preview.",
            provenance="container_packaging_contract:artifact",
        ),
        ContainerArtifact(
            path="src/eaios/sprint6/portfolio_walkthrough.py",
            artifact_type=ContainerArtifactType.SOURCE_MODULE,
            required=True,
            purpose="Read-only portfolio walkthrough contract.",
            provenance="container_packaging_contract:artifact",
        ),
        ContainerArtifact(
            path="docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",
            artifact_type=ContainerArtifactType.DOCUMENTATION,
            required=True,
            purpose="Sprint 6 closure and governance baseline.",
            provenance="container_packaging_contract:artifact",
        ),
        ContainerArtifact(
            path="docs/EAIOS_2_SPRINT_6_GCP_DEPLOYMENT_DESIGN.md",
            artifact_type=ContainerArtifactType.DOCUMENTATION,
            required=True,
            purpose="Review-only cloud deployment design dependency.",
            provenance="container_packaging_contract:artifact",
        ),
        ContainerArtifact(
            path="tests/test_sprint6_closeout.py",
            artifact_type=ContainerArtifactType.TEST_MODULE,
            required=True,
            purpose="Regression guard for portfolio readiness boundaries.",
            provenance="container_packaging_contract:artifact",
        ),
    )

    return ContainerPackagingContract(
        contract_id="sprint7-container-packaging-contract-001",
        mode=ContainerPackagingMode.REVIEW_ONLY_CONTRACT,
        title="EAIOS Sprint 7 Container Packaging Contract",
        source_sprint="Sprint 7-1",
        image_name="eaios-portfolio-review",
        image_tag_policy="versioned_demo_tag_required",
        runtime_entrypoint="eaios sprint6 package show-manifest --read-only --format text",
        artifacts=artifacts,
        required_reviews=(
            "container_packaging_review",
            "dependency_review",
            "secret_handling_review",
            "runtime_entrypoint_review",
            "image_registry_review",
            "cloud_deployment_review",
            "human_approval_review",
        ),
        blocked_actions=(
            "build_container_image",
            "run_container",
            "push_container_image",
            "write_to_image_registry",
            "create_cloud_resources",
            "load_secret_material",
            "call_real_provider",
            "call_real_connector",
            "execute_remediation",
            "send_notification",
            "score_benchmark_from_container_output",
            "update_benchmark_truth_from_container_output",
            "enable_autonomous_remediation",
        ),
        environment_variables_allowed=(
            "EAIOS_MODE=read_only",
            "EAIOS_DEMO_PROFILE=portfolio_review",
            "EAIOS_HUMAN_REVIEW_REQUIRED=true",
        ),
        environment_variables_blocked=(
            "PROVIDER_API_SECRET",
            "CONNECTOR_WRITE_TOKEN",
            "CLOUD_DEPLOYMENT_TOKEN",
            "BENCHMARK_TRUTH_WRITE_TOKEN",
            "AUTONOMOUS_REMEDIATION_ENABLED",
        ),
        build_performed=False,
        container_run_performed=False,
        image_push_performed=False,
        registry_write_performed=False,
        cloud_resources_created=False,
        secrets_loaded=False,
        provider_calls_performed=False,
        real_connectors_called=False,
        remediation_performed=False,
        notifications_sent=False,
        benchmark_scoring_performed=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="container_packaging_contract:model",
    )


def summarize_container_packaging_contract(
    contract: ContainerPackagingContract,
) -> dict[str, object]:
    return {
        "contract_id": contract.contract_id,
        "mode": contract.mode.value,
        "title": contract.title,
        "source_sprint": contract.source_sprint,
        "image_name": contract.image_name,
        "image_tag_policy": contract.image_tag_policy,
        "runtime_entrypoint": contract.runtime_entrypoint,
        "artifact_count": len(contract.artifacts),
        "required_review_count": len(contract.required_reviews),
        "blocked_action_count": len(contract.blocked_actions),
        "build_performed": contract.build_performed,
        "container_run_performed": contract.container_run_performed,
        "image_push_performed": contract.image_push_performed,
        "registry_write_performed": contract.registry_write_performed,
        "cloud_resources_created": contract.cloud_resources_created,
        "secrets_loaded": contract.secrets_loaded,
        "provider_calls_performed": contract.provider_calls_performed,
        "real_connectors_called": contract.real_connectors_called,
        "remediation_performed": contract.remediation_performed,
        "notifications_sent": contract.notifications_sent,
        "benchmark_scoring_performed": contract.benchmark_scoring_performed,
        "autonomous_remediation_allowed": contract.autonomous_remediation_allowed,
        "human_review_required": contract.human_review_required,
    }


def to_view_model(contract: ContainerPackagingContract) -> dict[str, Any]:
    return {
        "summary": summarize_container_packaging_contract(contract),
        "artifacts": [
            {
                "path": artifact.path,
                "artifact_type": artifact.artifact_type.value,
                "required": artifact.required,
                "purpose": artifact.purpose,
                "provenance": artifact.provenance,
            }
            for artifact in contract.artifacts
        ],
        "required_reviews": list(contract.required_reviews),
        "blocked_actions": list(contract.blocked_actions),
        "environment_variables_allowed": list(contract.environment_variables_allowed),
        "environment_variables_blocked": list(contract.environment_variables_blocked),
        "provenance": contract.provenance,
    }
