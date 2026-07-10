"""
Governance passport component model.

Pure presentation helper.
"""


def governance_passport_rows(run_view_model: dict) -> list[dict]:
    return run_view_model["governance_trace_view"]["rows"]
