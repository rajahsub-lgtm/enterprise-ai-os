import json
from pathlib import Path


MANIFEST = Path(
    "data/domain/it_application_health/rcaeval_train_ticket_source_manifest.json"
)
DOC = Path("docs/EAIOS_2_SPRINT_4_RCAEVAL_MANIFEST_CONTRACT.md")


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_rcaeval_manifest_and_contract_exist():
    assert MANIFEST.exists()
    assert DOC.exists()


def test_rcaeval_manifest_declares_benchmark_truth_layer():
    manifest = load_manifest()

    assert manifest["dataset_name"] == "RCAEval / Train Ticket"
    assert manifest["dataset_role"] == "benchmark_truth_layer"
    assert manifest["dataset_source_type"] == "public_research_benchmark"
    assert manifest["source_repository"] == "https://github.com/phamquiluan/RCAEval"
    assert manifest["source_dataset_record"] == "https://zenodo.org/records/14590730"


def test_rcaeval_manifest_requires_license_verification_before_samples():
    manifest = load_manifest()

    assert manifest["license_status"] == "UNVERIFIED_PENDING_4A_LICENSE_CHECK"
    assert (
        manifest[
            "license_verification_required_before_commit_of_derived_samples"
        ]
        is True
    )
    assert manifest["raw_data_committed"] is False
    assert manifest["large_dataset_committed"] is False
    assert manifest["sample_committed"] is False


def test_rcaeval_manifest_blocks_large_or_unverified_data_commits():
    manifest = load_manifest()

    prohibited = set(
        manifest["prohibited_repo_artifacts_until_license_verified"]
    )

    assert "large raw RCAEval archives" in prohibited
    assert "bulk metrics" in prohibited
    assert "bulk logs" in prohibited
    assert "bulk traces" in prohibited
    assert "copied benchmark failure records" in prohibited
    assert "unverified third-party data" in prohibited


def test_rcaeval_manifest_names_expected_truth_layer_fields():
    manifest = load_manifest()

    expected_fields = set(manifest["truth_layer_fields_expected"])

    assert "failure_case_id" in expected_fields
    assert "service_topology" in expected_fields
    assert "telemetry_symptoms" in expected_fields
    assert "root_cause_service" in expected_fields
    assert "root_cause_indicator" in expected_fields
    assert "fault_type" in expected_fields
    assert "time_window" in expected_fields


def test_rcaeval_manifest_names_synthetic_augmentation_fields():
    manifest = load_manifest()

    synthetic_fields = set(manifest["synthetic_augmentation_fields"])

    assert "SyntheticIncident" in synthetic_fields
    assert "SyntheticAlert" in synthetic_fields
    assert "SyntheticProblem" in synthetic_fields
    assert "SyntheticChange" in synthetic_fields
    assert "SyntheticKnowledgeArticle" in synthetic_fields
    assert "SyntheticBusinessImpactRecord" in synthetic_fields


def test_rcaeval_manifest_locks_anti_circularity_rules():
    manifest = load_manifest()
    rules = manifest["anti_circularity_rules"]

    assert rules["root_cause_labels_from_synthetic_generator_allowed"] is False
    assert rules["benchmark_scoring_against_kb_content_allowed"] is False
    assert (
        rules["cluster_membership_source"]
        == "deterministic scenario composition using source_failure_case_id"
    )
    assert (
        rules["root_cause_source"]
        == "RCAEval-derived root_cause_service and root_cause_indicator"
    )
    assert rules["knowledge_base_role"] == (
        "governed evidence source, not answer key"
    )


def test_rcaeval_manifest_distinguishes_verification_target_and_result():
    manifest = load_manifest()

    assert manifest["benchmark_verification_objects"] == {
        "target": "BenchmarkVerificationTarget",
        "result": "BenchmarkVerificationResult",
    }


def test_rcaeval_manifest_documents_regeneration_fallback():
    manifest = load_manifest()

    fallback = manifest["regeneration_fallback"]

    assert fallback["required"] is True
    assert "regenerate telemetry" in fallback["reason"].lower()
    assert fallback["synthetic_only_labels_benchmark_scorable"] is False


def test_manifest_contract_documents_provenance_before_ingestion():
    text = DOC.read_text(encoding="utf-8")

    assert "provenance before ingestion" in text
    assert "license_status = UNVERIFIED_PENDING_4A_LICENSE_CHECK" in text
    assert "No copied benchmark records" in text
    assert "large raw RCAEval archives" in text


def test_manifest_contract_documents_composition_based_cluster_truth():
    text = DOC.read_text(encoding="utf-8")

    assert "RCAEval is an RCA benchmark, not a native incident-clustering benchmark." in text
    assert "source_failure_case_id" in text
    assert "All generated observations from the same source failure case belong to the expected cluster." in text


def test_manifest_contract_documents_kb_not_answer_key():
    text = DOC.read_text(encoding="utf-8")

    assert "KB Is Not the Answer Key" in text
    assert "Benchmark verification is independent of retrieved knowledge." in text
    assert "SyntheticKnowledgeArticle" in text
    assert "The KB is a governed evidence source, not benchmark truth." in text


def test_manifest_contract_uses_existing_it_application_health_domain_tree():
    text = DOC.read_text(encoding="utf-8")

    assert "data/domain/it_application_health/" in text
    assert "data/domain/app_health/" not in text
