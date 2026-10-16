# Clinical Safety & Limitations — RehabLens

*Rubric move: we state our limitations before a judge asks, and we show the
plan that turns each limitation into evidence.*

## 1. What RehabLens is

- A **movement-similarity research tool** that scores how closely a visible 2D
  movement matches an expert reference.
- A **flagging aid** for physical therapists — "this patient's form drifted,
  please look" — not a treatment decision-maker.

## 2. What RehabLens is NOT

- ❌ Not a medical device.
- ❌ Not a diagnosis, prognosis, or prescription.
- ❌ Not proof that an exercise is safe or unsafe.
- ❌ Not a substitute for a licensed physical therapist.

Every patient-facing screen in the demo carries this framing, and scores are
labelled *"Movement Score (research prototype)"* — never "recovery score" or
"health score."

## 3. Known technical limitations

| Limitation | Why it exists | Our mitigation |
|---|---|---|
| Single-camera 2D pose has depth ambiguity | No depth sensor on a phone camera | Confidence-gated scoring: frames with low-visibility joints are excluded, not guessed at |
| Camera angle changes the measured angles | 2D projection of 3D motion | Reference videos are recorded in the same camera view; the dataset manifest records `camera_view` per clip (front/side/back/diagonal) |
| Current LSTM trained on one demonstrator + augmentations | Data-collection stage of the project | Multi-participant dataset, split by participant so nobody appears in train and test; clinician-reviewed labels only |
| Augmented-pair accuracy (94.2%) is not patient-level validation | Prototype phase | Pilot study design in §5 |
| Clothing, lighting, and multiple people degrade pose detection | Real-world capture | Largest-person selection, single-person guidance in capture UI, visibility flags in model input |

## 4. Feedback design: fail soft

The system is designed so the cheapest failure mode is *"no score"*, never
*wrong advice*:

1. Low-confidence frames → session marked "unable to score" with a capture tip.
2. Score below threshold → "This movement looks different from the reference.
   Please check it with your therapist" — with the aligned angle chart so the
   therapist can see *why*.
3. High score → "Great consistency. Continue as prescribed." — the score
   describes similarity, not safety.

## 5. Validation plan (before any commercial claim)

1. **Participant-split retraining.** Collect consented recordings from ≥30
   participants across ≥5 exercises, each labelled by a qualified reviewer as
   `correct`, `knee_moves_inward`, `range_too_small`, `unstable`, or
   `uncertain`. Split by participant (group-level k-fold).
2. **Metric targets.** Report balanced accuracy and agreement (e.g., Cohen's
   κ) between model flags and reviewer labels; require κ ≥ 0.6 against
   clinician labels before pilot use.
3. **Pilot study.** With 1–2 outpatient clinics: measure adherence and
   range-of-motion deltas vs. a standard-HEP control group; publish protocol
   before enrolling (preregistration).
4. **Regulatory posture.** Keep the product in the wellness/RTM-adjacent
   space during the competition phase; a future medical-device pathway
   (e.g., FDA 510(k) as a physical-therapy decision-support software) is
   evaluated as a roadmap item, not assumed.

## 6. Human-in-the-loop by construction

The prototype's dataset workflow (`prototype/DATASET_WORKFLOW.md`) enforces
review: every imported movement starts as `needs_review`, and a human reviewer
must set correctness labels before the clip can be used for training. The
product inherits this: model flags go to a dashboard where the therapist — not
the model — decides what changes.

*This document answers the judge question "how do you know it won't hurt
someone?" with: architecture (confidence gating), design (fail-soft
feedback), and process (human review, participant-split validation, pilot
preregistration).*
