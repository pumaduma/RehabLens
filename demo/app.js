/* ============================================================
   RehabLens — on-device AI form coach (browser demo)
   ------------------------------------------------------------
   Pipeline (mirrors the research prototype in /prototype):
     1. MediaPipe Pose tracks 33 body landmarks (on-device)
     2. Joint angles computed per frame ("digital goniometry")
     3. Rep state machine counts repetitions
     4. Each rep is scored: depth (55%) + symmetry (25%) + tempo (20%)
        → a 0–100 Movement Score, an explainable stand-in for the
          Siamese-LSTM similarity score used in the research pipeline.
   No video, landmarks, or metrics leave this device.
   ============================================================ */

import {
  PoseLandmarker,
  FilesetResolver,
  DrawingUtils,
} from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14";

/* ---------------- DOM ---------------- */
const $ = (id) => document.getElementById(id);
const video = $("video");
const overlay = $("overlay");
const ctx = overlay.getContext("2d");
const chartCanvas = $("chart");
const chartCtx = chartCanvas.getContext("2d");
const startBtn = $("startBtn");
const fileInput = $("fileInput");
const idleState = $("idleState");
const repFlash = $("repFlash");

/* ---------------- Landmark indices (MediaPipe Pose) ---------------- */
const L = {
  lShoulder: 11, rShoulder: 12, lElbow: 13, rElbow: 14, lWrist: 15, rWrist: 16,
  lHip: 23, rHip: 24, lKnee: 25, rKnee: 26, lAnkle: 27, rAnkle: 28,
};

/* ---------------- Exercise definitions ---------------- */
const EXERCISES = {
  kneeExtension: {
    name: "Seated Knee Extension",
    icon: "🦵",
    metricLabel: "knee angle",
    // primary angle: knee (hip–knee–ankle)
    angleOf(lm) { return sideAngle(lm, L.lHip, L.lKnee, L.lAnkle, L.rHip, L.rKnee, L.rAnkle); },
    restAngle: 90,        // seated, knee bent
    targetExtreme: 15,    // straighten to ≤ 15°
    extremeIsMin: true,
    rangeTarget: 75,      // ~90° → 15°
    goThreshold: 25,      // "extended" when below this
    returnThreshold: 60,  // rep done when back above this
    expectedRepSec: 3,
    targetText: "Straighten your knee from ~90° to under 15°, then lower slowly. 10 reps.",
    cue: {
      start: "Extend your knee slowly until it's straight 🦵",
      toward: (cur) => `Straighten more — target ≤ 15°, you're at ${Math.round(cur)}°`,
      reached: "Full extension! Lower slowly back down 🎯",
    },
  },
  sitToStand: {
    name: "Sit-to-Stand Squat",
    icon: "🪑",
    metricLabel: "knee angle",
    angleOf(lm) { return sideAngle(lm, L.lHip, L.lKnee, L.lAnkle, L.rHip, L.rKnee, L.rAnkle); },
    restAngle: 170,       // standing tall
    targetExtreme: 95,    // squat to ≤ 95° knee flexion
    extremeIsMin: true,
    rangeTarget: 75,      // ~170° → 95°
    goThreshold: 100,
    returnThreshold: 145,
    expectedRepSec: 3.5,
    targetText: "Stand tall, sit down until knees reach ~90°, then stand. 10 reps.",
    cue: {
      start: "Bend your knees and sit back like there's a chair 🪑",
      toward: (cur) => `Go deeper — target ≤ 95°, you're at ${Math.round(cur)}°`,
      reached: "Great depth! Push through your heels and stand 👟",
    },
  },
  gluteBridge: {
    name: "Glute Bridge",
    icon: "🌉",
    metricLabel: "hip angle",
    angleOf(lm) { return sideAngle(lm, L.lShoulder, L.lHip, L.lKnee, L.rShoulder, L.rHip, L.rKnee); },
    restAngle: 110,       // lying, knees bent
    targetExtreme: 165,   // lift hips until body is a straight line
    extremeIsMin: false,
    rangeTarget: 55,      // ~110° → 165°
    goThreshold: 150,
    returnThreshold: 125,
    expectedRepSec: 3,
    targetText: "Lie on your back, knees bent. Lift hips until your body is a straight line. 10 reps.",
    cue: {
      start: "Lift your hips toward the ceiling 🌉",
      toward: (cur) => `Lift higher — target ≥ 165°, you're at ${Math.round(cur)}°`,
      reached: "Hips up — squeeze glutes, then lower slowly 🎯",
    },
  },
  shoulderFlexion: {
    name: "Shoulder Flexion",
    icon: "🙆",
    metricLabel: "shoulder angle",
    angleOf(lm) { return sideAngle(lm, L.lHip, L.lShoulder, L.lElbow, L.rHip, L.rShoulder, L.rElbow); },
    restAngle: 25,        // arm at side
    targetExtreme: 155,   // arm overhead
    extremeIsMin: false,
    rangeTarget: 130,     // ~25° → 155°
    goThreshold: 135,
    returnThreshold: 60,
    expectedRepSec: 3,
    targetText: "Raise your arm overhead, keep the elbow straight, lower slowly. 10 reps per side.",
    cue: {
      start: "Raise your arm slowly toward the ceiling 🙆",
      toward: (cur) => `Reach higher — target ≥ 155°, you're at ${Math.round(cur)}°`,
      reached: "Overhead! Lower slowly, keep control 🎯",
    },
  },
  elbowCurl: {
    name: "Elbow Curl",
    icon: "💪",
    metricLabel: "elbow angle",
    angleOf(lm) { return sideAngle(lm, L.lShoulder, L.lElbow, L.lWrist, L.rShoulder, L.rElbow, L.rWrist); },
    restAngle: 160,       // arm nearly straight
    targetExtreme: 70,    // curl to ≤ 70°
    extremeIsMin: true,
    rangeTarget: 90,      // ~160° → 70°
    goThreshold: 80,
    returnThreshold: 140,
    expectedRepSec: 3,
    targetText: "Curl the elbow fully, then lower slowly to straight. 10 reps per side.",
    cue: {
      start: "Curl your elbow up toward your shoulder 💪",
      toward: (cur) => `Curl deeper — target ≤ 70°, you're at ${Math.round(cur)}°`,
      reached: "Full curl! Lower slowly to straight 🎯",
    },
  },
};

