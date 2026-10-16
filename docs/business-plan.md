# Business Plan — RehabLens

*Companion to the [Innovation Brief](innovation-brief.md). Numbers sourced in
[market-research.md](market-research.md). Financials are deliberately modest:
sane beats sophisticated, and judges reward honesty.*

## 1. Mission

Give every physical-therapy patient a coach at home and every therapist eyes
between visits — with nothing more than the camera they already own.

## 2. Problem → product fit

- **Patients** recover slower because home exercise is unsupervised; 50–70%
  don't do it correctly or at all.
- **Therapists** lose the data that would let them adjust plans between visits.
- **Clinics** lose revenue opportunities they are already entitled to (RTM
  billing) while paying for longer recovery cycles.

RehabLens converts every home exercise session into: a live form score for the
patient, and a progress report + billable monitoring record for the clinic.

## 3. Product

1. **Patient app / web capture** — camera-based, on-device pose tracking;
   real-time cues, rep counting, and a 0–100 Movement Score per exercise.
2. **Therapist dashboard** — patient progress trends, range-of-motion charts,
   flagged sessions, RTM documentation export.
3. **Scoring engine** — Siamese bidirectional LSTM comparing motion sequences
   to expert references (prototype accuracy 94.2% on augmented pairs; see
   [`../prototype/`](../prototype/)).

## 4. Market

**TAM / SAM / SOM (bottom-up, year-3 target):**

| Layer | Number | Basis |
|---|---|---|
| TAM | $52.3B | U.S. PT services market, 2025 (Grand View Research) |
| SAM | ≈ $72M ARR | ≈40,000 U.S. outpatient orthopedic clinics × ~$1,788/yr ($149/mo) |
| SOM | ≈ $894K ARR | 500 clinics by year 3 (~1.2% of SAM) |

Adjacent upside (not counted in SOM): white-label licensing to telehealth
platforms and insurer outcome partnerships.

## 5. Business model

**Subscription, B2B2C:**

| Tier | Price | Includes |
|---|---|---|
| Clinic | $149/mo | Unlimited patients, 3 therapist seats, dashboard, patient app |
| Therapist add-on | $59/mo | Additional seat |
| RTM Pro | $249/mo | Auto-generated RTM documentation for 98975/98977 billing |

Patients pay nothing. The clinic's ROI comes from three directions:

1. **Reimbursement:** one monitored Medicare patient ≈ $19–$54/mo in RTM
   codes (setup 98975 ≈ $21.71 one-time; supply/data 98976/98977 ≈
   $22–$54/mo) — the software pays for itself after 1–3 monitored patients.
2. **Throughput:** PTs see more patients because between-visit progress is
   already charted.
3. **Outcomes marketing:** "monitored recovery" becomes a clinic differentiator.

## 6. Unit economics (per clinic, steady state)

| Line | Monthly | Annual |
|---|---|---|
| Revenue | $149 | $1,788 |
| Hosting + inference | $8 | $96 |
| Support & onboarding (amortized) | $10 | $120 |
| Payments/processing | $5 | $60 |
| **Gross margin** | **≈85%** | **≈$1,512** |

CAC estimate: $400/clinic (demo-led sales, conference presence, pilot
referrals). Payback: ~3.2 months. LTV (3-yr retention at 90%): ≈ $4,300 →
**LTV:CAC ≈ 11** in steady state.

## 7. Three-year financial projection (conservative)

| | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| Paying clinics (EOP) | 20 | 120 | 500 |
| ARR (EOP) | $36K | $214K | $894K |
| Revenue recognized | $18K | $125K | $554K |
| Team | 5 students + coach | 5 students + coach + 1 PT consultant | + 1 engineer |
| Cloud & infra | $4K | $18K | $60K |
| Marketing (conf., pilots, content) | $5K | $25K | $80K |
| Other opex | $4K | $12K | $40K |
| **Net income** | **$5K** | **$70K** | **$374K** |

Assumptions: no salaries for student founders in years 1–2; pricing held flat;
churn 10%/yr; all revenue subscription. The model becomes venture-scale only
after the white-label and insurer channels open — which is why they are
roadmap items, not forecasts.

## 8. Go-to-market

1. **Pilot-first:** 1–2 local outpatient clinics run a 3-month pilot with
   post-op knee/hip patients (our dataset's strongest exercise coverage).
2. **Evidence marketing:** publish the pilot's adherence and range-of-motion
   deltas; every customer conversation starts with data, not slides.
3. **Community channel:** demo at state APTA chapter meetings and student
   science events; a $149/mo price point is signable by a clinic owner, not a
   procurement department.
4. **Reimbursement channel:** partner with one billing consultancy to certify
   the RTM documentation workflow; then the pitch is "this pays for itself."
5. **Year 3:** white-label conversations with telehealth PT platforms; opt-in
   anonymized outcome-data partnerships with insurers.

## 9. Risks

See the risk table in the [Innovation Brief §Q9](innovation-brief.md) and the
full safety case in [clinical-safety.md](clinical-safety.md).

## 10. The honest unknowns (we will tell judges these)

- Multi-participant generalization of the scoring model is **unproven**; the
  pilot is designed to answer exactly this.
- 2D pose from a single camera has inherent limits (depth ambiguity); our
  mitigation is confidence-gated scoring, not pretending the problem away.
- RTM billing varies by payer and state; we validate with a billing-savvy
  clinic before claiming it in marketing.
