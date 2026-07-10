from pathlib import Path


DEPRECATION_MAP = Path("docs/EAIOS_2_LEGACY_DEPRECATION_MAP.md")

SPRINT3_CORE_DIRS = [
    Path("src/governance"),
    Path("src/contracts"),
    Path("src/orchestration"),
    Path("src/views"),
]

LEGACY_IMPORT_TOKENS = [
    "from src.eaios.runtime",
    "import src.eaios.runtime",
]

REQUIRED_DEPRECATION_MAP_PHRASES = [
    "Sprint 3 must not create a second parallel governed retrieval stack.",
    "ActionRequest",
    "SourceAccessRequest",
    "GovernedKnowledgeClient",
    "GovernedEvidenceClient",
    "KnowledgeRepository",
    "EvidenceFactory",
    "ContentSafetyGateway",
    "EvidenceStore",
    "GovernanceBroker / AGS",
    "structured-record evidence",
    "free-text evidence",
    "Sprint 3.1 / v1.2",
]


def python_files_under(path: Path) -> list[Path]:
    if not path.exists():
        return []

    return [
        file_path
        for file_path in path.rglob("*.py")
        if "__pycache__" not in file_path.parts
    ]


def test_legacy_deprecation_map_exists_and_names_required_boundaries():
    assert DEPRECATION_MAP.exists()

    text = DEPRECATION_MAP.read_text(encoding="utf-8")

    for phrase in REQUIRED_DEPRECATION_MAP_PHRASES:
        assert phrase in text


def test_sprint3_core_packages_do_not_import_legacy_runtime_namespace():
    offenders = []

    for directory in SPRINT3_CORE_DIRS:
        for file_path in python_files_under(directory):
            text = file_path.read_text(encoding="utf-8")
            for token in LEGACY_IMPORT_TOKENS:
                if token in text:
                    offenders.append(f"{file_path}: {token}")

    assert offenders == []


def test_current_app_entrypoint_does_not_use_legacy_demo_or_runtime():
    app_path = Path("app.py")
    assert app_path.exists()

    text = app_path.read_text(encoding="utf-8")

    assert "demo.py" not in text
    assert "runpy.run_path" not in text
    assert "from src.eaios.runtime" not in text
    assert "import src.eaios.runtime" not in text


def test_retired_eaios1_demo_entrypoint_is_absent():
    assert not Path("demo.py").exists()


def test_old_hard_coded_application_health_examples_are_absent():
    assert not Path("examples/application-health").exists()
    assert not Path("examples/application-health-realistic").exists()
