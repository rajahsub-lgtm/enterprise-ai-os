"""Sprint 5 MCP connector simulation harness.

This module defines a read-only simulation harness for future MCP/tool
connectors.

It does not connect to real systems, call providers, load secrets, execute
tools, execute remediation, send notifications, update benchmark truth, score
benchmarks, or enable autonomous remediation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from eaios.sprint5.provider_plugin_seam import (
    ProviderPluginSeamProfile,
    build_provider_plugin_seam_profile,
    summarize_provider_plugin_seam_profile,
    to_view_model as provider_seam_to_view_model,
)


class MCPConnectorHarnessMode(str, Enum):
    READ_ONLY_SIMULATION = "READ_ONLY_SIMULATION"
    REAL_CONNECTORS_DISABLED = "REAL_CONNECTORS_DISABLED"


class MCPConnectorKind(str, Enum):
    OBSERVABILITY = "OBSERVABILITY"
    CMDB = "CMDB"
    ITSM = "ITSM"
    KNOWLEDGE = "KNOWLEDGE"
    CHANGE = "CHANGE"
    NOTIFICATION = "NOTIFICATION"
    REMEDIATION = "REMEDIATION"


class MCPConnectorRequestType(str, Enum):
    READ_CONTEXT = "READ_CONTEXT"
    SEARCH_KNOWLEDGE = "SEARCH_KNOWLEDGE"
    PROPOSE_REMEDIATION = "PROPOSE_REMEDIATION"
    SEND_NOTIFICATION = "SEND_NOTIFICATION"
    SCORE_BENCHMARK = "SCORE_BENCHMARK"


class MCPConnectorSimulationState(str, Enum):
    SIMULATED_READ_ONLY_AVAILABLE = "SIMULATED_READ_ONLY_AVAILABLE"
    BLOCKED_REAL_CONNECTOR_DISABLED = "BLOCKED_REAL_CONNECTOR_DISABLED"
    BLOCKED_EXTERNAL_ACTION = "BLOCKED_EXTERNAL_ACTION"
    BLOCKED_BENCHMARK_SCORING = "BLOCKED_BENCHMARK_SCORING"


@dataclass(frozen=True)
class MCPConnectorDefinition:
    connector_id: str
    kind: MCPConnectorKind
    display_name: str
    simulated: bool
    real_connector_enabled: bool
    requires_secret: bool
    can_read_context: bool
    can_write_external_system: bool
    can_execute_remediation: bool
    can_send_notification: bool
    can_score_benchmark: bool
    provenance: str


@dataclass(frozen=True)
class MCPConnectorSimulationRequest:
    request_id: str
    connector_id: str
    request_type: MCPConnectorRequestType
    purpose: str
    read_only: bool
    asks_for_real_connector: bool
    asks_for_external_write: bool
    asks_for_remediation: bool
    asks_for_notification: bool
    asks_to_score_benchmark: bool
    provenance: str


@dataclass(frozen=True)
class MCPConnectorSimulationResult:
    result_id: str
    request_id: str
    connector_id: str
    request_type: MCPConnectorRequestType
    state: MCPConnectorSimulationState
    allowed: bool
    simulated_output_ref: str
    reason: str
    real_connector_called: bool
    secret_loaded: bool
    external_write_performed: bool
    remediation_performed: bool
    notification_sent: bool
    benchmark_scoring_allowed: bool
    human_review_required: bool
    provenance: str


@dataclass(frozen=True)
class MCPConnectorHarnessProfile:
    profile_id: str
    source_provider_profile_id: str
    mode: MCPConnectorHarnessMode
    connector_definitions: tuple[MCPConnectorDefinition, ...]
    simulation_requests: tuple[MCPConnectorSimulationRequest, ...]
    simulation_results: tuple[MCPConnectorSimulationResult, ...]
    simulated_fixtures: dict[str, dict[str, object]]
    blocked_capabilities: tuple[str, ...]
    safety_controls: tuple[str, ...]
    provider_seam_summary: dict[str, object]
    provider_seam_view: dict[str, Any]
    real_connectors_allowed: bool
    real_connector_called: bool
    secrets_loaded: bool
    external_write_performed: bool
    remediation_performed: bool
    notification_sent: bool
    benchmark_scoring_allowed_from_connector: bool
    autonomous_remediation_allowed: bool
    human_review_required: bool
    provenance: str


def build_mcp_connector_harness_profile(
    provider_profile: ProviderPluginSeamProfile | None = None,
) -> MCPConnectorHarnessProfile:
    if provider_profile is None:
        provider_profile = build_provider_plugin_seam_profile()

    connectors = _build_connector_definitions()
    requests = _build_simulation_requests()
    connector_by_id = {connector.connector_id: connector for connector in connectors}
    results = tuple(
        _simulate_request(connector_by_id[request.connector_id], request)
        for request in requests
    )

    return MCPConnectorHarnessProfile(
        profile_id="sprint5-mcp-connector-harness-profile-001",
        source_provider_profile_id=provider_profile.profile_id,
        mode=MCPConnectorHarnessMode.READ_ONLY_SIMULATION,
        connector_definitions=connectors,
        simulation_requests=requests,
        simulation_results=results,
        simulated_fixtures={
            "connector-request-observability-read-001": {
                "service": "payment-service",
                "signal": "latency_p95_ms",
                "mode": "simulated_read_only",
            },
            "connector-request-knowledge-search-001": {
                "query": "payment latency stale conflicting evidence",
                "mode": "simulated_read_only",
            },
        },
        blocked_capabilities=(
            "real_connector_call",
            "secret_loading",
            "external_write",
            "remediation_execution",
            "notification_send",
            "benchmark_scoring_from_connector",
            "autonomous_remediation",
        ),
        safety_controls=(
            "read_only_simulation_only",
            "real_connectors_disabled",
            "secrets_blocked",
            "external_writes_blocked",
            "remediation_blocked",
            "notifications_blocked",
            "benchmark_scoring_blocked",
            "human_review_required",
        ),
        provider_seam_summary=summarize_provider_plugin_seam_profile(provider_profile),
        provider_seam_view=provider_seam_to_view_model(provider_profile),
        real_connectors_allowed=False,
        real_connector_called=False,
        secrets_loaded=False,
        external_write_performed=False,
        remediation_performed=False,
        notification_sent=False,
        benchmark_scoring_allowed_from_connector=False,
        autonomous_remediation_allowed=False,
        human_review_required=True,
        provenance="mcp_connector_harness:simulation_profile",
    )


def summarize_mcp_connector_harness_profile(
    profile: MCPConnectorHarnessProfile,
) -> dict[str, object]:
    return {
        "profile_id": profile.profile_id,
        "source_provider_profile_id": profile.source_provider_profile_id,
        "mode": profile.mode.value,
        "connector_count": len(profile.connector_definitions),
        "simulation_request_count": len(profile.simulation_requests),
        "simulation_result_count": len(profile.simulation_results),
        "allowed_result_count": len(
            [result for result in profile.simulation_results if result.allowed]
        ),
        "blocked_result_count": len(
            [result for result in profile.simulation_results if not result.allowed]
        ),
        "fixture_count": len(profile.simulated_fixtures),
        "blocked_capability_count": len(profile.blocked_capabilities),
        "safety_control_count": len(profile.safety_controls),
        "real_connectors_allowed": profile.real_connectors_allowed,
        "real_connector_called": profile.real_connector_called,
        "secrets_loaded": profile.secrets_loaded,
        "external_write_performed": profile.external_write_performed,
        "remediation_performed": profile.remediation_performed,
        "notification_sent": profile.notification_sent,
        "benchmark_scoring_allowed_from_connector": (
            profile.benchmark_scoring_allowed_from_connector
        ),
        "autonomous_remediation_allowed": profile.autonomous_remediation_allowed,
        "human_review_required": profile.human_review_required,
    }


def to_view_model(profile: MCPConnectorHarnessProfile) -> dict[str, Any]:
    return {
        "summary": summarize_mcp_connector_harness_profile(profile),
        "connector_definitions": [
            {
                "connector_id": connector.connector_id,
                "kind": connector.kind.value,
                "display_name": connector.display_name,
                "simulated": connector.simulated,
                "real_connector_enabled": connector.real_connector_enabled,
                "requires_secret": connector.requires_secret,
                "can_read_context": connector.can_read_context,
                "can_write_external_system": connector.can_write_external_system,
                "can_execute_remediation": connector.can_execute_remediation,
                "can_send_notification": connector.can_send_notification,
                "can_score_benchmark": connector.can_score_benchmark,
                "provenance": connector.provenance,
            }
            for connector in profile.connector_definitions
        ],
        "simulation_requests": [
            {
                "request_id": request.request_id,
                "connector_id": request.connector_id,
                "request_type": request.request_type.value,
                "purpose": request.purpose,
                "read_only": request.read_only,
                "asks_for_real_connector": request.asks_for_real_connector,
                "asks_for_external_write": request.asks_for_external_write,
                "asks_for_remediation": request.asks_for_remediation,
                "asks_for_notification": request.asks_for_notification,
                "asks_to_score_benchmark": request.asks_to_score_benchmark,
                "provenance": request.provenance,
            }
            for request in profile.simulation_requests
        ],
        "simulation_results": [
            {
                "result_id": result.result_id,
                "request_id": result.request_id,
                "connector_id": result.connector_id,
                "request_type": result.request_type.value,
                "state": result.state.value,
                "allowed": result.allowed,
                "simulated_output_ref": result.simulated_output_ref,
                "reason": result.reason,
                "real_connector_called": result.real_connector_called,
                "secret_loaded": result.secret_loaded,
                "external_write_performed": result.external_write_performed,
                "remediation_performed": result.remediation_performed,
                "notification_sent": result.notification_sent,
                "benchmark_scoring_allowed": result.benchmark_scoring_allowed,
                "human_review_required": result.human_review_required,
                "provenance": result.provenance,
            }
            for result in profile.simulation_results
        ],
        "simulated_fixtures": profile.simulated_fixtures,
        "blocked_capabilities": list(profile.blocked_capabilities),
        "safety_controls": list(profile.safety_controls),
        "provider_seam_summary": profile.provider_seam_summary,
        "provider_seam_view": profile.provider_seam_view,
        "real_connectors_allowed": profile.real_connectors_allowed,
        "real_connector_called": profile.real_connector_called,
        "secrets_loaded": profile.secrets_loaded,
        "external_write_performed": profile.external_write_performed,
        "remediation_performed": profile.remediation_performed,
        "notification_sent": profile.notification_sent,
        "benchmark_scoring_allowed_from_connector": (
            profile.benchmark_scoring_allowed_from_connector
        ),
        "autonomous_remediation_allowed": profile.autonomous_remediation_allowed,
        "human_review_required": profile.human_review_required,
        "provenance": profile.provenance,
    }


def _build_connector_definitions() -> tuple[MCPConnectorDefinition, ...]:
    return (
        MCPConnectorDefinition(
            connector_id="connector.observability.simulated",
            kind=MCPConnectorKind.OBSERVABILITY,
            display_name="Simulated observability connector",
            simulated=True,
            real_connector_enabled=False,
            requires_secret=False,
            can_read_context=True,
            can_write_external_system=False,
            can_execute_remediation=False,
            can_send_notification=False,
            can_score_benchmark=False,
            provenance="mcp_connector_harness:connector_definition",
        ),
        MCPConnectorDefinition(
            connector_id="connector.knowledge.simulated",
            kind=MCPConnectorKind.KNOWLEDGE,
            display_name="Simulated knowledge connector",
            simulated=True,
            real_connector_enabled=False,
            requires_secret=False,
            can_read_context=True,
            can_write_external_system=False,
            can_execute_remediation=False,
            can_send_notification=False,
            can_score_benchmark=False,
            provenance="mcp_connector_harness:connector_definition",
        ),
        MCPConnectorDefinition(
            connector_id="connector.remediation.disabled",
            kind=MCPConnectorKind.REMEDIATION,
            display_name="Disabled remediation connector",
            simulated=True,
            real_connector_enabled=False,
            requires_secret=True,
            can_read_context=False,
            can_write_external_system=True,
            can_execute_remediation=True,
            can_send_notification=False,
            can_score_benchmark=False,
            provenance="mcp_connector_harness:connector_definition",
        ),
        MCPConnectorDefinition(
            connector_id="connector.notification.disabled",
            kind=MCPConnectorKind.NOTIFICATION,
            display_name="Disabled notification connector",
            simulated=True,
            real_connector_enabled=False,
            requires_secret=True,
            can_read_context=False,
            can_write_external_system=True,
            can_execute_remediation=False,
            can_send_notification=True,
            can_score_benchmark=False,
            provenance="mcp_connector_harness:connector_definition",
        ),
        MCPConnectorDefinition(
            connector_id="connector.benchmark.disabled",
            kind=MCPConnectorKind.CMDB,
            display_name="Disabled benchmark scoring connector",
            simulated=True,
            real_connector_enabled=False,
            requires_secret=False,
            can_read_context=False,
            can_write_external_system=False,
            can_execute_remediation=False,
            can_send_notification=False,
            can_score_benchmark=True,
            provenance="mcp_connector_harness:connector_definition",
        ),
    )


def _build_simulation_requests() -> tuple[MCPConnectorSimulationRequest, ...]:
    return (
        MCPConnectorSimulationRequest(
            request_id="connector-request-observability-read-001",
            connector_id="connector.observability.simulated",
            request_type=MCPConnectorRequestType.READ_CONTEXT,
            purpose="Read simulated payment latency context.",
            read_only=True,
            asks_for_real_connector=False,
            asks_for_external_write=False,
            asks_for_remediation=False,
            asks_for_notification=False,
            asks_to_score_benchmark=False,
            provenance="mcp_connector_harness:simulation_request",
        ),
        MCPConnectorSimulationRequest(
            request_id="connector-request-knowledge-search-001",
            connector_id="connector.knowledge.simulated",
            request_type=MCPConnectorRequestType.SEARCH_KNOWLEDGE,
            purpose="Search simulated governed knowledge context.",
            read_only=True,
            asks_for_real_connector=False,
            asks_for_external_write=False,
            asks_for_remediation=False,
            asks_for_notification=False,
            asks_to_score_benchmark=False,
            provenance="mcp_connector_harness:simulation_request",
        ),
        MCPConnectorSimulationRequest(
            request_id="connector-request-remediation-001",
            connector_id="connector.remediation.disabled",
            request_type=MCPConnectorRequestType.PROPOSE_REMEDIATION,
            purpose="Attempt remediation through connector harness.",
            read_only=False,
            asks_for_real_connector=True,
            asks_for_external_write=True,
            asks_for_remediation=True,
            asks_for_notification=False,
            asks_to_score_benchmark=False,
            provenance="mcp_connector_harness:simulation_request",
        ),
        MCPConnectorSimulationRequest(
            request_id="connector-request-notification-001",
            connector_id="connector.notification.disabled",
            request_type=MCPConnectorRequestType.SEND_NOTIFICATION,
            purpose="Attempt notification through connector harness.",
            read_only=False,
            asks_for_real_connector=True,
            asks_for_external_write=True,
            asks_for_remediation=False,
            asks_for_notification=True,
            asks_to_score_benchmark=False,
            provenance="mcp_connector_harness:simulation_request",
        ),
        MCPConnectorSimulationRequest(
            request_id="connector-request-benchmark-score-001",
            connector_id="connector.benchmark.disabled",
            request_type=MCPConnectorRequestType.SCORE_BENCHMARK,
            purpose="Attempt benchmark scoring through connector harness.",
            read_only=False,
            asks_for_real_connector=False,
            asks_for_external_write=False,
            asks_for_remediation=False,
            asks_for_notification=False,
            asks_to_score_benchmark=True,
            provenance="mcp_connector_harness:simulation_request",
        ),
    )


def _simulate_request(
    connector: MCPConnectorDefinition,
    request: MCPConnectorSimulationRequest,
) -> MCPConnectorSimulationResult:
    if request.asks_to_score_benchmark or connector.can_score_benchmark:
        return _blocked_result(
            request,
            MCPConnectorSimulationState.BLOCKED_BENCHMARK_SCORING,
            "Connector harness cannot score benchmarks or change benchmark truth.",
        )

    if (
        request.asks_for_external_write
        or request.asks_for_remediation
        or request.asks_for_notification
        or connector.can_write_external_system
        or connector.can_execute_remediation
        or connector.can_send_notification
    ):
        return _blocked_result(
            request,
            MCPConnectorSimulationState.BLOCKED_EXTERNAL_ACTION,
            "Connector harness blocks external writes, remediation, and notifications.",
        )

    if request.asks_for_real_connector or connector.real_connector_enabled:
        return _blocked_result(
            request,
            MCPConnectorSimulationState.BLOCKED_REAL_CONNECTOR_DISABLED,
            "Real connectors are disabled by default.",
        )

    return MCPConnectorSimulationResult(
        result_id=f"connector-simulation::{request.request_id}",
        request_id=request.request_id,
        connector_id=request.connector_id,
        request_type=request.request_type,
        state=MCPConnectorSimulationState.SIMULATED_READ_ONLY_AVAILABLE,
        allowed=True,
        simulated_output_ref=f"fixture::{request.request_id}",
        reason="Read-only simulated connector output is available.",
        real_connector_called=False,
        secret_loaded=False,
        external_write_performed=False,
        remediation_performed=False,
        notification_sent=False,
        benchmark_scoring_allowed=False,
        human_review_required=True,
        provenance="mcp_connector_harness:simulation_result",
    )


def _blocked_result(
    request: MCPConnectorSimulationRequest,
    state: MCPConnectorSimulationState,
    reason: str,
) -> MCPConnectorSimulationResult:
    return MCPConnectorSimulationResult(
        result_id=f"connector-simulation::{request.request_id}",
        request_id=request.request_id,
        connector_id=request.connector_id,
        request_type=request.request_type,
        state=state,
        allowed=False,
        simulated_output_ref="",
        reason=reason,
        real_connector_called=False,
        secret_loaded=False,
        external_write_performed=False,
        remediation_performed=False,
        notification_sent=False,
        benchmark_scoring_allowed=False,
        human_review_required=True,
        provenance="mcp_connector_harness:simulation_result",
    )
