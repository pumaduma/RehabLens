# RehabLens research prototype — LSTM rehabilitation movement scoring

This folder contains the **RehabLens** prototype that compares a home
rehabilitation video with an expert reference video.

1. YOLO Pose detects body landmarks.
2. The program calculates left and right hip, knee, thigh, and shin angles.
3. A Siamese bidirectional LSTM encodes both movement sequences.
4. Cosine similarity produces a 0–100 movement score.
5. The program exports a side-by-side video, angle graph, CSV data, and report.

The bridge-to-bridge verification scored 99.5/100. A bridge-to-squat negative
test scored 0.0/100. The augmented-pair check reached 94.2% accuracy.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Score your own video against an expert reference:
python dataset_tools/compare_rehab_videos.py \
  --standard <expert_reference.mp4> --user <your_video.mp4>
```

## More detail

- [`LSTM_COMPARISON.md`](LSTM_COMPARISON.md) — model architecture, inputs, and
  training data.
- [`DATASET_WORKFLOW.md`](DATASET_WORKFLOW.md) — dataset import, angle
  analysis, and human-review workflow (double-click `.command` launchers for
  macOS).

## Safety

The model is a classroom prototype. It measures visible 2D motion similarity
and must not be treated as a medical diagnosis or proof that an exercise is
safe. See [`../docs/clinical-safety.md`](../docs/clinical-safety.md) for the
full safety case and validation plan.

*Project home: [`../README.md`](../README.md) · Live browser demo:
[`../docs/demo/`](../docs/demo/)*
