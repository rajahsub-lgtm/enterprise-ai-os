from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint5.mcp_connector_harness import (
    MCPConnectorHarnessMode,
    MCPConnectorSimulationState,
    build_mcp_connector_harness_profile,
    summarize_mcp_connector_harness_profile,
    to_view_model,
)


def _profile():
    return build_mcp_connector_harness_profile()


def test_mcp_connector_harness_profile_builds_from_provider_seam():
    profile = _profile()

    assert profile.profile_id == "sprint5-mcp-connector-harness-profile-001"
    assert profile.source_provider_profile_id == "sprint5-provider-plugin-seam-profile-001"
    assert profile.mode == MCPConnectorHarnessMode.READ_ONLY_SIMULATION
    assert profile.provenance == "mcp_connector_harness:simulation_profile"


def test_mcp_connector_harness_has_connector_definitions():
    profile = _profile()

    assert len(profile.connector_definitions) == 5

    connector_ids = tuple(connector.connector_id for connector in profile.connector_definitions)

    assert connector_ids == (
        "connector.observability.simulated",
        "connector.knowledge.simulated",
        "connector.remediation.disabled",
        "connector.notification.disabled",
        "connector.benchmark.disabled",
    )


def test_mcp_connector_harness_real_connectors_disabled():
    profile = _profile()

    for connector in profile.connector_definitions:
        assert connector.simulated is True
        assert connector.real_connector_enabled is False
        assert connector.provenance == "mcp_connector_harness:connector_definition"


def test_mcp_connector_harness_has_expected_simulation_requests():
    profile = _profile()

    assert len(profile.simulation_requests) == 5

    request_ids = tuple(request.request_id for request in profile.simulation_requests)

    assert request_ids == (
        "connector-request-observability-read-001",
        "connector-request-knowledge-search-001",
        "connector-request-remediation-001",
        "connector-request-notification-001",
        "connector-request-benchmark-score-001",
    )


def test_mcp_connector_harness_allows_only_read_only_simulated_requests():
    profile = _profile()

    allowed = [result for result in profile.simulation_results if result.allowed]

    assert len(allowed) == 2

    assert tuple(result.request_id for result in allowed) == (
        "connector-request-observability-read-001",
        "connector-request-knowledge-search-001",
    )

    for result in allowed:
        assert result.state == MCPConnectorSimulationState.SIMULATED_READ_ONLY_AVAILABLE
        assert result.simulated_output_ref == f"fixture::{result.request_id}"
        assert result.real_connector_called is False
        assert result.secret_loaded is False
        assert result.external_write_performed is False
        assert result.remediation_performed is False
        assert result.notification_sent is False
        assert result.benchmark_scoring_allowed is False
        assert result.human_review_required is True


def test_mcp_connector_harness_blocks_remediation_request():
    profile = _profile()

    result = next(
        item for item in profile.simulation_results
        if item.request_id == "connector-request-remediation-001"
    )

    assert result.allowed is False
    assert result.state == MCPConnectorSimulationState.BLOCKED_EXTERNAL_ACTION
    assert "external writes, remediation, and notifications" in result.reason
    assert result.remediation_performed is False


def test_mcp_connector_harness_blocks_notification_request():
    profile = _profile()

    result = next(
        item for item in profile.simulation_results
        if item.request_id == "connector-request-notification-001"
    )

    assert result.allowed is False
    assert result.state == MCPConnectorSimulationState.BLOCKED_EXTERNAL_ACTION
    assert result.notification_sent is False


def test_mcp_connector_harness_blocks_benchmark_scoring_request():
    profile = _profile()

    result = next(
        item for item in profile.simulation_results
        if item.request_id == "connector-request-benchmark-score-001"
    )

    assert result.allowed is False
    assert result.state == MCPConnectorSimulationState.BLOCKED_BENCHMARK_SCORING
    assert "cannot score benchmarks" in result.reason
    assert result.benchmark_scoring_allowed is False


