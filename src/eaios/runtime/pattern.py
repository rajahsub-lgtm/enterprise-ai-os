from dataclasses import dataclass


@dataclass
class Pattern:
    """
    Represents a learned enterprise pattern.
    """

    issue: str

    occurrences: int

    historical_success_rate: float

    average_resolution: str

    known_resolution: str

    recent_failures: int

    strength: int

    trend: str
    
    last_validated: str