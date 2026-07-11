from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_mcp_observation import (
    build_governed_mcp_observation_snapshot,
    summarize_governed_mcp_observation,
    to_view_model,
)


def _snapshot():
    return build_governed_mcp_observation_snapshot()


def test_governed_mcp_observation_builds_snapshot():
    snapshot = _snapshot()

    assert snapshot.snapshot_id == "governed-mcp-observation::composition-structural-001"
    assert snapshot.source_snapshot_id == "governed-reasoning::composition-structural-001"
    assert snapshot.provenance == "governed_mcp_observation:snapshot"


def test_governed_mcp_observation_includes_manifest_summary():
    snapshot = _snapshot()

    assert snapshot.manifest_summary["manifest_id"] == "it-application-health-governed-mcp-tools-v1"
    assert snapshot.manifest_summary["domain"] == "it_application_health"
    assert snapshot.manifest_summary["tool_count"] == 7
    assert snapshot.manifest_summary["human_approval_required"] is True
    assert snapshot.manifest_summary["autonomous_action_allowed"] is False
    assert snapshot.manifest_summary["benchmark_scoring_allowed_from_tool_output"] is False


def test_governed_mcp_observation_includes_execution_summary():
    snapshot = _snapshot()

    assert snapshot.execution_summary["plan_id"] == "sprint4c-governed-mcp-tool-execution-plan-001"
    assert snapshot.execution_summary["envelope_count"] == 4
    assert snapshot.execution_summary["validation_count"] == 4
    assert snapshot.execution_summary["allowed_count"] == 3
    assert snapshot.execution_summary["denied_count"] == 1
    assert snapshot.execution_summary["real_tool_execution_performed"] is False


def test_governed_mcp_observation_includes_evidence_summary():
    snapshot = _snapshot()

    assert snapshot.evidence_summary["integration_id"] == (
        "sprint4c-governed-mcp-tool-evidence-integration-001"
    )
    assert snapshot.evidence_summary["evidence_record_count"] == 4
    assert snapshot.evidence_summary["available_count"] == 3
    assert snapshot.evidence_summary["denied_count"] == 1
    assert snapshot.evidence_summary["degraded_count"] == 0
    assert snapshot.evidence_summary["real_tool_execution_performed"] is False


def test_governed_mcp_observation_includes_tool_catalog():
    snapshot = _snapshot()

    assert len(snapshot.tool_catalog) == 7

    tool_ids = {tool["tool_id"] for tool in snapshot.tool_catalog}

    assert "observability.telemetry.read" in tool_ids
    assert "cmdb.topology.read" in tool_ids
    assert "knowledge.search.read" in tool_ids
    assert "remediation.plan.propose" in tool_ids

    for tool in snapshot.tool_catalog:
        assert tool["requires_human_approval"] is True
        assert tool["autonomous_execution_allowed"] is False
        assert tool["benchmark_scoring_allowed"] is False
        assert tool["provenance_required"] is True


def test_governed_mcp_observation_records_denied_tool_calls():
    snapshot = _snapshot()

    assert len(snapshot.denied_tool_records) == 1

    denied = snapshot.denied_tool_records[0]

    assert denied["request_id"] == "mcp-request-denied-remediation-payment"
    assert denied["tool_id"] == "remediation.plan.propose"
    assert denied["operation"] == "restart_service"
    assert denied["evidence_state"] == "DENIED_RECORDED"
    assert denied["denied_reason_summary"] == "Operation is globally denied."
    assert denied["degraded_mode_reason"] == (
        "Tool denied; downstream reasoning must use degraded-mode evidence."
    )
    assert denied["human_approval_required"] is True
    assert denied["autonomous_execution_allowed"] is False
    assert denied["output_can_score_benchmark"] is False


def test_governed_mcp_observation_preserves_governance_boundaries():
    snapshot = _snapshot()

    assert "governed_mcp_tool_manifest_required" in snapshot.governance_boundaries
    assert "tool_request_envelope_required" in snapshot.governance_boundaries
    assert "permission_validation_required" in snapshot.governance_boundaries
    assert "provenance_required" in snapshot.governance_boundaries
    assert "audit_required" in snapshot.governance_boundaries
    assert "kill_switch_required" in snapshot.governance_boundaries
    assert "budget_check_required" in snapshot.governance_boundaries
    assert "degraded_mode_required" in snapshot.governance_boundaries
    assert "denied_tool_calls_recorded" in snapshot.governance_boundaries
    assert "real_tool_execution_blocked" in snapshot.governance_boundaries
    assert "tool_output_cannot_define_benchmark_truth" in snapshot.governance_boundaries
    assert "tool_output_cannot_score_benchmark" in snapshot.governance_boundaries
    assert "human_approval_required" in snapshot.governance_boundaries
    assert "autonomous_execution_disabled" in snapshot.governance_boundaries


def test_governed_mcp_observation_preserves_no_execution_no_truth_no_scoring():
    snapshot = _snapshot()

    assert snapshot.real_tool_execution_performed is False
    assert snapshot.human_approval_required is True
    assert snapshot.autonomous_execution_allowed is False
    assert snapshot.benchmark_scoring_allowed_from_tool_output is False
    assert snapshot.tool_output_can_define_benchmark_truth is False

    assert snapshot.execution_view["summary"]["real_tool_execution_performed"] is False
    assert snapshot.evidence_view["summary"]["real_tool_execution_performed"] is False


def test_governed_mcp_observation_summary_is_view_ready():
    snapshot = _snapshot()

    assert summarize_governed_mcp_observation(snapshot) == {
        "snapshot_id": "governed-mcp-observation::composition-structural-001",
        "source_snapshot_id": "governed-reasoning::composition-structural-001",
        "tool_count": 7,
        "envelope_count": 4,
        "validation_count": 4,
        "allowed_count": 3,
        "denied_count": 1,
        "evidence_record_count": 4,
        "available_evidence_count": 3,
        "denied_evidence_count": 1,
        "degraded_evidence_count": 0,
        "real_tool_execution_performed": False,
        "human_approval_required": True,
        "autonomous_execution_allowed": False,
        "benchmark_scoring_allowed_from_tool_output": False,
        "tool_output_can_define_benchmark_truth": False,
    }


def test_governed_mcp_observation_view_model_is_json_serializable():
    snapshot = _snapshot()

    serialized = json.dumps(to_view_model(snapshot), indent=2)

    assert "governed-mcp-observation::composition-structural-001" in serialized
    assert "governance_boundaries" in serialized
    assert "tool_catalog" in serialized
    assert "denied_tool_records" in serialized
    assert "manifest" in serialized
    assert "execution" in serialized
    assert "evidence" in serialized
    assert "real_tool_execution_performed" in serialized


def test_governed_mcp_observation_module_does_not_execute_real_tools_or_score_benchmark():
    source = Path("src/eaios/sprint4/governed_mcp_observation.py").read_text(
        encoding="utf-8"
    )

    assert "subprocess" not in source
    assert "import requests" not in source.lower()
    assert "import httpx" not in source.lower()
    assert "execute_tool(" not in source
    assert "restart_service(" not in source
    assert "score_benchmark_result(" not in source
