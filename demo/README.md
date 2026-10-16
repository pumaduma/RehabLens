# RehabLens — Live Browser Demo

An on-device AI form coach that runs entirely in your browser. This demo brings
the research pipeline's scoring idea to a page judges (and pilot clinics) can
open on any phone or laptop — no Python, no install.

## Try it

1. Open [`index.html`](index.html) in a browser, **or** enable GitHub Pages on
   the repo (`Settings → Pages → Deploy from a branch` → `main` / `/demo`) for
   a public URL.
2. Allow camera access (camera needs `https://` or `localhost` — GitHub Pages
   is ideal).
3. Pick an exercise, stand side-on so your whole body is visible, and move.
4. No camera? Use **📁 Try a video** to analyze a local video file.

## What it does

| Feature | How |
|---|---|
| Pose tracking | MediaPipe Pose Landmarker (lite model), 33 landmarks, runs on-device |
| Digital goniometry | Knee, hip, shoulder, and elbow angles computed live from landmarks |
| Rep counting | A state machine on the primary joint angle (depth threshold → return threshold) |
| Movement Score (0–100) | Per rep: depth quality 55% + symmetry 25% + tempo 20% |
| Coaching cues | Live plain-language feedback ("Go deeper — target ≤ 95°, you're at 118°") |
| Session report | Reps, average/best score, consistency, and range-of-motion achieved |
| Sparkline | Live angle trace vs. the target depth line |

## Exercises

- 🦵 Seated Knee Extension (knee angle)
- 🪑 Sit-to-Stand Squat (knee angle)
- 🌉 Glute Bridge (hip angle)
- 🙆 Shoulder Flexion (shoulder angle)
- 💪 Elbow Curl (elbow angle)

Each exercise has a target angle and expected range of motion encoded in
[`app.js`](app.js) under `EXERCISES` — easy to tune for a pilot protocol.

## How this relates to the research prototype

The competition's core innovation is the **Siamese bidirectional LSTM** in
[`../prototype/`](../prototype/), which compares a patient's *entire motion
sequence* to an expert reference and scores similarity (bridge-vs-bridge
99.5/100, bridge-vs-squat 0.0/100, 94.2% augmented-pair accuracy).

This browser demo is an **explainable, real-time approximation** of that idea:
instead of a learned motion embedding, it scores each rep with transparent
rules (depth, symmetry, tempo) that a judge can understand and verify on the
spot. The LSTM remains the research answer; the demo is the "show, don't tell"
answer for the pitch.

## Privacy

- All processing happens on-device with the MediaPipe wasm runtime.
- No video frames, landmarks, or metrics are uploaded anywhere.
- No cookies, accounts, or analytics.

## Technical notes

- MediaPipe assets load from CDNs (jsDelivr + Google storage) — an internet
  connection is required for the first load.
- The video preview is mirrored like a selfie camera; joint angles are
  unaffected by mirroring.
- If the GPU delegate fails, the app automatically falls back to CPU.
- Only one person should be in frame (the model tracks the single detected
  pose), matching the prototype's single-subject guidance.

## Files

| File | Purpose |
|---|---|
| [`index.html`](index.html) | Page structure |
| [`styles.css`](styles.css) | Design (teal/navy medical palette) |
| [`app.js`](app.js) | Pose pipeline, goniometry, rep machine, scoring, charting |

**Disclaimer:** research prototype. The Movement Score measures visible 2D
motion similarity; it is not a medical device, diagnosis, or proof that an
exercise is safe.
