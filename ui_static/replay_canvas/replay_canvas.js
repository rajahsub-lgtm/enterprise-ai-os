
const REPLAY_JSON_PATH = "../../ui_replay_exports/eaios_sprint3_replay.json";

const PRESENTER_ACTS = [
  {
    act_id: "act-1",
    label: "Act 1 ? First-time alert",
    run_label: "First-time / no memory",
    headline: "No trusted memory exists, so EAIOS performs full due diligence.",
    demo_cue: "Select Act 1, press Play, and watch the full evidence path unfold.",
    talking_points: [
      "The alert is the same Digital Checkout payment authorization degradation.",
      "Because memory is unavailable or immature, EAIOS does not shortcut investigation.",
      "Governance gates still stamp source access before evidence can move.",
      "Review-required evidence is excluded from reasoning.",
      "The act ends with human review, not autonomous remediation."
    ],
    closing_line: "When confidence is low, EAIOS expands diligence. It does not lower governance."
  },
  {
    act_id: "act-2",
    label: "Act 2 ? Trusted memory",
    run_label: "Trusted memory / validated pattern",
    headline: "Trusted enterprise memory increases confidence and narrows validation.",
    demo_cue: "Select Act 2, press Play, and compare the shorter governed path.",
    talking_points: [
      "The alert is still the same alert.",
      "The difference is enterprise memory: prior validated pattern exists.",
      "EAIOS can move from full due diligence to targeted validation.",
      "Memory influences confidence, but memory is still evidence, not truth.",
      "Human approval remains required before action."
    ],
    closing_line: "The system adapts behavior, but governance boundaries remain constant."
  },
  {
    act_id: "act-3",
    label: "Act 3 ? Drift or conflict",
    run_label: "Drift or conflict",
    headline: "When memory drifts or conflicts, EAIOS expands validation again.",
    demo_cue: "Select Act 3, press Play, and show how uncertainty becomes visible.",
    talking_points: [
      "The same alert now carries drift or conflict signals.",
      "EAIOS does not blindly trust memory just because memory exists.",
      "Evidence gaps and excluded evidence are shown, not hidden.",
      "Validation expands because confidence is not stable.",
      "The human reviewer gets a richer explanation of uncertainty."
    ],
    closing_line: "EAIOS is valuable because it knows when not to over-trust its own memory."
  }
];



let payload = null;
let currentRun = null;
let currentEventIndex = -1;
let timer = null;

const playPause = document.getElementById("play-pause");
const nextButton = document.getElementById("next-event");
const resetButton = document.getElementById("reset");
const selector = document.getElementById("run-selector");

async function loadReplay() {
  const response = await fetch(REPLAY_JSON_PATH);
  payload = await response.json();

  document.getElementById("comparison-title").textContent = payload.comparison.comparison_label;

  payload.runs.forEach((run, index) => {
    const option = document.createElement("option");
    option.value = run.run_id;
    option.textContent = run.scenario_label;
    selector.appendChild(option);
    if (index === 0) currentRun = run;
  });

  selector.addEventListener("change", () => {
    currentRun = payload.runs.find((run) => run.run_id === selector.value);
    resetReplay();
  });

  playPause.addEventListener("click", togglePlay);
  nextButton.addEventListener("click", nextEvent);
  resetButton.addEventListener("click", resetReplay);

  renderPresenterMode();
  setPresenterAct(PRESENTER_ACTS[0]);
}


function renderPresenterMode() {
  const buttonContainer = document.getElementById("presenter-act-buttons");
  if (!buttonContainer || !payload) return;

  buttonContainer.innerHTML = "";

  PRESENTER_ACTS.forEach((act) => {
    const button = document.createElement("button");
    button.className = "act-button";
    button.dataset.actId = act.act_id;
    button.textContent = act.label;
    button.addEventListener("click", () => setPresenterAct(act));
    buttonContainer.appendChild(button);
  });
}

