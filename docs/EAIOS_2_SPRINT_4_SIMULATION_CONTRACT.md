# EAIOS 2 Sprint 4 Simulation Contract

## Purpose

This contract defines the simulation and benchmark boundary for Sprint 4.

Sprint 4 is benchmark-grounded, not purely synthetic.

## Layer Model

```text
Layer 0 ? RCAEval / Train Ticket benchmark truth
Layer 1 ? EAIOS domain adapter
Layer 2 ? Synthetic ITIL operating wrapper
Layer 3 ? Synthetic imperfect knowledge base
Layer 4 ? EAIOS orchestration traces
Layer 5 ? Collective learning and dashboard views
```

## Layer 0 ? Benchmark Truth

RCAEval / Train Ticket provides:

- service topology
- fault scenarios
- telemetry symptoms
- root-cause service labels
- root-cause indicator labels
- benchmark verification target

This layer is not authored by the EAIOS synthetic generator.

## Layer 1 ? Domain Adapter

The app-health domain adapter maps benchmark truth into EAIOS contracts:

```text
TrainTicketFaultScenario
ServiceTopology
TelemetrySymptom
EnvironmentSnapshot
IssueCluster
ApplicationHealthSnapshot
BenchmarkVerificationTarget
```

The telemetry-to-observation adapter is deterministic and label-grounded.

It does not learn detection rules.

It maps labeled benchmark faults into observations, alerts, and candidate ITIL records by rule.

## Layer 2 ? Synthetic ITIL Wrapper

Synthetic ITIL records are derived from benchmark faults.

Generated records include:

```text
SyntheticIncident
SyntheticAlert
SyntheticProblem
SyntheticChange
SyntheticKnownError
SyntheticBusinessService
SyntheticSupportGroup
SyntheticOwnershipRecord
SyntheticBusinessImpactRecord
```

Every synthetic record must include provenance:

```text
source_layer
derived_from_fault_id
derived_from_service
generation_seed
synthetic_field_flags
benchmark_scoring_eligible
```

## Layer 3 ? Synthetic Knowledge Base

The knowledge base is synthetic and deliberately imperfect.

It must include:

```text
exact article
partial article
stale article
conflicting article
missing article case
risky remediation article
human-approval-required article
wrong-application article
```

Knowledge is never truth.

Knowledge becomes governed evidence only after retrieval, safety classification, LLM analysis, citation, and evidence-fusion eligibility checks.

## Layer 4 ? Orchestration Traces

EAIOS generates orchestration records:

```text
GovernedEvidencePackage
KnowledgeAnalysisResult
AgentMessage
McpToolCallEvent
A2AAgentExchange
RestorationRecommendation
HumanApprovalPackage
BenchmarkVerificationResult
```

## Layer 5 ? Learning and Dashboard

Learning writes are governed actions.

Dashboard views must be derived from orchestration data.

The dashboard must not invent decisions, scores, messages, or benchmark results.

## Anti-Circularity Rule

Synthetic generation may create enterprise context.

Synthetic generation must not invent benchmark-scored root-cause labels.

If a label is synthetic-only, it must be marked:

```text
benchmark_scoring_eligible = false
```

## Dataset Handling Rule

Large raw benchmark datasets are not committed to the repo.

The repo may commit:

```text
source manifest
license/provenance note
schema adapter
small sample if license permits
generation config
deterministic tests
```

The repo must not commit:

```text
large raw RCAEval archives
bulk telemetry dumps
unverified third-party data
private/customer data
```

## Required Manifests

Sprint 4 must include a public dataset manifest with:

```text
dataset_name
dataset_source_url
dataset_license
license_verified
permitted_repo_artifacts
raw_data_committed
sample_committed
transformation_summary
schema_mapping_summary
regeneration_fallback
```

## Benchmark Verification States

```text
MATCHED
PARTIAL
MISSED
NOT_SCORABLE
```

A benchmark verification result must preserve:

```text
predicted_root_cause_service
expected_root_cause_service
predicted_root_cause_indicator
expected_root_cause_indicator
matched_issue_ids
missed_issue_ids
noise_excluded
comparison_note
```


## Precise Benchmark Semantics

RCAEval provides root-cause labels, not native ITIL incident clusters.

Sprint 4 derives cluster membership from deterministic scenario composition:

```text
source_failure_case_id
source_root_cause_service
source_root_cause_indicator
composition_scenario_id
noise_record
benchmark_scoring_eligible
```

Expected clusters are groups of generated observations that share the same `source_failure_case_id`.

Expected root cause is RCAEval's labeled root-cause service and root-cause indicator.

Synthetic ITIL records may add enterprise context, but they must preserve the original benchmark-derived identifiers.

## Knowledge Independence Rule

The knowledge base is not the benchmark answer key.

BenchmarkVerificationResult must be scored against:

```text
BenchmarkVerificationTarget
scenario composition membership
RCAEval root-cause service label
RCAEval root-cause indicator label
```

BenchmarkVerificationResult must not be scored against:

```text
SyntheticKnowledgeArticle
LLM-generated explanation
runbook recommendation
known-error text
postmortem summary
```

## Verification Object Names

```text
BenchmarkVerificationTarget
  Input target used for scoring.

BenchmarkVerificationResult
  Output score produced after EAIOS proposes clusters/root cause.
```
