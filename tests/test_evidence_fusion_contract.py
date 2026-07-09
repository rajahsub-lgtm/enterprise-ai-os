from src.domain_adapters.it_application_health.itil_case_adapter import (
    ItApplicationHealthCaseAdapter,
)
from src.domain_adapters.it_application_health.itil_repository_loader import (
    ItApplicationHealthRepository,
)
from src.governance.evidence_fusion import EvidenceFusionEngine


def build_case(scenario_id: str) -> dict:
    repository = ItApplicationHealthRepository()
    adapter = ItApplicationHealthCaseAdapter(repository)
    return adapter.build_case(scenario_id)


def fuse_case(scenario_id: str) -> dict:
    return EvidenceFusionEngine().fuse(build_case(scenario_id))


def test_evidence_fusion_returns_contract_shape():
    fusion = fuse_case("GS-001")

    assert fusion["fusion_id"] == "FUSION-CASE-GS-001"
    assert fusion["case_id"] == "CASE-GS-001"
    assert fusion["scenario_id"] == "GS-001"
    assert fusion["business_outcome"] == "Maintain Application Health"
    assert fusion["goal_category"] == "operational_troubleshooting"

    assert "supporting_evidence" in fusion
    assert "weakening_evidence" in fusion
    assert "conflicting_evidence" in fusion
    assert "missing_evidence" in fusion
    assert "evidence_gaps" in fusion
    assert "fusion_confidence" in fusion
    assert fusion["autonomous_action_allowed"] is False


def test_high_impact_checkout_case_has_supporting_evidence_and_high_confidence():
    fusion = fuse_case("GS-001")

    assert fusion["supporting_evidence"]
    assert len(fusion["supporting_evidence"]) >= 9
    assert fusion["fusion_confidence"] == "HIGH"
    assert fusion["requires_human_review"] is True
    assert fusion["conflicting_evidence"] == []
    assert fusion["missing_evidence"] == []


def test_known_pattern_case_keeps_memory_as_supporting_evidence():
    fusion = fuse_case("GS-002")

    memory_evidence = [
        evidence
        for evidence in fusion["supporting_evidence"]
        if evidence["evidence_type"] == "memory_context"
    ]

    assert len(memory_evidence) == 1
    assert memory_evidence[0]["source_record_id"] == "MEM-DB-CONNECTION-EXHAUSTION-001"
    assert fusion["autonomous_action_allowed"] is False


def test_conditional_knowledge_creates_weakening_evidence():
    fusion = fuse_case("GS-003")

    weakening_types = {
        evidence["evidence_type"]
        for evidence in fusion["weakening_evidence"]
    }

    assert "source_trust_limitation" in weakening_types
    assert fusion["fusion_confidence"] == "MEDIUM"


def test_unknown_impact_creates_missing_evidence_and_low_confidence():
    fusion = fuse_case("GS-005")

    assert fusion["fusion_confidence"] == "LOW"
    assert fusion["requires_human_review"] is True

    missing_types = {
        evidence["evidence_type"]
        for evidence in fusion["missing_evidence"]
    }

    assert "missing_impact_mapping" in missing_types
    assert "missing_human_validation" in missing_types

    gap_types = {
        gap["gap_type"]
        for gap in fusion["evidence_gaps"]
    }

    assert "missing_required_evidence" in gap_types


def test_conflicting_case_creates_conflicting_evidence_and_gap():
    fusion = fuse_case("GS-006")

    assert fusion["fusion_confidence"] == "LOW"
    assert fusion["conflicting_evidence"]

    conflict = fusion["conflicting_evidence"][0]

    assert conflict["evidence_type"] == "multi_entity_low_confidence_conflict"
    assert "CI-NETWORK-EDGE-003" in conflict["entity_ids"]
    assert "CI-CHECKOUT-API-001" in conflict["entity_ids"]

    gap_types = {
        gap["gap_type"]
        for gap in fusion["evidence_gaps"]
    }

    assert "conflict_resolution_required" in gap_types


def test_unvalidated_memory_weakens_confidence_but_does_not_authorize_action():
    fusion = fuse_case("GS-006")

    weakening_types = {
        evidence["evidence_type"]
        for evidence in fusion["weakening_evidence"]
    }

    assert "memory_validation_limitation" in weakening_types
    assert fusion["autonomous_action_allowed"] is False
    assert fusion["requires_human_review"] is True


def test_evidence_fusion_does_not_create_recommendation_or_execution():
    fusion = fuse_case("GS-001")

    assert "recommendation" not in fusion
    assert "action" not in fusion
    assert "execution" not in fusion
    assert fusion["autonomous_action_allowed"] is False
