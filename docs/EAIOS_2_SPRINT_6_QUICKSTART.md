# EAIOS 2 Sprint 6 Quickstart

EAIOS Portfolio Demo Quickstart

Sprint 6 quickstart is a read-only portfolio demo guide.

EAIOS demonstrates benchmark-grounded governed AIOps through a read-only operator experience, cloud-readiness review, provider seam, MCP connector harness, and portfolio packaging plan.

## What You Can Show

local demo package manifest
local CLI entrypoint contract
dry-run artifact export plan
Sprint 5 operator demo narrative
Sprint 5 closeout checkpoint
cloud-readiness review state
provider and connector seams

## What You Must Not Claim

Do not claim the demo deploys cloud resources.
Do not claim the demo writes export folders.
Do not claim the demo copies files into a package.
Do not claim the demo creates archives.
Do not claim the demo loads secrets.
Do not claim the demo calls real LLM providers.
Do not claim the demo connects real MCP tools.
Do not claim the demo executes remediation.
Do not claim the demo scores benchmarks from demo output.

## Sprint 5 Command Contract

eaios sprint5 run --scenario application-health --read-only

src/eaios/sprint5/scenario_command.py

This is not a real shell executor.

## Sprint 6 Local CLI Contract

src/eaios/sprint6/local_cli.py

eaios sprint6 package show-manifest --read-only --format text

SHOW_PACKAGE_MANIFEST
SHOW_GOVERNANCE_BOUNDARIES
SHOW_READINESS_SUMMARY
JSON_VIEW_MODEL

## Sprint 6 Package Manifest

src/eaios/sprint6/demo_package.py

sprint6-demo-package-manifest-001

LOCAL_MANIFEST_ONLY

The manifest does not write package artifacts.

## Sprint 6 Dry-Run Artifact Export Plan

src/eaios/sprint6/artifact_export_plan.py

sprint6-artifact-export-plan-001

DRY_RUN_ONLY

artifacts/eaios-demo

The plan does not create the export folder.
The plan does not copy files.
The plan does not create an archive.

## Test Commands

python -m pytest tests\\test_sprint6_demo_package.py --basetemp .pytest_tmp
python -m pytest tests\\test_sprint6_local_cli.py --basetemp .pytest_tmp
python -m pytest tests\\test_sprint6_artifact_export_plan.py --basetemp .pytest_tmp
python -m pytest tests\\test_sprint6_quickstart.py --basetemp .pytest_tmp
python -m pytest --basetemp .pytest_tmp

## Walkthrough

1. Open the Sprint 5 demo narrative.
2. Explain the application-health scenario and benchmark-grounded governance.
3. Show the Sprint 5 closeout checkpoint.
4. Show the Sprint 6 local demo package manifest.
5. Show the Sprint 6 local CLI contract.
6. Show the Sprint 6 dry-run artifact export plan.
7. Emphasize that all unsafe actions remain blocked.
8. Close with the cloud-readiness and human-review story.

## Governance Boundaries

read_only_demo
local_manifest_only
dry_run_only
human_review_required
package_file_write_blocked
export_folder_creation_blocked
file_copy_blocked
archive_creation_blocked
shell_command_execution_blocked
cloud_resource_creation_blocked
secret_loading_blocked
provider_call_blocked
real_connector_call_blocked
external_write_blocked
remediation_blocked
notification_blocked
benchmark_scoring_from_package_blocked
benchmark_scoring_from_export_blocked
autonomous_remediation_disabled

## Cloud Readiness

REVIEW_READY_NOT_DEPLOYED
GCP_READINESS_REVIEW_ONLY

cloud_architecture_review
security_and_secret_handling_review
provider_integration_review
mcp_connector_permission_review
production_deployment_approval

## Demo Close

This is a portfolio-ready, read-only demo of EAIOS governance and operator experience.

It explains the demo without executing unsafe actions.

The next slice can create an optional static HTML review page model or portfolio walkthrough contract.
