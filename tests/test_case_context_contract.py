import pytest

from src.contracts.case_context import CaseContextPhase
from src.contracts.case_context_validator import (
    CaseContextValidationError,
    CaseContextValidator,
)


def initial_context() -> dict:
    return {
        "case_id": "CASE-001",
        "business_outcome": "Maintain Business Capability",
        "goal_category": "application_health_management",
        "initial_signal": {
            "signal_id": "SIG-001",
            "summary": "A production-facing condition requires evaluation.",
        },
    }


def partial_context() -> dict:
    context = initial_context()
    context["joint_goal"] = "Maintain business capability while preserving controls."
    return context


def governed_evidence_package() -> dict:
    return {
        "package_id": "GEP-CASE-001",
        "evidence_items": [
            {
                "evidence_id": "ev-abc123",
                "source_id": "enterprise_memory",
                "agent_id": "memory_pattern_agent",
                "access_decision": "ALLOW",
                "audit_id": "audit-001",
                "content_safety_status": "SAFE_BY_APPROVED_PROVENANCE",
                "allowed_for_reasoning": True,
                "evidence_class": "memory_state_evidence",
            },
            {
                "evidence_id": "ev-def456",
                "source_id": "support_knowledge",
                "agent_id": "knowledge_retrieval_agent",
                "access_decision": "ALLOW",
                "audit_id": "audit-002",
                "content_safety_status": "SAFE",
                "allowed_for_reasoning": True,
                "evidence_class": "free_text_evidence",
            },
        ],
        "evidence_gaps": [],
    }


def governed_context() -> dict:
    context = partial_context()
    context["case_phase"] = CaseContextPhase.GOVERNED_EVIDENCE_COLLECTED.value
    context["governed_evidence_package"] = governed_evidence_package()
    return context


def fusion_result() -> dict:
    return {
        "fusion_id": "FUSION-CASE-001",
        "fusion_confidence": "HIGH",
        "supporting_evidence": [],
        "weakening_evidence": [],
        "conflicting_evidence": [],
        "missing_evidence": [],
        "evidence_gaps": [],
        "requires_human_review": True,
        "autonomous_action_allowed": False,
    }


def reasoning_explanation() -> dict:
    return {
        "reasoning_id": "REASON-CASE-001",
        "method": "lightweight_kt_problem_analysis",
        "kt_problem_analysis": {
            "situation": "A condition requires evaluation.",
            "is": ["The condition is present."],
            "is_not": ["Not approved for production action."],
            "distinctions": [],
            "possible_causes": [],
            "most_probable_hypothesis": "HYP-001",
        },
        "hypotheses": [],
        "selected_hypothesis_id": "HYP-001",
        "reasoning_summary": "Evidence supports a reviewable hypothesis.",
        "why_chain": [],
        "limits": ["Reasoning does not authorize action."],
        "requires_human_review": True,
        "autonomous_action_allowed": False,
    }


def recommendation_candidate() -> dict:
    return {
        "recommendation_id": "REC-CASE-001",
        "risk_level": "HIGH",
        "required_controls": ["human_approval_required"],
        "requires_human_approval": True,
        "approval_state": "PENDING",
        "autonomous_action_allowed": False,
        "candidate_status": "READY_FOR_HUMAN_REVIEW",
    }


def test_initial_signal_context_can_be_minimal():
    result = CaseContextValidator().validate(
        initial_context(),
        CaseContextPhase.INITIAL_SIGNAL,
    )

    assert result["valid"] is True
    assert result["missing_fields"] == []
    assert result["errors"] == []


def test_partial_context_requires_joint_goal_but_not_evidence():
    result = CaseContextValidator().validate(
        partial_context(),
        CaseContextPhase.PARTIAL_CONTEXT,
    )

    assert result["valid"] is True


def test_partial_context_missing_joint_goal_is_invalid_for_partial_phase():
    result = CaseContextValidator().validate(
        initial_context(),
        CaseContextPhase.PARTIAL_CONTEXT,
    )

    assert result["valid"] is False
    assert "joint_goal" in result["missing_fields"]


def test_governed_evidence_collected_requires_package():
    result = CaseContextValidator().validate(
        partial_context(),
        CaseContextPhase.GOVERNED_EVIDENCE_COLLECTED,
    )

    assert result["valid"] is False
    assert "governed_evidence_package" in result["missing_fields"]


