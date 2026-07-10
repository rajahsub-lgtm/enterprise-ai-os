const REPLAY_JSON_PATH = "../../ui_replay_exports/eaios_sprint3_replay.json";

const PRESENTER_ACTS = [
  {
    act_id: "act-1",
    label: "Act 1 — First-time alert",
    run_label: "First-time / no memory",
    headline: "No trusted memory exists, so EAIOS performs full due diligence.",
    demo_cue: "Press Play and watch seven governed visual events unfold.",
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
    label: "Act 2 — Trusted memory",
    run_label: "Trusted memory / validated pattern",
    headline: "Trusted enterprise memory increases confidence and narrows validation.",
    demo_cue: "Press Play and watch the replay stop after three targeted validation events.",
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
    label: "Act 3 — Drift or conflict",
    run_label: "Drift or conflict",
    headline: "When memory drifts or conflicts, EAIOS expands validation again.",
    demo_cue: "Press Play and watch five validation events expose uncertainty.",
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
let currentAct = null;
let currentEventIndex = -1;
let visualEvents = [];
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
    currentAct = PRESENTER_ACTS.find((act) => act.run_label === currentRun.scenario_label);
    resetReplay();
    renderPresenterSelection();
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
  currentAct = act;
  selector.value = run.run_id;
  resetReplay();
  renderPresenterSelection();
}

function renderPresenterSelection() {
  if (!currentAct) return;

  document.querySelectorAll(".act-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.actId === currentAct.act_id);
  });

  document.getElementById("presenter-headline").textContent = currentAct.headline;
  document.getElementById("presenter-act-label").textContent = currentAct.label;
  document.getElementById("presenter-scenario-label").textContent = currentAct.run_label;
  document.getElementById("presenter-demo-cue").textContent = currentAct.demo_cue;
  document.getElementById("presenter-closing-line").textContent = currentAct.closing_line;

  const talkingPoints = document.getElementById("presenter-talking-points");
  talkingPoints.innerHTML = "";

  currentAct.talking_points.forEach((point) => {
    const item = document.createElement("li");
    item.textContent = point;
    talkingPoints.appendChild(item);
  });
}

function resetReplay() {
  stopPlayback();
  currentEventIndex = -1;
  visualEvents = visualEventsForCurrentRun();

  renderSummary();
  renderNodes();
  renderEvidence();
  renderCurrentEvent(null);
  renderLog([]);
  renderTraceabilityFooter();
  renderDemoReadinessPolish();
}

function visualEventsForCurrentRun() {
  return payload.visual_paths_by_run[currentRun.run_id] || [];
}

function togglePlay() {
  if (timer) return stopPlayback();

  playPause.textContent = "Pause";
  timer = setInterval(() => {
    if (!nextEvent()) stopPlayback();
  }, 1100);
}

function stopPlayback() {
  if (timer) clearInterval(timer);
  timer = null;
  playPause.textContent = "Play";
}

function nextEvent() {
  if (!currentRun || currentEventIndex >= visualEvents.length - 1) return false;

  currentEventIndex += 1;
  const event = visualEvents[currentEventIndex];

  applyEvent(event);
  renderCurrentEvent(event);
  renderLog(visualEvents.slice(0, currentEventIndex + 1));
  renderTraceabilityFooter();
  renderDemoReadinessPolish();

  return true;
}

