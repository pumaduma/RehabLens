# Competition Guide — How this repo maps to the Conrad Challenge

*The Conrad Challenge has three gates: the Activation Stage, the Innovation
Brief (the document that decides who advances), and the Summit pitch. This
page maps each gate to files in this repository so nothing gets written twice.*

## The rubric we built against

| Criterion | Weight | Where we earn it |
|---|---|---|
| Innovation | 30% | Sequence-aware LSTM scoring — see [`../prototype/`](../prototype/), [`./demo/`](./demo/), and Innovation Brief Q3–Q4 |
| Storytelling | 20% | The Maria story in [`../README.md`](../README.md) and Brief Q2; 90-second video script below |
| Practicality | 20% | Zero hardware, on-device privacy, fail-soft feedback — Brief Q3, Q9; [`clinical-safety.md`](clinical-safety.md) |
| Marketing | 20% | B2B2C clinic subscription + RTM reimbursement hook — Brief Q6–Q7; [`business-plan.md`](business-plan.md) |
| Financial understanding | 10% | Sane unit economics + 3-year projection — Brief Q8; [`business-plan.md`](business-plan.md) |

## Gate 1 — Activation Stage

Submit before the deadline (typically late fall):

- [ ] Team registration (2–5 students, one adult coach)
- [ ] Category: **Health & Nutrition**
- [ ] One-page idea summary → use the root [`../README.md`](../README.md) hero,
  problem, and solution sections
- [ ] 90-second video → use the script below

### 90-second video script (≈150 words)

> **[0:00–0:12 — the person]** *"Three weeks after knee surgery, Maria does
> her exercises every single day. She's doing everything right — except nobody
> can see that her knee drifts inward on every squat. Her therapist finds out
> at the follow-up visit, when recovery has already stalled. That gap between
> clinic visits is where recovery is lost."*
>
> **[0:12–0:35 — the invention]** *"We built RehabLens. Point any phone camera
> at a home exercise, and our AI scores the movement against the therapist's
> expert reference — in real time. It tells patients 'bend your knee 15° more,'
> counts their reps, and tracks their range of motion. A Siamese neural network
> compares the whole motion sequence, not just a single angle."*
>
> **[0:35–0:55 — the proof]** *"Our prototype scored the same exercise 99.5 out
> of 100, and caught a completely different exercise at zero. And here's the
> part clinics love: the monitoring we generate lets them bill Medicare's
> remote-therapy codes — the software pays for itself."*
>
> **[0:55–1:30 — the ask]** *"This year we're validating with real patients and
> a partner clinic. We're [team names], and we're giving every therapist eyes
> between visits."*

Filming tips: record the demo running live (phone filming a phone, or screen
recording + inset of the team). Show the score changing when form changes.
Close on the demo URL.

## Gate 2 — Innovation Brief

The document that decides advancement. Our answers: [`innovation-brief.md`](innovation-brief.md).
Copy each Q-section into the matching portal field, then personalize:

1. Replace the team table in the root README with real names/roles.
2. Add every real PT/patient conversation you've had into Brief Q5 —
   3–5 conversations measurably strengthens the entry.
3. If you add validation numbers, update the tables in README + Brief Q4.
4. Double-check every cited number still matches [`market-research.md`](market-research.md).

## Gate 3 — Summit finals (if we advance)

- **5-minute pitch + Q&A.** Slides: [`../pitch/RehabLens_Pitch_Deck.pptx`](../pitch/RehabLens_Pitch_Deck.pptx).
- **Live demo.** Phones out: judges open the browser demo and move. Have the
  exercise picker pre-set to "Seated Knee Extension" and one device mirrored
  to the projector.
- **Prepared Q&A (rehearse these):**
  - *"How is this different from [Hinge Health / wearable X]?"* → hardware-free,
    sequence-aware scoring, priced for independent clinics.
  - *"What if the AI is wrong?"* → fail-soft design; "check with your
    therapist," never a prescription; participant-split validation plan.
  - *"Who pays?"* → clinics, because RTM reimbursement makes it revenue-positive.
  - *"Why hasn't a big company done this?"* → they went enterprise/employer
    channel; we serve the long tail of 40k clinics.

## Reuse note

The same material transfers almost verbatim to the Diamond Challenge and
Blue Ocean competitions — write once, submit thrice.