def test_fusion_ready_context_accepts_governed_safety_classified_evidence():
    context = governed_context()
    context["case_phase"] = CaseContextPhase.FUSION_READY.value

    result = CaseContextValidator().validate(
        context,
        CaseContextPhase.FUSION_READY,
    )

    assert result["valid"] is True


def test_fusion_ready_context_rejects_raw_ungoverned_records():
    context = partial_context()
    context["case_phase"] = CaseContextPhase.FUSION_READY.value
    context["raw_source_records"] = [
        {
            "source_id": "enterprise_memory",
            "record": {"summary": "raw record without governed evidence"},
        }
    ]

    result = CaseContextValidator().validate(
        context,
        CaseContextPhase.FUSION_READY,
    )

    assert result["valid"] is False
    assert "governed_evidence_package" in result["missing_fields"]


def test_evidence_item_allowed_for_reasoning_requires_safe_status():
    context = governed_context()
    context["case_phase"] = CaseContextPhase.FUSION_READY.value
    context["governed_evidence_package"]["evidence_items"][0][
        "content_safety_status"
    ] = "UNSAFE"

    result = CaseContextValidator().validate(
        context,
        CaseContextPhase.FUSION_READY,
    )

    assert result["valid"] is False
    assert any("cannot be allowed for reasoning" in error for error in result["errors"])


def test_denied_access_can_be_represented_as_evidence_gap():
    context = partial_context()
    context["case_phase"] = CaseContextPhase.FUSION_READY.value
    context["governed_evidence_package"] = {
        "package_id": "GEP-CASE-001",
        "evidence_items": [],
        "evidence_gaps": [
            {
                "gap_id": "GAP-001",
                "source_id": "restricted_source",
                "agent_id": "memory_pattern_agent",
                "reason": "Access denied by governance policy.",
            }
        ],
    }

    result = CaseContextValidator().validate(
        context,
        CaseContextPhase.FUSION_READY,
    )

    assert result["valid"] is True


def test_reasoning_ready_requires_valid_fusion_result():
    context = governed_context()
    context["case_phase"] = CaseContextPhase.REASONING_READY.value
    context["evidence_fusion"] = fusion_result()

    result = CaseContextValidator().validate(
        context,
        CaseContextPhase.REASONING_READY,
    )

    assert result["valid"] is True


def test_recommendation_ready_requires_reasoning_explanation():
    context = governed_context()
    context["case_phase"] = CaseContextPhase.RECOMMENDATION_READY.value
    context["evidence_fusion"] = fusion_result()
    context["reasoning_explanation"] = reasoning_explanation()

    result = CaseContextValidator().validate(
        context,
        CaseContextPhase.RECOMMENDATION_READY,
    )

    assert result["valid"] is True


def test_human_review_ready_requires_candidate_and_approval_boundary():
    context = governed_context()
    context["case_phase"] = CaseContextPhase.HUMAN_REVIEW_READY.value
    context["evidence_fusion"] = fusion_result()
    context["reasoning_explanation"] = reasoning_explanation()
    context["recommendation_candidate"] = recommendation_candidate()
    context["human_approval_required"] = True
    context["autonomous_action_allowed"] = False

    result = CaseContextValidator().validate(
        context,
        CaseContextPhase.HUMAN_REVIEW_READY,
    )

    assert result["valid"] is True


def test_human_review_ready_rejects_autonomous_action_allowed():
    context = governed_context()
    context["case_phase"] = CaseContextPhase.HUMAN_REVIEW_READY.value
    context["evidence_fusion"] = fusion_result()
    context["reasoning_explanation"] = reasoning_explanation()
    context["recommendation_candidate"] = recommendation_candidate()
    context["human_approval_required"] = True
    context["autonomous_action_allowed"] = True

    result = CaseContextValidator().validate(
        context,
        CaseContextPhase.HUMAN_REVIEW_READY,
    )

    assert result["valid"] is False
    assert "autonomous_action_allowed must be False" in result["errors"]


def test_assert_valid_raises_for_invalid_context():
    with pytest.raises(CaseContextValidationError):
        CaseContextValidator().assert_valid(
            partial_context(),
            CaseContextPhase.FUSION_READY,
        )
