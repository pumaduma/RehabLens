# RehabLens — dataset

All movement data used by the RehabLens prototype, organized by provenance and
licence. Nothing here may identify a real patient: files use anonymous IDs and
every folder carries a manifest with source and consent notes.

## Layout

| Folder | Contents |
|---|---|
| [`expert_reference_sources/`](expert_reference_sources/) | 20-clip knee-rehab reference manifest (Cambridge University Hospitals) — clips themselves are kept private until redistribution rights are confirmed |
| [`pexels_pose_samples/`](pexels_pose_samples/) | Licensed (Pexels) movement samples used to test pose extraction |
| [`raw/`](raw/) | Original uploaded exercise videos (UCSF orthopaedic demos, hip/lunge exercises) with upload guidance and privacy rules |

## Ground rules

1. **Consent first** — only upload recordings you are authorized to share.
2. **No identifiers** — anonymous IDs (`P001`, `CUH01`, …), never names.
3. **Manifests are mandatory** — source URL, licence, camera view, and review
   status per file (see `LEG_REHAB_20_MANIFEST.csv` as the model).
4. **Human review before training** — new movements enter as `needs_review`;
   a reviewer assigns labels before the clip can train the LSTM.

See [`../docs/data-ethics.md`](../docs/data-ethics.md) for the full data
governance policy.
