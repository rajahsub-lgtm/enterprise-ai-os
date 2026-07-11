from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint5.gcp_readiness_checklist import (
    GCPDeploymentReadinessState,
    GCPReadinessCategory,
    GCPReadinessDecision,
    build_gcp_readiness_checklist,
    summarize_gcp_readiness_checklist,
    to_view_model,
)


def _checklist():
    return build_gcp_readiness_checklist()


def test_gcp_readiness_checklist_builds_from_mcp_harness():
    checklist = _checklist()

    assert checklist.checklist_id == "sprint5-gcp-readiness-checklist-001"
    assert checklist.source_connector_harness_profile_id == (
        "sprint5-mcp-connector-harness-profile-001"
    )
    assert checklist.target_environment == "GCP_READINESS_REVIEW_ONLY"
    assert checklist.readiness_state == GCPDeploymentReadinessState.REVIEW_READY_NOT_DEPLOYED
    assert checklist.provenance == "gcp_readiness_checklist:review_only_checklist"


def test_gcp_readiness_checklist_has_expected_categories():
    checklist = _checklist()

    assert len(checklist.checks) == 9

    categories = tuple(check.category for check in checklist.checks)

    assert categories == (
        GCPReadinessCategory.RUNTIME_PACKAGING,
        GCPReadinessCategory.CONFIGURATION_BOUNDARY,
        GCPReadinessCategory.SECRET_HANDLING,
        GCPReadinessCategory.PROVIDER_INTEGRATION,
        GCPReadinessCategory.CONNECTOR_INTEGRATION,
        GCPReadinessCategory.EXTERNAL_WRITES,
        GCPReadinessCategory.AUDIT_EXPORT,
        GCPReadinessCategory.HUMAN_APPROVAL,
        GCPReadinessCategory.DEPLOYMENT_ACTION,
    )


def test_gcp_readiness_checks_pass_because_blocks_are_explicit():
    checklist = _checklist()

    for check in checklist.checks:
        assert check.passed is True
        assert check.blocking is True
        assert check.provenance == "gcp_readiness_checklist:check"


def test_gcp_readiness_secret_provider_connector_checks_are_blocked_for_review():
    checklist = _checklist()

    blocked_checks = [
        check for check in checklist.checks
        if check.category in {
            GCPReadinessCategory.SECRET_HANDLING,
            GCPReadinessCategory.PROVIDER_INTEGRATION,
            GCPReadinessCategory.CONNECTOR_INTEGRATION,
            GCPReadinessCategory.EXTERNAL_WRITES,
            GCPReadinessCategory.DEPLOYMENT_ACTION,
        }
    ]

    assert len(blocked_checks) == 5

    for check in blocked_checks:
        assert check.decision == GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW
        assert len(check.blockers) >= 1


def test_gcp_readiness_ready_checks_are_read_only():
    checklist = _checklist()

    ready_checks = [
        check for check in checklist.checks
        if check.category in {
            GCPReadinessCategory.RUNTIME_PACKAGING,
            GCPReadinessCategory.CONFIGURATION_BOUNDARY,
            GCPReadinessCategory.AUDIT_EXPORT,
            GCPReadinessCategory.HUMAN_APPROVAL,
        }
    ]

    assert len(ready_checks) == 4

    for check in ready_checks:
        assert check.decision == GCPReadinessDecision.READY_READ_ONLY


def test_gcp_readiness_deployment_gates_are_explicit():
    checklist = _checklist()

    assert len(checklist.deployment_gates) == 6

    gate_ids = tuple(gate.gate_id for gate in checklist.deployment_gates)

    assert gate_ids == (
        "gcp-gate-local-review-export-001",
        "gcp-gate-cloud-resource-creation-001",
        "gcp-gate-secret-loading-001",
        "gcp-gate-provider-network-001",
        "gcp-gate-real-connectors-001",
        "gcp-gate-remediation-benchmark-001",
    )


def test_gcp_readiness_allows_only_local_review_export_gate():
    checklist = _checklist()

    allowed = [gate for gate in checklist.deployment_gates if gate.allowed]
    blocked = [gate for gate in checklist.deployment_gates if not gate.allowed]

    assert len(allowed) == 1
    assert allowed[0].gate_id == "gcp-gate-local-review-export-001"
    assert allowed[0].decision == GCPReadinessDecision.READY_READ_ONLY

    assert len(blocked) == 5
    for gate in blocked:
        assert gate.decision == GCPReadinessDecision.BLOCKED_REQUIRES_REVIEW


