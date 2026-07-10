from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from eaios.sprint4.governed_knowledge_reasoning import (
    ReasoningConfidence,
    ReasoningState,
    build_governed_knowledge_reasoning,
    summarize_governed_knowledge_reasoning,
    to_view_model,
)


def _result():
    return build_governed_knowledge_reasoning()


def test_governed_knowledge_reasoning_builds_one_reasoning_record_per_cluster():
    result = _result()

    assert result.total_clusters == 2
    assert len(result.cluster_reasoning) == 2
    assert {
        reasoning.source_failure_case_id for reasoning in result.cluster_reasoning
    } == {
        "structural-failure-payment-latency-001",
        "structural-failure-inventory-errors-001",
    }


def test_payment_cluster_reasoning_preserves_conflict_and_staleness():
    result = _result()

    payment = next(
        reasoning for reasoning in result.cluster_reasoning
        if reasoning.source_failure_case_id == "structural-failure-payment-latency-001"
    )

    assert payment.reasoning_state == ReasoningState.SUPPORTED_WITH_CONFLICTS
    assert payment.confidence == ReasoningConfidence.MEDIUM_WITH_REVIEW
    assert payment.conflict_warnings
    assert payment.stale_warnings
    assert payment.knowledge_gaps == ()
    assert payment.risky_action_warnings == ()
    assert any("exact governed evidence" in item for item in payment.supported_observations)
    assert any("partial governed evidence" in item for item in payment.supported_observations)


def test_inventory_cluster_reasoning_preserves_risky_and_missing_knowledge():
    result = _result()

    inventory = next(
        reasoning for reasoning in result.cluster_reasoning
        if reasoning.source_failure_case_id == "structural-failure-inventory-errors-001"
    )

    assert inventory.reasoning_state == ReasoningState.RISKY_OR_INCOMPLETE
    assert inventory.confidence == ReasoningConfidence.LOW_WITH_REVIEW
    assert inventory.knowledge_gaps == ("route-planning-service::dependency_error_rate",)
    assert inventory.risky_action_warnings
    assert any("risky_remediation" in warning for warning in inventory.risky_action_warnings)
    assert any("Should a new knowledge article be created" in question for question in inventory.human_review_questions)
    assert any("blast-radius" in question for question in inventory.human_review_questions)


def test_governed_reasoning_never_claims_benchmark_truth_or_scores():
    result = _result()

    assert result.benchmark_scoring_allowed is False

    for reasoning in result.cluster_reasoning:
        assert reasoning.benchmark_truth_claim_allowed is False
        assert reasoning.benchmark_scoring_allowed is False
        assert reasoning.human_approval_required is True
        assert reasoning.autonomous_action_allowed is False


def test_governed_reasoning_contract_defines_future_llm_boundaries():
    result = _result()

    assert "llm_output_must_be_schema_valid" in result.reasoning_contract
    assert "llm_output_must_cite_governed_evidence" in result.reasoning_contract
    assert "llm_output_must_preserve_uncertainty" in result.reasoning_contract
    assert "llm_output_must_not_define_benchmark_truth" in result.reasoning_contract
    assert "llm_output_must_not_score_benchmark_results" in result.reasoning_contract
    assert "llm_output_must_require_human_approval_for_actions" in result.reasoning_contract
    assert "llm_output_must_not_enable_autonomous_action" in result.reasoning_contract


def test_evidence_signals_preserve_quality_safety_contribution_and_limitations():
    result = _result()

    all_signals = [
        signal
        for reasoning in result.cluster_reasoning
        for signal in reasoning.evidence_signals
    ]

    qualities = {signal.quality for signal in all_signals}
    limitations = {signal.limitation for signal in all_signals}
    contributions = {signal.contribution for signal in all_signals}

    assert "exact" in qualities
    assert "conflicting" in qualities
    assert "stale" in qualities
    assert "missing" in qualities
    assert "still not benchmark truth" in limitations
    assert "must be reconciled before conclusion" in limitations
    assert "cannot support conclusion" in limitations
    assert "supports hypothesis" in contributions
    assert "raises contradiction" in contributions


def test_governed_reasoning_summary_is_view_ready():
    result = _result()

    summary = summarize_governed_knowledge_reasoning(result)

    assert summary == {
        "total_clusters": 2,
        "reasoning_states": (
            "SUPPORTED_WITH_CONFLICTS",
            "RISKY_OR_INCOMPLETE",
        ),
        "clusters_with_conflicts": (
            "cluster::structural-failure-payment-latency-001",
        ),
        "clusters_with_stale_evidence": (
            "cluster::structural-failure-payment-latency-001",
        ),
        "clusters_with_knowledge_gaps": (
            "cluster::structural-failure-inventory-errors-001",
        ),
        "clusters_with_risky_evidence": (
            "cluster::structural-failure-inventory-errors-001",
        ),
        "human_approval_required": True,
        "benchmark_scoring_allowed": False,
        "autonomous_action_allowed": False,
    }


def test_governed_reasoning_view_model_is_json_serializable():
    result = _result()

    view_model = to_view_model(result)
    serialized = json.dumps(view_model, indent=2)

    assert "SUPPORTED_WITH_CONFLICTS" in serialized
    assert "RISKY_OR_INCOMPLETE" in serialized
    assert "llm_output_must_not_score_benchmark_results" in serialized
    assert "benchmark_truth_claim_allowed" in serialized
    assert "autonomous_action_allowed" in serialized


def test_governed_reasoning_module_does_not_call_real_llm_or_benchmark_scoring():
    source = Path("src/eaios/sprint4/governed_knowledge_reasoning.py").read_text(
        encoding="utf-8"
    )

    assert "openai" not in source.lower()
    assert "anthropic" not in source.lower()
    assert "requests" not in source.lower()
    assert "httpx" not in source.lower()
    assert "from eaios.sprint4.rcaeval_contracts import" not in source
    assert "score_benchmark_result(" not in source
    assert "BenchmarkVerificationTarget" not in source
    assert "BenchmarkVerificationResult" not in source