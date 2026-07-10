from pathlib import Path


CLOSEOUT = Path("docs/EAIOS_2_SPRINT_4A_CLOSEOUT.md")

REQUIRED_FILES = [
    Path("data/domain/it_application_health/rcaeval_train_ticket_source_manifest.json"),
    Path("data/domain/it_application_health/rcaeval_train_ticket_structural_sample.json"),
    Path("docs/EAIOS_2_SPRINT_4_RCAEVAL_MANIFEST_CONTRACT.md"),
    Path("docs/EAIOS_2_SPRINT_4A_CLOSEOUT.md"),
    Path("src/eaios/sprint4/__init__.py"),
    Path("src/eaios/sprint4/rcaeval_contracts.py"),
    Path("src/eaios/sprint4/itil_synthesizer.py"),
    Path("src/eaios/sprint4/issue_clustering.py"),
    Path("src/eaios/sprint4/application_health_observation.py"),
    Path("tests/test_sprint4_rcaeval_manifest_contract.py"),
    Path("tests/test_sprint4_rcaeval_structural_sample.py"),
    Path("tests/test_sprint4_itil_record_synthesizer.py"),
    Path("tests/test_sprint4_issue_clustering.py"),
    Path("tests/test_sprint4_application_health_observation.py"),
]


def _text() -> str:
    return CLOSEOUT.read_text(encoding="utf-8")


def test_sprint4_4a_closeout_file_exists():
    assert CLOSEOUT.exists()


def test_sprint4_4a_required_files_exist():
    missing = [str(path) for path in REQUIRED_FILES if not path.exists()]

    assert missing == []


def test_sprint4_4a_closeout_lists_completed_slices():
    text = _text()

    assert "4A-1 RCAEval source manifest + public dataset provenance contract" in text
    assert "4A-2 Structural Train Ticket sample + adapter contracts" in text
    assert "4A-3 ITIL record synthesizer from benchmark symptoms" in text
    assert "4A-4 Issue clustering over synthesized ITIL records" in text
    assert "4A-5 Application health observation snapshot" in text
    assert "4A-6 Closeout contract and architecture checkpoint" in text


def test_sprint4_4a_closeout_locks_layer_boundary():
    text = _text()

    assert "Layer 0: RCAEval / Train Ticket benchmark truth layer" in text
    assert "Layer 1: EAIOS structural adapter contracts" in text
    assert "Layer 2: Synthetic ITIL operating wrapper" in text
    assert "Layer 3: Application health observation snapshot" in text
    assert "Layer 4: Benchmark verification result" in text
    assert "Sprint 4B" in text


def test_sprint4_4a_closeout_defines_benchmark_truth():
    text = _text()

    assert "source_failure_case_id" in text
    assert "expected_root_cause_service" in text
    assert "expected_root_cause_indicator" in text
    assert "copied_from_rcaeval = false" in text
    assert "raw_benchmark_data = false" in text
    assert "UNVERIFIED_PENDING_4A_LICENSE_CHECK" in text


def test_sprint4_4a_closeout_blocks_raw_or_copied_dataset_commitments():
    text = _text()

    assert "No raw RCAEval archive" in text
    assert "copied failure record" in text
    assert "bulk trace" in text
    assert "bulk log" in text
    assert "bulk metric" in text


def test_sprint4_4a_closeout_defines_synthetic_itil_wrapper():
    text = _text()

    assert "SyntheticAlert" in text
    assert "SyntheticIncident" in text
    assert "SyntheticProblemCandidate" in text
    assert "SyntheticChangeContext" in text
    assert "ApplicationHealthSnapshot" in text


def test_sprint4_4a_closeout_preserves_anti_circularity():
    text = _text()

    assert "Knowledge cannot define benchmark truth." in text
    assert "Knowledge cannot become the answer key." in text
    assert "BenchmarkVerificationTarget" in text
    assert "SyntheticKnowledgeArticle" in text
    assert "LLM explanation" in text


def test_sprint4_4a_closeout_documents_observation_snapshot_contract():
    text = _text()

    assert "ApplicationHealthObservationSnapshot" in text
    assert "to_view_model(snapshot)" in text
    assert "JSON-serializable" in text
    assert "benchmark_results" in text
    assert "clustering_summary" in text
    assert "governance_boundaries" in text


def test_sprint4_4a_closeout_documents_end_to_end_flow():
    text = _text()

    assert "Structural Train Ticket sample" in text
    assert "TrainTicketFaultScenario" in text
    assert "TelemetrySymptom" in text
    assert "IssueCluster" in text
    assert "BenchmarkVerificationResult" in text
    assert "dashboard/export-ready view model" in text


def test_sprint4_4a_closeout_preserves_governance_boundaries():
    text = _text()

    assert "human_approval_required" in text
    assert "autonomous_action_disabled" in text
    assert "benchmark_truth_external" in text
    assert "composition_based_cluster_truth" in text
    assert "noise_excluded_from_benchmark_scoring" in text
    assert "kb_not_answer_key" in text
    assert "Autonomous remediation remains disabled." in text
    assert "Human approval remains required." in text


def test_sprint4_4a_closeout_preserves_existing_domain_tree():
    text = _text()

    assert "data/domain/it_application_health/" in text
    assert "No parallel `data/domain/app_health/` tree is introduced." in text


def test_sprint4_4a_closeout_sets_4b_entry_criteria():
    text = _text()

    assert "The benchmark target exists before KB reasoning." in text
    assert "The observation snapshot exists before LLM reasoning." in text
    assert "The benchmark result can be scored without KB content." in text
    assert "The synthetic ITIL wrapper preserves source failure provenance." in text


def test_sprint4_4a_closeout_defines_4b_direction_without_contaminating_scoring():
    text = _text()

    assert "exact knowledge" in text
    assert "partial knowledge" in text
    assert "stale knowledge" in text
    assert "conflicting knowledge" in text
    assert "missing knowledge" in text
    assert "risky remediation knowledge" in text
    assert "wrong-application knowledge" in text
    assert "4B must not replace `BenchmarkVerificationTarget`." in text
    assert "4B must not score against retrieved knowledge." in text
