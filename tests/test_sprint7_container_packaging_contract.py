from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.container_packaging_contract import (
    ContainerArtifactType,
    ContainerPackagingMode,
    build_container_packaging_contract,
    summarize_container_packaging_contract,
    to_view_model,
)


def _contract():
    return build_container_packaging_contract()


def test_container_packaging_contract_builds_review_only_model():
    contract = _contract()

    assert contract.contract_id == "sprint7-container-packaging-contract-001"
    assert contract.mode == ContainerPackagingMode.REVIEW_ONLY_CONTRACT
    assert contract.title == "EAIOS Sprint 7 Container Packaging Contract"
    assert contract.source_sprint == "Sprint 7-1"
    assert contract.image_name == "eaios-portfolio-review"
    assert contract.image_tag_policy == "versioned_demo_tag_required"
    assert contract.runtime_entrypoint == (
        "eaios sprint6 package show-manifest --read-only --format text"
    )
    assert contract.provenance == "container_packaging_contract:model"


def test_container_packaging_contract_artifacts_are_declared():
    contract = _contract()

    assert len(contract.artifacts) == 6

    paths = tuple(artifact.path for artifact in contract.artifacts)
    assert paths == (
        "src/eaios/sprint6/local_cli.py",
        "src/eaios/sprint6/static_review_page.py",
        "src/eaios/sprint6/portfolio_walkthrough.py",
        "docs/EAIOS_2_SPRINT_6_CLOSEOUT.md",
        "docs/EAIOS_2_SPRINT_6_GCP_DEPLOYMENT_DESIGN.md",
        "tests/test_sprint6_closeout.py",
    )

    assert all(artifact.required is True for artifact in contract.artifacts)
    assert all(
        artifact.provenance == "container_packaging_contract:artifact"
        for artifact in contract.artifacts
    )


def test_container_packaging_contract_artifact_types_are_explicit():
    contract = _contract()

    artifact_types = tuple(artifact.artifact_type for artifact in contract.artifacts)

    assert artifact_types == (
        ContainerArtifactType.SOURCE_MODULE,
        ContainerArtifactType.SOURCE_MODULE,
        ContainerArtifactType.SOURCE_MODULE,
        ContainerArtifactType.DOCUMENTATION,
        ContainerArtifactType.DOCUMENTATION,
        ContainerArtifactType.TEST_MODULE,
    )


def test_container_packaging_contract_required_reviews_are_explicit():
    contract = _contract()

    assert contract.required_reviews == (
        "container_packaging_review",
        "dependency_review",
        "secret_handling_review",
        "runtime_entrypoint_review",
        "image_registry_review",
        "cloud_deployment_review",
        "human_approval_review",
    )


def test_container_packaging_contract_blocked_actions_are_explicit():
    contract = _contract()

    assert contract.blocked_actions == (
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
    )


def test_container_packaging_contract_environment_boundaries_are_explicit():
    contract = _contract()

    assert contract.environment_variables_allowed == (
        "EAIOS_MODE=read_only",
        "EAIOS_DEMO_PROFILE=portfolio_review",
        "EAIOS_HUMAN_REVIEW_REQUIRED=true",
    )

    assert contract.environment_variables_blocked == (
        "PROVIDER_API_SECRET",
        "CONNECTOR_WRITE_TOKEN",
        "CLOUD_DEPLOYMENT_TOKEN",
        "BENCHMARK_TRUTH_WRITE_TOKEN",
        "AUTONOMOUS_REMEDIATION_ENABLED",
    )


def test_container_packaging_contract_preserves_no_execution_boundaries():
    contract = _contract()

    assert contract.build_performed is False
    assert contract.container_run_performed is False
    assert contract.image_push_performed is False
    assert contract.registry_write_performed is False
    assert contract.cloud_resources_created is False
    assert contract.secrets_loaded is False
    assert contract.provider_calls_performed is False
    assert contract.real_connectors_called is False
    assert contract.remediation_performed is False
    assert contract.notifications_sent is False
    assert contract.benchmark_scoring_performed is False
    assert contract.autonomous_remediation_allowed is False
    assert contract.human_review_required is True


def test_container_packaging_contract_summary_is_view_ready():
    contract = _contract()

    assert summarize_container_packaging_contract(contract) == {
        "contract_id": "sprint7-container-packaging-contract-001",
        "mode": "REVIEW_ONLY_CONTRACT",
        "title": "EAIOS Sprint 7 Container Packaging Contract",
        "source_sprint": "Sprint 7-1",
        "image_name": "eaios-portfolio-review",
        "image_tag_policy": "versioned_demo_tag_required",
        "runtime_entrypoint": "eaios sprint6 package show-manifest --read-only --format text",
        "artifact_count": 6,
        "required_review_count": 7,
        "blocked_action_count": 13,
        "build_performed": False,
        "container_run_performed": False,
        "image_push_performed": False,
        "registry_write_performed": False,
        "cloud_resources_created": False,
        "secrets_loaded": False,
        "provider_calls_performed": False,
        "real_connectors_called": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_container_packaging_contract_view_model_is_json_serializable():
    contract = _contract()

    serialized = json.dumps(to_view_model(contract), indent=2)

    assert "sprint7-container-packaging-contract-001" in serialized
    assert "eaios-portfolio-review" in serialized
    assert "build_container_image" in serialized
    assert "PROVIDER_API_SECRET" in serialized


def test_container_packaging_contract_module_does_not_execute_container_actions():
    source = Path("src/eaios/sprint7/container_packaging_contract.py").read_text(
        encoding="utf-8"
    ).lower()

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "docker build" not in source
    assert "docker run" not in source
    assert "docker push" not in source
    assert "gcloud run deploy" not in source
    assert "terraform apply" not in source
    assert "kubectl apply" not in source
    assert "write_text(" not in source
    assert "mkdir(" not in source
    assert "requests.post" not in source
    assert "httpx.post" not in source
    assert "openai" not in source
    assert "anthropic" not in source
