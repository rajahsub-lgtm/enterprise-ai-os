from pathlib import Path


PLAN = Path("docs/EAIOS_2_SPRINT_4_PLAN.md")
SIMULATION = Path("docs/EAIOS_2_SPRINT_4_SIMULATION_CONTRACT.md")
GOVERNANCE = Path("docs/EAIOS_2_SPRINT_4_GOVERNANCE_ACTIVATION_MAP.md")


def test_sprint4_docs_exist():
    assert PLAN.exists()
    assert SIMULATION.exists()
    assert GOVERNANCE.exists()


def test_sprint4_plan_locks_benchmark_grounded_headline():
    text = PLAN.read_text(encoding="utf-8")

    assert "Benchmark-Grounded Governed AIOps" in text
    assert "verifiable against an external benchmark" in text
    assert "RCAEval / Train Ticket" in text
    assert "benchmark truth layer" in text


def test_sprint4_plan_locks_itil_as_wrapper_not_truth_layer():
    text = PLAN.read_text(encoding="utf-8")

    assert "Synthetic generation is used for the enterprise operating wrapper" in text
    assert "UCI 498" in text
    assert "not the causal truth layer" in text


def test_sprint4_plan_documents_anti_circularity_rule():
    text = PLAN.read_text(encoding="utf-8")

    assert "## Anti-Circularity Rule" in text
    assert "must not invent the root-cause labels" in text
    assert "RCAEval-derived ground truth" in text


def test_sprint4_plan_documents_full_end_to_end_flow():
    text = PLAN.read_text(encoding="utf-8")

    assert "Train Ticket fault scenario creates telemetry symptoms" in text
    assert "maps those symptoms into governed ITIL-style incidents" in text
    assert "real LLM analyzes retrieved KB" in text
    assert "Agents communicate through governed MCP / A2A exchanges" in text
    assert "compared against RCAEval ground truth" in text
    assert "collective memory is updated" in text


def test_sprint4_plan_documents_sub_sprints():
    text = PLAN.read_text(encoding="utf-8")

    assert "4.0  Plan + simulation and governance contract" in text
    assert "4A   Benchmark-grounded environment + observation adapter + clustering" in text
    assert "4B   Real LLM knowledge engine over imperfect governed KB" in text
    assert "4C   Governed MCP tool/source boundary" in text
    assert "4D   Real A2A multi-agent cross-issue orchestration + restoration" in text
    assert "4E   Governed collective learning + restoration dashboard" in text


def test_simulation_contract_documents_layer_model_and_dataset_rules():
    text = SIMULATION.read_text(encoding="utf-8")

    assert "Layer 0 ? RCAEval / Train Ticket benchmark truth" in text
    assert "Layer 2 ? Synthetic ITIL operating wrapper" in text
    assert "Layer 3 ? Synthetic imperfect knowledge base" in text
    assert "Large raw benchmark datasets are not committed to the repo." in text
    assert "license_verified" in text
    assert "regeneration_fallback" in text


def test_simulation_contract_marks_synthetic_labels_not_benchmark_scorable():
    text = SIMULATION.read_text(encoding="utf-8")

    assert "benchmark_scoring_eligible = false" in text
    assert "Synthetic generation must not invent benchmark-scored root-cause labels." in text


def test_simulation_contract_documents_benchmark_verification_states():
    text = SIMULATION.read_text(encoding="utf-8")

    assert "MATCHED" in text
    assert "PARTIAL" in text
    assert "MISSED" in text
    assert "NOT_SCORABLE" in text
    assert "predicted_root_cause_service" in text
    assert "expected_root_cause_service" in text


def test_governance_activation_map_documents_real_engine_controls():
    text = GOVERNANCE.read_text(encoding="utf-8")

    assert "GOV-013" in text
    assert "GOV-015" in text
    assert "GOV-019" in text
    assert "GOV-027" in text
    assert "GOV-028" in text
    assert "GOV-021" in text
    assert "Secrets" in text
    assert "ADR-016" in text


def test_governance_activation_map_documents_ground_cite_abstain():
    text = GOVERNANCE.read_text(encoding="utf-8")

    assert "Ground, Cite, Abstain" in text
    assert "structured uncertainty" in text
    assert "citations to retrieved evidence" in text
    assert "abstention reason" in text
    assert "Thin or absent knowledge must lower confidence" in text


def test_governance_activation_map_documents_mcp_a2a_and_learning_boundaries():
    text = GOVERNANCE.read_text(encoding="utf-8")

    assert "Every MCP tool call must be" in text
    assert "A2A is a governed surface." in text
    assert "A2A must not launder unsafe or ungoverned content." in text
    assert "Only validated outcomes may update authoritative memory." in text
    assert "Autonomous production action is disabled end to end." in text


def test_sprint4_plan_clustering_ground_truth_is_composition_based():
    text = PLAN.read_text(encoding="utf-8")

    assert "RCAEval is an RCA benchmark, not a native incident-clustering benchmark." in text
    assert "source_failure_case_id" in text
    assert "Expected cluster" in text
    assert "RCAEval root-cause service and root-cause indicator labels" in text


def test_sprint4_plan_benchmark_verification_independent_of_knowledge_base():
    text = PLAN.read_text(encoding="utf-8")

    assert "Benchmark Verification Is Independent of the Knowledge Base" in text
    assert "benchmark verification is scored only against RCAEval-derived labels" in text
    assert "KB article content" in text
    assert "This prevents the KB from becoming an answer key." in text


def test_sprint4_plan_requires_secret_free_deterministic_suite():
    text = PLAN.read_text(encoding="utf-8")

    assert "Deterministic Suite Requires No Secrets" in text
    assert "must pass with no API key present" in text
    assert "CI must not require hosted-model credentials" in text


def test_sprint4_plan_activates_gov_021_stop_control():
    plan_text = PLAN.read_text(encoding="utf-8")
    governance_text = GOVERNANCE.read_text(encoding="utf-8")

    assert "GOV-021 Governed Stop / Kill Switch" in plan_text
    assert "GOV-021" in governance_text
    assert "operator stop" in governance_text
    assert "budget stop" in governance_text
    assert "safety stop" in governance_text


def test_sprint4_plan_uses_existing_it_application_health_domain_tree():
    text = PLAN.read_text(encoding="utf-8")

    assert "data/domain/it_application_health/" in text
    assert "It must not introduce a parallel `data/domain/app_health/` tree." in text

def test_sprint4_simulation_contract_distinguishes_verification_target_and_result():
    text = SIMULATION.read_text(encoding="utf-8")

    assert "BenchmarkVerificationTarget" in text
    assert "BenchmarkVerificationResult" in text
    assert "Input target used for scoring." in text
    assert "Output score produced after EAIOS proposes clusters/root cause." in text


def test_sprint4_simulation_contract_scores_clusters_by_composition_not_kb():
    text = SIMULATION.read_text(encoding="utf-8")

    assert "Expected clusters are groups of generated observations that share the same `source_failure_case_id`." in text
    assert "The knowledge base is not the benchmark answer key." in text
    assert "BenchmarkVerificationResult must not be scored against:" in text
    assert "SyntheticKnowledgeArticle" in text
