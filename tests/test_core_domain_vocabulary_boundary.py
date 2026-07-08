from pathlib import Path


CORE_PATHS = [
    Path("src/governance"),
]

ALLOWED_FILES = {
    Path("src/governance/knowledge_repository.py"),
}

BANNED_ITIL_TERMS = [
    "incident",
    "alert",
    "outage",
    "runbook",
    "major incident",
    "service health",
    "remediation",
    "change request",
    "cmdb",
    "known error",
]


def test_core_governance_files_do_not_use_itil_domain_vocabulary():
    violations = []

    for root in CORE_PATHS:
        for path in root.rglob("*.py"):
            if path in ALLOWED_FILES:
                continue

            content = path.read_text(encoding="utf-8").lower()

            for term in BANNED_ITIL_TERMS:
                if term in content:
                    violations.append(f"{path}: {term}")

    assert not violations, (
        "IT application-health vocabulary leaked into core governance files:\n"
        + "\n".join(violations)
    )