function setPresenterAct(act) {
  if (!payload || !act) return;

  const run = payload.runs.find((candidate) => candidate.scenario_label === act.run_label);
  if (!run) return;

  currentRun = run;
  selector.value = run.run_id;
  resetReplay();

  document.querySelectorAll(".act-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.actId === act.act_id);
  });

  document.getElementById("presenter-headline").textContent = act.headline;
  document.getElementById("presenter-act-label").textContent = act.label;
  document.getElementById("presenter-scenario-label").textContent = act.run_label;
  document.getElementById("presenter-demo-cue").textContent = act.demo_cue;
  document.getElementById("presenter-closing-line").textContent = act.closing_line;

  const talkingPoints = document.getElementById("presenter-talking-points");
  talkingPoints.innerHTML = "";

  act.talking_points.forEach((point) => {
    const item = document.createElement("li");
    item.textContent = point;
    talkingPoints.appendChild(item);
  });
}


function resetReplay() {
  stopPlayback();
  currentEventIndex = -1;
  renderSummary();
  renderNodes();
  renderEvidence();
  renderCurrentEvent(null);
  renderLog([]);
  renderTraceabilityFooter();
}

function togglePlay() {
  if (timer) return stopPlayback();
  playPause.textContent = "Pause";
  timer = setInterval(() => {
    if (!nextEvent()) stopPlayback();
  }, 900);
}

function stopPlayback() {
  if (timer) clearInterval(timer);
  timer = null;
  playPause.textContent = "Play";
}

function nextEvent() {
  if (!currentRun || currentEventIndex >= currentRun.animation_events.length - 1) return false;
  currentEventIndex += 1;
  const event = currentRun.animation_events[currentEventIndex];
  applyEvent(event);
  renderCurrentEvent(event);
  renderLog(currentRun.animation_events.slice(0, currentEventIndex + 1));
  renderTraceabilityFooter();
  return true;
}

function renderSummary() {
  document.getElementById("run-summary").innerHTML = `
    <h3>${escapeHtml(currentRun.scenario_label)}</h3>
    ${metric("Confidence", currentRun.operational_confidence)}
    ${metric("Direction", currentRun.confidence_direction)}
    ${metric("Pattern maturity", currentRun.pattern_maturity)}
    ${metric("Due diligence", currentRun.selected_due_diligence_level)}
    ${metric("Visual path steps", agentStepsForCurrentRun().length)}
    ${metric("Governance", "Mandatory")}
    ${metric("Human approval", "Required")}
    ${metric("Autonomous action", "Off")}
  `;
}

function metric(label, value) {
  return `<div class="metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`;
}

function renderNodes() {
  const lane = document.getElementById("agent-lane");
  lane.innerHTML = "";

  const agentSteps = agentStepsForCurrentRun();
  const gateEventsByAgent = governanceGateEventsByAgent();

  agentSteps.forEach((step, index) => {
    const agent = document.createElement("div");
    agent.className = "node path-step";
    agent.dataset.nodeId = `agent::${step.agent_id}`;
    agent.dataset.stepId = step.step_id;
    agent.innerHTML = `
      <small>Step ${index + 1}</small>
      <strong>${escapeHtml(readable(step.agent_id))}</strong>
      <em>${escapeHtml(step.status)}</em>
    `;
    lane.appendChild(agent);

    const gateEvents = gateEventsByAgent.get(step.agent_id) || [];
    const gateEvent = gateEvents.shift();

    if (gateEvent) {
      const gate = document.createElement("div");
      gate.className = `node gate ${decisionClass(gateEvent.decision)}`;
      gate.dataset.nodeId = gateEvent.node_id;
      gate.innerHTML = `<strong>${escapeHtml(gateEvent.decision)}</strong><br>${escapeHtml(gateEvent.source_id)}`;
      lane.appendChild(gate);
    }
  });

  document.querySelectorAll(".node").forEach((node) => node.classList.remove("active"));
}

