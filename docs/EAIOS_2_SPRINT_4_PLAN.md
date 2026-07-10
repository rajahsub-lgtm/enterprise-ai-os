# EAIOS 2 Sprint 4 ? Benchmark-Grounded Governed AIOps

## Headline Claim

EAIOS reasons over and governs knowledge and records to restore application health and learn ? and its conclusions are verifiable against an external benchmark.

## North Star

EAIOS observes a realistic microservice application under real fault scenarios, maps symptoms into governed ITIL records, clusters interacting issues using topology and evidence, analyzes partial/stale/conflicting knowledge with a real LLM into structured uncertain evidence, fuses it under governance, coordinates governed agents via MCP/A2A, proposes a human-approved restoration package, checks its answer against RCAEval ground truth, and improves next time through governed collective learning.

## Grounding Decision

Sprint 4 is based on RCAEval / Train Ticket.

RCAEval / Train Ticket is the benchmark truth layer:

- real microservice topology
- fault-injected telemetry
- independently labeled root causes
- benchmark-verifiable clustering and RCA outcomes

Synthetic generation is used for the enterprise operating wrapper:

- ITIL-style incidents
- alerts
- problems
- changes
- known errors
- ownership
- support groups
- business services
- business impact
- knowledge articles
- runbooks
- postmortems
- human approval outcomes

UCI 498 and other ITSM datasets may be used only as optional references for ITIL field shape and lifecycle vocabulary. They are not the causal truth layer.

## Anti-Circularity Rule

Synthetic generation may create ITIL records, knowledge articles, business impact, noise, and human-review outcomes.

Synthetic generation must not invent the root-cause labels used to evaluate clustering or RCA.

Benchmark-scored root-cause and shared-cause labels must come from RCAEval-derived ground truth, or be explicitly marked synthetic-only and excluded from benchmark scoring.

## End-to-End Flow

```text
1.  Train Ticket fault scenario creates telemetry symptoms across multiple services.
2.  EAIOS maps those symptoms into governed ITIL-style incidents and alerts.
3.  Several tickets look separate at first.
4.  EAIOS clusters them using topology, telemetry, and evidence.
5.  The knowledge base has partial / stale / conflicting articles.
6.  A real LLM analyzes retrieved KB and returns structured, uncertain evidence.
7.  Evidence fusion weighs telemetry + topology + knowledge + change context.
8.  Agents communicate through governed MCP / A2A exchanges.
9.  EAIOS proposes a human-approved restoration package.
10. The result is compared against RCAEval ground truth.
11. After a validated outcome, collective memory is updated.
12. The next similar issue is handled with better confidence or fewer steps.
```

## Architectural Non-Negotiables

1. Deterministic seam is the test boundary.
2. Telemetry-to-observation adapter is deterministic and label-grounded.
3. Governance is never bypassed.
4. LLM and retrieved content are untrusted.
5. Ground, cite, abstain.
6. A2A does not launder content.
7. Learning is a governed action.
8. No autonomous production action.
9. Benchmark verification is part of the Definition of Done.

## Sub-Sprints

```text
4.0  Plan + simulation and governance contract
4A   Benchmark-grounded environment + observation adapter + clustering
4B   Real LLM knowledge engine over imperfect governed KB
4C   Governed MCP tool/source boundary
4D   Real A2A multi-agent cross-issue orchestration + restoration
4E   Governed collective learning + restoration dashboard
```

## 4.0 Deliverables

```text
docs/EAIOS_2_SPRINT_4_PLAN.md
docs/EAIOS_2_SPRINT_4_SIMULATION_CONTRACT.md
docs/EAIOS_2_SPRINT_4_GOVERNANCE_ACTIVATION_MAP.md
tests/test_sprint4_plan_contract.py
```

## 4A ? Benchmark-Grounded Environment

Purpose:

Stand up the simulated microservice estate from RCAEval / Train Ticket, deterministically turn labeled faults into governed ITIL observations, and cluster interacting issues with a harness that holds RCAEval ground truth for verification.

Deliverables:

```text
scripts/ingest_rcaeval_scenarios.py
data/domain/it_application_health/sprint4_generation_config.json
data/domain/it_application_health/sprint4_sample_manifest.json
src/contracts/environment_snapshot.py
src/contracts/issue_cluster.py
src/domain_adapters/app_health/service_topology.py
src/domain_adapters/app_health/telemetry_observation_adapter.py
src/domain_adapters/app_health/itil_record_synthesizer.py
src/orchestration/issue_clustering.py
src/verification/rcaeval_ground_truth.py
src/views/application_health_timeline_view.py
tests/test_telemetry_observation_adapter.py
tests/test_itil_record_synthesizer.py
tests/test_sprint4_issue_clustering.py
tests/test_rcaeval_ground_truth_harness.py
```

Definition of Done:

- Ingestion and record synthesis are deterministic from a seed.
- A single fault scenario surfaces as multiple separate-looking incidents.
- Clustering groups incidents that share a real fault and excludes noise.
- Ground-truth harness scores cluster/root-cause output as matched, partial, or missed.
- Observation adapter is rule-based and explainable.

## 4B ? Real LLM Knowledge Engine

Purpose:

Synthesize a realistic knowledge base that is deliberately partial, stale, and conflicting; retrieve over it through a governed vector store; and have a real LLM return structured uncertain evidence that fusion can weigh.

