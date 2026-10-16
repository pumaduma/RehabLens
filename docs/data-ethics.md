# Data Ethics & Privacy — RehabLens

RehabLens handles the most sensitive kind of image data: video of people's
bodies, often while injured. Our ethics posture is a feature of the product,
and we state it up front.

## 1. Principles

1. **Consent first, always.** No video is ever captured, stored, or processed
   without informed consent that names exactly how the data will be used.
2. **Minimum collection.** We capture only what the feature needs — motion
   metrics, not identities.
3. **On-device by default.** Pose extraction runs on the user's device; raw
   video never leaves the phone in the consumer demo.
4. **The human decides.** The therapist, not the model, makes care decisions.
5. **Research data ≠ product data.** Dataset clips and product metrics are
   governed separately.

## 2. In the demo (today)

- 100% on-device: MediaPipe runs in the browser; no frames, landmarks, or
  metrics are uploaded anywhere.
- No accounts, no cookies, no analytics.
- An on-screen banner states this plainly.

## 3. In the research dataset (today)

- Anonymous participant IDs (`P001`, `CUH01`, …) — never names.
- A per-file manifest records source, licence, camera view, and consent
  status (`dataset/expert_reference_sources/LEG_REHAB_20_MANIFEST.csv`).
- Clips whose redistribution rights are unclear (the Cambridge University
  Hospitals series) are kept out of the public repo; only the manifest and
  links ship. See `dataset/` READMEs.
- Human review: imported movements start as `needs_review`; labels are added
  by a reviewer, and a qualified physical therapist must approve definitions
  used for patient-facing feedback.

## 4. In the pilot and product (planned)

| Area | Commitment |
|---|---|
| Consent | Lay-language consent form naming the pilot purpose, retention period, and withdrawal right; re-consent if data use changes |
| Minimization | Clinic dashboard receives **metrics only** (angles, scores, reps, timestamps) unless a clinician explicitly requests a flagged clip for review |
| Retention | Raw video: never stored server-side by default; flagged clips auto-delete after 30 days |
| Access | Patient can view, export, and delete their own data at any time |
| Minors | Parental/guardian consent required; pediatric protocols reviewed with the coach |
| Regulatory path | U.S. deployment targets HIPAA-compliant hosting (BAA with provider) before any PHI; GDPR-style rights (access/erasure) by default worldwide |
| Model bias | Report accuracy across participant subgroups (age, gender, limb), not just overall; investigate before scaling |

## 5. What we will not do

- ❌ Sell or share individual patient data with insurers, employers, or
  advertisers.
- ❌ Use exercise video to infer health status beyond the prescribed exercise
  session.
- ❌ Keep video longer than needed to deliver or improve the service.

## 6. Judge-ready answers

- *"What if the model is biased?"* — We evaluate per-subgroup, publish the
  results, and refuse to ship a feature whose subgroup performance we haven't
  measured.
- *"What happens if a patient withdraws consent?"* — Their account data and
  clips are deleted within 30 days; already-anonymized aggregate statistics
  (which cannot identify them) may remain.
- *"Is the demo HIPAA-compliant?"* — The demo collects nothing, so nothing
  needs protecting. The clinic dashboard will be, before any real patient
  data flows.
