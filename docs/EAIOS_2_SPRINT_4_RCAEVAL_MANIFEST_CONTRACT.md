# EAIOS 2 Sprint 4 RCAEval Manifest Contract

## Purpose

This document locks the public dataset provenance boundary for Sprint 4 before ingestion begins.

Sprint 4 uses RCAEval / Train Ticket as the benchmark truth layer, but the repo must not blindly commit public benchmark data.

The first rule of 4A is provenance before ingestion.

## Manifest Location

```text
data/domain/it_application_health/rcaeval_train_ticket_source_manifest.json
```

## Dataset Role

RCAEval / Train Ticket is used as the benchmark truth layer.

It is expected to provide or identify:

```text
failure_case_id
service_topology
telemetry_symptoms
root_cause_service
root_cause_indicator
fault_type
time_window
```

This truth layer is mapped into EAIOS contracts by deterministic adapters.

## License Posture

The manifest starts with:

```text
license_status = UNVERIFIED_PENDING_4A_LICENSE_CHECK
```

No copied benchmark records, raw archives, bulk telemetry, logs, or traces may be committed until license posture is verified.

Until then, the repo may contain only:

```text
source manifest
schema contract
adapter tests
small hand-authored structural sample with no copied benchmark records
download instructions
regeneration fallback notes
```

## Dataset Handling Boundary

The repo must not commit:

```text
large raw RCAEval archives
bulk metrics
bulk logs
bulk traces
copied benchmark failure records
unverified third-party data
private/customer data
```

The repo may commit:

```text
manifest
license/provenance note
schema adapter
small structural sample if license permits
generation config
deterministic tests
```

## Anti-Circularity Rules

### Rule 1 ? Root-Cause Truth

Synthetic generation must not invent benchmark-scored root-cause labels.

Benchmark-scored root cause must come from RCAEval-derived fields:

```text
root_cause_service
root_cause_indicator
```

### Rule 2 ? Cluster Membership

RCAEval is an RCA benchmark, not a native incident-clustering benchmark.

Sprint 4 derives cluster membership from deterministic scenario composition:

```text
source_failure_case_id
```

All generated observations from the same source failure case belong to the expected cluster.

Noise records are explicitly marked as noise.

### Rule 3 ? KB Is Not the Answer Key

Benchmark verification is independent of retrieved knowledge.

The synthetic KB may contain exact, partial, stale, conflicting, risky, or missing knowledge.

BenchmarkVerificationResult must not be scored against:

```text
SyntheticKnowledgeArticle
LLM-generated explanation
runbook recommendation
known-error text
postmortem summary
```

The KB is a governed evidence source, not benchmark truth.

## Verification Objects

Sprint 4 distinguishes:

```text
BenchmarkVerificationTarget
  Benchmark labels, composition membership, expected root cause, and scoring context.

BenchmarkVerificationResult
  EAIOS scored output: matched, partial, missed, or not scorable.
```

## Regeneration Fallback

If license or redistribution constraints block derived sample commits, the fallback is:

```text
Regenerate Train Ticket-style telemetry from open-source scenario definitions.
Mark regenerated labels as synthetic-only unless externally verified.
Exclude synthetic-only labels from RCAEval benchmark scoring.
```

## Acceptance Criteria

This contract is accepted when tests prove:

- the manifest exists
- raw data is not committed
- license verification is required
- anti-circularity rules are explicit
- KB content cannot become benchmark truth
- benchmark target/result naming is clear
- existing domain tree `data/domain/it_application_health/` is used
