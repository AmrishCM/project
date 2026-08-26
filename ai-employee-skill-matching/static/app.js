// static/app.js

// ------- Sample JDs (format similar to your Wipro JD) -------
const SAMPLE_PM = `Wipro – Project Manager (Band C1 / C2) – Job Description
Job Purpose
The Project Manager is responsible for end-to-end delivery of medium to large projects...
Required Skills & Competencies
Project Planning & Tracking
Agile/Scrum/Waterfall proficiency
Financial & risk management
Stakeholder & vendor management
Tools: JIRA, MS Project, Asana, Kanban, Excel
Experience & Qualifications
10–15 years total experience
Location
Chennai, Coimbatore`;

const SAMPLE_FE = `Wipro – Frontend Developer – Job Description
Job Purpose
Frontend Developer builds responsive web applications with modern UI.
Key Responsibilities
Develop UI using HTML, CSS, JavaScript/TypeScript
Build React components, state management (Redux)
Consume REST APIs, handle auth, improve performance
Required Skills & Competencies
HTML, CSS, JavaScript, TypeScript, React
REST API integration, UI/UX basics
Tools: Git, Chrome DevTools, Jira
Experience & Qualifications
2–6 years experience
Location
Chennai, Coimbatore`;

const SAMPLE_DEVOPS = `Wipro – DevOps Engineer – Job Description
Job Purpose
DevOps Engineer manages CI/CD and cloud infrastructure operations.
Key Responsibilities
Build CI/CD pipelines (Jenkins)
Containerization (Docker), orchestration (Kubernetes)
Infrastructure as code (Terraform/CloudFormation)
Monitoring, Linux, automation scripts
Required Skills & Competencies
AWS/Azure/GCP, Docker, Kubernetes, Terraform, Jenkins
Linux, networking, security basics
Experience & Qualifications
3–8 years experience
Location
Chennai, Coimbatore`;


// ------- UI helpers -------
const jdText = document.getElementById("jdText");
const logs = document.getElementById("logs");
const previewBody = document.getElementById("previewBody");

const kTotal = document.getElementById("kTotal");
const kTop = document.getElementById("kTop");
const kAvg = document.getElementById("kAvg");
const kSoon = document.getElementById("kSoon");

const btnCopyPath = document.getElementById("btnCopyPath");
let lastReportPath = "";


function log(msg) {
  const t = new Date().toLocaleTimeString();
  logs.textContent = `[${t}] ${msg}\n` + logs.textContent;
}

function animateCounter(el, to, decimals = 0) {
  const from = Number(el.textContent) || 0;
  const start = performance.now();
  const dur = 650;

  function step(now) {
    const p = Math.min(1, (now - start) / dur);
    const val = from + (to - from) * p;
    el.textContent = decimals ? val.toFixed(decimals) : Math.round(val);
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}


// ------- Weights UI -------
const DEFAULT_WEIGHTS = {
  skills: 40,
  experience: 30,
  certifications: 10,
  relocation: 10,
  availability: 10,
  ml_similarity: 0
};

function getWeightsFromUI() {
  const w = {
    skills: Number(document.getElementById("w_skills").value),
    experience: Number(document.getElementById("w_experience").value),
    certifications: Number(document.getElementById("w_certifications").value),
    relocation: Number(document.getElementById("w_relocation").value),
    availability: Number(document.getElementById("w_availability").value),
    ml_similarity: Number(document.getElementById("w_ml_similarity").value),
  };
  return w;
}

function refreshWeightsUI() {
  const w = getWeightsFromUI();
  document.getElementById("w_skills_v").innerText = `${w.skills}%`;
  document.getElementById("w_experience_v").innerText = `${w.experience}%`;
  document.getElementById("w_certifications_v").innerText = `${w.certifications}%`;
  document.getElementById("w_relocation_v").innerText = `${w.relocation}%`;
  document.getElementById("w_availability_v").innerText = `${w.availability}%`;
  document.getElementById("w_ml_similarity_v").innerText = `${w.ml_similarity}%`;

  const total = w.skills + w.experience + w.certifications + w.relocation + w.availability + w.ml_similarity;
  document.getElementById("weightsTotal").innerText = total;

  localStorage.setItem("ai_match_weights", JSON.stringify(w));
}

function setWeightsToUI(w) {
  document.getElementById("w_skills").value = w.skills;
  document.getElementById("w_experience").value = w.experience;
  document.getElementById("w_certifications").value = w.certifications;
  document.getElementById("w_relocation").value = w.relocation;
  document.getElementById("w_availability").value = w.availability;
  document.getElementById("w_ml_similarity").value = w.ml_similarity;
  refreshWeightsUI();
}

function initWeights() {
  let w = DEFAULT_WEIGHTS;
  try {
    const saved = JSON.parse(localStorage.getItem("ai_match_weights") || "null");
    if (saved) w = { ...DEFAULT_WEIGHTS, ...saved };
  } catch {}
  setWeightsToUI(w);

  ["w_skills","w_experience","w_certifications","w_relocation","w_availability","w_ml_similarity"]
    .forEach(id => document.getElementById(id).addEventListener("input", refreshWeightsUI));

  document.getElementById("btnResetWeights").addEventListener("click", () => setWeightsToUI(DEFAULT_WEIGHTS));
}


// ------- API calls -------
async function apiPost(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt);
  }
  return await res.json();
}

