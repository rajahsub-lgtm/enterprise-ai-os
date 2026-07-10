"""
Control-room header component.

Pure presentation helper. No engine decisions are made here.
"""


def control_header_model() -> dict:
    return {
        "business_outcome": "Maintain Application Health",
        "joint_goal": "Maintain service health while preserving controls",
        "governance": "Mandatory",
        "human_approval": "Required",
        "autonomous_action": "Off",
        "memory": "Evidence, not truth",
    }