/* ---------------- State ---------------- */
let currentExercise = "kneeExtension";
let landmarker = null;
let drawUtils = null;
let cameraStream = null;
let mode = null; // 'camera' | 'upload' | null
let rafId = null;
let lastVideoTime = -1;

const session = {
  reps: 0, scores: [], best: null, angleMin: null, angleMax: null,
};

const rep = {
  active: false, reached: false, started: false,
  startTime: null, min: null, max: null,
  symSum: 0, symN: 0,
};

let angleBuffer = [];       // {t, v} for sparkline
let lastAngle = null;
let lastCue = "";

/* ---------------- Geometry helpers ---------------- */
function angle3(a, b, c) {
  const v1 = { x: a.x - b.x, y: a.y - b.y };
  const v2 = { x: c.x - b.x, y: c.y - b.y };
  const m = Math.hypot(v1.x, v1.y) * Math.hypot(v2.x, v2.y);
  if (m < 1e-9) return null;
  const cos = Math.max(-1, Math.min(1, (v1.x * v2.x + v1.y * v2.y) / m));
  return (Math.acos(cos) * 180) / Math.PI;
}

/** Compute an angle on the more-visible side (L or R), returns {value, vis}. */
function sideAngle(lm, lA, lB, lC, rA, rB, rC) {
  const pick = (a, b, c) => {
    const [pa, pb, pc] = [lm[a], lm[b], lm[c]];
    if (!pa || !pb || !pc) return null;
    const vis = Math.min(pa.visibility ?? 0, pb.visibility ?? 0, pc.visibility ?? 0);
    return { value: angle3(pa, pb, pc), vis };
  };
  const left = pick(lA, lB, lC);
  const right = pick(rA, rB, rC);
  if (!left && !right) return null;
  if (left && right) return left.vis >= right.vis ? left : right;
  return left || right;
}

/** Symmetry metric: how level the shoulders/hips are (deg of tilt). */
function symmetryTilt(lm) {
  const ls = lm[L.lShoulder], rs = lm[L.rShoulder];
  const lh = lm[L.lHip], rh = lm[L.rHip];
  if (!ls || !rs || !lh || !rh) return null;
  const shoulderTilt = Math.abs(ls.y - rs.y);
  const hipTilt = Math.abs(lh.y - rh.y);
  return (shoulderTilt + hipTilt) / 2; // normalized coords → small values
}

function clamp01(x) { return Math.max(0, Math.min(1, x)); }

