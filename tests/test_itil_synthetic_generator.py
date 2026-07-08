import hashlib
import importlib.util
import json
from pathlib import Path


GENERATOR_PATH = Path("scripts/generate_itil_synthetic_repository.py")


def load_generator_module():
    spec = importlib.util.spec_from_file_location(
        "generate_itil_synthetic_repository",
        GENERATOR_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def stable_hash(data: dict) -> str:
    payload = json.dumps(data, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def test_generator_module_exists():
    assert GENERATOR_PATH.exists()


def test_generator_is_deterministic_for_same_seed():
    generator = load_generator_module()

    first = generator.generate_repository(
        seed=2525,
        event_count=25,
        incident_count=10,
    )
    second = generator.generate_repository(
        seed=2525,
        event_count=25,
        incident_count=10,
    )

    assert stable_hash(first) == stable_hash(second)


def test_generator_changes_noise_for_different_seed():
    generator = load_generator_module()

    first = generator.generate_repository(
        seed=2525,
        event_count=25,
        incident_count=10,
    )
    second = generator.generate_repository(
        seed=2526,
        event_count=25,
        incident_count=10,
    )

    assert stable_hash(first["generated_noise"]) != stable_hash(second["generated_noise"])


def test_generator_preserves_business_outcome_and_golden_scenarios():
    generator = load_generator_module()

    repository = generator.generate_repository(
        seed=2525,
        event_count=25,
        incident_count=10,
    )

    assert repository["business_outcome"] == "Maintain Application Health"
    assert repository["counts"]["golden_scenarios"] == 6
    assert repository["golden"]["scenarios"]["scenario_count"] == 6


def test_generator_can_create_full_target_noise_counts_without_committing_output():
    generator = load_generator_module()

    repository = generator.generate_repository(
        seed=2525,
        event_count=5000,
        incident_count=2400,
    )

    assert repository["counts"]["generated_monitoring_events"] == 5000
    assert repository["counts"]["generated_incidents"] == 2400
    assert repository["counts"]["total_monitoring_events"] == 5009
    assert repository["counts"]["total_incidents"] == 2407


def test_generated_noise_references_known_cmdb_cis():
    generator = load_generator_module()

    repository = generator.generate_repository(
        seed=2525,
        event_count=100,
        incident_count=50,
    )

    ci_ids = {
        ci["ci_id"]
        for ci in repository["golden"]["topology"]["cis"]
    }

    for event in repository["generated_noise"]["monitoring_events"]:
        assert event["related_ci"] in ci_ids

    for incident in repository["generated_noise"]["incidents"]:
        assert incident["related_ci"] in ci_ids


def test_generated_noise_uses_noise_scenario_id_not_golden_scenario_ids():
    generator = load_generator_module()

    repository = generator.generate_repository(
        seed=2525,
        event_count=100,
        incident_count=50,
    )

    assert {
        event["scenario_id"]
        for event in repository["generated_noise"]["monitoring_events"]
    } == {"NOISE"}

    assert {
        incident["scenario_id"]
        for incident in repository["generated_noise"]["incidents"]
    } == {"NOISE"}


def test_generator_does_not_write_generated_repository_by_default(tmp_path):
    generator = load_generator_module()

    output_path = tmp_path / "generated.json"

    repository = generator.generate_repository(
        seed=2525,
        event_count=5,
        incident_count=2,
    )

    assert repository
    assert not output_path.exists()
