# EAIOS 2 Sprint 4A Closeout

## Status

Sprint 4A is complete when this document and its tests pass.

Sprint 4A created the benchmark-grounded application-health observation layer.

It proves that EAIOS can take a benchmark-shaped Train Ticket / RCAEval structural input and turn it into governed enterprise AIOps records without copying raw benchmark data, without using knowledge as an answer key, and without allowing autonomous remediation.

## 4A Slices Completed

```text
4A-1 RCAEval source manifest + public dataset provenance contract
4A-2 Structural Train Ticket sample + adapter contracts
4A-3 ITIL record synthesizer from benchmark symptoms
4A-4 Issue clustering over synthesized ITIL records
4A-5 Application health observation snapshot
4A-6 Closeout contract and architecture checkpoint
```

## Files Added

```text id="bcsllw"
data/domain/it_application_health/rcaeval_train_ticket_source_manifest.json
data/domain/it_application_health/rcaeval_train_ticket_structural_sample.json
docs/EAIOS_2_SPRINT_4_RCAEVAL_MANIFEST_CONTRACT.md
docs/EAIOS_2_SPRINT_4A_CLOSEOUT.md
src/eaios/sprint4/__init__.py
src/eaios/sprint4/rcaeval_contracts.py
src/eaios/sprint4/itil_synthesizer.py
src/eaios/sprint4/issue_clustering.py
src/eaios/sprint4/application_health_observation.py
tests/test_sprint4_rcaeval_manifest_contract.py
tests/test_sprint4_rcaeval_structural_sample.py
tests/test_sprint4_itil_record_synthesizer.py
tests/test_sprint4_issue_clustering.py
tests/test_sprint4_application_health_observation.py
tests/test_sprint4_4a_closeout.py
```

## Layer Boundary

Sprint 4A establishes this layer stack:

```text id="nw9r7a"
Layer 0: RCAEval / Train Ticket benchmark truth layer
Layer 1: EAIOS structural adapter contracts
Layer 2: Synthetic ITIL operating wrapper
Layer 3: Application health observation snapshot
Layer 4: Benchmark verification result
```

Sprint 4A does not yet add the real LLM knowledge engine. That begins in Sprint 4B.

## Benchmark Truth

Benchmark-scored truth is limited to:

```text id="a9409o"
source_failure_case_id
expected issue membership by scenario composition
expected_root_cause_service
expected_root_cause_indicator
noise exclusion
```

The structural sample is hand-authored and explicitly marked:

```text id="u64oki"
copied_from_rcaeval = false
raw_benchmark_data = false
```

The public source manifest keeps the RCAEval license posture as:

```text id="ie2acv"
UNVERIFIED_PENDING_4A_LICENSE_CHECK
```

No raw RCAEval archive, copied failure record, bulk trace, bulk log, or bulk metric is committed.

## Synthetic Wrapper

The synthetic ITIL wrapper may create:

```text id="7fk44m"
SyntheticAlert
SyntheticIncident
SyntheticProblemCandidate
SyntheticChangeContext
ApplicationHealthSnapshot
```

These records are enterprise operating context. They are not independent benchmark truth.

They preserve:

```text id="jves20"
source_failure_case_id
benchmark_scoring_eligible
noise_record
provenance
human_approval_required
autonomous_action_allowed = false
```

## Anti-Circularity Rule

Sprint 4A preserves the core Sprint 4 anti-circularity rule:

```text id="bmasza"
Knowledge can inform reasoning later.
Knowledge cannot define benchmark truth.
Knowledge cannot become the answer key.
```

Benchmark verification is scored against `BenchmarkVerificationTarget`, not against:

```text id="hka3ks"
SyntheticKnowledgeArticle
LLM explanation
runbook recommendation
known-error text
postmortem summary
```

## Observation Snapshot Contract

The stable 4A output contract is:

```text id="d2p4te"
ApplicationHealthObservationSnapshot
```

It contains:

```text id="4syjdj"
snapshot_id
composition_scenario_id
source_dataset_role
sample_path
copied_from_rcaeval
raw_benchmark_data
counts
service_health
clusters
benchmark_results
clustering_summary
governance_boundaries
provenance
```

The dashboard/export primitive view is produced by:

```text id="oak5zg"
to_view_model(snapshot)
```

The view model is JSON-serializable and intentionally primitive so later UI, MCP, A2A, dashboard, and evaluation layers do not need to know internal dataclass structure.

## 4A End-to-End Flow

```text id="0bhuzw"
Structural Train Ticket sample
-> TrainTicketFaultScenario
-> TelemetrySymptom
-> BenchmarkVerificationTarget
-> SyntheticAlert
-> SyntheticIncident
-> SyntheticProblemCandidate
-> SyntheticChangeContext
-> ApplicationHealthSnapshot
-> IssueCluster
-> BenchmarkVerificationResult
-> ApplicationHealthObservationSnapshot
-> dashboard/export-ready view model
```

## Governance Boundaries Preserved

Sprint 4A preserves these boundaries:

```text id="no2ypz"
human_approval_required
autonomous_action_disabled
benchmark_truth_external
composition_based_cluster_truth
noise_excluded_from_benchmark_scoring
kb_not_answer_key
```

Autonomous remediation remains disabled.

Human approval remains required.

Noise records are excluded from benchmark scoring.

The existing domain tree remains:

```text id="epuj4d"
data/domain/it_application_health/
```

No parallel `data/domain/app_health/` tree is introduced.

## 4B Entry Criteria

Sprint 4B may begin only because 4A has locked these boundaries:

```text id="fk6c4p"
The benchmark target exists before KB reasoning.
The observation snapshot exists before LLM reasoning.
The benchmark result can be scored without KB content.
The synthetic ITIL wrapper preserves source failure provenance.
The view model exposes stable evidence and scoring fields.
Human approval and no-autonomous-action boundaries are already present.
```

## Sprint 4B Direction

Sprint 4B introduces the governed imperfect knowledge layer:

```text id="qmm06k"
exact knowledge
partial knowledge
stale knowledge
conflicting knowledge
missing knowledge
risky remediation knowledge
wrong-application knowledge
human-approval-required knowledge
```

4B must treat KB and LLM output as uncertain governed evidence.

4B must not replace `BenchmarkVerificationTarget`.

4B must not score against retrieved knowledge.

4B must preserve 4A benchmark results as the external verification layer.

## 4A Closeout Statement

Sprint 4A completes the benchmark-grounded AIOps foundation.

EAIOS now has a stable, governed, test-backed observation contract that connects benchmark-shaped application telemetry to enterprise ITIL operating records, issue clusters, and benchmark verification results.

This is the safe foundation for Sprint 4B real LLM knowledge reasoning.