/* ---------------- Scoring ---------------- */
function scoreRep() {
  const ex = EXERCISES[currentExercise];
  const extreme = ex.extremeIsMin ? rep.min : rep.max;
  if (extreme == null || rep.startTime == null) return null;

  const rangeAchieved = Math.abs(extreme - ex.restAngle);
  const depthScore = clamp01(rangeAchieved / ex.rangeTarget) * 100;

  const avgTilt = rep.symN ? rep.symSum / rep.symN : 0;
  const symmetryScore = clamp01(1 - avgTilt * 6) * 100;

  const durSec = (performance.now() - rep.startTime) / 1000;
  const tempoScore = clamp01(1 - Math.abs(durSec - ex.expectedRepSec) / ex.expectedRepSec) * 100;

  return Math.round(0.55 * depthScore + 0.25 * symmetryScore + 0.2 * tempoScore);
}

/* ---------------- Cue engine ---------------- */
function setCue(text, warn = false) {
  if (text === lastCue) return;
  lastCue = text;
  $("cueText").textContent = text;
  $("cueBar").style.background = warn ? "#fef2f2" : "#ecfeff";
  $("cueBar").style.borderColor = warn ? "#fca5a5" : "#67e8f9";
}

function addTip(text) {
  const list = $("tipsList");
  const li = document.createElement("li");
  li.textContent = text;
  list.prepend(li);
  while (list.children.length > 4) list.lastElementChild.remove();
}

/* ---------------- Session summary ---------------- */
function updateSummary() {
  $("sumReps").textContent = session.reps;
  const avg = session.scores.length
    ? Math.round(session.scores.reduce((a, b) => a + b, 0) / session.scores.length)
    : null;
  $("sumAvg").textContent = avg == null ? "—" : `${avg}`;
  $("sumBest").textContent = session.best == null ? "—" : `${session.best}`;
  let consistency = "—";
  if (session.scores.length >= 3) {
    const mean = session.scores.reduce((a, b) => a + b, 0) / session.scores.length;
    const std = Math.sqrt(session.scores.reduce((a, b) => a + (b - mean) ** 2, 0) / session.scores.length);
    consistency = `${Math.max(0, Math.round(100 - 2 * std))}%`;
  }
  $("sumConsistency").textContent = consistency;
  $("sumDepth").textContent =
    session.angleMin == null ? "—" : `${Math.round(session.angleMin)}–${Math.round(session.angleMax)}°`;
}

/* ---------------- Chart ---------------- */
function drawChart() {
  const c = chartCtx, w = chartCanvas.width, h = chartCanvas.height;
  c.clearRect(0, 0, w, h);
  const ex = EXERCISES[currentExercise];
  if (!angleBuffer.length) return;

  // scale: pad around [rest, target] range
  const lo = Math.min(ex.restAngle, ex.targetExtreme) - 15;
  const hi = Math.max(ex.restAngle, ex.targetExtreme) + 15;
  const span = hi - lo || 1;
  const yOf = (v) => h - 8 - ((v - lo) / span) * (h - 24);

  // target line
  c.strokeStyle = "rgba(249,115,22,0.85)";
  c.setLineDash([6, 5]);
  c.lineWidth = 1.6;
  c.beginPath();
  c.moveTo(0, yOf(ex.targetExtreme));
  c.lineTo(w, yOf(ex.targetExtreme));
  c.stroke();
  c.setLineDash([]);

  // angle trace
  c.strokeStyle = "#0d9488";
  c.lineWidth = 2;
  c.beginPath();
  const n = angleBuffer.length;
  angleBuffer.forEach((p, i) => {
    const x = 6 + (i / Math.max(n - 1, 1)) * (w - 12);
    const y = yOf(p.v);
    i === 0 ? c.moveTo(x, y) : c.lineTo(x, y);
  });
  c.stroke();

  // axis labels
  c.fillStyle = "#94a3b8";
  c.font = "10px system-ui";
  c.fillText(`${Math.round(hi)}°`, 4, 12);
  c.fillText(`${Math.round(lo)}°`, 4, h - 3);
}

