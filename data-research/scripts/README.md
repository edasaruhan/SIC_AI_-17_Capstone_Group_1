# Synthetic data generator (K4)

## Requirements

- Python 3.10+ (stdlib only — no pip packages)

## Run

```bash
cd data-research/scripts
python3 synthetic_data.py --n 100 --seed 42 --out ./sample_output
```

## Outputs

| File | Description |
|------|-------------|
| `metadata.json` | seed, schema_version, counts, disclaimer |
| `students.csv` | segment_label, exam_track, risk_prior |
| `parent_profiles.csv` | free_text_tr (synthetic) |
| `surveys.csv` | student + parent items |
| `focus_sessions.csv` | planned/completed minutes |
| `phone_events.csv` | category, duration_sec, notify_flag (≥600s distractor) |
| `weekly_metrics.csv` | weekly aggregates |
| `parent_intents.csv` | raw vs softened message templates |

## Rules

- `notify_flag = true` iff distractor category and `duration_sec >= 600` and in focus block
- Education/communication apps are non-distractors
- No real PII; IDs like `stu_0001`
- **Not a pilot dataset** — demo and pipeline only

## Schema

See `../../02-schema/02_data_dictionary.md` (schema_version 1.0.0 aligned).
