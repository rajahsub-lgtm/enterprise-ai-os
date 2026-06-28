import json
from pathlib import Path
from datetime import datetime


class ExecutionLogger:
    """
    Records every EAIOS execution.

    The execution log becomes raw enterprise experience
    from which future Enterprise Memory can evolve.
    """

    def __init__(
        self,
        log_path: str = "data/memory/execution_history.json",
    ) -> None:
        self.log_path = Path(log_path)

    def record(self, record: dict) -> None:
        history = []

        if self.log_path.exists():
            with self.log_path.open("r", encoding="utf-8") as f:
                history = json.load(f)

        history.append(record)

        with self.log_path.open("w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    def build_record(
        self,
        trace,
        confidence,
        strategy,
        recommendation,
    ) -> dict:

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "business_outcome": trace.business_outcome,
            "capability": trace.capability,
            "confidence": confidence["operational_confidence"],
            "strategy": strategy["strategy"],
            "recommendation": recommendation["recommendation"],
            "human_validation": recommendation["requires_human_approval"],
            "safety_status": trace.safety_status,
        }