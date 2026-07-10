"""
Confidence panel component model.

Pure presentation helper.
"""


def confidence_panel_model(run_view_model: dict) -> dict:
    return {
        "operational_confidence": run_view_model["operational_confidence"],
        "confidence_direction": run_view_model["confidence_direction"],
        "pattern_maturity": run_view_model["pattern_maturity"],
        "selected_due_diligence_level": run_view_model[
            "selected_due_diligence_level"
        ],
        "why": run_view_model["why"],
    }
