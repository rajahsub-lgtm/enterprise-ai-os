from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_9_INTERVIEW_QA_PACK.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_interview_qa_pack_file_exists():
    assert DOC.exists()


def test_interview_qa_pack_declares_purpose_and_positioning():
    text = _text()

    assert "concise interview answers" in text
    assert "enterprise AI architect" in text
    assert "EAIOS is a governed enterprise AI operating-system pattern." in text
    assert "synthetic in data execution and real in enterprise architecture" in text


def test_interview_qa_pack_contains_one_sentence_answer_and_sound_bite():
    text = _text()

    assert "One-Sentence Answer" in text
    assert "coordinate AI capabilities around application health" in text
    assert "Most agent demos try to prove an agent can act." in text
    assert "EAIOS proves the enterprise can decide when an agent must not act." in text


def test_interview_qa_pack_answers_what_and_why():
    text = _text()

    for expected in [
        "## Q1. What is EAIOS?",
        "## Q2. What problem does it solve?",
        "## Q3. Why is this different from a normal agent demo?",
        "## Q4. Is the demo real or synthetic?",
        "## Q5. Why use synthetic data?",
    ]:
        assert expected in text


def test_interview_qa_pack_distinguishes_real_synthetic_and_not_real_yet():
    text = _text()

    for expected in [
        "The data execution is synthetic.",
        "The architecture is real.",
        "The real parts are the architecture",
        "The operating records are synthetic.",
        "The production integrations are not enabled.",
        "does not connect to real ServiceNow",
    ]:
        assert expected in text



def test_interview_qa_pack_centers_high_evidence_low_confidence():
    text = _text()

    assert "HIGH evidence / LOW operational confidence split" in text
    assert "evidence is coherent enough to support a hypothesis" in text
    assert "lacks enough validation to act safely" in text
    assert "does not confuse evidence strength with permission to act" in text
    assert "Strong evidence is not the same as permission to act." in text


def test_interview_qa_pack_covers_service_observability_and_business_mapping():
    text = _text()

    for expected in [
        "## Q13. How does EAIOS map to ServiceNow?",
        "## Q14. How does it map to observability tools?",
        "## Q15. How does it map to CMDB and business impact?",
        "ServiceNow would likely provide incidents",
        "BigPanda or similar tools would provide correlated alerts",
        "Dynatrace or similar tools would provide metrics",
        "SAP SolMan would provide SAP-specific",
        "Solution 360 or BSI-style data provides business service impact",
    ]:
        assert expected in text


def test_interview_qa_pack_covers_provider_mcp_and_safety_boundaries():
    text = _text()

    for expected in [
        "## Q16. What is the provider boundary?",
        "AI providers are not enabled in the current demo.",
        "Provider output is advisory until validated and reviewed.",
        "## Q17. What is the MCP connector boundary?",
        "MCP connectors are not enabled in the current demo.",
        "## Q18. How do you prevent unsafe action?",
        "autonomous remediation disabled",
    ]:
        assert expected in text


def test_interview_qa_pack_covers_benchmark_cloud_and_production_path():
    text = _text()

    for expected in [
        "## Q19. What is benchmark truth isolation?",
        "Benchmark truth is kept separate from runtime output.",
        "## Q20. Why defer cloud deployment?",
        "Cloud deployment is deferred",
        "## Q21. How would you move from demo to production?",
        "enable controlled read-only integration",
        "expand only after governance approval",
    ]:
        assert expected in text


def test_interview_qa_pack_covers_audience_specific_explanations():
    text = _text()

    for expected in [
        "## Q23. How does this relate to AIOps?",
        "## Q24. How does this relate to ITIL?",
        "## Q25. How does this relate to AI governance?",
        "## Q26. What is your role in this architecture?",
        "## Q27. What is the simplest way to explain EAIOS to an executive?",
        "## Q28. What is the simplest way to explain EAIOS to an engineer?",
        "## Q29. What is the simplest way to explain EAIOS to a risk leader?",
    ]:
        assert expected in text


def test_interview_qa_pack_contains_rapid_answer_bank_and_final_close():
    text = _text()

    for expected in [
        "## Q30. What is the final interview close?",
        "Rapid Answer Bank",
        "Is this production?",
        "Does it call tools?",
        "Does it remediate?",
        "The future is governed orchestration of AI capabilities around business outcomes.",
    ]:
        assert expected in text
