from pathlib import Path


CLOSEOUT = Path("docs/EAIOS_2_SPRINT_4C_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("data/domain/it_application_health/governed_mcp_tool_manifest.json"),
    Path("src/eaios/sprint4/governed_mcp_tool_manifest.py"),
    Path("src/eaios/sprint4/governed_mcp_tool_execution.py"),
    Path("src/eaios/sprint4/governed_mcp_tool_evidence.py"),
    Path("src/eaios/sprint4/governed_mcp_observation.py"),
    Path("tests/test_sprint4_governed_mcp_tool_manifest.py"),
    Path("tests/test_sprint4_governed_mcp_tool_execution.py"),
    Path("tests/test_sprint4_governed_mcp_tool_evidence.py"),
    Path("tests/test_sprint4_governed_mcp_observation.py"),
]


def _text() -> str:
    return CLOSEOUT.read_text(encoding="utf-8")


def test_sprint4_4c_closeout_file_exists():
    assert CLOSEOUT.exists()


def test_sprint4_4c_required_files_exist():
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    assert missing == []


def test_sprint4_4c_closeout_lists_completed_slices():
    text = _text()

    assert "4C-1 Governed MCP tool manifest and permission policy" in text
    assert "4C-2 MCP tool request envelope and execution validator" in text
    assert "4C-3 MCP tool result provenance and degraded evidence integration" in text
    assert "4C-4 Governed MCP observation snapshot" in text
    assert "4C-5 Closeout contract and architecture checkpoint" in text


def test_sprint4_4c_closeout_locks_layer_boundary():
    text = _text()

    assert "Layer 10: Governed MCP tool manifest" in text
    assert "Layer 11: MCP request envelope and permission validation" in text
    assert "Layer 12: MCP tool evidence and denied/degraded records" in text
    assert "Layer 13: Governed MCP observation snapshot" in text


def test_sprint4_4c_closeout_states_core_thesis():
    text = _text()

    assert "Tools may extend context." in text
    assert "Tools cannot act silently." in text
    assert "Tools cannot remediate autonomously." in text
    assert "Tools cannot define benchmark truth." in text
    assert "Tools cannot score benchmark results." in text
    assert "Denied tool calls are first-class evidence." in text
    assert "Human approval remains required." in text


def test_sprint4_4c_closeout_documents_tool_modes():
    text = _text()

    assert "read_only" in text
    assert "proposal_only" in text
    assert "draft_only" in text


def test_sprint4_4c_closeout_documents_manifest_contract():
    text = _text()

    assert "GovernedMCPTool" in text
    assert "GovernedMCPToolManifest" in text
    assert "MCPToolRequest" in text
    assert "MCPToolPermissionResult" in text
    assert "ToolAccessMode" in text
    assert "ToolPermissionDecision" in text


def test_sprint4_4c_closeout_documents_manifest_policy():
    text = _text()

    assert "real_tool_execution_allowed = false" in text
    assert "autonomous_action_allowed = false" in text
    assert "human_approval_required = true" in text
    assert "benchmark_scoring_allowed_from_tool_output = false" in text
    assert "tool_output_can_define_benchmark_truth = false" in text
    assert "provenance_required = true" in text
    assert "audit_required = true" in text
    assert "kill_switch_required = true" in text


def test_sprint4_4c_closeout_documents_tool_catalog():
    text = _text()

    assert "observability.telemetry.read" in text
    assert "cmdb.topology.read" in text
    assert "incident.records.read" in text
    assert "knowledge.search.read" in text
    assert "change.context.read" in text
    assert "remediation.plan.propose" in text
    assert "notification.draft.prepare" in text


def test_sprint4_4c_closeout_documents_globally_denied_operations():
    text = _text()

    assert "execute_remediation" in text
    assert "restart_service" in text
    assert "scale_service" in text
    assert "modify_database" in text
    assert "deploy_code" in text
    assert "rollback_change" in text
    assert "send_email" in text
    assert "send_chat" in text
    assert "page_on_call" in text
    assert "publish_status_page" in text
    assert "score_benchmark_from_tool_output" in text


def test_sprint4_4c_closeout_documents_request_envelope():
    text = _text()

    assert "request_id" in text
    assert "tool_id" in text
    assert "operation" in text
    assert "cluster_id" in text
    assert "source_failure_case_id" in text
    assert "human_approval_required" in text
    assert "autonomous_execution_requested" in text
    assert "benchmark_scoring_requested" in text


def test_sprint4_4c_closeout_documents_execution_validation_boundary():
    text = _text()

    assert "MCPToolExecutionValidation" in text
    assert "MCPToolExecutionValidationPlan" in text
    assert "MCPExecutionState" in text
    assert "VALIDATED_ALLOWED_SIMULATED" in text
    assert "VALIDATED_DENIED" in text
    assert "No request becomes real execution." in text


def test_sprint4_4c_closeout_documents_tool_evidence_contract():
    text = _text()

    assert "MCPToolEvidenceRecord" in text
    assert "MCPToolEvidenceIntegration" in text
    assert "MCPToolEvidenceState" in text
    assert "AVAILABLE_SIMULATED" in text
    assert "DENIED_RECORDED" in text
    assert "DEGRADED_MODE" in text


def test_sprint4_4c_closeout_documents_observation_snapshot():
    text = _text()

    assert "GovernedMCPObservationSnapshot" in text
    assert "manifest_summary" in text
    assert "execution_summary" in text
    assert "evidence_summary" in text
    assert "tool_catalog" in text
    assert "denied_tool_records" in text


def test_sprint4_4c_closeout_preserves_governance_boundaries():
    text = _text()

    assert "governed_mcp_tool_manifest_required" in text
    assert "tool_request_envelope_required" in text
    assert "permission_validation_required" in text
    assert "provenance_required" in text
    assert "audit_required" in text
    assert "kill_switch_required" in text
    assert "degraded_mode_required" in text
    assert "denied_tool_calls_recorded" in text
    assert "real_tool_execution_blocked" in text
    assert "tool_output_cannot_define_benchmark_truth" in text
    assert "tool_output_cannot_score_benchmark" in text
    assert "autonomous_execution_disabled" in text


def test_sprint4_4c_closeout_preserves_benchmark_separation():
    text = _text()

    assert "Tool output cannot define benchmark truth." in text
    assert "Tool output cannot score benchmark results." in text
    assert "Tool output cannot replace BenchmarkVerificationTarget." in text
    assert "Tool output cannot replace BenchmarkVerificationResult." in text
    assert "Denied tool calls cannot change benchmark scoring." in text
    assert "Degraded-mode evidence cannot change benchmark scoring." in text


def test_sprint4_4c_closeout_sets_4d_entry_criteria():
    text = _text()

    assert "governed MCP manifest" in text
    assert "tool permission policy" in text
    assert "tool request envelope" in text
    assert "permission validator" in text
    assert "denied request record" in text
    assert "degraded-mode evidence" in text
    assert "MCP observation snapshot" in text
    assert "no-real-execution boundary" in text


def test_sprint4_4c_closeout_defines_4d_direction():
    text = _text()

    assert "cross-cluster orchestration plan" in text
    assert "restoration candidate package" in text
    assert "human approval packet" in text
    assert "risk and rollback notes" in text
    assert "operator decision record" in text
    assert "safe restoration state machine" in text
    assert "A2A-style coordination contract" in text
    assert "restoration dashboard view" in text