/* ---------------- Rep state machine ---------------- */
function processFrame(lm, nowMs) {
  const ex = EXERCISES[currentExercise];
  const angle = ex.angleOf(lm);
  const tilt = symmetryTilt(lm);
  if (!angle || angle.vis < 0.4) {
    setCue("Can't see you clearly — step back so your whole body is in frame", true);
    return;
  }

  const value = angle.value;
  lastAngle = value;
  angleBuffer.push({ t: nowMs, v: value });
  if (angleBuffer.length > 300) angleBuffer.shift();

  // session ROM
  session.angleMin = session.angleMin == null ? value : Math.min(session.angleMin, value);
  session.angleMax = session.angleMax == null ? value : Math.max(session.angleMax, value);

  $("statAngle").textContent = `${Math.round(value)}°`;
  $("statRom").textContent = `${Math.round(session.angleMin)}–${Math.round(session.angleMax)}°`;

  // ---- rep state machine ----
  if (!rep.started) {
    const moving = Math.abs(value - ex.restAngle) > 0.12 * ex.rangeTarget;
    if (moving) {
      rep.started = true;
      rep.startTime = nowMs;
      rep.min = rep.max = value;
      rep.symSum = 0; rep.symN = 0;
      setCue(ex.cue.start);
    } else {
      setCue("Waiting for movement…");
    }
  } else {
    rep.min = Math.min(rep.min, value);
    rep.max = Math.max(rep.max, value);
    if (tilt != null) { rep.symSum += tilt; rep.symN++; }

    if (!rep.reached) {
      const hit = ex.extremeIsMin ? value <= ex.goThreshold : value >= ex.goThreshold;
      if (hit) {
        rep.reached = true;
        setCue(ex.cue.reached);
      } else {
        setCue(ex.cue.toward(value), true);
      }
    } else {
      const returned = ex.extremeIsMin ? value >= ex.returnThreshold : value <= ex.returnThreshold;
      if (returned) {
        completeRep();
      }
    }
  }

  // stat colors
  const scoreEl = $("statScore");
  const curScore = session.scores.length ? session.scores[session.scores.length - 1] : null;
  scoreEl.className = "stat-value" + (curScore == null ? "" : curScore >= 70 ? " good" : " warn");
}

function completeRep() {
  const score = scoreRep();
  session.reps++;
  $("statReps").textContent = session.reps;
  rep.started = false;
  rep.reached = false;
  rep.startTime = null;

  if (score != null) {
    session.scores.push(score);
    session.best = session.best == null ? score : Math.max(session.best, score);
    $("statScore").textContent = `${score}`;
    flashRep(score);
    const msg =
      score >= 85 ? `Rep ${session.reps}: ${score}/100 — excellent consistency! 🏆` :
      score >= 70 ? `Rep ${session.reps}: ${score}/100 — solid form 👍` :
      `Rep ${session.reps}: ${score}/100 — your movement differs from the reference; check with your therapist`;
    addTip(msg);
    setCue(`Rep ${session.reps} complete — score ${score}/100. Keep going!`);
  } else {
    flashRep(null);
  }
  updateSummary();
  drawChart();
}

function flashRep(score) {
  const el = repFlash;
  el.hidden = false;
  el.innerHTML = `<div class="flash-inner">${score == null ? `Rep ${session.reps} ✓` : `Rep ${session.reps} · Score ${score}`}</div>`;
  clearTimeout(el._t);
  el._t = setTimeout(() => { el.hidden = true; }, 1150);
}

/* ---------------- Drawing ---------------- */
function drawOverlay(lm) {
  ctx.clearRect(0, 0, overlay.width, overlay.height);
  if (!lm) return;
  drawUtils.drawLandmarks(ctx, lm, { radius: 3, color: "#14b8a6", fillColor: "#a7f3d0" });
  drawUtils.drawConnectors(ctx, lm, PoseLandmarker.POSE_CONNECTIONS, { color: "#5eead4", lineWidth: 2 });
}

/* ---------------- Main loop ---------------- */
function loop() {
  rafId = requestAnimationFrame(loop);
  if (!landmarker || !mode) return;
  if (mode === "camera" && video.readyState < 2) return;
  if (mode === "upload" && video.currentTime === lastVideoTime) return;
  lastVideoTime = video.currentTime;

  let lm = null;
  try {
    const res = landmarker.detectForVideo(video, performance.now());
    if (res.landmarks && res.landmarks.length) lm = res.landmarks[0];
  } catch (err) {
    console.error(err);
    return;
  }
  drawOverlay(lm);
  if (lm) processFrame(lm, performance.now());
  drawChart();
}

/* ---------------- Camera & upload ---------------- */
async function startCamera() {
  if (cameraStream) return;
  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false,
    });
    mode = "camera";
    video.srcObject = cameraStream;
    await video.play();
    idleState.hidden = true;
    fileInput.value = "";
    startBtn.textContent = "⏹ Stop";
    startBtn.classList.add("running");
    setCue("Waiting for movement…");
  } catch (err) {
    idleState.hidden = false;
    $("idleTitle").textContent = "Camera unavailable";
    $("idleText").innerHTML =
      `We couldn't access the camera (${err.name}). Camera access needs <strong>https://</strong> or <strong>localhost</strong> — try the GitHub Pages link in the repo README, or use <strong>Try a video</strong> below.`;
  }
}

