# EAIOS 2 Sprint 4 Governance Activation Map

## Purpose

Sprint 4 activates governance controls that were not required when the system was deterministic and in-process.

## Activated Controls

| Control | Sprint 4 Reason |
|---|---|
| GOV-013 | RAG injection risk from retrieved KB content |
| GOV-015 | LLM output is not truth |
| GOV-019 | hosted model / third-party / data boundary |
| GOV-027 | token cost, loop caps, budget enforcement |
| GOV-028 | provider outage, timeout, degraded mode |
| GOV-021 | governed stop / kill switch for live LLM, MCP, and A2A execution |
| GOV-024 | reassess before any real non-synthetic data |
| Secrets | API keys and credentials now exist |
| ADR-016 | governed writable memory and anti-poisoning |

## Control Rules

### Retrieval

Knowledge retrieval flows through the broker.

The vector store is a governed source.

Retrieved chunks are untrusted until classified.

### LLM Output

LLM output is not truth.

LLM output must be:

```text
schema-validated
safety-classified
grounded
cited
abstention-aware
converted into governed evidence
```

Unsupported claims are rejected or downgraded.

### Ground, Cite, Abstain

The LLM analyzer must produce:

```text
structured uncertainty
citations to retrieved evidence
confidence
recommended evidence use
abstention reason when knowledge is weak
```

Thin or absent knowledge must lower confidence and expand diligence.

### MCP

Every MCP tool call must be:

```text
broker-authorized
policy-evaluated
audited
provenance-preserving
```

Denied calls create a trace and evidence gap.

### A2A

A2A is a governed surface.

Agent-to-agent exchanges must preserve:

```text
source agent
target agent
goal context
evidence provenance
safety classification
usage constraints
audit record
```

A2A must not launder unsafe or ungoverned content.

### Learning

Learning writes are governed actions.

Only validated outcomes may update authoritative memory.

Unvalidated, stale, or conflicting memory remains supporting-only.

### Restoration

Every restoration recommendation is a human-approval package.

Autonomous production action is disabled end to end.

## Non-Goals

```text
No real customer data.
No production cloud deployment.
No financial-domain adapter.
No model fine-tuning.
No learned anomaly detector.
No autonomous production action.
No abandoning deterministic tests.
```


## GOV-021 Governed Stop / Kill Switch

Real LLM, MCP, and A2A execution require a governed stop capability.

A run may be stopped by:

```text
operator stop
policy stop
safety stop
budget stop
loop cap
timeout
provider failure
tool failure
```

A stopped run must preserve:

```text
stop_reason
stop_actor
partial evidence
agent state
MCP tool-call trail
A2A exchange trail
audit record
human-review status
```

A stop is not a failure of governance.

A stop is a governed safety outcome.

## Secret-Free Deterministic Suite

The deterministic unit and headless e2e suite must pass with no API key present.

Live provider credentials are required only for explicit real-engine contract/eval runs.

Missing hosted-model credentials must not fail the core deterministic suite.
