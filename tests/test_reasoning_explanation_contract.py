from src.domain_adapters.it_application_health.application_health_concept_demo import (
    ApplicationHealthConceptDemo,
)
from src.domain_adapters.it_application_health.itil_case_adapter import (
    ItApplicationHealthCaseAdapter,
)
from src.domain_adapters.it_application_health.itil_repository_loader import (
    ItApplicationHealthRepository,
)
from src.governance.evidence_fusion import EvidenceFusionEngine
from src.governance.reasoning_explanation import ReasoningExplanationEngine
from src.governance.recommendation_candidate import RecommendationCandidateBuilder


def build_case_and_fusion(scenario_id: str) -> tuple[dict, dict]:
    repository = ItApplicationHealthRepository()
    case_context = ItApplicationHealthCaseAdapter(repository).build_case(scenario_id)
    fusion = EvidenceFusionEngine().fuse(case_context)
    return case_context, fusion


def explain_case(scenario_id: str) -> dict:
    case_context, fusion = build_case_and_fusion(scenario_id)
    return ReasoningExplanationEngine().explain(
        case_context=case_context,
        fusion=fusion,
    )


def test_reasoning_explanation_contract_shape():
    reasoning = explain_case("GS-001")

    assert reasoning["reasoning_id"] == "REASON-CASE-GS-001"
    assert reasoning["case_id"] == "CASE-GS-001"
    assert reasoning["business_outcome"] == "Maintain Application Health"
    assert reasoning["method"] == "lightweight_kt_problem_analysis"

    assert reasoning["kt_problem_analysis"]
    assert reasoning["hypotheses"]
    assert reasoning["selected_hypothesis_id"]
    assert reasoning["reasoning_summary"]
    assert reasoning["why_chain"]
    assert reasoning["requires_human_review"] is True
    assert reasoning["autonomous_action_allowed"] is False


def test_reasoning_uses_kt_style_problem_analysis_sections():
    reasoning = explain_case("GS-001")

    kt = reasoning["kt_problem_analysis"]

    assert kt["situation"]
    assert kt["is"]
    assert kt["is_not"]
    assert kt["distinctions"]
    assert "possible_causes" in kt
    assert "most_probable_hypothesis" in kt


def test_reasoning_for_high_confidence_case_selects_evidence_aligned_hypothesis():
    reasoning = explain_case("GS-001")

    assert reasoning["reasoning_confidence"] == "HIGH"
    assert reasoning["selected_hypothesis_id"] == "HYP-CASE-GS-001-EVIDENCE-ALIGNED"

    selected = next(
        hypothesis
        for hypothesis in reasoning["hypotheses"]
        if hypothesis["hypothesis_id"] == reasoning["selected_hypothesis_id"]
    )

    assert selected["hypothesis_type"] == "evidence_aligned_explanation"
    assert selected["supporting_evidence_ids"]


def test_reasoning_for_known_pattern_keeps_memory_as_evidence_not_truth():
    reasoning = explain_case("GS-002")

    hypothesis_types = {
        hypothesis["hypothesis_type"]
        for hypothesis in reasoning["hypotheses"]
    }

    assert "memory_supported_pattern" in hypothesis_types

    memory_hypothesis = next(
        hypothesis
        for hypothesis in reasoning["hypotheses"]
        if hypothesis["hypothesis_type"] == "memory_supported_pattern"
    )

    assert memory_hypothesis["supporting_evidence_ids"]
    assert memory_hypothesis["confidence"] == "MEDIUM"
    assert "truth" not in memory_hypothesis


def test_reasoning_for_unknown_impact_selects_missing_context_hypothesis():
    reasoning = explain_case("GS-005")

    assert reasoning["reasoning_confidence"] == "LOW"
    assert reasoning["selected_hypothesis_id"] == "HYP-CASE-GS-005-UNKNOWN-IMPACT"

    selected = next(
        hypothesis
        for hypothesis in reasoning["hypotheses"]
        if hypothesis["hypothesis_id"] == reasoning["selected_hypothesis_id"]
    )

    assert selected["hypothesis_type"] == "missing_context"
    assert selected["missing_evidence_ids"]
    assert selected["requires_additional_evidence"] is True


def test_reasoning_for_conflicting_case_selects_conflict_hypothesis():
    reasoning = explain_case("GS-006")

    assert reasoning["reasoning_confidence"] == "LOW"
    assert reasoning["selected_hypothesis_id"] == "HYP-CASE-GS-006-CONFLICTING-SIGNALS"

    selected = next(
        hypothesis
        for hypothesis in reasoning["hypotheses"]
        if hypothesis["hypothesis_id"] == reasoning["selected_hypothesis_id"]
    )

    assert selected["hypothesis_type"] == "conflicting_evidence"
    assert selected["conflicting_evidence_ids"]
    assert selected["requires_additional_evidence"] is True


def test_reasoning_why_chain_explains_review_boundary():
    reasoning = explain_case("GS-001")

    answers = " ".join(item["answer"] for item in reasoning["why_chain"])

    assert "does not authorize action" in answers
    assert reasoning["limits"]
    assert reasoning["requires_human_review"] is True


def test_recommendation_candidate_can_reference_reasoning_package():
    case_context, fusion = build_case_and_fusion("GS-001")
    reasoning = ReasoningExplanationEngine().explain(
        case_context=case_context,
        fusion=fusion,
    )

    candidate = RecommendationCandidateBuilder().build(
        case_context=case_context,
        fusion=fusion,
        reasoning=reasoning,
    )

    assert candidate["reasoning_id"] == reasoning["reasoning_id"]
    assert candidate["selected_hypothesis_id"] == reasoning["selected_hypothesis_id"]
    assert candidate["reasoning_summary"] == reasoning["reasoning_summary"]
    assert "reasoning_review_required" in candidate["required_controls"]
    assert candidate["requires_human_approval"] is True


def test_application_health_demo_includes_reasoning_between_fusion_and_candidate():
    result = ApplicationHealthConceptDemo().run("GS-001")

    assert result["evidence_fusion"]
    assert result["reasoning_explanation"]
    assert result["recommendation_candidate"]

    reasoning = result["reasoning_explanation"]
    candidate = result["recommendation_candidate"]

    assert candidate["reasoning_id"] == reasoning["reasoning_id"]
    assert candidate["selected_hypothesis_id"] == reasoning["selected_hypothesis_id"]
    assert result["human_review_package"]["reasoning_id"] == reasoning["reasoning_id"]


def test_application_health_demo_path_still_disallows_autonomous_action():
    for scenario_id in ["GS-001", "GS-002", "GS-003", "GS-004", "GS-005", "GS-006"]:
        result = ApplicationHealthConceptDemo().run(scenario_id)

        assert result["reasoning_explanation"]["autonomous_action_allowed"] is False
        assert result["recommendation_candidate"]["autonomous_action_allowed"] is False
        assert result["human_review_package"]["autonomous_action_allowed"] is False
        assert result["safety_summary"]["autonomous_action_allowed"] is False
