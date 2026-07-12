from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint7.cloud_deploy_preflight import (
    CloudDeployCheckStatus,
    CloudDeployPreflightMode,
    CloudDeployPreflightStatus,
    build_cloud_deploy_preflight,
    summarize_cloud_deploy_preflight,
    to_view_model,
)


def _preflight():
    return build_cloud_deploy_preflight()


def test_cloud_deploy_preflight_builds_review_only_model():
    preflight = _preflight()

    assert preflight.preflight_id == "sprint7-cloud-deploy-preflight-001"
    assert preflight.mode == CloudDeployPreflightMode.REVIEW_ONLY_PREFLIGHT
    assert preflight.status == CloudDeployPreflightStatus.BLOCKED_PENDING_REVIEWS
    assert preflight.title == "EAIOS Cloud Deploy Preflight"
    assert preflight.target_platform == "GCP Cloud Run read-only preview"
    assert preflight.source_web_surface_id == "sprint7-local-web-review-surface-001"
    assert preflight.provenance == "cloud_deploy_preflight:model"


def test_cloud_deploy_preflight_checks_are_declared():
    preflight = _preflight()

    assert len(preflight.checks) == 8

    names = tuple(check.name for check in preflight.checks)
    assert names == (
        "Cloud architecture review",
        "Container packaging review",
        "Secret handling review",
        "Provider integration review",
        "MCP connector permission review",
        "Benchmark truth isolation review",
        "Human approval workflow review",
        "Local web review surface",
    )

    assert all(check.provenance == "cloud_deploy_preflight:check" for check in preflight.checks)


def test_cloud_deploy_preflight_check_statuses_are_explicit():
    preflight = _preflight()

    assert tuple(check.status for check in preflight.checks) == (
        CloudDeployCheckStatus.REQUIRED,
        CloudDeployCheckStatus.REQUIRED,
        CloudDeployCheckStatus.BLOCKING,
        CloudDeployCheckStatus.BLOCKING,
        CloudDeployCheckStatus.BLOCKING,
        CloudDeployCheckStatus.REQUIRED,
        CloudDeployCheckStatus.REQUIRED,
        CloudDeployCheckStatus.SATISFIED_BY_DESIGN,
    )


def test_cloud_deploy_preflight_required_reviews_are_derived_from_checks():
    preflight = _preflight()

    assert preflight.required_reviews == (
        "cloud_architecture_review",
        "container_packaging_review",
        "security_and_secret_handling_review",
        "provider_integration_review",
        "mcp_connector_permission_review",
        "benchmark_truth_isolation_review",
        "human_approval_workflow_review",
        "local_web_review_surface_review",
    )


def test_cloud_deploy_preflight_blocked_actions_are_explicit():
    preflight = _preflight()

    assert preflight.blocked_actions == (
        "generate_deployment_command",
        "execute_deployment_command",
        "build_container_image",
        "push_container_image",
        "create_cloud_resources",
        "create_service_account",
        "load_secret_material",
        "enable_network_egress",
        "call_real_provider",
        "call_real_connector",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_cloud_runtime",
        "update_benchmark_truth_from_cloud_runtime",
        "enable_autonomous_remediation",
    )


def test_cloud_deploy_preflight_preserves_no_execution_boundaries():
    preflight = _preflight()

    assert preflight.deployment_commands_generated is False
    assert preflight.deployment_commands_executed is False
    assert preflight.container_image_built is False
    assert preflight.container_image_pushed is False
    assert preflight.cloud_resources_created is False
    assert preflight.service_account_created is False
    assert preflight.secrets_loaded is False
    assert preflight.network_egress_enabled is False
    assert preflight.provider_calls_performed is False
    assert preflight.real_connectors_called is False
    assert preflight.remediation_performed is False
    assert preflight.notifications_sent is False
    assert preflight.benchmark_scoring_performed is False
    assert preflight.benchmark_truth_updated is False
    assert preflight.autonomous_remediation_allowed is False
    assert preflight.human_review_required is True


def test_cloud_deploy_preflight_embeds_web_surface_summary():
    preflight = _preflight()

    assert preflight.web_surface_summary["surface_id"] == (
        "sprint7-local-web-review-surface-001"
    )
    assert preflight.web_surface_summary["mode"] == "SURFACE_MODEL_ONLY"
    assert preflight.web_surface_summary["server_started"] is False
    assert preflight.web_surface_summary["human_review_required"] is True


def test_cloud_deploy_preflight_summary_is_view_ready():
    preflight = _preflight()

    assert summarize_cloud_deploy_preflight(preflight) == {
        "preflight_id": "sprint7-cloud-deploy-preflight-001",
        "mode": "REVIEW_ONLY_PREFLIGHT",
        "status": "BLOCKED_PENDING_REVIEWS",
        "title": "EAIOS Cloud Deploy Preflight",
        "target_platform": "GCP Cloud Run read-only preview",
        "source_web_surface_id": "sprint7-local-web-review-surface-001",
        "check_count": 8,
        "required_review_count": 8,
        "blocked_action_count": 15,
        "deployment_commands_generated": False,
        "deployment_commands_executed": False,
        "container_image_built": False,
        "container_image_pushed": False,
        "cloud_resources_created": False,
        "service_account_created": False,
        "secrets_loaded": False,
        "network_egress_enabled": False,
        "provider_calls_performed": False,
        "real_connectors_called": False,
        "remediation_performed": False,
        "notifications_sent": False,
        "benchmark_scoring_performed": False,
        "benchmark_truth_updated": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_cloud_deploy_preflight_view_model_is_json_serializable():
    preflight = _preflight()

    serialized = json.dumps(to_view_model(preflight), indent=2)

    assert "sprint7-cloud-deploy-preflight-001" in serialized
    assert "BLOCKED_PENDING_REVIEWS" in serialized
    assert "security_and_secret_handling_review" in serialized
    assert "score_benchmark_from_cloud_runtime" in serialized


def test_cloud_deploy_preflight_module_does_not_execute_deployment_actions():
    source = Path("src/eaios/sprint7/cloud_deploy_preflight.py").read_text(
        encoding="utf-8"
    ).lower()

    assert "subprocess" not in source
    assert "os.system" not in source
    assert "gcloud run deploy" not in source
    assert "terraform apply" not in source
    assert "kubectl apply" not in source
    assert "docker build" not in source
    assert "docker push" not in source
    assert "write_text(" not in source
    assert "mkdir(" not in source
    assert "requests.post" not in source
    assert "httpx.post" not in source
    assert "openai" not in source
    assert "anthropic" not in source
