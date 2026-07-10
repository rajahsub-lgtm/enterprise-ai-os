"""
Evidence workbench component model.

Classification: EAIOS Presentation Layer

This module renders evidence already classified by Sprint 3-engine outputs.

It does not decide whether evidence is eligible for reasoning.
It only groups and labels evidence for presentation.
"""

from __future__ import annotations

from typing import Any


EVIDENCE_CLASS_SEMANTICS = {
    "free_text_evidence": {
        "label": "Free text evidence",
        "reasoning_safety_semantics": "Content safety scan",
        "prompt_injection_scan_required": True,
        "story": "Knowledge articles and other free text must pass content-safety review before reasoning.",
    },
    "structured_record_evidence": {
        "label": "Structured record evidence",
        "reasoning_safety_semantics": "Approved provenance",
        "prompt_injection_scan_required": False,
        "story": "CMDB, incident, change, and operational records are trusted through approved provenance, not prompt-injection semantics.",
    },
    "memory_state_evidence": {
        "label": "Memory state evidence",
        "reasoning_safety_semantics": "Approved provenance",
        "prompt_injection_scan_required": False,
        "story": "Enterprise memory is evidence, not truth. It can influence confidence only within governance boundaries.",
    },
}


def evidence_workbench_model(run_view_model: dict[str, Any]) -> dict[str, Any]:
    reasoning_eligible = run_view_model.get("evidence_for_reasoning", [])
    excluded = run_view_model.get("excluded_evidence", [])
    gaps = run_view_model.get("evidence_gaps", [])

    return {
        "title": "Evidence workbench",
        "summary": {
            "reasoning_eligible_count": len(reasoning_eligible),
            "excluded_count": len(excluded),
            "gap_count": len(gaps),
        },
        "reasoning_eligible": [
            _evidence_card(item, status="Reasoning eligible")
            for item in reasoning_eligible
        ],
        "excluded": [
            _evidence_card(item, status="Excluded from reasoning")
            for item in excluded
        ],
        "gaps": [
            _gap_card(gap)
            for gap in gaps
        ],
        "evidence_class_semantics": EVIDENCE_CLASS_SEMANTICS,
        "story": "Fusion consumes governed evidence packages, not raw source records.",
    }


def _evidence_card(item: dict[str, Any], *, status: str) -> dict[str, Any]:
    evidence_class = item.get("evidence_class", "unknown")
    semantics = EVIDENCE_CLASS_SEMANTICS.get(
        evidence_class,
        {
            "label": evidence_class,
            "reasoning_safety_semantics": "Unknown",
            "prompt_injection_scan_required": None,
            "story": "No registered presentation semantics available.",
        },
    )

    return {
        "status": status,
        "evidence_id": item.get("evidence_id"),
        "audit_id": item.get("audit_id"),
        "source_id": item.get("source_id"),
        "evidence_class": evidence_class,
        "evidence_class_label": semantics["label"],
        "reasoning_safety_semantics": semantics[
            "reasoning_safety_semantics"
        ],
        "prompt_injection_scan_required": semantics[
            "prompt_injection_scan_required"
        ],
        "content_safety_status": item.get("content_safety_status"),
        "allowed_for_reasoning": item.get("allowed_for_reasoning"),
        "payload": item.get("payload", {}),
        "story": semantics["story"],
    }


def _gap_card(gap: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "Evidence gap",
        "gap_id": gap.get("gap_id"),
        "audit_id": gap.get("audit_id"),
        "agent_id": gap.get("agent_id"),
        "source_id": gap.get("source_id"),
        "reason": gap.get("reason"),
        "story": "Denied or missing source access is visible as an evidence gap, not silently ignored.",
    }
