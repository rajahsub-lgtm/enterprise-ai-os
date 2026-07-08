\# ADR-006: Mandatory Governance Broker for Agent and Data Access



\## Status



Accepted



\## Context



EAIOS 2 introduces Zero Trust Agent Governance.



If agents can call each other directly, access data sources directly, or invoke tools directly, governance becomes advisory rather than enforceable.



Runtime governance requires that agent actions be intercepted before execution.



This is especially important for agentic AI because agents may dynamically choose tools, retrieve context, call other agents, summarize evidence, recommend actions, and learn from outcomes.



\## Decision



EAIOS will apply the established Zero Trust access-control pattern from NIST SP 800-207.



The Access Governance System acts as the Policy Decision Point. It evaluates policies, Goal Context, agent identity, source metadata, risk context, and required controls to produce an access decision.



Each Governance Broker interception acts as a Policy Enforcement Point. It prevents direct access to agents, tools, models, and data sources unless the Access Governance System authorizes the action.



Agents receive governed clients only. They do not receive raw endpoints, raw tool handles, direct agent handles, or direct data-source access.



Direct calls must be structurally impossible, not merely discouraged.



\## Architecture



```text

Agent

&#x20; â†“

Governed Client

&#x20; â†“

Governance Broker / PEP

&#x20; â†“

Access Governance System / PDP

&#x20; â†“

Approve / Deny / Escalate

&#x20; â†“

Agent / Tool / Data Source


