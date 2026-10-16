# RehabLens — Conrad Innovation Brief

> **Category:** Health & Nutrition
> **Team size:** 2–5 students + adult coach
> **Stage:** Innovation Brief (Stage 2)
>
> This document is structured as our answers to the ten core Innovation Brief
> questions. Each section can be copied directly into the corresponding field
> in the Conrad submission portal. Facts and figures are sourced in
> [`market-research.md`](market-research.md).

---

## Q1. What is your innovation? (one-sentence summary)

**RehabLens is an AI form-coach for physical therapy that scores a patient's
home-exercise video against their therapist's expert reference — using a
sequence-aware neural network — and turns every session into a progress report
for the clinic.**

---

## Q2. What problem does it solve, and who has that problem?

After an injury or surgery, a physical therapist prescribes a home exercise
program (HEP) — the single most important part of recovery. But between weekly
clinic visits, the therapist is blind: there is no way to know whether the
patient exercised, and no way to know whether they moved *correctly*.

Only ~35% of PT patients fully adhere to their HEP, and non-adherence runs as
high as 70%. Even motivated patients — like the 63-year-old knee-replacement
patient who inspired this project — perform exercises with silent form errors
(knee drifting inward, incomplete range of motion, compensating with the wrong
muscles) that stall recovery and raise re-injury risk. The therapist discovers
the problem weeks later at a follow-up visit, when the recovery window has
already lengthened.

**Who has the problem:** three groups, in order of pain:

1. **Patients** (especially post-surgical and older adults) who want to recover
   faster but have no feedback at home;
2. **Physical therapists** who must trust that unsupervised patients are
   exercising correctly, with no data between visits;
3. **Clinics and health systems** that absorb the cost of longer recoveries
   and extra visits — in a U.S. market worth $52B+ and growing faster than the
   PT workforce can staff.

---

## Q3. What makes it innovative? Why is it better than what exists?

Today's tools fall into three families, and none closes the form-quality gap:

| Existing approach | What it does | What it misses |
|---|---|---|
| Printed sheets & video links | Show *what* to do | No feedback at all |
| Wearables (motion sensors) | Count reps, estimate angles | Extra hardware cost, no visual form feedback, patient must buy/charge/strap devices |
| Telehealth exercise apps | Play videos, log "done" | Self-reported; no objective movement-quality measurement |

**RehabLens's innovation is sequence-aware movement scoring from a plain
camera.** Where other systems measure a static snapshot of one joint angle, our
Siamese bidirectional LSTM encodes the *entire motion sequence* — the patient's
and the therapist's reference — into the same embedding space and scores their
similarity. That means the score captures depth, timing, coordination, and
compensation patterns, not just "did the knee reach 90°."

Three practical advantages follow:

- **Zero hardware.** Any smartphone camera. No wearables, no sensors, no setup.
- **Private by design.** Pose extraction runs on-device in the demo; only
  anonymized metrics (never video) travel to the clinic dashboard.
- **Bills itself.** Clinics can bill Medicare Remote Therapeutic Monitoring
  codes (98975/98977, ~$19–$54 per patient) for the monitoring RehabLens
  enables — so the product pays for itself while improving outcomes.

---

## Q4. How does it work? (the science)

The prototype pipeline ([`prototype/`](../prototype/)) has five stages:

1. **Pose estimation** — YOLO Pose detects 17 body landmarks in every frame.
2. **Digital goniometry** — hip, knee, thigh, and shin angles are computed
   per frame, plus a confidence value per joint.
3. **Sequence encoding** — each video becomes 96 time steps × 16 values
   (8 angles + 8 visibility flags), so occluded joints are handled honestly.
4. **Siamese LSTM scoring** — a shared two-layer bidirectional LSTM (hidden
   size 64) encodes the patient's sequence and the expert reference into
   32-dimension motion embeddings; cosine similarity becomes a 0–100
   Movement Score.
5. **Explainable output** — side-by-side skeleton video, aligned angle curves
   (dynamic time warping), CSV data, and a plain-language report.

The browser demo ([`demo/`](../demo/)) implements stages 1–2 plus real-time
rep counting, depth feedback, and reference-curve scoring with MediaPipe Pose,
running 100% on-device.

**Validation so far:**

| Test | Result |
|---|---|
| Same movement, two recordings (bridge vs bridge) | 99.5 / 100 |
| Different movements (bridge vs squat — negative control) | 0.0 / 100 |
| Augmented-pair accuracy (20 clips, 12 movement groups, 94.2% correct) | 94.2% |

**Honest caveat:** current training data comes from a single source
demonstrator with augmentations (speed, angle noise, mirroring, simulated
dropouts). This is a proof of concept, not a patient-level clinical test —
see [`clinical-safety.md`](clinical-safety.md) for the validation plan.

---

## Q5. How did we validate the problem and the solution?

- **Problem validation:** literature review (sourced in
  [`market-research.md`](market-research.md)) plus conversations with the
  adult coach and, where available, physical therapists about what they cannot
  see between visits. *(Team: log your real interviews here — even 3–5
  conversations with PTs or patients strengthens this answer enormously.)*