def test_gcp_readiness_deployment_gates_cannot_create_or_execute():
    checklist = _checklist()

    for gate in checklist.deployment_gates:
        assert gate.can_create_cloud_resources is False
        assert gate.can_load_secrets is False
        assert gate.can_access_network is False
        assert gate.can_enable_real_connectors is False
        assert gate.can_execute_remediation is False
        assert gate.can_score_benchmark is False
        assert gate.provenance == "gcp_readiness_checklist:deployment_gate"


def test_gcp_readiness_allowed_next_steps_are_review_only():
    checklist = _checklist()

    assert checklist.allowed_next_steps == (
        "review_local_demo_export",
        "review_operator_screen_model",
        "review_cloud_safety_profile",
        "review_provider_plugin_seam",
        "review_mcp_connector_harness",
    )


def test_gcp_readiness_blocked_deployment_actions_are_explicit():
    checklist = _checklist()

    assert checklist.blocked_deployment_actions == (
        "create_cloud_resources",
        "run_shell_deployment_command",
        "load_secret_material",
        "enable_real_provider",
        "enable_real_mcp_connectors",
        "perform_external_write",
        "execute_remediation",
        "send_notification",
        "score_benchmark_from_deployment",
    )


def test_gcp_readiness_required_human_reviews_are_explicit():
    checklist = _checklist()

    assert checklist.required_human_reviews == (
        "cloud_architecture_review",
        "security_and_secret_handling_review",
        "provider_integration_review",
        "mcp_connector_permission_review",
        "production_deployment_approval",
    )


def test_gcp_readiness_embeds_connector_harness_summary_and_view():
    checklist = _checklist()

    assert checklist.connector_harness_summary["profile_id"] == (
        "sprint5-mcp-connector-harness-profile-001"
    )
    assert checklist.connector_harness_summary["real_connector_called"] is False

    assert checklist.connector_harness_view["summary"]["profile_id"] == (
        "sprint5-mcp-connector-harness-profile-001"
    )
    assert checklist.connector_harness_view["summary"][
        "benchmark_scoring_allowed_from_connector"
    ] is False


def test_gcp_readiness_preserves_no_deployment_or_cloud_execution_boundaries():
    checklist = _checklist()

    assert checklist.deployment_plan_generated is True
    assert checklist.deployment_actions_performed is False
    assert checklist.cloud_resources_created is False
    assert checklist.shell_commands_executed is False
    assert checklist.secrets_loaded is False
    assert checklist.network_access_performed is False
    assert checklist.provider_calls_allowed is False
    assert checklist.real_connectors_allowed is False
    assert checklist.external_writes_allowed is False
    assert checklist.remediation_allowed is False
    assert checklist.notification_allowed is False
    assert checklist.benchmark_scoring_allowed_from_readiness is False
    assert checklist.autonomous_remediation_allowed is False
    assert checklist.human_review_required is True


def test_gcp_readiness_summary_is_view_ready():
    checklist = _checklist()

    assert summarize_gcp_readiness_checklist(checklist) == {
        "checklist_id": "sprint5-gcp-readiness-checklist-001",
        "source_connector_harness_profile_id": (
            "sprint5-mcp-connector-harness-profile-001"
        ),
        "target_environment": "GCP_READINESS_REVIEW_ONLY",
        "readiness_state": "REVIEW_READY_NOT_DEPLOYED",
        "check_count": 9,
        "passed_check_count": 9,
        "deployment_gate_count": 6,
        "allowed_gate_count": 1,
        "blocked_gate_count": 5,
        "allowed_next_step_count": 5,
        "blocked_deployment_action_count": 9,
        "required_human_review_count": 5,
        "deployment_plan_generated": True,
        "deployment_actions_performed": False,
        "cloud_resources_created": False,
        "shell_commands_executed": False,
        "secrets_loaded": False,
        "network_access_performed": False,
        "provider_calls_allowed": False,
        "real_connectors_allowed": False,
        "external_writes_allowed": False,
        "remediation_allowed": False,
        "notification_allowed": False,
        "benchmark_scoring_allowed_from_readiness": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_gcp_readiness_view_model_is_json_serializable():
    checklist = _checklist()

    serialized = json.dumps(to_view_model(checklist), indent=2)

    assert "sprint5-gcp-readiness-checklist-001" in serialized
    assert "GCP_READINESS_REVIEW_ONLY" in serialized
    assert "create_cloud_resources" in serialized
    assert "provider_integration_review" in serialized
    assert "benchmark_scoring_allowed_from_readiness" in serialized


def test_gcp_readiness_module_does_not_deploy_or_score_benchmark():
    source = Path("src/eaios/sprint5/gcp_readiness_checklist.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "google.cloud" not in source.lower()
    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
