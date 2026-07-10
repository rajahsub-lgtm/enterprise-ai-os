from src.domain_adapters.it_application_health.application_health_concept_demo import (
    ApplicationHealthConceptDemo,
)
from src.governance.operational_confidence import OperationalConfidenceGate


def base_case(memory_records: list[dict] | None = None) -> dict:
    return {
        "case_id": "CASE-TEST-001",
        "scenario_id": "TEST-001",
        "business_outcome": "Maintain Application Health",
        "goal_category": "application_health_management",
        "case_summary": "A recurring condition is being evaluated.",
        "impact": {
            "impact_tier": "HIGH",
            "impact_confidence": "HIGH",
        },
        "observations": [
            {
                "summary": "Observed condition matches the evaluated signature.",
            }
        ],
        "context_records": {
            "memory_context": memory_records or [],
        },
        "human_approval_required": True,
        "autonomous_action_allowed": False,
    }


def clean_high_fusion() -> dict:
    return {
        "fusion_confidence": "HIGH",
        "supporting_evidence": [],
        "weakening_evidence": [],
        "conflicting_evidence": [],
        "missing_evidence": [],
        "evidence_gaps": [],
    }


def conflicting_fusion() -> dict:
    return {
        "fusion_confidence": "LOW",
        "supporting_evidence": [],
        "weakening_evidence": [],
        "conflicting_evidence": [
            {
                "evidence_id": "EVIDENCE-CONFLICT-001",
                "evidence_type": "synthetic_conflict",
            }
        ],
        "missing_evidence": [],
        "evidence_gaps": [],
    }


def missing_fusion() -> dict:
    return {
        "fusion_confidence": "LOW",
        "supporting_evidence": [],
        "weakening_evidence": [],
        "conflicting_evidence": [],
        "missing_evidence": [
            {
                "evidence_id": "EVIDENCE-MISSING-001",
                "evidence_type": "required_context",
            }
        ],
        "evidence_gaps": [],
    }


def trusted_memory() -> dict:
    return {
        "pattern_id": "MEM-TRUSTED-001",
        "validation_state": "HUMAN_VALIDATED",
        "successful_uses": 50,
        "failed_uses": 0,
        "similarity": 0.94,
        "freshness": "CURRENT",
    }


def drifting_memory() -> dict:
    return {
        "pattern_id": "MEM-DRIFTING-001",
        "validation_state": "HUMAN_VALIDATED",
        "successful_uses": 50,
        "failed_uses": 4,
        "similarity": 0.51,
        "freshness": "CURRENT",
    }


def test_new_condition_requires_full_due_diligence():
    decision = OperationalConfidenceGate().evaluate(
        case_context=base_case(),
        fusion=clean_high_fusion(),
    )

    assert decision["pattern_maturity"] == "NONE"
    assert decision["operational_confidence"] == "LOW"
    assert decision["confidence_direction"] == "NEW"
    assert decision["selected_due_diligence_level"] == "FULL_DUE_DILIGENCE"
    assert decision["knowledge_retrieval_required"] is True
    assert decision["governance_required"] is True
    assert decision["human_approval_required"] is True
    assert decision["autonomous_action_allowed"] is False


def test_trusted_memory_allows_targeted_validation_but_not_governance_bypass():
    decision = OperationalConfidenceGate().evaluate(
        case_context=base_case([trusted_memory()]),
        fusion=clean_high_fusion(),
    )

    assert decision["pattern_maturity"] == "TRUSTED"
    assert decision["operational_confidence"] == "HIGH"
    assert decision["selected_due_diligence_level"] == "TARGETED_VALIDATION"
    assert decision["knowledge_retrieval_required"] is False

    assert decision["governance_required"] is True
    assert decision["human_approval_required"] is True
    assert decision["autonomous_action_allowed"] is False
    assert decision["why"]


def test_conflicting_evidence_decreases_operational_confidence():
    decision = OperationalConfidenceGate().evaluate(
        case_context=base_case([trusted_memory()]),
        fusion=conflicting_fusion(),
        previous_operational_confidence="HIGH",
    )

    assert decision["pattern_maturity"] == "UNRELIABLE_FOR_CURRENT_CASE"
    assert decision["operational_confidence"] == "LOW"
    assert decision["confidence_direction"] == "DECREASING"
    assert decision["selected_due_diligence_level"] == "EXPANDED_VALIDATION"
    assert decision["knowledge_retrieval_required"] is True


def test_missing_evidence_forces_expanded_due_diligence():
    decision = OperationalConfidenceGate().evaluate(
        case_context=base_case([trusted_memory()]),
        fusion=missing_fusion(),
        previous_operational_confidence="HIGH",
    )

    assert decision["pattern_maturity"] == "INCOMPLETE_CONTEXT"
    assert decision["operational_confidence"] == "LOW"
    assert decision["confidence_direction"] == "DECREASING"
    assert decision["knowledge_retrieval_required"] is True


def test_drifting_memory_requires_expanded_validation():
    decision = OperationalConfidenceGate().evaluate(
        case_context=base_case([drifting_memory()]),
        fusion=clean_high_fusion(),
        previous_operational_confidence="HIGH",
    )

    assert decision["pattern_maturity"] == "TRUSTED_BUT_DRIFTING"
    assert decision["operational_confidence"] == "LOW"
    assert decision["confidence_direction"] == "DECREASING"
    assert decision["selected_due_diligence_level"] == "EXPANDED_VALIDATION"
    assert decision["knowledge_retrieval_required"] is True


def test_unknown_impact_requires_impact_assessment_path():
    case = base_case([trusted_memory()])
    case["impact"] = {
        "impact_tier": "UNKNOWN",
        "impact_confidence": "LOW",
    }

    decision = OperationalConfidenceGate().evaluate(
        case_context=case,
        fusion=clean_high_fusion(),
    )

    assert decision["pattern_maturity"] == "UNKNOWN_IMPACT"
    assert decision["operational_confidence"] == "LOW"
    assert decision["selected_due_diligence_level"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert decision["knowledge_retrieval_required"] is True


def test_application_health_demo_includes_operational_confidence_decision():
    result = ApplicationHealthConceptDemo().run("GS-001")

    assert result["operational_confidence"]
    assert result["human_review_package"]["operational_confidence"]
    assert result["human_review_package"]["selected_due_diligence_level"]
    assert result["operational_confidence"]["governance_required"] is True
    assert result["operational_confidence"]["human_approval_required"] is True
    assert result["operational_confidence"]["autonomous_action_allowed"] is False


def test_application_health_demo_confidence_gate_is_safe_for_all_golden_scenarios():
    for scenario_id in ["GS-001", "GS-002", "GS-003", "GS-004", "GS-005", "GS-006"]:
        result = ApplicationHealthConceptDemo().run(scenario_id)
        decision = result["operational_confidence"]

        assert decision["governance_required"] is True
        assert decision["human_approval_required"] is True
        assert decision["autonomous_action_allowed"] is False
        assert result["safety_summary"]["autonomous_action_allowed"] is False
