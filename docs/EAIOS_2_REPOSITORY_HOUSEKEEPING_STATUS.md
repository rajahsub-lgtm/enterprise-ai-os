# EAIOS 2 Repository Housekeeping Status

## Purpose

This document captures the transition from EAIOS 1 skeleton demo artifacts to the EAIOS 2 Sprint 2.5 architecture foundation.

## What Changed

The repo no longer uses the original hard-coded EAIOS 1 demo path as the primary demo.

The current executable path is:

```text
Business Outcome
→ Domain Repository
→ Case Context
→ Evidence Fusion
→ Reasoning Explanation
→ Recommendation Candidate
→ Human Review Package
```

With operational confidence enabled:

```text
Case Context + Memory + Evidence State
→ Operational Confidence Gate
→ Adaptive Due Diligence Decision
```

## Retired Artifact Types

The cleanup retires old EAIOS 1-style artifacts such as:

- Hard-coded `demo.py`
- Hard-coded application-health example JSON files
- Old smoke test validating the EAIOS 1 path

## Current Replacement

The old skeleton path is replaced by:

- `app.py`
- `data/domain/it_application_health/golden_scenarios.json`
- `data/domain/it_application_health/business_impact_map.json`
- `data/domain/it_application_health/cmdb_topology.json`
- `data/domain/it_application_health/operational_records.json`
- `src/domain_adapters/it_application_health/`
- `src/governance/evidence_fusion.py`
- `src/governance/reasoning_explanation.py`
- `src/governance/recommendation_candidate.py`
- `src/governance/operational_confidence.py`

## Governance Boundary

Cleanup does not weaken governance.

The current path still requires:

- Governed source access
- Evidence provenance
- Content safety
- Auditability
- Human approval
- No autonomous production action

## Important Note

References to `knowledge_agent` in governance registry and policy files are not EAIOS 1 skeleton artifacts. They are current governed-retrieval agent identities and should remain unless replaced by a future registry migration.

## Sprint 3 Readiness

The repository is now positioned for Sprint 3:

```text
Peer-reviewable demo of explainable adaptive multi-agent orchestration
under strict governance, using expanded synthetic app-health data.
```

Sprint 3 will demonstrate that the same alert can lead to different orchestration behavior depending on operational confidence, memory maturity, conflicting evidence, and collective learning.

The behavior is adaptive, but not random.
The behavior is optimized, but still governed.