- **Technical validation:** the prototype's positive/negative control tests
  and augmented-pair accuracy above, plus a human-review workflow in which a
  qualified reviewer labels every new clip before it enters training.
- **Next validation step:** a consented pilot with multiple participants,
  split by person across train/validation/test so the same individual never
  appears in more than one group (see roadmap).

---

## Q6. Who is the customer, and how big is the market?

**Primary customer:** U.S. outpatient orthopedic physical-therapy clinics
(~40,000 sites). **Secondary:** telehealth PT platforms, hospital outpatient
departments, and eventually insurers who want to pay for outcomes instead of
visits.

Market sizing (bottom-up, conservative):

- **TAM** — U.S. physical-therapy services: **$52.3B** in 2025, growing
  4.9% annually to $76.6B by 2033 (Grand View Research).
- **SAM** — outpatient orthopedic clinics' digital-HEP / RTM software spend:
  ≈ 40,000 clinics × ~$1,800/yr ≈ **$72M/yr** at full adoption.
- **SOM (year 3 target)** — 500 clinics ≈ **$894K ARR**, roughly 1.2% of SAM.

Detail and sources: [`market-research.md`](market-research.md).

---

## Q7. How will we make money? (business model)

**B2B2C subscription:** clinics pay, patients use it free as part of their care
plan.

- Clinic subscription: **$149/month** per clinic (unlimited patients, 3
  therapist seats; $59/month per additional therapist).
- Optional RTM-enabled tier ($249/month) that generates the documentation
  clinics need to bill Medicare codes 98975/98977 — where each monitored
  patient can earn the clinic **~$19–$54/month**, several times the software
  cost.
- Later: white-label licensing to telehealth platforms (per-patient-per-month
  fee), and outcome-data partnerships with insurers (opt-in, anonymized).

**Why now:** telehealth PT utilization is structurally higher post-COVID, the
2026 CMS therapy code list expanded remote-monitoring billing, and clinics are
actively looking for tools that create billable monitoring without extra staff
time. The reimbursement tailwind is the "why now" that makes the model work.

---

## Q8. What does it cost to build and run, and what funding do we need?

Unit economics per clinic (steady state):

| Line | Monthly |
|---|---|
| Revenue | $149 |
| Hosting / inference | $8 |
| Support & onboarding | $10 |
| Payment processing | ~$5 |
| **Gross margin** | **~85%** |

Build costs are dominated by model validation, not hardware: we need a
consented multi-participant dataset (~$0 if collected through our school and
pilot clinics), cloud compute for training ($50–200), and pilot onboarding.

**Funding needed:** roughly **$5,000–$10,000** to cover cloud compute, a HIPAA-
capable hosting setup for the clinic dashboard, and pilot materials — plus
in-kind mentorship. We plan to fund this through Conrad and equivalent
competition awards, school research grants, and a local clinic pilot partner.
Three-year financials are in [`business-plan.md`](business-plan.md).

---

## Q9. What are the risks and limitations, and how do we handle them?

We treat our limitations as a safety case, not a footnote:

| Risk / limitation | Our mitigation |
|---|---|
| 2D camera pose can be fooled by camera angle, clothing, or occlusion | We measure joint-visibility confidence and refuse to score low-confidence frames; the training pipeline explicitly simulates occlusions |
| Single-demonstrator training data limits generalization | Multi-participant consented dataset, split by person; clinician-reviewed labels only |
| Wrong form feedback could hurt someone | Scores are "flag for your therapist," never a prescription; human review workflow; explicit non-medical-device positioning |
| Privacy risk from video | On-device processing in the demo; anonymized metrics only to the cloud; consent-first data governance (see [`data-ethics.md`](data-ethics.md)) |
| Reimbursement rules vary | RTM tier ships with billing documentation; we validate with a billing-savvy pilot clinic |
| Established competitors (Sword Health, Hinge Health) | We are open, PT-owned, hardware-free, and priced for independent clinics rather than self-insured employers |

---

## Q10. What is our plan and team?

**Timeline (24 months):**

- **Months 0–3:** recruit pilot clinic; collect first consented
  multi-participant dataset; refine demo.
- **Months 4–8:** retrain LSTM on multi-participant data; participant-split
  evaluation; publish results; pilot v1 with 1–2 clinics.
- **Months 9–14:** therapist dashboard; RTM documentation workflow; 10-clinic
  pilot.
- **Months 15–24:** commercial launch at $149/month; target 120 paying
  clinics by month 24. Full detail: [`roadmap.md`](roadmap.md).

**Team:** 2–5 students (machine learning, product/UX, business) plus an adult
coach who acts as clinical advisor. Names and bios: see root
[`README.md`](../README.md).

---

*Supporting detail: [`business-plan.md`](business-plan.md) ·
[`market-research.md`](market-research.md) ·
[`clinical-safety.md`](clinical-safety.md) · [`data-ethics.md`](data-ethics.md) ·
[`roadmap.md`](roadmap.md)*
