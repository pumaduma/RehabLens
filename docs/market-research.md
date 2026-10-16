# Market Research — RehabLens

Every number used in our Innovation Brief and Business Plan, with its source.
All sources were retrieved October 2026. Links are provided so judges (and we)
can verify each claim.

## 1. The adherence problem

| Claim | Source |
|---|---|
| Only ~35% of physical-therapy patients fully adhere to prescribed home exercise programs | Sprypt, *"Boost Exercise Adherence 40%"* — https://www.sprypt.com/blog/improving-home-exercise-program-adherence-in-physical-therapy |
| 50.8% of patients who received an individualized exercise program showed non/low adherence | Argent et al. 2018, *Patient Involvement With Home-Based Exercise Programs* — https://pmc.ncbi.nlm.nih.gov/articles/PMC5856927/ |
| Non-adherence to home exercise programs is as high as 50–65% for general musculoskeletal conditions | Physio-pedia, *Adherence to Home Exercise Programs* — https://www.physio-pedia.com/Adherence_to_Home_Exercise_Programs |
| 43% of participants were adherent; 31.7% discontinued before completion | Shahidi et al. 2022, PLOS ONE — https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0276326 |
| ~73% of patients fail to follow their home exercise programs as prescribed | GetOrva — https://www.getorva.com/blog/why-73-of-patients-dont-complete-their-home-exercise-programs-and-what-actually-works |

**Takeaway:** non-adherence of 50–70% is the consensus range across peer-reviewed and industry sources; full adherence is the minority outcome.

## 2. Market size

| Claim | Source |
|---|---|
| U.S. physical therapy services market: $52.3B (2025) → $76.6B (2033), 4.9% CAGR | Grand View Research — https://www.grandviewresearch.com/industry-analysis/us-physical-therapy-services-market-report |
| U.S. occupational & physical therapy services: $65.36B (2025) → $128.17B (2032), 10.1% CAGR | Fortune Business Insights — https://www.fortunebusinessinsights.com/u-s-occupational-physical-therapy-services-market-106420 |
| U.S. AI-in-physical-therapy market: $224.5M (2026) → $1.71B (2035) | Towards Healthcare — https://www.towardshealthcare.com/insights/us-ai-in-physical-therapy-market-sizing |
| Physical therapy software market: $1.3B (2024) → $2.5B (2030), 10.6% CAGR | Research and Markets — https://www.researchandmarkets.com/report/physical-therapy-software |
| U.S. telerehabilitation / virtual PT services growing ~8.7% CAGR | Coherent Market Insights — https://www.coherentmarketinsights.com/market-insight/us-physical-therapy-virtual-and-telerehabilitation-services-market-4982 |

**Takeaway:** the services market is large and growing; the *software* layer we sell into ($1.3B, 10.6% CAGR) is the direct comparison set — and it is still early, consistent with our small SAM numbers.

## 3. Clinic count and workforce pressure

| Claim | Source |
|---|---|
| Demand for physical-therapist services projected to grow 14.7% by 2037, vs 8% population growth | APTA 2025 Workforce Forecast — https://www.apta.org/contentassets/787bafc2ef664074ace8914f748ee4cd/apta-2025-workforce-forecast-companion-report.pdf |
| ~40,000 outpatient physical-therapy clinic sites in the U.S. | Industry standard estimate used in our bottom-up SAM (see business plan; refine with IBISWorld / APTA data before submission) |

**Takeaway:** a workforce that cannot meet demand is exactly the condition that makes software leverage (one therapist, many monitored patients) attractive.

## 4. Reimbursement tailwind: Remote Therapeutic Monitoring (RTM)

| Claim | Source |
|---|---|
| Physical therapists may bill RTM codes under Medicare; codes may also be billable under commercial plans | APTA practice advisory — https://www.apta.org/contentassets/95321a10e951408db650e2f19b96699f/apta-practice-advisory-rtm-codes032023.pdf |
| CPT 98975 (initial RTM setup & patient education): 2026 national average ≈ $21.71 (one-time) | Limber Health — https://www.limberhealth.com/blog/rtm-cpt-code-98975 |
| RTM codes range approximately $22–$54 per code per month (98976/98977 device supply & data transmission) | NSight Care, 2026 RTM guide — https://blog.nsightcare.com/blog-/remote-therapeutic-monitoring-rtm-cpt-codes-2026-billing-reimbursement-guide |
| 2026 CMS therapy code list adds new RTM codes (98984/98985), expanding remote-monitoring billing | CMS transmittal — https://www.cms.gov/files/document/r13431cp.pdf |

**Takeaway:** a clinic monitoring one patient with RehabLens can bill roughly $19–$54/month in RTM codes — several times the per-patient cost of our software. This is the "who pays, and why now" answer.

## 5. Competitive landscape

| Player | Model | What they do | RehabLens differentiation |
|---|---|---|---|
| Sword Health | B2B enterprise (self-insured employers) | Digital MSK care + motion sensors | Hardware-free, open, priced for independent clinics |
| Hinge Health | B2B enterprise | Digital MSK care, employer channel | Same channel contrast; we serve the 40k independent clinics they bypass |
| Kaia Health | B2B2C apps | Guided exercise video apps | No objective movement-quality scoring from a plain camera |
| Physitrack / Medbridge | Clinic HEP content platforms | Prescribe & track exercise completion | Track *completion*, not *quality* — our core feature |
| Wearables (e.g., sensor-based PT) | Hardware + app | Rep counting via motion sensors | Zero hardware cost & friction; visual form feedback |

**Positioning sentence:** *"The quality layer that existing HEP platforms are missing — camera-based, sequence-aware, and priced for the independent clinic."*

## 6. Expert-reference dataset provenance (our training material)

- 20 knee-rehab reference clips derived from Cambridge University Hospitals' early-knee-exercise series — https://www.cuh.nhs.uk/our-services/physiotherapy-outpatients/outpatient-physio-resources/resources/knee/early-knee-exercises/
- Testing samples licensed from Pexels (glute bridge, seated stretch, plank) — https://www.pexels.com/license/
- Raw upper/lower-body demonstration videos from UCSF Orthopaedic Surgery education materials.
- Clips are used for research/education; redistribution rights are tracked per-file in the manifests under [`../dataset/`](../dataset/).