function agentStepsForCurrentRun() {
  const steps =
    currentRun.agent_steps ||
    currentRun.orchestration_steps ||
    currentRun.orchestration_trace?.agent_steps ||
    [];

  return steps.map((step, index) => {
    return {
      step_id: step.step_id || `visual-step-${index + 1}`,
      agent_id: step.agent_id || step.agent || step.name || "unknown_agent",
      status: step.status || "PLANNED"
    };
  });
}

function governanceGateEventsByAgent() {
  const grouped = new Map();

  currentRun.animation_events
    .filter((event) => event.event_type === "GOVERNANCE_GATE_STAMPED")
    .forEach((event) => {
      const existing = grouped.get(event.agent_id) || [];
      existing.push(event);
      grouped.set(event.agent_id, existing);
    });

  return grouped;
}

function renderEvidence() {
  const eligible = document.getElementById("eligible-evidence");
  const excluded = document.getElementById("excluded-evidence");
  const gaps = document.getElementById("evidence-gaps");

  eligible.innerHTML = "";
  excluded.innerHTML = "";
  gaps.innerHTML = "";

  currentRun.evidence_for_reasoning.forEach((item) => eligible.appendChild(token(item, "eligible")));
  currentRun.excluded_evidence.forEach((item) => excluded.appendChild(token(item, "excluded")));

  currentRun.evidence_gaps.forEach((gap) => {
    const el = document.createElement("div");
    el.className = "gap-token";
    el.dataset.auditId = gap.audit_id || "";
    el.innerHTML = `<strong>Gap</strong><br>${escapeHtml(gap.source_id)}<br>${escapeHtml(gap.reason)}`;
    gaps.appendChild(el);
  });
}

function token(item, type) {
  const el = document.createElement("div");
  el.className = `token ${type}`;
  el.dataset.evidenceId = item.evidence_id || "";
  el.innerHTML = `<strong>${escapeHtml(item.evidence_id)}</strong><br>${escapeHtml(item.evidence_class)}<br>${escapeHtml(item.content_safety_status)}`;
  return el;
}

function applyEvent(event) {
  clearActive();

  if (event.node_id) activateNode(event.node_id, event);

  if (event.event_type === "EVIDENCE_TOKEN_MOVED") {
    revealToken(event.evidence_id);
    activateNode("evidence_fusion", event);
  }
  if (event.event_type === "EVIDENCE_EXCLUDED") {
    revealToken(event.evidence_id);
  }
  if (event.event_type === "EVIDENCE_GAP_CREATED") {
    revealGap(event.audit_id);
  }
  if (event.event_type === "CONFIDENCE_UPDATED") activateNode("operational_confidence", event);
  if (event.event_type === "DUE_DILIGENCE_SELECTED") activateNode("due_diligence", event);
  if (event.event_type === "HUMAN_REVIEW_REQUIRED") activateNode("human_review", event);
}

function activateNode(nodeId, event) {
  const node = document.querySelector(`[data-node-id="${cssEscape(nodeId)}"]`);
  if (!node) return;
  node.classList.add("active");
  if (event.decision === "ALLOW") node.classList.add("allow");
  if (event.decision === "DENY") node.classList.add("deny");
  if (event.content_safety_status === "REVIEW_REQUIRED") node.classList.add("review");
}

function clearActive() {
  document.querySelectorAll(".node").forEach((node) => node.classList.remove("active"));
}

function revealToken(evidenceId) {
  const token = document.querySelector(`[data-evidence-id="${cssEscape(evidenceId)}"]`);
  if (token) token.classList.add("visible");
}

function revealGap(auditId) {
  const gap = document.querySelector(`[data-audit-id="${cssEscape(auditId)}"]`);
  if (gap) gap.classList.add("visible");
}