Definition of Done:

- Retrieval flows through the broker.
- Vector store is a governed source.
- Retrieved chunks and LLM output are safety-classified before reasoning.
- LLM returns structured uncertain evidence with citations.
- Stale/conflicting articles weaken confidence.
- Thin or absent knowledge causes abstention or expanded diligence.
- Deterministic suite still runs against mocks.

## 4C ? Governed MCP Boundary

Purpose:

Agent source/tool access flows over real MCP, with the broker in front of every call.

Definition of Done:

- Every MCP call is broker-authorized and audited.
- Unauthorized tool call is denied and creates a trace/gap.
- Evidence retrieved via MCP carries governed provenance.

## 4D ? Real A2A Cross-Issue Orchestration

Purpose:

Governed agents coordinate across issue clusters via real agent-to-agent exchanges, compose the single-case orchestrator, and produce a human-approved restoration package.

Definition of Done:

- Cross-issue orchestration reuses the single-case orchestrator.
- Every A2A exchange is governed, audited, and provenance-preserving.
- Unsafe or ungoverned A2A payload is rejected.
- Restoration package always requires human approval.
- Autonomous action remains disabled.

## 4E ? Collective Learning + Dashboard

Purpose:

Verify against benchmark, learn from validated outcomes, and demonstrate measurably better behavior next time with a dashboard that visualizes what actually happened.

Definition of Done:

- EAIOS clustering/root-cause output is scored against RCAEval ground truth.
- Learning write updates memory only on validated outcome.
- Unvalidated outcome does not become authoritative memory.
- Run issue X, learn, run X-prime, and assert measurably better behavior.
- Dashboard shows timeline, clusters, A2A trace, and benchmark verification.

## Testing Strategy

```text
Deterministic layer:
  unit + e2e headless suite with mocks

Real-engine layer:
  contract/property tests for LLM/MCP/A2A

Benchmark layer:
  clustering/RCA scored against RCAEval ground truth

Eval layer:
  labeled knowledge Q/A set with quality baseline
```

Golden-output tests are not used for non-deterministic real engines.

## Final Sprint 4 Definition of Done

Sprint 4 is complete when the headless system proves:

```text
A real Train Ticket fault scenario is ingested.
Symptoms map deterministically to governed ITIL records.
Separate-looking incidents from one fault are clustered correctly.
Noise is excluded.
Knowledge is retrieved through a governed vector store.
Retrieved and generated content is safety-classified.
A real LLM returns structured, uncertain, cited evidence.
Stale/conflicting articles weaken confidence.
Thin/absent knowledge lowers confidence and expands diligence.
Agents coordinate through governed MCP + A2A exchanges.
No A2A exchange bypasses the evidence seam.
Restoration package always requires human approval.
Autonomous action remains disabled.
Root-cause/clustering result is scored against RCAEval ground truth.
Collective learning updates memory only on validated outcomes.
The same issue after learning is handled measurably better.
The deterministic test suite remains green.
```


## Final Lock Amendments

### Clustering Ground Truth Is Composition-Based

RCAEval is an RCA benchmark, not a native incident-clustering benchmark.

Sprint 4 defines clustering ground truth through deterministic scenario composition:

```text
RCAEval failure case       ? source_failure_case_id
Generated symptom          ? source_failure_case_id
Generated incident/alert   ? source_failure_case_id
Expected cluster           ? all observations derived from the same source_failure_case_id
Expected root cause        ? RCAEval root-cause service and root-cause indicator labels
```

This means:

- Cluster membership is derived from the composed benchmark failure case.
- Root-cause service and indicator are derived from RCAEval labels.
- Noise records are explicitly marked as noise and excluded from expected clusters.
- Benchmark scoring never depends on labels invented by the ITIL wrapper generator.

### Benchmark Verification Is Independent of the Knowledge Base

The synthetic knowledge base may contain exact, partial, stale, conflicting, risky, or missing knowledge.

However, benchmark verification is scored only against RCAEval-derived labels and scenario-composition membership.

Benchmark verification is never scored against:

```text
KB article content
LLM summaries
runbook recommendations
synthetic known-error text
postmortem text
```

This prevents the KB from becoming an answer key.

The LLM knowledge engine is evaluated as a governed evidence producer, not as the owner of benchmark truth.

### Deterministic Suite Requires No Secrets

The deterministic unit and headless e2e suite must pass with no API key present.

Live LLM, MCP, or A2A implementations must stay behind interfaces and use contract/property/eval tests.

CI must not require hosted-model credentials to keep the deterministic suite green.

### GOV-021 Governed Stop / Kill Switch

Sprint 4 activates GOV-021 because real LLM, MCP, and A2A execution introduce runtime stop risk.

A governed orchestration run must support:

```text
operator stop
budget stop
policy stop
safety stop
timeout stop
provider-failure stop
```

A stopped run must preserve audit trail, partial evidence, active agent state, and reason for stop.

### Naming Alignment

Sprint 4 uses the existing domain tree:

```text
data/domain/it_application_health/
```

It must not introduce a parallel `data/domain/app_health/` tree.

### Benchmark Verification Naming

Sprint 4 distinguishes the verification target from the scored output:

```text
BenchmarkVerificationTarget
  The benchmark labels, composition membership, expected root cause, and scoring context.

BenchmarkVerificationResult
  The scored EAIOS output: matched, partial, missed, or not scorable.
```
