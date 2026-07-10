from pathlib import Path


CLOSEOUT = Path("docs/EAIOS_2_SPRINT_4B_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("data/domain/it_application_health/governed_imperfect_knowledge_base.json"),
    Path("src/eaios/sprint4/governed_knowledge_base.py"),
    Path("src/eaios/sprint4/cluster_knowledge_evidence.py"),
    Path("src/eaios/sprint4/governed_knowledge_reasoning.py"),
    Path("src/eaios/sprint4/governed_llm_output_validator.py"),
    Path("src/eaios/sprint4/governed_llm_reasoning_engine.py"),
    Path("src/eaios/sprint4/governed_reasoning_observation.py"),
    Path("tests/test_sprint4_governed_knowledge_base.py"),
    Path("tests/test_sprint4_cluster_knowledge_evidence.py"),
    Path("tests/test_sprint4_governed_knowledge_reasoning.py"),
    Path("tests/test_sprint4_governed_llm_output_validator.py"),
    Path("tests/test_sprint4_governed_llm_reasoning_engine.py"),
    Path("tests/test_sprint4_governed_reasoning_observation.py"),
]


def _text() -> str:
    return CLOSEOUT.read_text(encoding="utf-8")


def test_sprint4_4b_closeout_file_exists():
    assert CLOSEOUT.exists()


def test_sprint4_4b_required_files_exist():
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]
    assert missing == []


def test_sprint4_4b_closeout_lists_completed_slices():
    text = _text()

    assert "4B-1 Governed imperfect synthetic knowledge base" in text
    assert "4B-2 Attach governed KB evidence to issue clusters" in text
    assert "4B-3 Governed knowledge reasoning contract" in text
    assert "4B-4 Governed LLM output validator" in text
    assert "4B-5 Governed LLM reasoning engine seam" in text
    assert "4B-6 Governed reasoning observation snapshot" in text
    assert "4B-7 Closeout contract and architecture checkpoint" in text


def test_sprint4_4b_closeout_locks_layer_boundary():
    text = _text()

    assert "Layer 0: RCAEval / Train Ticket benchmark truth layer" in text
    assert "Layer 5: Governed imperfect knowledge evidence" in text
    assert "Layer 6: Governed knowledge reasoning" in text
    assert "Layer 7: Governed LLM output validation" in text
    assert "Layer 8: Provider-neutral LLM reasoning engine seam" in text
    assert "Layer 9: Governed reasoning observation snapshot" in text


def test_sprint4_4b_closeout_states_core_thesis():
    text = _text()

    assert "Knowledge can inform reasoning." in text
    assert "Knowledge cannot define benchmark truth." in text
    assert "Knowledge cannot become the answer key." in text
    assert "LLM output cannot score the benchmark." in text
    assert "Autonomous action remains disabled." in text


def test_sprint4_4b_closeout_lists_imperfect_knowledge_types():
    text = _text()

    assert "exact knowledge" in text
    assert "partial knowledge" in text
    assert "stale knowledge" in text
    assert "conflicting knowledge" in text
    assert "missing knowledge" in text
    assert "risky remediation knowledge" in text
    assert "wrong-application knowledge" in text
    assert "human-approval-required knowledge" in text


def test_sprint4_4b_closeout_documents_evidence_contract():
    text = _text()

    assert "GovernedKnowledgeEvidence" in text
    assert "KnowledgeRetrievalResult" in text
    assert "ClusterKnowledgeEvidenceBundle" in text
    assert "ClusterKnowledgeEvidenceResult" in text
    assert "benchmark_truth_eligible = false" in text
    assert "can_score_benchmark = false" in text


def test_sprint4_4b_closeout_documents_reasoning_contract():
    text = _text()

    assert "ClusterKnowledgeReasoning" in text
    assert "GovernedKnowledgeReasoningResult" in text
    assert "EvidenceReasoningSignal" in text
    assert "conflict warnings" in text
    assert "stale warnings" in text
    assert "knowledge gaps" in text
    assert "risky action warnings" in text


def test_sprint4_4b_closeout_documents_llm_validator():
    text = _text()

    assert "missing citations" in text
    assert "unknown citations" in text
    assert "missing uncertainty flags" in text
    assert "benchmark truth claims" in text
    assert "benchmark scoring claims" in text
    assert "overconfident conclusions" in text


def test_sprint4_4b_closeout_documents_llm_engine_safety_envelope():
    text = _text()

    assert "LLMReasoningPromptPacket" in text
    assert "LLMSafetyEnvelope" in text
    assert "max_prompt_evidence_items" in text
    assert "max_reasoning_loops" in text
    assert "max_estimated_tokens" in text
    assert "max_estimated_cost_usd" in text
    assert "provider_call_allowed = false" in text


def test_sprint4_4b_closeout_documents_observation_snapshot():
    text = _text()

    assert "GovernedReasoningObservationSnapshot" in text
    assert "knowledge_evidence_summary" in text
    assert "knowledge_reasoning_summary" in text
    assert "llm_engine_summary" in text
    assert "application_health_view" in text
    assert "llm_engine_view" in text


def test_sprint4_4b_closeout_preserves_benchmark_separation():
    text = _text()

    assert "Benchmark scoring remains from 4A only." in text
    assert "KB evidence cannot score benchmark results." in text
    assert "LLM output cannot score benchmark results." in text
    assert "KB evidence cannot replace BenchmarkVerificationTarget." in text
    assert "LLM output cannot replace BenchmarkVerificationTarget." in text


def test_sprint4_4b_closeout_preserves_governance_boundaries():
    text = _text()

    assert "benchmark_truth_external" in text
    assert "benchmark_scoring_from_4a_only" in text
    assert "kb_evidence_cannot_define_truth" in text
    assert "llm_output_cannot_score_benchmark" in text
    assert "citations_required" in text
    assert "uncertainty_required" in text
    assert "human_approval_required" in text
    assert "autonomous_action_disabled" in text
    assert "provider_call_blocked" in text


def test_sprint4_4b_closeout_sets_4c_entry_criteria():
    text = _text()

    assert "KB evidence as governed uncertain evidence" in text
    assert "LLM output schema contract" in text
    assert "LLM output validation gate" in text
    assert "provider-neutral reasoning seam" in text
    assert "benchmark scoring separation" in text


def test_sprint4_4b_closeout_defines_4c_direction():
    text = _text()

    assert "MCP tool manifest" in text
    assert "tool permission policy" in text
    assert "tool request envelope" in text
    assert "tool execution validator" in text
    assert "tool result provenance" in text
    assert "kill-switch and budget controls" in text
    assert "No autonomous remediation." in text
