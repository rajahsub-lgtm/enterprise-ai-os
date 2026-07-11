# EAIOS 2 Sprint 5 Demo Narrative

## Status

Sprint 5 demo narrative is complete when this document and its tests pass.

This narrative explains the read-only operator experience built on top of Sprint 4 benchmark-grounded governed AIOps.

## Demo Title

```text
EAIOS Operator Experience: Benchmark-Grounded Governed AIOps
```

## One-Line Demo

```text
EAIOS shows an operator how application-health evidence, governed reasoning, safe restoration, human approval, learning, and cloud readiness fit together ? without executing remediation or weakening governance.
```

## What This Demo Shows

Sprint 5 demonstrates:

```text
read-only operator dashboard export
read-only CLI demo runner
single end-to-end scenario command
operator review screen model
cloud-safe configuration profile
provider plug-in safety seam
MCP connector simulation harness
GCP deployment readiness checklist
README demo narrative
```

## What This Demo Does Not Do

Sprint 5 does not:

```text
execute remediation
restart services
scale services
modify databases
deploy code
rollback production
send notifications
page on-call
publish status
call real tools
call real LLM providers
load secrets
access external networks
create cloud resources
write external data
score benchmarks from demo output
apply dashboard changes automatically
enable autonomous remediation
auto-approve production knowledge
```

## Read-Only Command Path

The canonical demo command path is:

```text
eaios sprint5 run --scenario application-health --read-only
```

In Sprint 5 this command is represented as a contract, not as a real shell executor.

The source contract is:

```text
src/eaios/sprint5/scenario_command.py
```

The command result state is:

```text
COMPLETED_READ_ONLY
```

## Operator Dashboard Export

The operator dashboard export is created by:

```text
src/eaios/sprint5/operator_experience.py
```

It produces:

```text
OperatorDashboardExport
OperatorDashboardCard
json_view_model
markdown_summary
cli_text
```

The export mode is:

```text
READ_ONLY_DEMO
```

The export keeps these boundaries:

```text
real_tool_execution_performed = false
autonomous_remediation_allowed = false
dashboard_changes_applied = false
benchmark_scoring_allowed_from_export = false
human_review_required = true
```

## CLI Demo Runner

The CLI demo runner is created by:

```text
src/eaios/sprint5/demo_runner.py
```

It produces:

```text
DemoRunResult
DemoRunStep
rendered_markdown
rendered_cli_text
rendered_json_view_model
governance_checks
blocked_actions
```

The demo mode is:

```text
READ_ONLY_LOCAL
```

The runner does not run shell commands or perform external actions.

## Single Scenario Command

The scenario command contract is created by:

```text
src/eaios/sprint5/scenario_command.py
```

It supports:

```text
RUN_APPLICATION_HEALTH_DEMO
EXPORT_OPERATOR_DASHBOARD
VERIFY_GOVERNANCE_BOUNDARIES
```

It supports output formats:

```text
CLI_TEXT
MARKDOWN
JSON_VIEW_MODEL
```

Unsupported commands are blocked.

Non-read-only invocations are blocked.

## Operator Review Screen

The operator review screen model is created by:

```text
src/eaios/sprint5/operator_review_screen.py
```

It produces:

```text
OperatorReviewScreenModel
OperatorReviewSectionCard
OperatorDecisionControl
```

Decision controls are disabled in the read-only demo:

```text
APPROVE_PACKAGE_FOR_MANUAL_EXECUTION
REQUEST_MORE_EVIDENCE
REJECT_PACKAGE
DEFER_TO_SERVICE_OWNER
```

Approval requires an external governed human process.

The screen does not record approvals, route work, or execute remediation.

## Cloud-Safe Configuration

The cloud-safe configuration profile is created by:

```text
src/eaios/sprint5/cloud_safety_config.py
```

It produces:

```text
CloudSafeConfigProfile
CloudCapabilityToggle
CloudSafetyChecklistItem
```

The target environment is:

```text
GCP_READINESS_REVIEW
```

Allowed capabilities remain local and read-only:

```text
runtime.read_only_demo
operator_review_screen_rendering
local_json_export
local_markdown_export
governance_check_summary
```

Blocked capabilities include:

```text
provider.llm
mcp.connectors
cloud.gcp_deploy
storage.external_write
dashboard.apply_changes
autonomous_remediation
benchmark_scoring_from_cloud_profile
```

## Provider Plug-In Safety Seam

The provider plug-in safety seam is created by:

```text
src/eaios/sprint5/provider_plugin_seam.py
```

It produces:

```text
ProviderPluginSeamProfile
ProviderRequestEnvelope
ProviderValidationResult
```

The provider mode is:

```text
DETERMINISTIC_FIXTURE_ONLY
```

Only deterministic local fixtures are allowed.

Real provider calls are disabled by default.

Secret loading is blocked.

Network access is blocked.

Benchmark scoring from provider output is blocked.

Autonomous action requests are blocked.

## MCP Connector Simulation Harness

The MCP connector simulation harness is created by:

```text
src/eaios/sprint5/mcp_connector_harness.py
```

It produces:

