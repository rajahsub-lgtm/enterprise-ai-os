# EAIOS 2 Legacy Runtime Quarantine and Removal Plan

## Status

The `src/eaios` legacy runtime is quarantined in place.

It is not deleted yet.

This is intentional because older business-outcome-first contract tests still reference parts of the legacy runtime.

## Current Boundary

Sprint 3-engine core packages are:

```text
src/governance
src/contracts
src/orchestration
src/views
```

These packages must not import from:

```text
src.eaios.runtime
```

## Interpretation

The legacy runtime is:

```text
quarantined
boundary-enforced
not part of Sprint 3-engine execution
not the adaptive orchestration runtime
not the governed evidence path
not the future UI state source
```

It is not:

```text
fully removed
a current runtime dependency
a source of truth for Sprint 3-UI
```

## Removal Plan

Schedule actual removal after Sprint 3-UI demonstrates that no UI or headless engine path depends on the legacy runtime.

Recommended cleanup slice:

```text
Sprint 3-cleanup or Sprint 4-0
```

Removal tasks:

```text
replace remaining business-outcome legacy contract tests with EAIOS 2 contracts
delete src/eaios runtime modules
remove legacy references from docs except historical notes
verify python -m pytest is green
tag a cleanup checkpoint
```

## Guardrail

Until removal, the legacy runtime should remain quarantined and should not receive new Sprint 3 feature work.
