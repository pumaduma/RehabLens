# Roadmap — RehabLens (24 months)

*Mapped to Conrad phases, then to product milestones. Each phase ends with a
decision gate: evidence required before we proceed.*

## Phase 0 — Competition (now → finals)

**Goal: win with evidence, not promises.**

- [x] YOLO Pose + Siamese LSTM prototype with positive/negative controls
- [x] 20-clip expert-reference dataset with provenance manifests
- [x] Browser demo: on-device pose tracking, goniometry, rep counting, scoring
- [x] Innovation Brief, business plan, pitch deck (this repo)
- [ ] 3–5 recorded conversations with physical therapists (problem validation)
- [ ] 90-second Activation Stage video + finals pitch rehearsal
- [ ] Demo day: judges try the browser demo on their own phones

## Phase 1 — Evidence (months 0–6)

- Recruit 1–2 local outpatient PT clinics as pilot partners
- Collect consented multi-participant dataset: ≥30 participants, ≥5 exercises
  (knee flexion, squat/sit-to-stand, glute bridge, shoulder flexion, wrist
  extension), clinician-reviewed labels, participant-split
- Retrain LSTM; report balanced accuracy + Cohen's κ vs clinician labels
  (target: κ ≥ 0.6)
- Ship therapist dashboard v0 (read-only: trends, flags, RTM export)

**Gate:** κ ≥ 0.6 and pilot clinic sign-off → proceed.

## Phase 2 — Pilot (months 6–12)

- 2-clinic, 3-month pilot with post-op knee/hip patients
- Measure: adherence rate, range-of-motion delta, therapist time saved,
  RTM claims filed vs. control
- Publish protocol first (preregistered); publish results as a white paper
- Dashboard v1: patient assignments, thresholds, review queue

**Gate:** adherence or ROM improvement with honest effect size, and ≥1 clinic
willing to pay → proceed.

## Phase 3 — Commercial (months 12–24)

- Pricing launch: $149/mo clinic tier, $59/mo extra seats, $249/mo RTM Pro
- Target 120 paying clinics by month 24 (state APTA chapters, conference
  demos, billing-consultancy channel)
- HIPAA-compliant hosting (BAA) before any real patient data
- Begin white-label conversations with 1–2 telehealth PT platforms

## Long-term horizon (beyond 24 months)

- Insurer outcome-data partnerships (opt-in, anonymized)
- FDA decision-support pathway evaluation
- Expansion: home health, occupational therapy, sports-medicine teams

## Team capacity note

Through Phase 2 the team is students + coach working part-time; the roadmap
is sized to that reality (a pilot, not a product launch, in year one). This
is a strength: the plan is executable, and judges reward plans a team can
actually run.