```text
MCPConnectorHarnessProfile
MCPConnectorDefinition
MCPConnectorSimulationRequest
MCPConnectorSimulationResult
```

The harness mode is:

```text
READ_ONLY_SIMULATION
```

The harness allows simulated read-only context and knowledge requests.

The harness blocks:

```text
real_connector_call
secret_loading
external_write
remediation_execution
notification_send
benchmark_scoring_from_connector
autonomous_remediation
```

## GCP Deployment Readiness Checklist

The GCP readiness checklist is created by:

```text
src/eaios/sprint5/gcp_readiness_checklist.py
```

It produces:

```text
GCPReadinessChecklist
GCPReadinessCheck
GCPDeploymentGate
```

The readiness state is:

```text
REVIEW_READY_NOT_DEPLOYED
```

The checklist generates a deployment readiness review, not a deployment.

Allowed next steps are review-only:

```text
review_local_demo_export
review_operator_screen_model
review_cloud_safety_profile
review_provider_plugin_seam
review_mcp_connector_harness
```

Blocked deployment actions include:

```text
create_cloud_resources
run_shell_deployment_command
load_secret_material
enable_real_provider
enable_real_mcp_connectors
perform_external_write
execute_remediation
send_notification
score_benchmark_from_deployment
```

Required human reviews include:

```text
cloud_architecture_review
security_and_secret_handling_review
provider_integration_review
mcp_connector_permission_review
production_deployment_approval
```

## Demo Storyboard

Use this story to explain the demo:

```text
1. EAIOS starts from a benchmark-grounded application-health scenario.
2. Sprint 4 produces governed evidence, reasoning, restoration, approval, learning, and dashboard candidates.
3. Sprint 5 turns that governed state into an operator-facing read-only experience.
4. The operator can review context, blocked actions, improvement candidates, and cloud readiness.
5. The system makes safety boundaries visible instead of hiding them.
6. The demo proves the architecture can be explained and reviewed without taking unsafe action.
```

## Operator Talk Track

A concise operator-facing talk track:

```text
This is a read-only governed AIOps demo.
The scenario is application health.
The benchmark truth remains external.
The dashboard shows what EAIOS knows, what it recommends for review, what it learned, and what remains blocked.
No remediation is executed.
No real tools or providers are called.
No secrets are loaded.
No cloud resources are created.
Human review remains required.
```

## Governance Talk Track

A concise governance-facing talk track:

```text
Sprint 5 demonstrates that EAIOS can expose its reasoning path, evidence, decisions, blocked actions, and cloud-readiness gates as reviewable artifacts.
The system does not treat KB, LLM, tool, restoration, learning, dashboard, or operator output as benchmark truth.
Every external or unsafe capability is blocked by default and represented as an explicit review gate.
```

## Cloud Readiness Talk Track

A concise cloud-readiness talk track:

```text
The GCP readiness checklist is not a deployment.
It is a review artifact.
It shows what would need approval before cloud resource creation, secret loading, provider calls, real MCP connectors, external writes, remediation, notifications, or benchmark scoring could be considered.
```

## End-to-End Sprint 5 Flow

```text
Sprint 4 governed learning dashboard
-> operator dashboard export
-> read-only demo runner
-> single scenario command
-> operator review screen
-> cloud-safe configuration profile
-> provider plug-in safety seam
-> MCP connector simulation harness
-> GCP deployment readiness checklist
-> demo narrative
```

## Sprint 5 Safety Boundaries

Sprint 5 preserves:

```text
read_only_demo
human_review_required
real_shell_command_execution_blocked
real_tool_execution_blocked
provider_call_blocked
secret_loading_blocked
network_access_blocked
external_write_blocked
cloud_resource_creation_blocked
remediation_blocked
notification_blocked
dashboard_changes_not_applied
benchmark_truth_external
benchmark_scoring_from_demo_blocked
autonomous_remediation_disabled
production_knowledge_auto_approval_blocked
```

## Demo Success Criteria

The Sprint 5 demo is successful when it can show:

```text
operator-facing dashboard export
CLI text output
Markdown output
JSON view model output
single application-health scenario command contract
disabled operator decision controls
explicit blocked actions
cloud-safe configuration boundary
provider seam blocked by default
MCP connector harness read-only simulation
GCP readiness checklist
governance boundaries visible in every layer
```

## Recommended Live Demo Sequence

Recommended order:

```text
1. Show the one-line demo.
2. Show the read-only command path.
3. Show the operator dashboard export.
4. Show the operator review screen.
5. Show disabled decision controls.
6. Show blocked actions.
7. Show the provider seam.
8. Show the MCP connector harness.
9. Show the GCP readiness checklist.
10. Close with the governance thesis.
```

## Closeout Statement

Sprint 5 creates the operator-facing and cloud-readiness demo narrative for EAIOS.

It turns Sprint 4 benchmark-grounded governed AIOps contracts into a reviewable, read-only experience.

The demo is ready for Sprint 5 closeout and future packaging work.


## Sprint 5 GCP Readiness Target Environment

GCP_READINESS_REVIEW_ONLY
