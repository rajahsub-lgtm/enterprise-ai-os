"""
Scenario selector component model.

Pure presentation helper.
"""


def scenario_selector_options(comparison_view_model: dict) -> list[dict]:
    return [
        {
            "run_id": run["run_id"],
            "label": run["scenario_label"],
            "confidence": run["operational_confidence"],
            "due_diligence": run["selected_due_diligence_level"],
        }
        for run in comparison_view_model["runs"]
    ]
