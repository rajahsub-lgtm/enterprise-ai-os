from pathlib import Path

from ui.components.evidence_workbench import (
    EVIDENCE_CLASS_SEMANTICS,
    evidence_workbench_model,
)
from ui.demo_fixtures import build_demo_comparison_view_model


STREAMLIT_APP = Path("ui/streamlit_app.py")


def selected_run():
    comparison = build_demo_comparison_view_model()
    return comparison["runs"][0]


def test_evidence_workbench_summarizes_reasoning_excluded_and_gaps():
    workbench = evidence_workbench_model(selected_run())

    assert workbench["title"] == "Evidence workbench"
    assert workbench["summary"] == {
        "reasoning_eligible_count": 1,
        "excluded_count": 1,
        "gap_count": 1,
    }
    assert workbench["story"] == (
        "Fusion consumes governed evidence packages, not raw source records."
    )


def test_evidence_workbench_routes_reasoning_eligible_memory_to_reasoning_section():
    workbench = evidence_workbench_model(selected_run())

    reasoning = workbench["reasoning_eligible"]

    assert len(reasoning) == 1

    item = reasoning[0]

    assert item["status"] == "Reasoning eligible"
    assert item["evidence_id"] == "run-no-memory-EVIDENCE-001"
    assert item["source_id"] == "enterprise_memory"
    assert item["evidence_class"] == "memory_state_evidence"
    assert item["reasoning_safety_semantics"] == "Approved provenance"
    assert item["prompt_injection_scan_required"] is False
    assert item["content_safety_status"] == "SAFE_BY_APPROVED_PROVENANCE"
    assert item["allowed_for_reasoning"] is True
    assert "evidence, not truth" in item["story"]


def test_evidence_workbench_routes_review_required_free_text_to_excluded_section():
    workbench = evidence_workbench_model(selected_run())

    excluded = workbench["excluded"]

    assert len(excluded) == 1

    item = excluded[0]

    assert item["status"] == "Excluded from reasoning"
    assert item["evidence_id"] == "run-no-memory-EVIDENCE-EXCLUDED-001"
    assert item["source_id"] == "support_knowledge"
    assert item["evidence_class"] == "free_text_evidence"
    assert item["reasoning_safety_semantics"] == "Content safety scan"
    assert item["prompt_injection_scan_required"] is True
    assert item["content_safety_status"] == "REVIEW_REQUIRED"
    assert item["allowed_for_reasoning"] is False


def test_evidence_workbench_surfaces_denied_access_as_gap():
    workbench = evidence_workbench_model(selected_run())

    gaps = workbench["gaps"]

    assert len(gaps) == 1

    gap = gaps[0]

    assert gap["status"] == "Evidence gap"
    assert gap["audit_id"] == "run-no-memory-AUDIT-003"
    assert gap["agent_id"] == "business_impact_agent"
    assert gap["source_id"] == "itil_business_impact_map"
    assert "not entitled" in gap["reason"]
    assert "not silently ignored" in gap["story"]


def test_evidence_class_semantics_include_structured_free_text_and_memory_rules():
    assert EVIDENCE_CLASS_SEMANTICS["free_text_evidence"] == {
        "label": "Free text evidence",
        "reasoning_safety_semantics": "Content safety scan",
        "prompt_injection_scan_required": True,
        "story": "Knowledge articles and other free text must pass content-safety review before reasoning.",
    }

    assert EVIDENCE_CLASS_SEMANTICS["structured_record_evidence"] == {
        "label": "Structured record evidence",
        "reasoning_safety_semantics": "Approved provenance",
        "prompt_injection_scan_required": False,
        "story": "CMDB, incident, change, and operational records are trusted through approved provenance, not prompt-injection semantics.",
    }

    assert EVIDENCE_CLASS_SEMANTICS["memory_state_evidence"] == {
        "label": "Memory state evidence",
        "reasoning_safety_semantics": "Approved provenance",
        "prompt_injection_scan_required": False,
        "story": "Enterprise memory is evidence, not truth. It can influence confidence only within governance boundaries.",
    }


def test_streamlit_app_renders_evidence_workbench_sections():
    text = STREAMLIT_APP.read_text(encoding="utf-8")

    assert "evidence_workbench_model" in text
    assert "Evidence workbench" in text
    assert "Reasoning eligible" in text
    assert "Evidence semantics" in text
    assert "Evidence gaps" in text
