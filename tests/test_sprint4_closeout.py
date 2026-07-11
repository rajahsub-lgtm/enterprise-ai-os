from pathlib import Path


CLOSEOUT = Path("docs/EAIOS_2_SPRINT_4_CLOSEOUT.md")

REQUIRED_CLOSEOUT_DOCS = [
    Path("docs/EAIOS_2_SPRINT_4A_CLOSEOUT.md"),
    Path("docs/EAIOS_2_SPRINT_4B_CLOSEOUT.md"),
    Path("docs/EAIOS_2_SPRINT_4C_CLOSEOUT.md"),
    Path("docs/EAIOS_2_SPRINT_4D_CLOSEOUT.md"),
    Path("docs/EAIOS_2_SPRINT_4E_CLOSEOUT.md"),
    Path("docs/EAIOS_2_SPRINT_4_CLOSEOUT.md"),
]

REQUIRED_SOURCE_FILES = [
    Path("src/eaios/sprint4/rcaeval_contracts.py"),
    Path("src/eaios/sprint4/itil_synthesizer.py"),
    Path("src/eaios/sprint4/issue_clustering.py"),
    Path("src/eaios/sprint4/application_health_observation.py"),
    Path("src/eaios/sprint4/governed_knowledge_base.py"),
    Path("src/eaios/sprint4/cluster_knowledge_evidence.py"),
    Path("src/eaios/sprint4/governed_knowledge_reasoning.py"),
    Path("src/eaios/sprint4/governed_llm_output_validator.py"),
    Path("src/eaios/sprint4/governed_llm_reasoning_engine.py"),
    Path("src/eaios/sprint4/governed_reasoning_observation.py"),
    Path("src/eaios/sprint4/governed_mcp_tool_manifest.py"),
    Path("src/eaios/sprint4/governed_mcp_tool_execution.py"),
    Path("src/eaios/sprint4/governed_mcp_tool_evidence.py"),
    Path("src/eaios/sprint4/governed_mcp_observation.py"),
    Path("src/eaios/sprint4/governed_restoration_orchestration.py"),
    Path("src/eaios/sprint4/governed_restoration_approval_packet.py"),
    Path("src/eaios/sprint4/governed_restoration_decision.py"),
    Path("src/eaios/sprint4/governed_restoration_observation.py"),
    Path("src/eaios/sprint4/governed_collective_learning.py"),
    Path("src/eaios/sprint4/governed_learning_improvement.py"),
    Path("src/eaios/sprint4/governed_learning_dashboard.py"),
]


def _text() -> str:
    return CLOSEOUT.read_text(encoding="utf-8")


def test_sprint4_final_closeout_file_exists():
    assert CLOSEOUT.exists()


def test_sprint4_final_closeout_docs_exist():
    missing = [str(path) for path in REQUIRED_CLOSEOUT_DOCS if not path.exists()]
    assert missing == []


def test_sprint4_final_source_files_exist():
    missing = [str(path) for path in REQUIRED_SOURCE_FILES if not path.exists()]
    assert missing == []


def test_sprint4_final_closeout_states_main_thesis():
    text = _text()

    assert "EAIOS reasons over and governs knowledge and records" in text
    assert "restore application health and learn" in text
    assert "verifiable against an external benchmark" in text


def test_sprint4_final_closeout_lists_all_sub_sprints():
    text = _text()

    assert "4A Benchmark-grounded environment and observation" in text
    assert "4B Governed KB and LLM reasoning boundary" in text
    assert "4C Governed MCP/tool boundary" in text
    assert "4D Governed restoration orchestration boundary" in text
    assert "4E Governed collective learning and dashboard improvement" in text


def test_sprint4_final_closeout_documents_complete_layer_stack():
    text = _text()

    assert "Layer 0: RCAEval / Train Ticket benchmark truth layer" in text
    assert "Layer 4: Benchmark verification result" in text
    assert "Layer 8: Provider-neutral LLM reasoning engine seam" in text
    assert "Layer 13: Governed MCP observation snapshot" in text
    assert "Layer 17: Governed restoration observation snapshot" in text
    assert "Layer 20: Governed learning dashboard snapshot" in text


def test_sprint4_final_closeout_documents_4a_result():
    text = _text()

    assert "RCAEval / Train Ticket source manifest" in text
    assert "synthetic ITIL records" in text
    assert "application health observation snapshot" in text
    assert "Benchmark truth is external." in text
    assert "Knowledge and LLM output do not define the answer key." in text


