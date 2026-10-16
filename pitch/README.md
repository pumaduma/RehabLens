# RehabLens — Pitch Deck

`RehabLens_Pitch_Deck.pptx` — 14 slides, built against the Conrad rubric:

| Rubric slice | Slide(s) |
|---|---|
| Storytelling (20%) | 2 — Maria's story, 14 — mission close |
| Innovation (30%) | 6 — Siamese LSTM, validation results |
| Practicality (20%) | 5 — live demo, 12 — safety case |
| Marketing (20%) | 8 — market, 9 — business model & RTM, 10 — competition |
| Financials (10%) | 11 — unit economics + 3-year projection |

Every slide has speaker notes with delivery tips and the exact numbers judges
will ask about.

## Rebuilding

The deck is generated from a script, so edits are reproducible:

```bash
python3 build_deck.py   # → RehabLens_Pitch_Deck.pptx
```

Edit `build_deck.py` (colors at the top, slide content in sections 1–14) and
re-run.

## Before you submit

1. Replace `[name]` placeholders (slides 1 and 14) with real team members.
2. Add a screenshot of the live demo to slide 5 if you want — the current
   mock screen is intentional and safe to keep.
3. Rehearse the speaker notes out loud; the deck is written for a 5-minute
   pitch with the demo taking the last minute.
