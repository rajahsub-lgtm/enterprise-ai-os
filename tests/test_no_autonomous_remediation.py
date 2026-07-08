from pathlib import Path


SOURCE_ROOTS = [
    Path("src"),
]

FORBIDDEN_FILE_NAME_TOKENS = [
    "autonomous_remediation",
    "auto_remediation",
    "remediation_executor",
    "action_executor",
    "production_executor",
]

FORBIDDEN_CONTENT_TOKENS = [
    "execute_autonomously = true",
    "\"execute_autonomously\": true",
    "'execute_autonomously': true",
    "autonomous_action_allowed = true",
    "\"autonomous_action_allowed\": true",
    "'autonomous_action_allowed': true",
]


def test_no_autonomous_remediation_executor_exists():
    violations = []

    for root in SOURCE_ROOTS:
        for path in root.rglob("*.py"):
            normalized_name = path.name.lower()

            for token in FORBIDDEN_FILE_NAME_TOKENS:
                if token in normalized_name:
                    violations.append(str(path))

    assert not violations, (
        "Autonomous remediation/executor modules are not allowed in Sprint 2.5:\n"
        + "\n".join(violations)
    )


def test_source_does_not_enable_autonomous_actions():
    violations = []

    for root in SOURCE_ROOTS:
        for path in root.rglob("*.py"):
            content = path.read_text(encoding="utf-8").lower()

            for token in FORBIDDEN_CONTENT_TOKENS:
                if token in content:
                    violations.append(f"{path}: {token}")

    assert not violations, (
        "Sprint 2.5 must not enable autonomous production action:\n"
        + "\n".join(violations)
    )