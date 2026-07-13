from pathlib import Path


DOC = Path("docs/EAIOS_2_SPRINT_9_CLOUD_GATE_PRE_REVIEW.md")


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_cloud_gate_pre_review_file_exists():
    assert DOC.exists()


def test_cloud_gate_pre_review_declares_purpose_and_non_approval():
    text = _text()

    assert "pre-review gate" in text
    assert "It does not approve cloud deployment." in text
    assert "It does not create cloud resources." in text
    assert "The purpose is to make the cloud decision reviewable" in text


def test_cloud_gate_pre_review_declares_current_decision():
    text = _text()

    assert "Cloud deployment is deferred." in text
    assert "interview-ready and review-only" in text
    assert "future cloud preview may be considered only after this gate" in text


def test_cloud_gate_pre_review_preserves_core_safety_posture():
    text = _text()

    for expected in [
        "static or review-only",
        "provider-disabled",
        "connector-disabled",
        "write-disabled",
        "notification-disabled",
        "remediation-disabled",
        "benchmark-isolated",
        "human-approval-required",
        "rollback-ready",
        "cost-bounded",
        "IAM-bounded",
        "audit-ready",
    ]:
        assert expected in text


def test_cloud_gate_pre_review_defines_allowed_and_disallowed_scope():
    text = _text()

    for expected in [
        "Allowed Cloud Preview Scope",
        "static documentation",
        "static portfolio pages",
        "static generated demo export",
        "read-only display of precomputed demo artifacts",
        "Disallowed Cloud Preview Scope",
        "production data connection",
        "real AI provider execution",
        "real MCP connector execution",
        "production remediation",
        "autonomous action",
    ]:
        assert expected in text


def test_cloud_gate_pre_review_prefers_static_review_site():
    text = _text()

    assert "Preferred candidate for an initial cloud preview:" in text
    assert "Static review site only." in text
    assert "It should not start an agent runtime." in text
    assert "It should not call external APIs." in text
    assert "It should not require secrets." in text



def test_cloud_gate_pre_review_defines_provider_and_mcp_gates():
    text = _text()

    for expected in [
        "Providers remain disabled by default.",
        "For Sprint 9, provider execution remains out of scope.",
        "MCP connectors remain disabled by default.",
        "For Sprint 9, MCP connector execution remains out of scope.",
        "schema validation",
        "permission class",
        "rollback or disable switch",
        "read-only first posture",
    ]:
        assert expected in text


def test_cloud_gate_pre_review_defines_data_iam_network_cost_and_audit_gates():
    text = _text()

    for expected in [
        "Data Gate",
        "The cloud preview must not use production data.",
        "IAM Gate",
        "least privilege",
        "Network Gate",
        "no production network dependency",
        "Cost Gate",
        "bounded cost posture",
        "Audit Gate",
        "what capabilities were disabled",
    ]:
        assert expected in text


def test_cloud_gate_pre_review_preserves_benchmark_and_human_approval():
    text = _text()

    for expected in [
        "Benchmark truth remains isolated.",
        "must not create, modify, infer, or overwrite benchmark truth",
        "must not define benchmark truth",
        "Human approval remains required.",
        "No action should be executable from the preview.",
    ]:
        assert expected in text


def test_cloud_gate_pre_review_requires_rollback_or_disable_plan():
    text = _text()

    for expected in [
        "Rollback or Disable Gate",
        "how to disable access",
        "how to stop serving the preview",
        "how to remove deployed artifacts",
        "who owns rollback",
        "expected rollback time",
        "how to confirm rollback is complete",
    ]:
        assert expected in text


def test_cloud_gate_pre_review_lists_review_questions():
    text = _text()

    for expected in [
        "What exactly is being deployed?",
        "Is it static or runtime-enabled?",
        "Does it require secrets?",
        "Does it call any provider?",
        "Does it call any MCP connector?",
        "Does it read production data?",
        "Does it write production data?",
        "Does it send notifications?",
        "Does it execute remediation?",
        "Does it update benchmark truth?",
        "Is human approval still required?",
        "What IAM roles are required?",
        "What network access is required?",
        "What is the cost boundary?",
        "What is the rollback or disable plan?",
    ]:
        assert expected in text


def test_cloud_gate_pre_review_recommends_no_deployment_yet():
    text = _text()

    assert "Do not deploy yet." in text
    assert "Complete Sprint 9 portfolio polish first." in text
    assert "Sprint 10 static cloud preview" in text
    assert "static-only" in text
    assert "preserve every current safety boundary" in text


def test_cloud_gate_pre_review_contains_interview_explanation_and_sound_bite():
    text = _text()

    assert "Cloud deployment is intentionally deferred." in text
    assert "cloud review gate covering static scope" in text
    assert "Cloud is not the milestone." in text
    assert "Governed readiness is the milestone." in text
    assert "preserve the enterprise safety model" in text