def test_mcp_connector_harness_has_simulated_fixtures():
    profile = _profile()

    assert profile.simulated_fixtures == {
        "connector-request-observability-read-001": {
            "service": "payment-service",
            "signal": "latency_p95_ms",
            "mode": "simulated_read_only",
        },
        "connector-request-knowledge-search-001": {
            "query": "payment latency stale conflicting evidence",
            "mode": "simulated_read_only",
        },
    }


def test_mcp_connector_harness_preserves_blocked_capabilities():
    profile = _profile()

    assert profile.blocked_capabilities == (
        "real_connector_call",
        "secret_loading",
        "external_write",
        "remediation_execution",
        "notification_send",
        "benchmark_scoring_from_connector",
        "autonomous_remediation",
    )


def test_mcp_connector_harness_preserves_safety_controls():
    profile = _profile()

    assert profile.safety_controls == (
        "read_only_simulation_only",
        "real_connectors_disabled",
        "secrets_blocked",
        "external_writes_blocked",
        "remediation_blocked",
        "notifications_blocked",
        "benchmark_scoring_blocked",
        "human_review_required",
    )


def test_mcp_connector_harness_embeds_provider_seam_summary_and_view():
    profile = _profile()

    assert profile.provider_seam_summary["profile_id"] == (
        "sprint5-provider-plugin-seam-profile-001"
    )
    assert profile.provider_seam_summary["real_provider_call_performed"] is False

    assert profile.provider_seam_view["summary"]["profile_id"] == (
        "sprint5-provider-plugin-seam-profile-001"
    )
    assert profile.provider_seam_view["summary"]["benchmark_scoring_allowed_from_provider"] is False


def test_mcp_connector_harness_preserves_no_connector_execution_boundaries():
    profile = _profile()

    assert profile.real_connectors_allowed is False
    assert profile.real_connector_called is False
    assert profile.secrets_loaded is False
    assert profile.external_write_performed is False
    assert profile.remediation_performed is False
    assert profile.notification_sent is False
    assert profile.benchmark_scoring_allowed_from_connector is False
    assert profile.autonomous_remediation_allowed is False
    assert profile.human_review_required is True

    for result in profile.simulation_results:
        assert result.real_connector_called is False
        assert result.secret_loaded is False
        assert result.external_write_performed is False
        assert result.remediation_performed is False
        assert result.notification_sent is False
        assert result.benchmark_scoring_allowed is False
        assert result.human_review_required is True


def test_mcp_connector_harness_summary_is_view_ready():
    profile = _profile()

    assert summarize_mcp_connector_harness_profile(profile) == {
        "profile_id": "sprint5-mcp-connector-harness-profile-001",
        "source_provider_profile_id": "sprint5-provider-plugin-seam-profile-001",
        "mode": "READ_ONLY_SIMULATION",
        "connector_count": 5,
        "simulation_request_count": 5,
        "simulation_result_count": 5,
        "allowed_result_count": 2,
        "blocked_result_count": 3,
        "fixture_count": 2,
        "blocked_capability_count": 7,
        "safety_control_count": 8,
        "real_connectors_allowed": False,
        "real_connector_called": False,
        "secrets_loaded": False,
        "external_write_performed": False,
        "remediation_performed": False,
        "notification_sent": False,
        "benchmark_scoring_allowed_from_connector": False,
        "autonomous_remediation_allowed": False,
        "human_review_required": True,
    }


def test_mcp_connector_harness_view_model_is_json_serializable():
    profile = _profile()

    serialized = json.dumps(to_view_model(profile), indent=2)

    assert "sprint5-mcp-connector-harness-profile-001" in serialized
    assert "READ_ONLY_SIMULATION" in serialized
    assert "connector-request-remediation-001" in serialized
    assert "BLOCKED_BENCHMARK_SCORING" in serialized
    assert "benchmark_scoring_allowed_from_connector" in serialized


def test_mcp_connector_harness_module_does_not_call_connectors_or_score_benchmark():
    source = Path("src/eaios/sprint5/mcp_connector_harness.py").read_text(
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