def test_sprint4_final_closeout_documents_4b_result():
    text = _text()

    assert "governed imperfect knowledge base" in text
    assert "LLM output validation" in text
    assert "provider-neutral LLM reasoning engine seam" in text
    assert "LLM output cannot score benchmarks." in text
    assert "LLM output cannot authorize autonomous remediation." in text


def test_sprint4_final_closeout_documents_4c_result():
    text = _text()

    assert "governed MCP tool manifest" in text
    assert "tool evidence integration" in text
    assert "denied/degraded evidence records" in text
    assert "Tools cannot silently act." in text
    assert "Denied tool calls are evidence." in text


def test_sprint4_final_closeout_documents_4d_result():
    text = _text()

    assert "cross-cluster restoration plan" in text
    assert "human approval packet" in text
    assert "safe restoration state machine" in text
    assert "Restoration cannot be executed autonomously." in text
    assert "Manual execution only remains distinct from autonomous execution." in text


def test_sprint4_final_closeout_documents_4e_result():
    text = _text()

    assert "operator feedback records" in text
    assert "decision outcome history" in text
    assert "review-only improvement queue" in text
    assert "Learning cannot update benchmark truth." in text
    assert "Dashboard changes are not applied automatically." in text


def test_sprint4_final_closeout_documents_end_to_end_flow():
    text = _text()

    assert "RCAEval / Train Ticket benchmark source" in text
    assert "-> governed KB retrieval" in text
    assert "-> governed MCP observation" in text
    assert "-> human approval packet" in text
    assert "-> governed learning dashboard" in text


def test_sprint4_final_closeout_preserves_anti_circularity_boundary():
    text = _text()

    assert "Synthetic generation cannot invent benchmark-scored labels." in text
    assert "Knowledge base content cannot become the answer key." in text
    assert "LLM output cannot become the answer key." in text
    assert "Tool output cannot become the answer key." in text
    assert "Restoration output cannot become the answer key." in text
    assert "Learning output cannot become the answer key." in text
    assert "Dashboard output cannot become the answer key." in text


def test_sprint4_final_closeout_locks_governance_boundaries():
    text = _text()

    assert "human_approval_required" in text
    assert "autonomous_remediation_disabled" in text
    assert "real_tool_execution_blocked" in text
    assert "benchmark_truth_external" in text
    assert "benchmark_scoring_from_llm_blocked" in text
    assert "benchmark_scoring_from_tool_output_blocked" in text
    assert "benchmark_scoring_from_learning_blocked" in text
    assert "review_only_improvement_candidates" in text
    assert "production_knowledge_auto_approval_blocked" in text


def test_sprint4_final_closeout_states_what_system_demonstrates():
    text = _text()

    assert "observe application-health failure scenarios" in text
    assert "map symptoms into governed operating records" in text
    assert "reason over imperfect knowledge" in text
    assert "govern tool access" in text
    assert "orchestrate restoration candidates" in text
    assert "capture feedback" in text
    assert "show before/after dashboard candidates" in text


def test_sprint4_final_closeout_states_what_system_does_not_do():
    text = _text()

    assert "execute remediation" in text
    assert "restart services" in text
    assert "call real tools" in text
    assert "call real LLM providers" in text
    assert "update benchmark truth" in text
    assert "apply dashboard changes automatically" in text
    assert "enable autonomous remediation" in text


def test_sprint4_final_closeout_defines_final_output_contract():
    text = _text()

    assert "GovernedLearningDashboardSnapshot" in text
    assert "restoration summary" in text
    assert "collective learning summary" in text
    assert "improvement summary" in text
    assert "before dashboard state" in text
    assert "after dashboard candidates" in text
    assert "dashboard deltas" in text


def test_sprint4_final_closeout_sets_sprint5_entry_criteria():
    text = _text()

    assert "benchmark-grounded verification" in text
    assert "governed reasoning boundary" in text
    assert "governed tool boundary" in text
    assert "governed restoration boundary" in text
    assert "governed learning boundary" in text
    assert "human approval boundary" in text


def test_sprint4_final_closeout_defines_sprint5_direction():
    text = _text()

    assert "dashboard/export rendering" in text
    assert "CLI demo runner" in text
    assert "single end-to-end scenario command" in text
    assert "operator review screen model" in text
    assert "GCP deployment readiness checklist" in text
    assert "README demo narrative" in text
