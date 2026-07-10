
const REPLAY_JSON_PATH = "../../ui_replay_exports/eaios_sprint3_replay.json";

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

  resetReplay();
}

function resetReplay() {
  stopPlayback();
  currentEventIndex = -1;
  renderSummary();
  renderNodes();
  renderEvidence();
  renderCurrentEvent(null);
  renderLog([]);
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
  return true;
}

function renderSummary() {
  document.getElementById("run-summary").innerHTML = `
    <h3>${escapeHtml(currentRun.scenario_label)}</h3>
    ${metric("Confidence", currentRun.operational_confidence)}
    ${metric("Direction", currentRun.confidence_direction)}
    ${metric("Pattern maturity", currentRun.pattern_maturity)}
    ${metric("Due diligence", currentRun.selected_due_diligence_level)}
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

  currentRun.animation_events
    .filter((event) => event.event_type === "GOVERNANCE_GATE_STAMPED")
    .forEach((event) => {
      const agent = document.createElement("div");
      agent.className = "node";
      agent.dataset.nodeId = `agent::${event.agent_id}`;
      agent.textContent = readable(event.agent_id);
      lane.appendChild(agent);

      const gate = document.createElement("div");
      gate.className = `node gate ${decisionClass(event.decision)}`;
      gate.dataset.nodeId = event.node_id;
      gate.innerHTML = `<strong>${escapeHtml(event.decision)}</strong><br>${escapeHtml(event.source_id)}`;
      lane.appendChild(gate);
    });

  document.querySelectorAll(".node").forEach((node) => node.classList.remove("active"));
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
