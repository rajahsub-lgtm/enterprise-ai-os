import json
from pathlib import Path

from src.governance.operational_confidence import OperationalConfidenceGate


MEMORY_STATES_PATH = Path(
    "data/domain/it_application_health/sprint3_demo_memory_states.json"
)


def base_context(memory_state: dict | None = None) -> dict:
    memory_context = [] if memory_state is None else [memory_state]

    return {
        "case_id": "CASE-S3-OC-001",
        "scenario_id": "SCENARIO-S3-OC-001",
        "business_outcome": "Maintain Business Capability",
        "goal_category": "capability_health_management",
        "impact": {
            "impact_tier": "HIGH",
            "impact_confidence": "HIGH",
        },
        "context_records": {
            "memory_context": memory_context,
        },
    }


def high_confidence_fusion() -> dict:
    return {
        "fusion_confidence": "HIGH",
        "conflicting_evidence": [],
        "missing_evidence": [],
        "weakening_evidence": [],
    }


def fusion_with_conflict() -> dict:
    return {
        "fusion_confidence": "LOW",
        "conflicting_evidence": [{"evidence_id": "conflict-001"}],
        "missing_evidence": [],
        "weakening_evidence": [],
    }


def fusion_with_missing_evidence() -> dict:
    return {
        "fusion_confidence": "LOW",
        "conflicting_evidence": [],
        "missing_evidence": [{"evidence_id": "missing-001"}],
        "weakening_evidence": [],
    }


def memory_states() -> list[dict]:
    return json.loads(MEMORY_STATES_PATH.read_text(encoding="utf-8"))


def memory_state_by_id(memory_state_id: str) -> dict:
    return {
        state["memory_state_id"]: state
        for state in memory_states()
    }[memory_state_id]


def test_sprint3_memory_state_fixture_contains_required_fields():
    required_fields = {
        "memory_state_id",
        "pattern_maturity",
        "prior_confidence",
        "outcome_history",
        "successful_uses",
        "failed_uses",
        "similarity",
        "freshness",
        "validation_state",
        "expected_confidence_direction",
        "expected_due_diligence_level",
    }

    for state in memory_states():
        assert required_fields.issubset(state)


def test_no_memory_requires_full_due_diligence_and_new_direction():
    result = OperationalConfidenceGate().evaluate(
        case_context=base_context(),
        fusion=high_confidence_fusion(),
    )

    assert result["pattern_maturity"] == "NONE"
    assert result["operational_confidence"] == "LOW"
    assert result["confidence_direction"] == "NEW"
    assert result["selected_due_diligence_level"] == "FULL_DUE_DILIGENCE"
    assert result["knowledge_retrieval_required"] is True
    assert "retrieve_support_knowledge" in result["required_agent_steps"]
    assert "skip_governance" in result["prohibited_shortcuts"]


def test_emerging_memory_increases_confidence_and_targets_knowledge_retrieval():
    state = memory_state_by_id("emerging_memory")

    result = OperationalConfidenceGate().evaluate(
        case_context=base_context(state),
        fusion=high_confidence_fusion(),
    )

    assert result["pattern_maturity"] == "EMERGING"
    assert result["operational_confidence"] == "MEDIUM"
    assert result["confidence_direction"] == "INCREASING"
    assert result["selected_due_diligence_level"] == "TARGETED_KNOWLEDGE_RETRIEVAL"
    assert result["required_agent_steps"] == [
        "retrieve_memory_patterns",
        "retrieve_support_knowledge",
    ]


def test_trusted_memory_uses_targeted_validation_without_skipping_governance():
    state = memory_state_by_id("trusted_memory")

    result = OperationalConfidenceGate().evaluate(
        case_context=base_context(state),
        fusion=high_confidence_fusion(),
    )

    assert result["pattern_maturity"] == "TRUSTED"
    assert result["operational_confidence"] == "HIGH"
    assert result["confidence_direction"] == "STABLE"
    assert result["selected_due_diligence_level"] == "TARGETED_VALIDATION"
    assert result["knowledge_retrieval_required"] is False
    assert result["required_agent_steps"] == [
        "retrieve_memory_patterns",
        "validate_current_context",
    ]
    assert result["governance_required"] is True
    assert result["human_approval_required"] is True
    assert result["autonomous_action_allowed"] is False


def test_drifting_memory_decreases_confidence_and_expands_due_diligence():
    state = memory_state_by_id("trusted_but_drifting_memory")

    result = OperationalConfidenceGate().evaluate(
        case_context=base_context(state),
        fusion=high_confidence_fusion(),
    )

    assert result["pattern_maturity"] == "TRUSTED_BUT_DRIFTING"
    assert result["operational_confidence"] == "LOW"
    assert result["confidence_direction"] == "DECREASING"
    assert result["selected_due_diligence_level"] == "EXPANDED_VALIDATION"
    assert "resolve_evidence_conflicts" in result["required_agent_steps"]
    assert "skip_context_validation" in result["prohibited_shortcuts"]


def test_conflicting_evidence_forces_expanded_validation():
    state = memory_state_by_id("trusted_memory")

    result = OperationalConfidenceGate().evaluate(
        case_context=base_context(state),
        fusion=fusion_with_conflict(),
    )

    assert result["pattern_maturity"] == "UNRELIABLE_FOR_CURRENT_CASE"
    assert result["operational_confidence"] == "LOW"
    assert result["selected_due_diligence_level"] == "EXPANDED_VALIDATION"
    assert result["knowledge_retrieval_required"] is True
    assert "resolve_evidence_conflicts" in result["required_agent_steps"]


def test_missing_evidence_forces_expanded_validation():
    state = memory_state_by_id("trusted_memory")

    result = OperationalConfidenceGate().evaluate(
        case_context=base_context(state),
        fusion=fusion_with_missing_evidence(),
    )

    assert result["pattern_maturity"] == "INCOMPLETE_CONTEXT"
    assert result["operational_confidence"] == "LOW"
    assert result["selected_due_diligence_level"] == "EXPANDED_VALIDATION"
    assert result["knowledge_retrieval_required"] is True


def test_unknown_impact_forces_escalation_path():
    context = base_context(memory_state_by_id("trusted_memory"))
    context["impact"] = {
        "impact_tier": "UNKNOWN",
        "impact_confidence": "LOW",
    }

    result = OperationalConfidenceGate().evaluate(
        case_context=context,
        fusion=high_confidence_fusion(),
    )

    assert result["pattern_maturity"] == "UNKNOWN_IMPACT"
    assert result["operational_confidence"] == "LOW"
    assert result["selected_due_diligence_level"] == "ESCALATE_FOR_IMPACT_ASSESSMENT"
    assert result["required_agent_steps"] == [
        "assess_impact_context",
        "retrieve_support_knowledge",
    ]


def test_required_output_is_orchestrator_consumable():
    result = OperationalConfidenceGate().evaluate(
        case_context=base_context(memory_state_by_id("trusted_memory")),
        fusion=high_confidence_fusion(),
    )

    required_fields = {
        "operational_confidence",
        "confidence_direction",
        "pattern_maturity",
        "selected_due_diligence_level",
        "knowledge_retrieval_required",
        "required_agent_steps",
        "prohibited_shortcuts",
        "why",
        "governance_required",
        "human_approval_required",
        "autonomous_action_allowed",
    }

    assert required_fields.issubset(result)
    assert isinstance(result["required_agent_steps"], list)
    assert isinstance(result["prohibited_shortcuts"], list)
    assert result["governance_required"] is True
    assert result["human_approval_required"] is True
    assert result["autonomous_action_allowed"] is False