function renderCurrentEvent(event) {
  const panel = document.getElementById("current-event");
  if (!event) {
    panel.innerHTML = "Press Play or Next event to start the replay.";
    return;
  }
  panel.innerHTML = `<strong>${escapeHtml(event.event_type)}</strong><br><br>${escapeHtml(event.caption)}<br><br><small>${escapeHtml(event.event_id)}</small>`;
}

function renderLog(events) {
  const log = document.getElementById("event-log");
  log.innerHTML = "";
  events.forEach((event) => {
    const item = document.createElement("li");
    item.className = eventClass(event);
    item.textContent = `${event.event_id}: ${event.caption}`;
    log.appendChild(item);
  });
}


function renderTraceabilityFooter() {
  if (!payload || !currentRun) return;

  const schemaVersion = document.getElementById("schema-version");
  const eventCounter = document.getElementById("event-counter");
  const animationEventCount = document.getElementById("animation-event-count");
  const rendererContract = document.getElementById("renderer-contract");
  const provenanceSummary = document.getElementById("provenance-summary");

  const current = Math.max(currentEventIndex + 1, 0);
  const total = currentRun.animation_events.length;

  schemaVersion.textContent = payload.schema_version;
  eventCounter.textContent = `${current} / ${total}`;
  animationEventCount.textContent = String(payload.animation_event_count);

  rendererContract.innerHTML = `
    <div><strong>Direction:</strong> ${escapeHtml(payload.renderer_contract.direction)}</div>
    <div><strong>Python owns decisions:</strong> ${escapeHtml(payload.renderer_contract.python_owns_decisions)}</div>
    <div><strong>Renderer owns play-head:</strong> ${escapeHtml(payload.renderer_contract.renderer_owns_playhead)}</div>
    <div><strong>Renderer must not invent decisions:</strong> ${escapeHtml(payload.renderer_contract.renderer_must_not_invent_decisions)}</div>
  `;

  provenanceSummary.innerHTML = `
    <div><strong>Audit IDs:</strong> ${escapeHtml(payload.provenance_summary.audit_ids.length)}</div>
    <div><strong>Evidence IDs:</strong> ${escapeHtml(payload.provenance_summary.evidence_ids.length)}</div>
    <div><strong>Governance decisions:</strong> ${escapeHtml(payload.provenance_summary.governance_decisions.join(", "))}</div>
    <div><strong>Approval states:</strong> ${escapeHtml(payload.provenance_summary.approval_states.join(", "))}</div>
    <div><strong>Confidence values:</strong> ${escapeHtml(payload.provenance_summary.operational_confidence_values.join(", "))}</div>
    <div><strong>Due diligence values:</strong> ${escapeHtml(payload.provenance_summary.due_diligence_values.join(", "))}</div>
  `;
}


function eventClass(event) {
  if (event.decision === "ALLOW") return "event-allow";
  if (event.decision === "DENY") return "event-deny";
  if (event.content_safety_status === "REVIEW_REQUIRED") return "event-review";
  return "";
}

function decisionClass(decision) {
  if (decision === "ALLOW") return "allow";
  if (decision === "DENY") return "deny";
  if (decision === "ESCALATE") return "review";
  return "";
}

function readable(value) {
  return String(value || "unknown").replaceAll("_", " ").replace(/\b\w/g, c => c.toUpperCase());
}

function escapeHtml(value) {
  return String(value ?? "").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;");
}

function cssEscape(value) {
  if (window.CSS && CSS.escape) return CSS.escape(value);
  return String(value).replace(/["\\]/g, "\\$&");
}

loadReplay().catch((error) => {
  document.body.innerHTML = `
    <main><section class="story">
      <h1>Replay failed to load</h1>
      <p>${escapeHtml(error.message)}</p>
      <p>Run from repo root: <code>python -m http.server 8765</code></p>
      <p>Then open: <code>http://localhost:8765/ui_static/replay_canvas/index.html</code></p>
    </section></main>
  `;
});