function stopAll() {
  mode = null;
  if (cameraStream) { cameraStream.getTracks().forEach((t) => t.stop()); cameraStream = null; }
  video.pause();
  video.srcObject = null;
  video.removeAttribute("src");
  startBtn.textContent = "▶ Start camera";
  startBtn.classList.remove("running");
  idleState.hidden = false;
  $("idleTitle").textContent = "Camera is off";
  $("idleText").innerHTML =
    'Press <strong>Start camera</strong> above, stand side-on to the camera so your whole body is visible, and begin your exercise.';
}

function handleFile(file) {
  if (!file) return;
  if (cameraStream) { cameraStream.getTracks().forEach((t) => t.stop()); cameraStream = null; }
  const url = URL.createObjectURL(file);
  video.srcObject = null;
  video.src = url;
  video.loop = true;
  video.muted = true;
  video.playsInline = true;
  video.play().catch(() => {});
  mode = "upload";
  lastVideoTime = -1;
  idleState.hidden = true;
  startBtn.textContent = "⏹ Stop";
  startBtn.classList.add("running");
  setCue("Playing video — analyzing…");
}

/* ---------------- Init ---------------- */
async function init() {
  try {
    const vision = await FilesetResolver.forVisionTasks(
      "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm"
    );
    landmarker = await PoseLandmarker.createFromOptions(vision, {
      baseOptions: {
        modelAssetPath:
          "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task",
        delegate: "GPU",
      },
      runningMode: "VIDEO",
      numPoses: 1,
      minPoseDetectionConfidence: 0.5,
      minPosePresenceConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });
  } catch (err) {
    console.error("GPU delegate failed, falling back to CPU", err);
    try {
      const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm"
      );
      landmarker = await PoseLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath:
            "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task",
          delegate: "CPU",
        },
        runningMode: "VIDEO",
        numPoses: 1,
      });
    } catch (err2) {
      startBtn.textContent = "❌ AI failed to load";
      startBtn.disabled = true;
      $("cueText").textContent =
        "The pose model needs an internet connection (it loads from a CDN) — please retry.";
      throw err2;
    }
  }
  drawUtils = new DrawingUtils(ctx);
  startBtn.disabled = false;
  startBtn.textContent = "▶ Start camera";
  requestAnimationFrame(loop);
}

/* ---------------- Events ---------------- */
startBtn.addEventListener("click", () => {
  if (mode) stopAll();
  else startCamera();
});

fileInput.addEventListener("change", () => handleFile(fileInput.files[0]));

$("resetBtn").addEventListener("click", () => {
  session.reps = 0; session.scores = []; session.best = null;
  session.angleMin = session.angleMax = null;
  rep.started = false; rep.reached = false;
  angleBuffer = []; lastAngle = null; lastCue = "";
  $("statReps").textContent = "0";
  $("statScore").textContent = "—";
  $("statAngle").textContent = "—";
  $("statRom").textContent = "—";
  $("tipsList").innerHTML =
    "<li>Stand side-on to the camera.</li><li>Move at a steady 2–4 seconds per rep.</li><li>A low score ≠ bad — it means \"check with your therapist.\"</li>";
  updateSummary();
  setCue("Session reset. Waiting for movement…");
});

document.querySelectorAll(".exercise-card").forEach((card) => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".exercise-card").forEach((c) => c.classList.remove("active"));
    card.classList.add("active");
    currentExercise = card.dataset.exercise;
    const ex = EXERCISES[currentExercise];
    $("targetText").textContent = ex.targetText;
    $("statScore").textContent = "—";
    $("statReps").textContent = "0";
    session.reps = 0; session.scores = []; session.best = null;
    session.angleMin = session.angleMax = null;
    angleBuffer = [];
    setCue("Exercise changed. Waiting for movement…");
  });
});

function resizeCanvas() {
  const rect = overlay.getBoundingClientRect();
  overlay.width = rect.width;
  overlay.height = rect.height;
  const w = chartCanvas.clientWidth;
  chartCanvas.width = w;
}
window.addEventListener("resize", resizeCanvas);
window.addEventListener("load", resizeCanvas);
resizeCanvas();

init();