function renderPreview(rows) {
  if (!rows || rows.length === 0) {
    previewBody.innerHTML = `<tr><td colspan="5" class="muted">No matches.</td></tr>`;
    return;
  }

  previewBody.innerHTML = rows.map(r => {
    const miss = (r.missing_skills || "").slice(0, 70);
    return `
      <tr>
        <td>${r.emp_id || ""}</td>
        <td>${r.name || ""}</td>
        <td>${r.role || ""}</td>
        <td><b>${r.final_match_score}</b></td>
        <td class="muted">${miss}</td>
      </tr>
    `;
  }).join("");
}

async function doPreview() {
  const jd = jdText.value.trim();
  if (!jd) return log("⚠️ Paste JD text first.");

  log("🔎 Running preview...");
  const weights = getWeightsFromUI();
  const data = await apiPost("/api/preview", { jd_text: jd, weights });

  animateCounter(kTotal, data.kpis.total_employees, 0);
  animateCounter(kTop, data.kpis.top_score, 1);
  animateCounter(kAvg, data.kpis.avg_score, 1);
  animateCounter(kSoon, data.kpis.soon_available_30d, 0);

  renderPreview(data.top10);
  log("✅ Preview ready (top 10).");
}

async function doGenerate() {
  const jd = jdText.value.trim();
  if (!jd) return log("⚠️ Paste JD text first.");

  log("📄 Generating Excel...");
  const weights = getWeightsFromUI();
  const out = await apiPost("/api/generate_excel", { jd_text: jd, weights });

  lastReportPath = out.report_path || "";
  btnCopyPath.disabled = !lastReportPath;

  log("✅ Excel ready. Download started...");
  window.location.href = out.download_url;
}


// ------- Theme toggle -------
function initTheme() {
  const btn = document.getElementById("btnTheme");
  const saved = localStorage.getItem("theme") || "dark";
  if (saved === "light") document.body.classList.add("light");

  btn.addEventListener("click", () => {
    document.body.classList.toggle("light");
    localStorage.setItem("theme", document.body.classList.contains("light") ? "light" : "dark");
  });
}


// ------- Buttons -------
window.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initWeights();

  document.getElementById("btnPM").addEventListener("click", () => { jdText.value = SAMPLE_PM; log("Loaded Sample PM JD"); });
  document.getElementById("btnFE").addEventListener("click", () => { jdText.value = SAMPLE_FE; log("Loaded Sample Frontend JD"); });
  document.getElementById("btnDevOps").addEventListener("click", () => { jdText.value = SAMPLE_DEVOPS; log("Loaded Sample DevOps JD"); });

  document.getElementById("btnClear").addEventListener("click", () => { jdText.value = ""; log("Cleared JD"); });
  document.getElementById("btnPreview").addEventListener("click", () => doPreview().catch(e => log("❌ " + e.message)));
  document.getElementById("btnGenerate").addEventListener("click", () => doGenerate().catch(e => log("❌ " + e.message)));

  btnCopyPath.addEventListener("click", async () => {
    if (!lastReportPath) return;
    await navigator.clipboard.writeText(lastReportPath);
    log("📌 Report path copied: " + lastReportPath);
  });

  log("Ready. Paste a JD and click Preview.");
});
