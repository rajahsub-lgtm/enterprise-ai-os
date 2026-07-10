"""
Human review boundary component model.

Pure presentation helper.
"""


def human_review_boundary_model(run_view_model: dict) -> dict:
    boundaries = run_view_model["safety_boundaries"]

    return {
        "title": "Human approval required",
        "governance_required": boundaries["governance_required"],
        "human_approval_required": boundaries["human_approval_required"],
        "autonomous_action_allowed": boundaries["autonomous_action_allowed"],
        "available_actions": [
            "Approve recommendation",
            "Reject recommendation",
            "Request more evidence",
        ],
        "note": "Simulation only. No production action is executed.",
    }
