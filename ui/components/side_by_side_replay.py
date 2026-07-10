"""
Side-by-side replay component model.

Pure presentation helper.
"""


def side_by_side_columns(comparison_view_model: dict) -> list[dict]:
    return [
        {
            "run_id": summary["run_id"],
            "scenario_label": summary["scenario_label"],
            "operational_confidence": summary["operational_confidence"],
            "selected_due_diligence_level": summary[
                "selected_due_diligence_level"
            ],
            "agent_step_count": summary["agent_step_count"],
            "evidence_count": summary["evidence_count"],
            "excluded_evidence_count": summary["excluded_evidence_count"],
            "evidence_gap_count": summary["evidence_gap_count"],
            "denied_source_access_count": summary[
                "denied_source_access_count"
            ],
            "governance_required": summary["governance_required"],
            "human_approval_required": summary["human_approval_required"],
            "autonomous_action_allowed": summary["autonomous_action_allowed"],
        }
        for summary in comparison_view_model["summary"]
    ]
