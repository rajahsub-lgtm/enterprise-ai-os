"""
Case context validator.

Classification: EAIOS Core

The validator allows incremental context assembly while preventing downstream
components from running against incomplete or ungoverned context.

Core rule:
Partial context is allowed. Fusion-ready context must be validated.
"""

from __future__ import annotations

from typing import Any

from src.contracts.case_context import (
    CaseContextPhase,
    PHASE_REQUIRED_FIELDS,
    phase_value,
)


class CaseContextValidationError(ValueError):
    pass


class CaseContextValidator:
    def validate(
        self,
        case_context: dict[str, Any],
        phase: CaseContextPhase | str,
    ) -> dict[str, Any]:
        normalized_phase = CaseContextPhase(phase_value(phase))
        required_fields = PHASE_REQUIRED_FIELDS[normalized_phase]

        missing_fields = sorted(
            field for field in required_fields if field not in case_context
        )

        errors: list[str] = []

        if missing_fields:
            errors.append(
                "Missing required fields for phase "
                f"{normalized_phase.value}: {', '.join(missing_fields)}"
            )

        if normalized_phase in {
            CaseContextPhase.GOVERNED_EVIDENCE_COLLECTED,
            CaseContextPhase.FUSION_READY,
            CaseContextPhase.REASONING_READY,
            CaseContextPhase.RECOMMENDATION_READY,
            CaseContextPhase.HUMAN_REVIEW_READY,
        }:
            errors.extend(self._validate_governed_evidence_package(case_context))

        if normalized_phase in {
            CaseContextPhase.REASONING_READY,
            CaseContextPhase.RECOMMENDATION_READY,
            CaseContextPhase.HUMAN_REVIEW_READY,
        }:
            errors.extend(self._validate_fusion_result(case_context))

        if normalized_phase in {
            CaseContextPhase.RECOMMENDATION_READY,
            CaseContextPhase.HUMAN_REVIEW_READY,
        }:
            errors.extend(self._validate_reasoning_explanation(case_context))

        if normalized_phase == CaseContextPhase.HUMAN_REVIEW_READY:
            errors.extend(self._validate_recommendation_candidate(case_context))
            errors.extend(self._validate_human_review_boundary(case_context))

        return {
            "valid": not missing_fields and not errors,
            "phase": normalized_phase.value,
            "missing_fields": missing_fields,
            "errors": errors,
        }

    def assert_valid(
        self,
        case_context: dict[str, Any],
        phase: CaseContextPhase | str,
    ) -> None:
        result = self.validate(case_context, phase)

        if not result["valid"]:
            raise CaseContextValidationError("; ".join(result["errors"]))

    def _validate_governed_evidence_package(
        self,
        case_context: dict[str, Any],
    ) -> list[str]:
        package = case_context.get("governed_evidence_package")
        errors: list[str] = []

        if package is None:
            return errors

        if not isinstance(package, dict):
            return ["governed_evidence_package must be a dictionary"]

        if not package.get("package_id"):
            errors.append("governed_evidence_package.package_id is required")

        evidence_items = package.get("evidence_items")
        evidence_gaps = package.get("evidence_gaps", [])

        if not isinstance(evidence_items, list):
            errors.append("governed_evidence_package.evidence_items must be a list")
            return errors

        if not isinstance(evidence_gaps, list):
            errors.append("governed_evidence_package.evidence_gaps must be a list")

        if not evidence_items and not evidence_gaps:
            errors.append(
                "governed_evidence_package must include evidence_items or evidence_gaps"
            )

        for index, evidence in enumerate(evidence_items):
            errors.extend(self._validate_evidence_item(evidence, index))

        for index, gap in enumerate(evidence_gaps):
            errors.extend(self._validate_evidence_gap(gap, index))

        return errors

    def _validate_evidence_item(
        self,
        evidence: dict[str, Any],
        index: int,
    ) -> list[str]:
        required_fields = {
            "evidence_id",
            "source_id",
            "agent_id",
            "access_decision",
            "audit_id",
            "content_safety_status",
            "allowed_for_reasoning",
            "evidence_class",
        }

        missing = sorted(field for field in required_fields if field not in evidence)
        errors = [
            f"evidence_items[{index}] missing required field: {field}"
            for field in missing
        ]

        if evidence.get("access_decision") != "ALLOW":
            errors.append(
                f"evidence_items[{index}] must have access_decision ALLOW"
            )

        if evidence.get("allowed_for_reasoning") is True:
            if evidence.get("content_safety_status") not in {
                "SAFE",
                "SAFE_BY_APPROVED_PROVENANCE",
            }:
                errors.append(
                    f"evidence_items[{index}] cannot be allowed for reasoning "
                    "unless safety status is SAFE or SAFE_BY_APPROVED_PROVENANCE"
                )

        if evidence.get("evidence_class") not in {
            "free_text_evidence",
            "structured_record_evidence",
            "memory_state_evidence",
        }:
            errors.append(
                f"evidence_items[{index}] has unsupported evidence_class"
            )

        return errors

    def _validate_evidence_gap(
        self,
        gap: dict[str, Any],
        index: int,
    ) -> list[str]:
        required_fields = {
            "gap_id",
            "source_id",
            "agent_id",
            "reason",
        }

        missing = sorted(field for field in required_fields if field not in gap)

        return [
            f"evidence_gaps[{index}] missing required field: {field}"
            for field in missing
        ]

    def _validate_fusion_result(
        self,
        case_context: dict[str, Any],
    ) -> list[str]:
        fusion = case_context.get("evidence_fusion")
        errors: list[str] = []

        if fusion is None:
            return errors

        required_fields = {
            "fusion_id",
            "fusion_confidence",
            "supporting_evidence",
            "weakening_evidence",
            "conflicting_evidence",
            "missing_evidence",
            "evidence_gaps",
            "requires_human_review",
            "autonomous_action_allowed",
        }

        missing = sorted(field for field in required_fields if field not in fusion)

        for field in missing:
            errors.append(f"evidence_fusion missing required field: {field}")

        if fusion.get("autonomous_action_allowed") is not False:
            errors.append("evidence_fusion.autonomous_action_allowed must be False")

        return errors

    def _validate_reasoning_explanation(
        self,
        case_context: dict[str, Any],
    ) -> list[str]:
        reasoning = case_context.get("reasoning_explanation")
        errors: list[str] = []

        if reasoning is None:
            return errors

        required_fields = {
            "reasoning_id",
            "method",
            "kt_problem_analysis",
            "hypotheses",
            "selected_hypothesis_id",
            "reasoning_summary",
            "why_chain",
            "limits",
            "requires_human_review",
            "autonomous_action_allowed",
        }

        missing = sorted(field for field in required_fields if field not in reasoning)

        for field in missing:
            errors.append(f"reasoning_explanation missing required field: {field}")

        if reasoning.get("autonomous_action_allowed") is not False:
            errors.append(
                "reasoning_explanation.autonomous_action_allowed must be False"
            )

        return errors

    def _validate_recommendation_candidate(
        self,
        case_context: dict[str, Any],
    ) -> list[str]:
        candidate = case_context.get("recommendation_candidate")
        errors: list[str] = []

        if candidate is None:
            return errors

        required_fields = {
            "recommendation_id",
            "risk_level",
            "required_controls",
            "requires_human_approval",
            "approval_state",
            "autonomous_action_allowed",
            "candidate_status",
        }

        missing = sorted(field for field in required_fields if field not in candidate)

        for field in missing:
            errors.append(f"recommendation_candidate missing required field: {field}")

        if candidate.get("requires_human_approval") is not True:
            errors.append(
                "recommendation_candidate.requires_human_approval must be True"
            )

        if candidate.get("autonomous_action_allowed") is not False:
            errors.append(
                "recommendation_candidate.autonomous_action_allowed must be False"
            )

        return errors

    def _validate_human_review_boundary(
        self,
        case_context: dict[str, Any],
    ) -> list[str]:
        errors: list[str] = []

        if case_context.get("human_approval_required") is not True:
            errors.append("human_approval_required must be True")

        if case_context.get("autonomous_action_allowed") is not False:
            errors.append("autonomous_action_allowed must be False")

        return errors
