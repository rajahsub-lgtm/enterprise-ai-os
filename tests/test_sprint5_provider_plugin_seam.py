from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint5.provider_plugin_seam import (
    ProviderPluginMode,
    ProviderSafetyDecision,
    build_provider_plugin_seam_profile,
    summarize_provider_plugin_seam_profile,
    to_view_model,
)


def _profile():
    return build_provider_plugin_seam_profile()


def test_provider_plugin_seam_profile_builds_from_cloud_config():
    profile = _profile()

    assert profile.profile_id == "sprint5-provider-plugin-seam-profile-001"
    assert profile.source_cloud_profile_id == "sprint5-cloud-safe-config-profile-001"
    assert profile.mode == ProviderPluginMode.DETERMINISTIC_FIXTURE_ONLY
    assert profile.provenance == "provider_plugin_seam:safety_profile"


def test_provider_plugin_seam_has_expected_request_envelopes():
    profile = _profile()

    assert len(profile.request_envelopes) == 4

    request_ids = tuple(envelope.request_id for envelope in profile.request_envelopes)

    assert request_ids == (
        "provider-request-local-summary-001",
        "provider-request-real-llm-draft-001",
        "provider-request-benchmark-score-001",
        "provider-request-action-001",
    )


def test_provider_plugin_seam_allows_only_deterministic_local_fixture():
    profile = _profile()

    allowed = [result for result in profile.validation_results if result.allowed]

    assert len(allowed) == 1
    assert allowed[0].request_id == "provider-request-local-summary-001"
    assert allowed[0].decision == ProviderSafetyDecision.ALLOWED_DETERMINISTIC_LOCAL
    assert allowed[0].deterministic_fixture_used is True
    assert allowed[0].real_provider_call_performed is False
    assert allowed[0].secret_loaded is False
    assert allowed[0].network_access_performed is False


def test_provider_plugin_seam_blocks_real_provider_request_before_any_call():
    profile = _profile()

    result = next(
        item for item in profile.validation_results
        if item.request_id == "provider-request-real-llm-draft-001"
    )

    assert result.allowed is False
    assert result.decision == ProviderSafetyDecision.BLOCKED_SECRET_REQUIRED
    assert "secret material" in result.reason
    assert result.real_provider_call_performed is False
    assert result.secret_loaded is False
    assert result.network_access_performed is False


def test_provider_plugin_seam_blocks_benchmark_scoring_request():
    profile = _profile()

    result = next(
        item for item in profile.validation_results
        if item.request_id == "provider-request-benchmark-score-001"
    )

    assert result.allowed is False
    assert result.decision == ProviderSafetyDecision.BLOCKED_BENCHMARK_SCORING
    assert "cannot define benchmark truth or score benchmarks" in result.reason
    assert result.benchmark_truth_updated is False
    assert result.benchmark_scoring_allowed is False


def test_provider_plugin_seam_blocks_action_request():
    profile = _profile()

    result = next(
        item for item in profile.validation_results
        if item.request_id == "provider-request-action-001"
    )

    assert result.allowed is False
    assert result.decision == ProviderSafetyDecision.BLOCKED_ACTION_REQUEST
    assert "cannot request autonomous action" in result.reason
    assert result.autonomous_action_allowed is False


def test_provider_plugin_seam_has_deterministic_fixture():
    profile = _profile()

    assert profile.deterministic_response_fixtures == {
        "provider-request-local-summary-001": (
            "Deterministic fixture: operator dashboard remains read-only; "
            "human review is required; unsafe actions remain blocked."
        )
    }


def test_provider_plugin_seam_preserves_safety_controls():
    profile = _profile()

    assert profile.safety_controls == (
        "real_provider_disabled_by_default",
        "secret_loading_blocked",
        "network_access_blocked",
        "deterministic_fixture_only",
        "benchmark_truth_update_blocked",
        "benchmark_scoring_from_provider_blocked",
        "autonomous_action_blocked",
        "human_review_required",
    )


def test_provider_plugin_seam_blocks_expected_capabilities():
    profile = _profile()

    assert profile.blocked_capabilities == (
        "real_llm_provider_call",
        "secret_loading",
        "network_access",
        "benchmark_truth_update",
        "benchmark_scoring_from_provider",
        "autonomous_remediation_instruction",
    )


def test_provider_plugin_seam_embeds_cloud_config_summary_and_view():
    profile = _profile()

    assert profile.cloud_config_summary["profile_id"] == "sprint5-cloud-safe-config-profile-001"
    assert profile.cloud_config_summary["provider_calls_allowed"] is False
    assert profile.cloud_config_summary["real_tool_connectors_allowed"] is False

    assert profile.cloud_config_view["summary"]["profile_id"] == (
        "sprint5-cloud-safe-config-profile-001"
    )
    assert profile.cloud_config_view["summary"]["benchmark_scoring_allowed_from_config"] is False


def test_provider_plugin_seam_preserves_no_provider_execution_boundaries():
    profile = _profile()

    assert profile.real_provider_calls_allowed is False
    assert profile.real_provider_call_performed is False
    assert profile.secrets_loaded is False
    assert profile.network_access_performed is False
    assert profile.benchmark_truth_update_allowed is False
    assert profile.benchmark_scoring_allowed_from_provider is False
    assert profile.autonomous_remediation_allowed is False
    assert profile.human_review_required is True

    for result in profile.validation_results:
        assert result.real_provider_call_performed is False
        assert result.secret_loaded is False
        assert result.network_access_performed is False
        assert result.benchmark_truth_updated is False
        assert result.benchmark_scoring_allowed is False
        assert result.autonomous_action_allowed is False
        assert result.human_review_required is True


def test_provider_plugin_seam_summary_is_view_ready():
    profile = _profile()

    assert summarize_provider_plugin_seam_profile(profile) == {
        "profile_id": "sprint5-provider-plugin-seam-profile-001",
        "source_cloud_profile_id": "sprint5-cloud-safe-config-profile-001",
        "mode": "DETERMINISTIC_FIXTURE_ONLY",
        "request_count": 4,
        "validation_count": 4,
        "allowed_validation_count": 1,
        "blocked_validation_count": 3,
        "fixture_count": 1,
        "safety_control_count": 8,
        "blocked_capability_count": 6,
        "real_provider_calls_allowed": False,
        "real_provider_call_performed": False,
        "secrets_loaded": False,
        "network_access_performed": False,
        "benchmark_truth_update_allowed": False,
        "benchmark_scoring_allowed_from_provider": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_provider_plugin_seam_view_model_is_json_serializable():
    profile = _profile()

    serialized = json.dumps(to_view_model(profile), indent=2)

    assert "sprint5-provider-plugin-seam-profile-001" in serialized
    assert "DETERMINISTIC_FIXTURE_ONLY" in serialized
    assert "provider-request-real-llm-draft-001" in serialized
    assert "BLOCKED_BENCHMARK_SCORING" in serialized
    assert "benchmark_scoring_allowed_from_provider" in serialized


def test_provider_plugin_seam_module_does_not_call_providers_or_score_benchmark():
    source = Path("src/eaios/sprint5/provider_plugin_seam.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "google.cloud" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
