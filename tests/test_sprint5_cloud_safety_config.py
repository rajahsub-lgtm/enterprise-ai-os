from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint5.cloud_safety_config import (
    CloudCapabilityDecision,
    CloudEnvironmentTarget,
    CloudReadinessState,
    CloudSafetyControl,
    build_cloud_safe_config_profile,
    summarize_cloud_safe_config_profile,
    to_view_model,
)


def _profile():
    return build_cloud_safe_config_profile()


def test_cloud_safe_config_profile_builds_from_operator_review_screen():
    profile = _profile()

    assert profile.profile_id == "sprint5-cloud-safe-config-profile-001"
    assert profile.source_screen_id == "sprint5-operator-review-screen-001"
    assert profile.target_environment == CloudEnvironmentTarget.GCP_READINESS_REVIEW
    assert profile.readiness_state == CloudReadinessState.REVIEW_READY
    assert profile.provenance == "cloud_safety_config:gcp_readiness_profile"


def test_cloud_safe_config_profile_has_capability_toggles():
    profile = _profile()

    assert len(profile.capability_toggles) == 6

    capability_ids = tuple(toggle.capability_id for toggle in profile.capability_toggles)

    assert capability_ids == (
        "runtime.read_only_demo",
        "provider.llm",
        "mcp.connectors",
        "cloud.gcp_deploy",
        "storage.external_write",
        "dashboard.apply_changes",
    )


def test_cloud_safe_config_allows_only_read_only_runtime_by_default():
    profile = _profile()

    runtime = next(
        toggle for toggle in profile.capability_toggles
        if toggle.capability_id == "runtime.read_only_demo"
    )

    assert runtime.decision == CloudCapabilityDecision.ALLOWED_READ_ONLY
    assert runtime.requested is True
    assert runtime.default_enabled is True
    assert runtime.can_enable_without_review is True
    assert runtime.requires_secret is False
    assert runtime.performs_external_action is False


def test_cloud_safe_config_blocks_provider_tool_cloud_and_write_capabilities():
    profile = _profile()

    blocked = [
        toggle for toggle in profile.capability_toggles
        if toggle.capability_id != "runtime.read_only_demo"
    ]

    assert len(blocked) == 5

    for toggle in blocked:
        assert toggle.decision == CloudCapabilityDecision.BLOCKED_REQUIRES_REVIEW
        assert toggle.default_enabled is False
        assert toggle.can_enable_without_review is False


def test_cloud_safe_config_secret_and_external_action_flags_are_explicit():
    profile = _profile()

    flags = {
        toggle.capability_id: (
            toggle.requires_secret,
            toggle.performs_external_action,
        )
        for toggle in profile.capability_toggles
    }

    assert flags["provider.llm"] == (True, True)
    assert flags["mcp.connectors"] == (True, True)
    assert flags["cloud.gcp_deploy"] == (True, True)
    assert flags["storage.external_write"] == (True, True)
    assert flags["dashboard.apply_changes"] == (False, False)


def test_cloud_safe_config_has_complete_safety_checklist():
    profile = _profile()

    assert len(profile.safety_checklist) == 8

    controls = tuple(item.control for item in profile.safety_checklist)

    assert controls == (
        CloudSafetyControl.READ_ONLY_RUNTIME,
        CloudSafetyControl.NO_EXTERNAL_WRITES,
        CloudSafetyControl.NO_SECRET_MATERIAL,
        CloudSafetyControl.PROVIDER_DISABLED_BY_DEFAULT,
        CloudSafetyControl.TOOL_CONNECTORS_DISABLED_BY_DEFAULT,
        CloudSafetyControl.HUMAN_APPROVAL_REQUIRED,
        CloudSafetyControl.BENCHMARK_TRUTH_EXTERNAL,
        CloudSafetyControl.AUDIT_EXPORT_REQUIRED,
    )


def test_cloud_safe_config_safety_checks_pass_and_are_blocking():
    profile = _profile()

    for item in profile.safety_checklist:
        assert item.passed is True
        assert item.blocking is True
        assert item.provenance == "cloud_safety_config:safety_check"


def test_cloud_safe_config_allowed_capabilities_are_read_only():
    profile = _profile()

    assert profile.allowed_capabilities == (
        "runtime.read_only_demo",
        "operator_review_screen_rendering",
        "local_json_export",
        "local_markdown_export",
        "governance_check_summary",
    )


def test_cloud_safe_config_blocked_capabilities_are_explicit():
    profile = _profile()

    assert profile.blocked_capabilities == (
        "provider.llm",
        "mcp.connectors",
        "cloud.gcp_deploy",
        "storage.external_write",
        "dashboard.apply_changes",
        "autonomous_remediation",
        "benchmark_scoring_from_cloud_profile",
    )


def test_cloud_safe_config_embeds_operator_screen_summary_and_view():
    profile = _profile()

    assert profile.screen_summary["screen_id"] == "sprint5-operator-review-screen-001"
    assert profile.screen_summary["mode"] == "READ_ONLY_REVIEW"
    assert profile.screen_summary["all_governance_checks_passed"] is True

    assert profile.screen_view["summary"]["screen_id"] == "sprint5-operator-review-screen-001"
    assert profile.screen_view["summary"]["benchmark_scoring_allowed_from_screen"] is False


def test_cloud_safe_config_preserves_no_cloud_execution_boundaries():
    profile = _profile()

    assert profile.deployment_actions_performed is False
    assert profile.secrets_required is False
    assert profile.external_network_required is False
    assert profile.cloud_resources_created is False
    assert profile.provider_calls_allowed is False
    assert profile.real_tool_connectors_allowed is False
    assert profile.external_writes_allowed is False
    assert profile.benchmark_scoring_allowed_from_config is False
    assert profile.autonomous_remediation_allowed is False
    assert profile.human_review_required is True


def test_cloud_safe_config_summary_is_view_ready():
    profile = _profile()

    assert summarize_cloud_safe_config_profile(profile) == {
        "profile_id": "sprint5-cloud-safe-config-profile-001",
        "source_screen_id": "sprint5-operator-review-screen-001",
        "target_environment": "GCP_READINESS_REVIEW",
        "readiness_state": "REVIEW_READY",
        "capability_toggle_count": 6,
        "safety_check_count": 8,
        "passed_safety_check_count": 8,
        "allowed_capability_count": 5,
        "blocked_capability_count": 7,
        "deployment_actions_performed": False,
        "secrets_required": False,
        "external_network_required": False,
        "cloud_resources_created": False,
        "provider_calls_allowed": False,
        "real_tool_connectors_allowed": False,
        "external_writes_allowed": False,
        "benchmark_scoring_allowed_from_config": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_cloud_safe_config_view_model_is_json_serializable():
    profile = _profile()

    serialized = json.dumps(to_view_model(profile), indent=2)

    assert "sprint5-cloud-safe-config-profile-001" in serialized
    assert "GCP_READINESS_REVIEW" in serialized
    assert "provider.llm" in serialized
    assert "mcp.connectors" in serialized
    assert "benchmark_scoring_allowed_from_config" in serialized


def test_cloud_safety_config_module_does_not_deploy_or_score_benchmark():
    source = Path("src/eaios/sprint5/cloud_safety_config.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "google.cloud" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
