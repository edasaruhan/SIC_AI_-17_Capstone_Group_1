#!/usr/bin/env python3
"""
AI Personal Coach — End-to-End Proof of Concept (PoC) Pipeline (K5)

Architectural Flow:
  Student Data (Features)
          ↓
  Risk Prediction Layer (LightGBM baseline model)
          ↓
  Risk Score (0.00 - 1.00) & Risk Level
          ↓
  Behavioral Segmentation Layer (5 student personas)
          ↓
  Deterministic Rule Engine (LLM-independent policy)
          ↓
  Personalized Parent Coaching Message (Constructive Nudge)

Usage:
  python poc_pipeline.py --all
  python poc_pipeline.py --student STU_002
  python poc_pipeline.py --json
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple
import joblib
import numpy as np
import pandas as pd

# Ensure UTF-8 stdout on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


FEATURE_COLS = [
    "vle_total_clicks",
    "avg_focus_duration_mins",
    "phone_distraction_10min_count",
    "parent_report_open_rate",
    "assessment_avg_score",
    "late_submission_ratio",
    "anxiety_survey_score",
    "night_study_ratio",
]

SEGMENT_NAMES = {
    "baslayamayan": "Başlayamayan (Cannot Start)",
    "telefonla_dagilan": "Telefonla Dağılan (Phone Distracted)",
    "geceye_kayan": "Geceye Kayan (Night Shifted)",
    "yarida_birakan": "Yarıda Bırakan (Abandons Midway)",
    "kaygiyla_erteleyen": "Kaygıyla Erteleyen (Anxiety Driven)",
}


class RiskLayer:
    """Predicts churn/dropout risk score using serialized LightGBM or Logistic baseline."""

    def __init__(self, model_path: Optional[Path] = None):
        base_dir = Path(__file__).resolve().parent
        default_lgb = base_dir / "data-research" / "modeling" / "lightgbm_model.joblib"
        default_lr = base_dir / "data-research" / "modeling" / "logistic_model.joblib"

        self.model = None
        self.model_name = "None"

        if model_path and model_path.exists():
            self.model = joblib.load(model_path)
            self.model_name = model_path.stem
        elif default_lgb.exists():
            self.model = joblib.load(default_lgb)
            self.model_name = "LightGBM Classifier"
        elif default_lr.exists():
            self.model = joblib.load(default_lr)
            self.model_name = "Logistic Regression"
        else:
            print("[!] Warning: No pre-trained model found. Training on the fly...")
            self._train_fallback(base_dir)

    def _train_fallback(self, base_dir: Path):
        data_csv = base_dir / "data-research" / "oulad_synthetic_processed.csv"
        if not data_csv.exists():
            raise FileNotFoundError(f"Cannot find dataset at {data_csv}")
        df = pd.read_csv(data_csv)
        X = df[FEATURE_COLS]
        y = df["churn_90d"]
        import lightgbm as lgb
        self.model = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42, verbose=-1)
        self.model.fit(X, y)
        self.model_name = "LightGBM (Trained on the fly)"

    def predict_risk(self, student_data: Dict[str, Any]) -> Tuple[float, str]:
        feat_vals = {col: [float(student_data[col])] for col in FEATURE_COLS}
        X_df = pd.DataFrame(feat_vals)
        prob = float(self.model.predict_proba(X_df)[0, 1])
        risk_score = round(prob, 4)

        if risk_score <= 0.25:
            risk_level = "Low (Düşük)"
        elif risk_score <= 0.50:
            risk_level = "Medium (Orta)"
        elif risk_score <= 0.75:
            risk_level = "High (Yüksek)"
        else:
            risk_level = "Critical (Kritik)"

        return risk_score, risk_level


class SegmentationLayer:
    """Verifies or assigns student persona based on multi-dimensional behavioral metrics."""

    @staticmethod
    def identify_segment(student: Dict[str, Any]) -> str:
        # If pre-assigned in fixture and valid, respect it
        if "sub_segment" in student and student["sub_segment"] in SEGMENT_NAMES:
            return student["sub_segment"]

        # Deterministic heuristic classifier
        phone_count = student.get("phone_distraction_10min_count", 0)
        night_ratio = student.get("night_study_ratio", 0.0)
        anxiety = student.get("anxiety_survey_score", 0.0)
        clicks = student.get("vle_total_clicks", 0)
        avg_focus = student.get("avg_focus_duration_mins", 0.0)

        if phone_count >= 4:
            return "telefonla_dagilan"
        elif night_ratio >= 0.65:
            return "geceye_kayan"
        elif anxiety >= 7.5:
            return "kaygiyla_erteleyen"
        elif clicks < 35 and avg_focus < 15.0:
            return "baslayamayan"
        else:
            return "yarida_birakan"


class RuleEngine:
    """
    Deterministic rule engine independent of LLM.
    Evaluates trigger conditions, parent peak timing, frequency capping, and escalation.
    """

    def __init__(self, risk_threshold: float = 0.50):
        self.risk_threshold = risk_threshold

    def evaluate(
        self,
        student: Dict[str, Any],
        risk_score: float,
        segment: str,
    ) -> Dict[str, Any]:
        inactivity_days = student.get("inactivity_days", 0)
        phone_distractions = student.get("phone_distraction_10min_count", 0)
        anxiety_score = student.get("anxiety_survey_score", 0.0)
        last_active_time = student.get("last_active_time", "20:30")
        unanswered_notifs = student.get("unanswered_notif_count", 0)

        trigger = False
        primary_reason = ""
        matched_rules = []

        # Rule 1: High risk combined with inactivity
        if risk_score >= self.risk_threshold and inactivity_days >= 2:
            trigger = True
            matched_rules.append("RULE_HIGH_RISK_INACTIVITY")
            primary_reason = f"Yüksek risk skoru ({risk_score:.2f}) ve {inactivity_days} gündür çalışma olmaması"

        # Rule 2: Phone distraction threshold during focus block
        if phone_distractions >= 4:
            trigger = True
            matched_rules.append("RULE_PHONE_DISTRACTION_BURST")
            if not primary_reason:
                primary_reason = f"Odak bloklarında {phone_distractions} kez 10 dk+ telefon kullanım uyarısı"

        # Rule 3: Anxiety-driven severe procrastination
        if anxiety_score >= 8.0 and inactivity_days >= 3:
            trigger = True
            matched_rules.append("RULE_ANXIETY_FREEZE")
            if not primary_reason:
                primary_reason = f"Yüksek sınav kaygısı ({anxiety_score}/10) nedeniyle ders başlatamama durumu"

        # Rule 4: Total night shift disruption
        if student.get("night_study_ratio", 0.0) >= 0.75 and inactivity_days >= 1:
            trigger = True
            matched_rules.append("RULE_NIGHT_SHIFT_DISRUPTION")
            if not primary_reason:
                primary_reason = "Çalışma saatlerinin gece 22:00 sonrasına yoğunlaşması ve biyolojik ritim kayması"

        # Fallback for moderate risk
        if not trigger and risk_score >= 0.55:
            trigger = True
            matched_rules.append("RULE_MODERATE_RISK_CHECK")
            primary_reason = f"Orta-yüksek churn riski ({risk_score:.2f}) tespit edildi"

        # Timing window check: Parent peak attention is 20:00 - 23:00
        hour = 20
        try:
            hour = int(last_active_time.split(":")[0])
        except Exception:
            pass
        in_peak_window = (20 <= hour <= 23)

        # Escalation policy: Risk >= 0.75 and unanswered notifications >= 3
        escalate_to_human = (risk_score >= 0.70 and unanswered_notifs >= 3)

        return {
            "trigger": trigger,
            "primary_reason": primary_reason if trigger else "Öğrenci aktif ve risk eşiği altında",
            "matched_rules": matched_rules,
            "in_peak_window": in_peak_window,
            "delivery_time_recommendation": "20:30 (Veli Akşam Pik Saati)" if in_peak_window else "Bir sonraki 20:00 pik penceresi",
            "escalate_to_human": escalate_to_human,
        }


class MessageLayer:
    """
    Constructive, empathetic parent coaching message generator.
    Guarantees non-blaming, action-oriented tone without relying on opaque LLM logic.
    """

    TEMPLATES = {
        "baslayamayan": (
            "Merhaba, {name}'in ders masasına oturmakta biraz zorlandığını fark ettik. "
            "Bu dönemde ilk adımı atmak en yorucu kısım olabilir. "
            "Bugün büyük bir hedef koymak yerine, sadece 15 dakikalık tek bir 'ısınma soru seti' ile başlamasını "
            "önerebilirsiniz. Bitince küçük bir mola onun hakkı! [Adım Adım Başarı]"
        ),
        "telefonla_dagilan": (
            "Merhaba, {name}'in son çalışma bloklarında odak süresinde bölünmeler gözlemledik. "
            "Eleştirmeden destek olmak için: 'Bugünkü 20 dakikalık odak bloğunda telefonu birlikte salona bırakalım mı?' "
            "teklifi odaklanmayı belirgin şekilde artırabilir. Birlikte başarabilirsiniz! [Odaklanma Desteği]"
        ),
        "geceye_kayan": (
            "Merhaba, {name}'in çalışma saatlerinin gece geç saatlere kaydığını tespit ettik. "
            "Gece çalışmaları uyku kalitesini ve gündüz okul/dershane verimini düşürebilir. "
            "Yarın için ilk çalışma bloğunu akşam 20:30'a çekerek daha zinde bir rutin oluşturmasına yardımcı olabilirsiniz. [Ritim Düzenleme]"
        ),
        "yarida_birakan": (
            "Merhaba, {name} derslere istekli başlıyor ancak blokları sonuna kadar sürdürmekte enerji kaybı yaşıyor. "
            "Oturumları 40 dakika yerine 20 dakikalık iki küçük parçaya bölmek motivasyonunu taze tutacaktır. "
            "Küçük adımlarla büyük ilerleme sağlayabiliriz! [Mikro Hedef]"
        ),
        "kaygiyla_erteleyen": (
            "Merhaba, {name}'in sınav hazırlığında yoğun bir sorumluluk hissi ve kaygı taşıdığını görüyoruz. "
            "Yanlış yapma endişesi bazen başlamayı geciktirebilir. "
            "Ona 'Sonuç ne olursa olsun çaban bizim için değerli' hissini hatırlatıp, süre tutmadan rahat bir deneme seti "
            "çözmesini teklif edebilirsiniz. Sevgi ve sabır en iyi rehberdir. [Empatik Destek]"
        ),
    }

    @classmethod
    def generate_message(
        cls,
        student_name: str,
        segment: str,
        rule_result: Dict[str, Any],
    ) -> str:
        if not rule_result["trigger"]:
            return "Bildirim kuralı tetiklenmedi (Öğrencinin çalışma dinamiği olağan akışında devam ediyor)."

        template = cls.TEMPLATES.get(segment, cls.TEMPLATES["baslayamayan"])
        message = template.format(name=student_name)

        if rule_result.get("escalate_to_human"):
            message += (
                "\n\n[Rehberlik Eskalasyonu]: Veli iletişiminde 3 gündür yanıt alınamadı ve risk skoru yüksek. "
                "AI sistemi, veliye 15 dakikalık ücretsiz birebir Rehberlik & Koçluk randevusu daveti yönlendirdi."
            )

        return message


class PersonalCoachPoCPipeline:
    """Master Pipeline orchestrating the 4 layers."""

    def __init__(self, risk_threshold: float = 0.50):
        self.risk_layer = RiskLayer()
        self.segment_layer = SegmentationLayer()
        self.rule_engine = RuleEngine(risk_threshold=risk_threshold)
        self.message_layer = MessageLayer()

    def process_student(self, student: Dict[str, Any]) -> Dict[str, Any]:
        student_id = student.get("student_id", "UNKNOWN")
        name = student.get("name", "Öğrenci")

        # Layer 1: Risk Layer
        risk_score, risk_level = self.risk_layer.predict_risk(student)

        # Layer 2: Segmentation Layer
        segment_code = self.segment_layer.identify_segment(student)
        segment_display = SEGMENT_NAMES.get(segment_code, segment_code)

        # Layer 3: Rule Engine
        rule_result = self.rule_engine.evaluate(student, risk_score, segment_code)

        # Layer 4: Message Layer
        parent_message = self.message_layer.generate_message(
            student_name=name,
            segment=segment_code,
            rule_result=rule_result,
        )

        return {
            "student_id": student_id,
            "name": name,
            "exam_type": student.get("exam_type", "N/A"),
            "grade": student.get("grade", "N/A"),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "segment_code": segment_code,
            "segment_display": segment_display,
            "trigger": rule_result["trigger"],
            "primary_reason": rule_result["primary_reason"],
            "matched_rules": rule_result["matched_rules"],
            "delivery_window": rule_result["delivery_time_recommendation"],
            "escalate_to_human": rule_result["escalate_to_human"],
            "parent_message": parent_message,
        }

    def process_all_fixtures(self, fixtures_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        if fixtures_path is None:
            base_dir = Path(__file__).resolve().parent
            fixtures_path = base_dir / "data-research" / "fixtures" / "poc_students.json"

        with open(fixtures_path, encoding="utf-8") as f:
            students = json.load(f)

        return [self.process_student(s) for s in students]


def format_card(res: Dict[str, Any]) -> str:
    trigger_badge = "[TETIKLENDI - TRUE]" if res["trigger"] else "[NORMAL - FALSE]"
    escalate_badge = "[EVET - Canli Rehberlik]" if res["escalate_to_human"] else "[YOK]"

    card = f"""
{'='*75}
Öğrenci ID     : {res['student_id']} ({res['name']}) | Sınav: {res['exam_type']} (Sınıf {res['grade']})
Risk Skoru     : {res['risk_score']:.4f} [{res['risk_level']}]
Segment        : {res['segment_display']}
Kural Kararı   : {trigger_badge}
Tetik Gerekçesi: {res['primary_reason']}
Teslim Zamanı  : {res['delivery_window']}
Eskalasyon     : {escalate_badge}
{'-'*75}
Kişiselleştirilmiş Veli Koçluk Mesajı:
"{res['parent_message']}"
{'='*75}
"""
    return card


def main():
    parser = argparse.ArgumentParser(description="AI Personal Coach — End-to-End PoC Pipeline CLI")
    parser.add_argument("--all", action="store_true", help="Process all students in test fixture")
    parser.add_argument("--student", type=str, default=None, help="Process a specific student ID (e.g. STU_002)")
    parser.add_argument("--risk-threshold", type=float, default=0.50, help="Risk threshold for rule engine trigger")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

    args = parser.parse_args()
    pipeline = PersonalCoachPoCPipeline(risk_threshold=args.risk_threshold)

    fixtures_path = Path(__file__).resolve().parent / "data-research" / "fixtures" / "poc_students.json"
    with open(fixtures_path, encoding="utf-8") as f:
        fixtures = json.load(f)

    if args.student:
        target = next((s for s in fixtures if s.get("student_id") == args.student), None)
        if not target:
            print(f"[!] Error: Student ID '{args.student}' not found in fixtures.")
            return
        result = pipeline.process_student(target)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_card(result))
    else:
        results = [pipeline.process_student(s) for s in fixtures]
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print("\n" + "="*80)
            print(" AI PERSONAL COACH — END-TO-END POC PIPELINE RUNNER (K5)")
            print(" Model: LightGBM Baseline | Target: churn_90d | Fixtures: 15 Students")
            print("="*80)

            # Summary table
            table_rows = []
            for r in results:
                table_rows.append({
                    "ID": r["student_id"],
                    "İsim": r["name"],
                    "Risk": f"{r['risk_score']:.2f}",
                    "Seviye": r["risk_level"].split()[0],
                    "Segment": r["segment_code"][:14],
                    "Tetik": "TRUE" if r["trigger"] else "FALSE",
                    "Eskalasyon": "EVET" if r["escalate_to_human"] else "-",
                })
            df_summary = pd.DataFrame(table_rows)
            print(df_summary.to_string(index=False))

            print("\n" + "="*80)
            print(" DETAYLI ÖĞRENCİ MÜDAHALE KARTLARI")
            print("="*80)
            for r in results:
                print(format_card(r))


if __name__ == "__main__":
    main()
