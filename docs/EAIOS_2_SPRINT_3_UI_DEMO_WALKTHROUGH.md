# EAIOS 2 Sprint 3-UI Demo Walkthrough

## Purpose

This walkthrough explains the Sprint 3-UI governed orchestration replay.

The demo is not a dashboard. It is a governed orchestration replay.

It shows:

- Same alert.
- Different enterprise memory state.
- Different operational confidence.
- Different due-diligence depth.
- Same governance boundary.
- Same human approval boundary.
- Autonomous production action remains disabled.

## Demo URL

Run from the repository root:

```powershell
python scripts\export_sprint3_ui_replay_json.py
python -m http.server 8765
Open:

```text
http://localhost:8765/ui_static/replay_canvas/index.html
Opening Narrative

Most agent demos show an agent taking action.

This demo shows something more important for the enterprise:

How does an AI operating system decide how much due diligence is required before a human reviews a recommendation?

EAIOS starts with the same Digital Checkout alert in every act:

Application: Digital Checkout
Symptom: Payment authorization latency and elevated error rate

The alert is constant. The enterprise memory state changes.

Act 1 — First-time Alert / No Memory
Story

No reliable prior memory pattern exists.

EAIOS cannot shortcut the investigation. It must perform full due diligence.

Expected Replay
Act 1 stops at 7 / 7 visual events.
Due diligence: FULL_DUE_DILIGENCE
Confidence: LOW
Governance: Mandatory
Human approval: Required
Autonomous action: Off
Talking Points
The same alert starts the replay.
Memory is unavailable or immature.
EAIOS expands the path because confidence is low.
Review-required evidence is excluded from reasoning.
Evidence gaps remain visible.
The replay ends at human review, not autonomous remediation.
Closing Line

When confidence is low, EAIOS expands due diligence. It does not lower governance.

Act 2 — Trusted Memory / Validated Pattern
Story

A trusted enterprise memory pattern exists.

EAIOS can narrow the path to targeted validation.

Expected Replay
Act 2 stops at 3 / 3 visual events.
Due diligence: TARGETED_VALIDATION
Confidence: HIGH
Governance: Mandatory
Human approval: Required
Autonomous action: Off
Talking Points
The alert is still the same alert.
The difference is enterprise memory.
Memory increases confidence but is still evidence, not truth.
EAIOS performs targeted validation.
Human approval remains required.
Closing Line

The system adapts behavior, but governance boundaries remain constant.

Act 3 — Drift or Conflict
Story

Memory exists, but it may be drifting or conflicting.

EAIOS does not blindly reuse memory. It expands validation.

Expected Replay
Act 3 stops at 5 / 5 visual events.
Due diligence: EXPANDED_VALIDATION
Confidence: MEDIUM
Governance: Mandatory
Human approval: Required
Autonomous action: Off
Talking Points
The same alert now carries drift or conflict signals.
Existing memory cannot be trusted blindly.
EAIOS exposes uncertainty.
Evidence gaps remain visible.
The human reviewer receives a richer review package.
Closing Line

EAIOS is valuable because it knows when not to over-trust its own memory.

What To Emphasize

The most important takeaway is not that the UI animates.

The important takeaway is this:

Python exports the visual replay contract.
The browser only plays it.
The renderer owns the play-head.
The renderer must not invent decisions or path length.

That means the replay is explainable, testable, and governable.

Demo Success Criteria

The demo is successful when the viewer can explain:

Why Act 1 takes seven events.
Why Act 2 stops after three events.
Why Act 3 expands to five events.
Why governance does not relax.
Why memory is evidence, not truth.
Why autonomous action remains disabled.
