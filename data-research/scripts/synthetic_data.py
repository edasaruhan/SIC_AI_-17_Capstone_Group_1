#!/usr/bin/env python3
"""
AI Personal Coach — synthetic data generator (K4)

Generates schema-compatible CSV files for:
  students, parent_profiles, surveys, focus_sessions,
  phone_events, weekly_metrics, parent_intents + metadata.json

No real PII. Stdlib only. Repeatable with --seed.

Example:
  python3 synthetic_data.py --n 100 --seed 42 --out ./sample_output
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"
NOTIFY_THRESHOLD_SEC = 600

SEGMENTS = [
    "baslayamayan",
    "yarida_birakan",
    "telefonla_dagilan",
    "kaygiyla_erteleyen",
    "geceye_kayan",
]

SEGMENT_PRIORS = {
    "baslayamayan": 0.20,
    "yarida_birakan": 0.20,
    "telefonla_dagilan": 0.25,
    "kaygiyla_erteleyen": 0.15,
    "geceye_kayan": 0.20,
}

DISTRACTORS = {"social", "game", "video"}
SAFE_CATS = {"education", "communication"}

SUBJECTS = ["matematik", "turkce", "fen", "tarih", "ingilizce", "fizik", "kimya"]

PARENT_TEMPLATES = {
    "baslayamayan": [
        "Masaya oturması saatler sürüyor, dersi bir türlü başlatamıyor.",
        "Plan yapıyoruz ama ilk adımı atmakta zorlanıyor.",
        "Başlamadan önce defalarca bahane buluyor.",
    ],
    "yarida_birakan": [
        "Dersi açıyor ama 15 dakikada bırakıyor, yarım kalıyor.",
        "İlk heyecanla başlıyor, sonra dağılıp kalkıyor.",
        "Blokları sonuna kadar getiremiyor.",
    ],
    "telefonla_dagilan": [
        "Akşam dersi açıyor ama telefon elinden düşmüyor, sosyal medyada kayboluyor.",
        "Odaklandığını sanıyoruz, uygulamalar dikkatini dağıtıyor.",
        "Telefon bildirimleri dersi sürekli bölüyor.",
    ],
    "kaygiyla_erteleyen": [
        "Deneme haftası olunca iyice kapanıyor, kaygıyla erteliyor.",
        "Yanlış yapmaktan korktuğu için başlamıyor.",
        "Sınav yaklaşınca çalışma düzeni bozuluyor.",
    ],
    "geceye_kayan": [
        "Gündüz boş geçiyor, gece geç saatlere yığıyor.",
        "Uyku düzeni bozuldu, gece çalışıp sabah verimsiz oluyor.",
        "Akşam geç başladığı için ertesi gün yetiştiremiyor.",
    ],
}

INTENT_RAW = [
    "Yine telefon, yine boş; böyle YKS kazanılmaz.",
    "Dersi yine böldü, çok kızgınım.",
    "Saatlerdir masada ama hiçbir şey bitmemiş.",
    "Herkes çalışıyor, o hâlâ erteiyor.",
]

INTENT_SOFT = [
    "Dikkatin dağıldığını gördük. Sorun değil, şimdi toparlanabilirsin. 20 dakikalık tek bir soru bloğu yap; bitince kısa mola senin.",
    "Bugün zor bir gün olabilir. Küçük bir adım yeterli: 15 dakika sadece ilk soru seti.",
    "Yarım kalan bloğu birlikte kapatabiliriz. Zamanlayıcıyı 25 dakikaya kur, sadece bir konuya bak.",
    "Geceye bırakmak yorucu olabilir. Yarın gündüz 2 kısa blok planlayalım.",
]

SURVEY_ITEMS_STUDENT = [
    ("q_chrono", ["morning", "evening", "mixed"]),
    ("q_start_vs_persist", ["start_harder", "persist_harder", "both"]),
    ("q_phone_reason", ["social", "game", "video", "message", "boredom"]),
    ("q_reward", ["break", "points", "parent_praise", "goal_progress"]),
    ("q_anxiety", ["freeze", "avoid", "rush", "ask_help"]),
]

SURVEY_ITEMS_PARENT = [
    ("qp_strength", ["disciplined", "curious", "social", "creative"]),
    ("qp_hard_subject", SUBJECTS),
    ("qp_home_routine", ["quiet_desk", "shared_room", "noisy", "library"]),
    ("qp_what_works", ["timer", "reward", "together_start", "short_blocks"]),
]


def weighted_choice(rng: random.Random, weights: dict[str, float]) -> str:
    keys = list(weights.keys())
    vals = [weights[k] for k in keys]
    return rng.choices(keys, weights=vals, k=1)[0]


def risk_for_segment(rng: random.Random, segment: str) -> float:
    bands = {
        "baslayamayan": (0.55, 0.85),
        "yarida_birakan": (0.45, 0.75),
        "telefonla_dagilan": (0.50, 0.90),
        "kaygiyla_erteleyen": (0.40, 0.70),
        "geceye_kayan": (0.35, 0.65),
    }
    lo, hi = bands[segment]
    return round(rng.uniform(lo, hi), 3)


def is_distractor(category: str, rng: random.Random) -> bool:
    if category in DISTRACTORS:
        return True
    if category in SAFE_CATS:
        return False
    return rng.random() < 0.25  # other


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def generate(n: int, seed: int, weeks: int, sessions_per_student: int, out: Path) -> dict[str, Any]:
    rng = random.Random(seed)
    out.mkdir(parents=True, exist_ok=True)

    students: list[dict[str, Any]] = []
    parents: list[dict[str, Any]] = []
    surveys: list[dict[str, Any]] = []
    sessions: list[dict[str, Any]] = []
    phones: list[dict[str, Any]] = []
    intents: list[dict[str, Any]] = []
    weekly: list[dict[str, Any]] = []

    survey_id = 0
    session_id = 0
    phone_id = 0
    intent_id = 0

    for i in range(1, n + 1):
        sid = f"stu_{i:04d}"
        pid = f"par_{i:04d}"
        segment = weighted_choice(rng, SEGMENT_PRIORS)
        exam = rng.choice(["LGS", "YKS"])
        if exam == "LGS":
            age_band = rng.choice(["13-14", "13-14", "15-17"])
        else:
            age_band = rng.choice(["15-17", "15-17", "18+"])
        chrono = rng.choice(["morning", "evening", "mixed"])
        if segment == "geceye_kayan":
            chrono = rng.choice(["evening", "evening", "mixed"])

        risk = risk_for_segment(rng, segment)
        students.append(
            {
                "student_id": sid,
                "exam_track": exam,
                "age_band": age_band,
                "chronotype": chrono,
                "segment_label": segment,
                "risk_prior": risk,
            }
        )

        tone = rng.choice(["anxious", "supportive", "strict"])
        parents.append(
            {
                "parent_id": pid,
                "student_id": sid,
                "free_text_tr": rng.choice(PARENT_TEMPLATES[segment]),
                "tone_hint": tone,
            }
        )

        # surveys — onboarding week 0
        for item_id, answers in SURVEY_ITEMS_STUDENT:
            survey_id += 1
            surveys.append(
                {
                    "survey_response_id": f"srv_{survey_id:05d}",
                    "respondent_role": "student",
                    "student_id": sid,
                    "item_id": item_id,
                    "answer_code": rng.choice(answers),
                    "week_no": 0,
                }
            )
        for item_id, answers in SURVEY_ITEMS_PARENT:
            survey_id += 1
            surveys.append(
                {
                    "survey_response_id": f"srv_{survey_id:05d}",
                    "respondent_role": "parent",
                    "student_id": sid,
                    "item_id": item_id,
                    "answer_code": rng.choice(answers),
                    "week_no": 0,
                }
            )

        # optional weekly mini survey
        for w in range(1, weeks + 1):
            if rng.random() < 0.5:
                survey_id += 1
                surveys.append(
                    {
                        "survey_response_id": f"srv_{survey_id:05d}",
                        "respondent_role": "student",
                        "student_id": sid,
                        "item_id": "q_week_dropout_point",
                        "answer_code": rng.choice(
                            ["start", "middle", "phone", "anxiety", "night"]
                        ),
                        "week_no": w,
                    }
                )

        week_notify = Counter()
        week_actions_done = Counter()
        week_actions_missed = Counter()
        week_top_cat: dict[int, Counter] = defaultdict(Counter)
        week_risk_acc: dict[int, list[float]] = defaultdict(list)

        n_sess = sessions_per_student
        if segment == "baslayamayan":
            n_sess = max(2, sessions_per_student // 2)

        for s_idx in range(n_sess):
            session_id += 1
            ses = f"ses_{session_id:05d}"
            week_no = (s_idx % weeks) + 1
            subject = rng.choice(SUBJECTS)

            # start hour by segment
            if segment == "geceye_kayan":
                start_hour = rng.choice([21, 22, 23, 0, 1, 14])
            elif segment == "baslayamayan":
                start_hour = rng.randint(9, 20)
            else:
                start_hour = rng.randint(8, 22)

            planned = rng.choice([25, 30, 40, 45, 50])

            if segment == "baslayamayan":
                completed = 0 if rng.random() < 0.7 else rng.randint(0, 10)
                abandoned = True
            elif segment == "yarida_birakan":
                completed = int(planned * rng.uniform(0.15, 0.55))
                abandoned = completed < planned
            elif segment == "kaygiyla_erteleyen" and week_no == weeks:
                # last week = exam pressure proxy
                completed = 0 if rng.random() < 0.5 else int(planned * rng.uniform(0.2, 0.6))
                abandoned = completed < planned * 0.9
            else:
                completed = int(planned * rng.uniform(0.6, 1.0))
                abandoned = completed < planned * 0.85

            sessions.append(
                {
                    "session_id": ses,
                    "student_id": sid,
                    "subject": subject,
                    "planned_min": planned,
                    "completed_min": completed,
                    "start_hour": start_hour,
                    "abandoned": str(abandoned).lower(),
                    "week_no": week_no,
                }
            )

            if completed >= planned * 0.85:
                week_actions_done[week_no] += 1
            else:
                week_actions_missed[week_no] += 1

            week_risk_acc[week_no].append(risk + rng.uniform(-0.05, 0.05))

            # phone events inside focus block
            n_phone = 0
            if segment == "telefonla_dagilan":
                n_phone = rng.randint(1, 3)
            elif segment == "baslayamayan":
                n_phone = 1 if rng.random() < 0.4 else 0
            else:
                n_phone = 1 if rng.random() < 0.55 else 0

            for _ in range(n_phone):
                phone_id += 1
                if segment == "telefonla_dagilan":
                    cat = rng.choices(
                        ["social", "game", "video", "education", "communication", "other"],
                        weights=[0.35, 0.25, 0.2, 0.05, 0.05, 0.1],
                        k=1,
                    )[0]
                    duration = rng.randint(180, 1200)
                    if rng.random() < 0.55:
                        duration = rng.randint(600, 1500)
                else:
                    cat = rng.choices(
                        ["social", "game", "video", "education", "communication", "other"],
                        weights=[0.2, 0.1, 0.15, 0.3, 0.15, 0.1],
                        k=1,
                    )[0]
                    duration = rng.randint(30, 500)

                dist = is_distractor(cat, rng)
                notify = bool(
                    dist and duration >= NOTIFY_THRESHOLD_SEC
                )
                phones.append(
                    {
                        "event_id": f"ph_{phone_id:05d}",
                        "session_id": ses,
                        "student_id": sid,
                        "app_category": cat,
                        "duration_sec": duration,
                        "in_focus_block": "true",
                        "is_distractor": str(dist).lower(),
                        "notify_flag": str(notify).lower(),
                        "week_no": week_no,
                    }
                )
                if notify:
                    week_notify[week_no] += 1
                    week_top_cat[week_no][cat] += 1

        # parent intent samples (1 per student)
        intent_id += 1
        intents.append(
            {
                "intent_id": f"int_{intent_id:04d}",
                "parent_id": pid,
                "student_id": sid,
                "raw_text_tr": rng.choice(INTENT_RAW),
                "softened_text_tr": rng.choice(INTENT_SOFT),
            }
        )

        for w in range(1, weeks + 1):
            risks = week_risk_acc.get(w) or [risk]
            top = ""
            if week_top_cat[w]:
                top = week_top_cat[w].most_common(1)[0][0]
            weekly.append(
                {
                    "student_id": sid,
                    "week_no": w,
                    "risk_avg": round(sum(risks) / len(risks), 3),
                    "actions_done": week_actions_done[w],
                    "actions_missed": week_actions_missed[w],
                    "distraction_count": week_notify[w],
                    "top_distractor_category": top,
                }
            )

    # write files
    write_csv(
        out / "students.csv",
        ["student_id", "exam_track", "age_band", "chronotype", "segment_label", "risk_prior"],
        students,
    )
    write_csv(
        out / "parent_profiles.csv",
        ["parent_id", "student_id", "free_text_tr", "tone_hint"],
        parents,
    )
    write_csv(
        out / "surveys.csv",
        [
            "survey_response_id",
            "respondent_role",
            "student_id",
            "item_id",
            "answer_code",
            "week_no",
        ],
        surveys,
    )
    write_csv(
        out / "focus_sessions.csv",
        [
            "session_id",
            "student_id",
            "subject",
            "planned_min",
            "completed_min",
            "start_hour",
            "abandoned",
            "week_no",
        ],
        sessions,
    )
    write_csv(
        out / "phone_events.csv",
        [
            "event_id",
            "session_id",
            "student_id",
            "app_category",
            "duration_sec",
            "in_focus_block",
            "is_distractor",
            "notify_flag",
            "week_no",
        ],
        phones,
    )
    write_csv(
        out / "weekly_metrics.csv",
        [
            "student_id",
            "week_no",
            "risk_avg",
            "actions_done",
            "actions_missed",
            "distraction_count",
            "top_distractor_category",
        ],
        weekly,
    )
    write_csv(
        out / "parent_intents.csv",
        ["intent_id", "parent_id", "student_id", "raw_text_tr", "softened_text_tr"],
        intents,
    )

    seg_counts = Counter(s["segment_label"] for s in students)
    notify_true = sum(1 for p in phones if p["notify_flag"] == "true")

    meta = {
        "schema_version": SCHEMA_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "n_students": n,
        "weeks": weeks,
        "sessions_per_student_target": sessions_per_student,
        "notify_threshold_sec": NOTIFY_THRESHOLD_SEC,
        "segment_priors": SEGMENT_PRIORS,
        "segment_counts": dict(seg_counts),
        "row_counts": {
            "students": len(students),
            "parent_profiles": len(parents),
            "surveys": len(surveys),
            "focus_sessions": len(sessions),
            "phone_events": len(phones),
            "weekly_metrics": len(weekly),
            "parent_intents": len(intents),
        },
        "notify_flag_true_count": notify_true,
        "disclaimer": (
            "Synthetic data only. No real PII. Not a field pilot. "
            "Do not treat metrics as real LGS/YKS or retention evidence."
        ),
    }
    (out / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return meta


def main() -> None:
    p = argparse.ArgumentParser(description="AI Personal Coach synthetic data (K4)")
    p.add_argument("--n", type=int, default=100, help="number of students")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", type=str, default="./output")
    p.add_argument("--weeks", type=int, default=4)
    p.add_argument("--sessions-per-student", type=int, default=8)
    args = p.parse_args()

    meta = generate(
        n=args.n,
        seed=args.seed,
        weeks=args.weeks,
        sessions_per_student=args.sessions_per_student,
        out=Path(args.out),
    )
    print(json.dumps(meta["row_counts"], indent=2))
    print(f"notify_flag_true_count={meta['notify_flag_true_count']}")
    print(f"segment_counts={meta['segment_counts']}")
    print(f"wrote → {args.out}")


if __name__ == "__main__":
    main()
