from pathlib import Path


SPRINT3_CORE_DIRS = [
    Path("src/governance"),
    Path("src/contracts"),
    Path("src/orchestration"),
    Path("src/views"),
]

DOMAIN_SPECIFIC_FORBIDDEN_TOKENS = [
    "application_health",
    "it_application_health",
    "digital_checkout",
    "payment_authorization",
    "product_catalog",
    "order_history",
    "itil_incidents",
    "itil_changes",
    "itil_cmdb_topology",
    "itil_business_impact_map",
    "itil_operational_records",
    "cmdb_topology",
    "business_impact_map",
]


def python_files_under(path: Path) -> list[Path]:
    if not path.exists():
        return []

    return [
        file_path
        for file_path in path.rglob("*.py")
        if "__pycache__" not in file_path.parts
    ]


def test_sprint3_core_packages_remain_domain_neutral():
    offenders = []

    for directory in SPRINT3_CORE_DIRS:
        for file_path in python_files_under(directory):
            text = file_path.read_text(encoding="utf-8").lower()
            for token in DOMAIN_SPECIFIC_FORBIDDEN_TOKENS:
                if token.lower() in text:
                    offenders.append(f"{file_path}: {token}")

    assert offenders == []


def test_domain_specific_source_ids_are_allowed_in_data_not_core_code():
    registry_paths = [
        Path("data/governance/data_sources.json"),
        Path("data/governance/policies.json"),
    ]

    registry_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in registry_paths
        if path.exists()
    )

    assert "itil_incidents" in registry_text
    assert "itil_cmdb_topology" in registry_text
    assert "itil_business_impact_map" in registry_text
