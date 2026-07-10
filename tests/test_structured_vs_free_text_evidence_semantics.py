import json
from pathlib import Path

import pytest

from src.governance.governed_evidence_package import GovernedEvidencePackage
from src.governance.source_access_result import SourceAccessResult


SOURCES_PATH = Path("data/governance/data_sources.json")


def source_records() -> list[dict]:
    document = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))

    if isinstance(document, list):
        return document

    for key in ["data_sources", "items", "records"]:
        if key in document and isinstance(document[key], list):
            return document[key]

    raise AssertionError("Could not find data source collection.")


def source_by_id() -> dict[str, dict]:
    return {
        source["source_id"]: source
        for source in source_records()
    }


def result(
    *,
    evidence_class: str,
    content_safety_status: str,
    allowed_for_reasoning: bool = True,
) -> SourceAccessResult:
    return SourceAccessResult(
        case_id="CASE-EVIDENCE-SEMANTICS",
        agent_id="agent",
        source_id="source",
        capability="capability",
        goal_category="goal",
        purpose="purpose",
        evidence_class=evidence_class,
        access_decision="ALLOW",
        audit_id="audit-001",
        evidence_id="ev-001",
        content_safety_status=content_safety_status,
        allowed_for_reasoning=allowed_for_reasoning,
    )


def test_registry_marks_free_text_sources_as_content_safety_scanned():
    support_knowledge = source_by_id()["support_knowledge"]

    assert support_knowledge["evidence_class"] == "free_text_evidence"
    assert support_knowledge["reasoning_safety_semantics"] == "CONTENT_SAFETY_SCAN"
    assert support_knowledge["prompt_injection_scan_required"] is True


def test_registry_marks_structured_sources_as_approved_provenance_not_prompt_scan():
    structured_sources = [
        "itil_incidents",
        "itil_changes",
        "itil_cmdb_topology",
        "itil_business_impact_map",
        "itil_operational_records",
    ]

    sources = source_by_id()

    for source_id in structured_sources:
        source = sources[source_id]

        assert source["evidence_class"] == "structured_record_evidence"
        assert source["reasoning_safety_semantics"] == "APPROVED_PROVENANCE"
        assert source["prompt_injection_scan_required"] is False


def test_registry_marks_enterprise_memory_as_memory_state_evidence():
    enterprise_memory = source_by_id()["enterprise_memory"]

    assert enterprise_memory["evidence_class"] == "memory_state_evidence"
    assert enterprise_memory["reasoning_safety_semantics"] == "APPROVED_PROVENANCE"
    assert enterprise_memory["prompt_injection_scan_required"] is False


def test_structured_record_evidence_requires_approved_provenance_for_reasoning():
    item = result(
        evidence_class="structured_record_evidence",
        content_safety_status="SAFE_BY_APPROVED_PROVENANCE",
    ).to_evidence_item()

    assert item["allowed_for_reasoning"] is True


def test_structured_record_evidence_rejects_free_text_safe_status_for_reasoning():
    with pytest.raises(ValueError):
        result(
            evidence_class="structured_record_evidence",
            content_safety_status="SAFE",
        ).to_evidence_item()


def test_free_text_evidence_requires_content_safety_status_for_reasoning():
    item = result(
        evidence_class="free_text_evidence",
        content_safety_status="SAFE",
    ).to_evidence_item()

    assert item["allowed_for_reasoning"] is True


def test_free_text_evidence_rejects_approved_provenance_without_content_scan():
    with pytest.raises(ValueError):
        result(
            evidence_class="free_text_evidence",
            content_safety_status="SAFE_BY_APPROVED_PROVENANCE",
        ).to_evidence_item()


def test_memory_state_evidence_uses_approved_provenance_for_reasoning():
    item = result(
        evidence_class="memory_state_evidence",
        content_safety_status="SAFE_BY_APPROVED_PROVENANCE",
    ).to_evidence_item()

    assert item["allowed_for_reasoning"] is True


def test_non_reasoning_evidence_can_be_packaged_as_excluded_without_wrong_semantics():
    package = GovernedEvidencePackage.from_results(
        case_id="CASE-EVIDENCE-SEMANTICS",
        results=[
            result(
                evidence_class="free_text_evidence",
                content_safety_status="SAFE_BY_APPROVED_PROVENANCE",
                allowed_for_reasoning=False,
            )
        ],
    )

    assert package.evidence_for_reasoning() == []
    assert package.excluded_evidence()
    assert package.evidence_gaps
