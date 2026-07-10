from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_mcp_tool_evidence import (
    MCPToolEvidenceState,
    build_governed_mcp_tool_evidence_integration,
    summarize_tool_evidence_integration,
    to_view_model,
)


def _integration():
    return build_governed_mcp_tool_evidence_integration()


def test_tool_evidence_integration_builds_from_execution_plan():
    integration = _integration()

    assert integration.integration_id == (
        "sprint4c-governed-mcp-tool-evidence-integration-001"
    )
    assert integration.source_plan_id == "sprint4c-governed-mcp-tool-execution-plan-001"
    assert integration.source_snapshot_id == "governed-reasoning::composition-structural-001"
    assert len(integration.evidence_records) == 4


def test_tool_evidence_integration_counts_available_and_denied_records():
    integration = _integration()

    assert integration.available_count == 3
    assert integration.denied_count == 1
    assert integration.degraded_count == 0

    states = tuple(record.evidence_state for record in integration.evidence_records)

    assert states.count(MCPToolEvidenceState.AVAILABLE_SIMULATED) == 3
    assert states.count(MCPToolEvidenceState.DENIED_RECORDED) == 1


def test_available_tool_evidence_records_are_simulated_and_usable():
    integration = _integration()

    available = [
        record for record in integration.evidence_records
        if record.evidence_state == MCPToolEvidenceState.AVAILABLE_SIMULATED
    ]

    assert len(available) == 3

    for record in available:
        assert record.usable_for_reasoning is True
        assert record.real_tool_execution_performed is False
        assert "no real execution performed" in record.evidence_summary
        assert record.denied_reason_summary is None
        assert record.degraded_mode_reason is None


def test_denied_tool_evidence_record_is_available_for_degraded_reasoning():
    integration = _integration()

    denied = next(
        record for record in integration.evidence_records
        if record.evidence_state == MCPToolEvidenceState.DENIED_RECORDED
    )

    assert denied.request_id == "mcp-request-denied-remediation-payment"
    assert denied.tool_id == "remediation.plan.propose"
    assert denied.operation == "restart_service"
    assert denied.usable_for_reasoning is True
    assert denied.denied_reason_summary == "Operation is globally denied."
    assert denied.degraded_mode_reason == (
        "Tool denied; downstream reasoning must use degraded-mode evidence."
    )
    assert "denial recorded for governance" in denied.evidence_summary


def test_tool_evidence_records_preserve_provenance_chain():
    integration = _integration()

    for record in integration.evidence_records:
        assert record.provenance_chain[0] == "governed-reasoning::composition-structural-001"
        assert record.provenance_chain[1] == "sprint4c-governed-mcp-tool-execution-plan-001"
        assert record.provenance_chain[2] == record.envelope_id
        assert record.provenance_chain[3] == record.request_id
        assert record.provenance_chain[4] == "governed_mcp_tool_execution:validation_only"
        assert "provenance_preserved:true" in record.audit_events


def test_tool_evidence_records_preserve_no_truth_no_scoring_boundary():
    integration = _integration()

    assert integration.real_tool_execution_performed is False
    assert integration.human_approval_required is True
    assert integration.autonomous_execution_allowed is False
    assert integration.benchmark_scoring_allowed_from_tool_output is False

    for record in integration.evidence_records:
        assert record.output_can_define_benchmark_truth is False
        assert record.output_can_score_benchmark is False
        assert record.human_approval_required is True
        assert record.autonomous_execution_allowed is False
        assert record.real_tool_execution_performed is False


def test_tool_evidence_integration_summary_is_view_ready():
    integration = _integration()

    assert summarize_tool_evidence_integration(integration) == {
        "integration_id": "sprint4c-governed-mcp-tool-evidence-integration-001",
        "source_plan_id": "sprint4c-governed-mcp-tool-execution-plan-001",
        "source_snapshot_id": "governed-reasoning::composition-structural-001",
        "evidence_record_count": 4,
        "available_count": 3,
        "denied_count": 1,
        "degraded_count": 0,
        "real_tool_execution_performed": False,
        "human_approval_required": True,
        "autonomous_execution_allowed": False,
        "benchmark_scoring_allowed_from_tool_output": False,
        "evidence_states": (
            "AVAILABLE_SIMULATED",
            "AVAILABLE_SIMULATED",
            "AVAILABLE_SIMULATED",
            "DENIED_RECORDED",
        ),
    }


def test_tool_evidence_view_model_is_json_serializable():
    integration = _integration()

    serialized = json.dumps(to_view_model(integration), indent=2)

    assert "sprint4c-governed-mcp-tool-evidence-integration-001" in serialized
    assert "mcp-tool-evidence::mcp-request-read-telemetry-payment" in serialized
    assert "mcp-tool-evidence::mcp-request-denied-remediation-payment" in serialized
    assert "AVAILABLE_SIMULATED" in serialized
    assert "DENIED_RECORDED" in serialized
    assert "benchmark_scoring_allowed_from_tool_output" in serialized


def test_tool_evidence_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_mcp_tool_evidence.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