function renderSummary() {
  document.getElementById("run-summary").innerHTML = `
    <h3>${escapeHtml(currentRun.scenario_label)}</h3>
    ${metric("Confidence", currentRun.operational_confidence)}
    ${metric("Direction", currentRun.confidence_direction)}
    ${metric("Pattern maturity", currentRun.pattern_maturity)}
    ${metric("Due diligence", currentRun.selected_due_diligence_level)}
    ${metric("Visual events", visualEventsForCurrentRun().length)}
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

  document.querySelectorAll(".node").forEach((node) => {
    node.classList.remove("active", "visible", "allow", "deny", "review");
    node.classList.add("not-yet-visible");
  });

  visualEvents
    .filter((event) => event.node_id.startsWith("visual::"))
    .forEach((event) => {
      const node = document.createElement("div");
      node.className = "node visual-event-node not-yet-visible";
      node.dataset.nodeId = event.node_id;
      node.innerHTML = `
        <small>Event ${event.visual_step_number}</small>
        <strong>${escapeHtml(event.label)}</strong>
      `;
      lane.appendChild(node);
    });
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
    revealReasoningEvidence();
    activateNode("evidence_fusion", event);
  }

  if (event.event_type === "EVIDENCE_EXCLUDED") {
    revealExcludedEvidence();
  }

  if (event.event_type === "EVIDENCE_GAP_CREATED") {
    revealEvidenceGaps();
  }

  if (event.event_type === "CONFIDENCE_UPDATED") activateNode("operational_confidence", event);
  if (event.event_type === "DUE_DILIGENCE_SELECTED") activateNode("due_diligence", event);
  if (event.event_type === "HUMAN_REVIEW_REQUIRED") activateNode("human_review", event);
}

function activateNode(nodeId, event) {
  const node = document.querySelector(`[data-node-id="${cssEscape(nodeId)}"]`);
  if (!node) return;

  node.classList.remove("not-yet-visible");
  node.classList.add("visible", "active");

  if (event.decision === "ALLOW") node.classList.add("allow");
  if (event.decision === "DENY") node.classList.add("deny");
  if (event.content_safety_status === "REVIEW_REQUIRED") node.classList.add("review");
}

function clearActive() {
  document.querySelectorAll(".node").forEach((node) => node.classList.remove("active"));
}

function revealReasoningEvidence() {
  document.querySelectorAll(".token.eligible").forEach((item) => item.classList.add("visible"));
}

function revealExcludedEvidence() {
  document.querySelectorAll(".token.excluded").forEach((item) => item.classList.add("visible"));
}

function revealEvidenceGaps() {
  document.querySelectorAll(".gap-token").forEach((item) => item.classList.add("visible"));
}

function revealToken(evidenceId) {
  const item = document.querySelector(`[data-evidence-id="${cssEscape(evidenceId)}"]`);
  if (item) item.classList.add("visible");
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

  panel.innerHTML = `
    <strong>${escapeHtml(event.label)}</strong><br><br>
    ${escapeHtml(event.caption)}<br><br>
    <small>${escapeHtml(event.event_id)} · ${event.visual_step_number} / ${event.visual_step_total}</small>
  `;
}

function renderLog(events) {
  const log = document.getElementById("event-log");
  log.innerHTML = "";

  events.forEach((event) => {
    const item = document.createElement("li");
    item.className = eventClass(event);
    item.textContent = `${event.visual_step_number}/${event.visual_step_total}: ${event.caption}`;
    log.appendChild(item);
  });
}


function renderDemoReadinessPolish() {
  if (!currentRun) return;

  const story = pathStoryForCurrentRun();
  const alert = currentRun.current_alert || payload.demo_story.same_alert || {};
  const current = Math.max(currentEventIndex + 1, 0);
  const total = visualEvents.length;
  const percent = total === 0 ? 0 : Math.round((current / total) * 100);
  const isComplete = total > 0 && current >= total;

  document.body.classList.remove(
    "path-full-diligence",
    "path-targeted-validation",
    "path-expanded-validation"
  );
  document.body.classList.add(story.path_class);

  setText("same-alert-title", alert.application || "Digital Checkout");
  setText(
    "same-alert-symptom",
    alert.symptom || "Payment authorization latency and elevated error rate"
  );

  setText("act-progress-label", `${current} / ${total}`);
  const progressBar = document.getElementById("act-progress-bar");
  if (progressBar) progressBar.style.width = `${percent}%`;

  setText("why-path-title", story.title);
  setText("why-path-explanation", story.explanation);

  if (isComplete) {
    setText("end-summary-title", story.end_title);
    setText("end-of-act-summary", story.end_summary);
  } else {
    setText("end-summary-title", "Replay in progress");
    setText(
      "end-of-act-summary",
      "Advance the replay to reveal the next governed visual event."
    );
  }
}

function pathStoryForCurrentRun() {
  const storyByScenario = payload.demo_story.path_story_by_scenario || {};

  return storyByScenario[currentRun.scenario_label] || {
    path_class: "path-expanded-validation",
    title: "Governed validation",
    explanation: "EAIOS selected a governed validation path for this scenario.",
    end_title: "Validation complete",
    end_summary: "The replay reached human review with governance intact."
  };
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}


function renderTraceabilityFooter() {
  if (!payload || !currentRun) return;

  const schemaVersion = document.getElementById("schema-version");
  const eventCounter = document.getElementById("event-counter");
  const animationEventCount = document.getElementById("animation-event-count");
  const rendererContract = document.getElementById("renderer-contract");
  const provenanceSummary = document.getElementById("provenance-summary");

  if (!schemaVersion || !eventCounter || !animationEventCount || !rendererContract || !provenanceSummary) return;

  const current = Math.max(currentEventIndex + 1, 0);
  const total = visualEvents.length;

  schemaVersion.textContent = payload.schema_version;
  eventCounter.textContent = `${current} / ${total}`;
  animationEventCount.textContent = String(total);

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

// Compatibility surface for tests and future export-driven path rendering.
function agentStepsForCurrentRun() {
  const steps =
    currentRun.agent_steps ||
    currentRun.orchestration_steps ||
    currentRun.orchestration_trace?.agent_steps ||
    [];

  return steps;
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
