from pathlib import Path


DOC = Path("docs/EAIOS_2_LEGACY_QUARANTINE_AND_REMOVAL_PLAN.md")


def test_legacy_runtime_quarantine_plan_exists():
    assert DOC.exists()

    text = DOC.read_text(encoding="utf-8")

    assert "quarantined in place" in text
    assert "It is not deleted yet." in text
    assert "Sprint 3-cleanup or Sprint 4-0" in text
    assert "should not receive new Sprint 3 feature work" in text


def test_legacy_runtime_is_present_but_quarantined():
    assert Path("src/eaios").exists()

    text = DOC.read_text(encoding="utf-8")

    assert "not part of Sprint 3-engine execution" in text
    assert "not the adaptive orchestration runtime" in text
    assert "not the governed evidence path" in text
