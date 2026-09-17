#!/usr/bin/env python3
"""
AI Personal Coach — End-to-End Proof of Concept (PoC) Pipeline (K5)
With Explainable AI (SHAP) & LLM Personalization Layer

Architectural Flow:
  Student Behavioral Data
          ↓
  Risk Prediction Layer (LightGBM baseline model)
          ↓
  Risk Score (0.00 - 1.00) & Operational Risk Level
          ↓
  Explainable AI (SHAP) Feature Contribution Layer
          ↓
  Behavioral Segmentation Layer (5 student personas)
          ↓
  Deterministic Rule Engine (LLM-independent policy)
          ↓
  LLM Personalization Layer (Tone-Calibrated Parent Message)

Usage:
  python poc_pipeline.py --all
  python poc_pipeline.py --student STU_002
  python poc_pipeline.py --risk-threshold 0.40
  python poc_pipeline.py --json
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple
import warnings
import joblib
import numpy as np
import pandas as pd
import shap

warnings.filterwarnings("ignore", category=UserWarning)

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

FEATURE_TR_NAMES = {
    "vle_total_clicks": "Platform Etkileşimi (VLE Tıklama)",
    "avg_focus_duration_mins": "Ortalama Odaklanma Süresi",
    "phone_distraction_10min_count": "Odak Bloğu Telefon Bölünmesi",
    "parent_report_open_rate": "Haftalık Veli Raporu İnceleme",
    "assessment_avg_score": "Ödev ve Deneme Başarısı",
    "late_submission_ratio": "Geç Ödev Teslim Oranı",
    "anxiety_survey_score": "Sınav Kaygısı Anketi",
    "night_study_ratio": "Gece Çalışma Oranı (>22:00)",
}

SEGMENT_NAMES = {
    "baslayamayan": "Başlayamayan (Cannot Start)",
    "telefonla_dagilan": "Telefonla Dağılan (Phone Distracted)",
    "geceye_kayan": "Geceye Kayan (Night Shifted)",
    "yarida_birakan": "Yarıda Bırakan (Abandons Midway)",
    "kaygiyla_erteleyen": "Kaygıyla Erteleyen (Anxiety Driven)",
}


class RiskLayer:
    """Predicts churn/dropout risk score using serialized LightGBM model."""

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
        elif risk_score <= 0.40:
            risk_level = "Medium-Low (Orta-Düşük)"
        elif risk_score <= 0.65:
            risk_level = "High (Yüksek)"
        else:
            risk_level = "Critical (Kritik)"

        return risk_score, risk_level


class ShapExplainerLayer:
    """Computes exact mathematical local explanations for each student prediction."""

    def __init__(self, model):
        base_dir = Path(__file__).resolve().parent
        shap_path = base_dir / "data-research" / "modeling" / "shap_explainer.joblib"

        if shap_path.exists():
            try:
                self.explainer = joblib.load(shap_path)
            except Exception:
                self.explainer = shap.TreeExplainer(model)
        else:
            self.explainer = shap.TreeExplainer(model)

    def explain_student(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        feat_vals = {col: [float(student_data[col])] for col in FEATURE_COLS}
        X_df = pd.DataFrame(feat_vals)
        raw_shap = self.explainer.shap_values(X_df)

        if isinstance(raw_shap, list):
            vals = raw_shap[1][0]
        elif len(raw_shap.shape) == 2:
            vals = raw_shap[0]
        else:
            vals = raw_shap

        contributions = []
        for col, val in zip(FEATURE_COLS, vals):
            contributions.append({
                "feature": col,
                "feature_tr": FEATURE_TR_NAMES.get(col, col),
                "shap_value": round(float(val), 4),
                "student_value": student_data[col],
            })

        # Risk drivers (positive SHAP pushes risk UP)
        risk_drivers = [c for c in contributions if c["shap_value"] > 0]
        risk_drivers.sort(key=lambda x: x["shap_value"], reverse=True)

        # Protective factors (negative SHAP pulls risk DOWN)
        protective_factors = [c for c in contributions if c["shap_value"] < 0]
        protective_factors.sort(key=lambda x: x["shap_value"])

        return {
            "all_contributions": contributions,
            "top_risk_drivers": risk_drivers[:3],
            "top_protective_factors": protective_factors[:2],
        }


class SegmentationLayer:
    """Verifies or assigns student persona based on multi-dimensional behavioral metrics."""

    @staticmethod
    def identify_segment(student: Dict[str, Any]) -> str:
        if "sub_segment" in student and student["sub_segment"] in SEGMENT_NAMES:
            return student["sub_segment"]

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

    def __init__(self, risk_threshold: float = 0.40):
        # Default 0.40 reflects the tuned operational threshold (Recall ~82%)
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
            primary_reason = f"Risk skoru ({risk_score:.2f}) ve {inactivity_days} gündür çalışma olmaması"

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
                primary_reason = "Çalışma saatlerinin gece 22:00 sonrasına yoğunlaşması ve ritim kayması"

        # Rule 5: Operational Risk Threshold Catch
        if not trigger and risk_score >= self.risk_threshold:
            trigger = True
            matched_rules.append("RULE_OPERATIONAL_RISK_CATCH")
            primary_reason = f"Erken churn riski eşiği ({risk_score:.2f} >= {self.risk_threshold}) aşıldı"

        # Timing window check: Parent peak attention is 20:00 - 23:00
        hour = 20
        try:
            hour = int(last_active_time.split(":")[0])
        except Exception:
            pass
        in_peak_window = (20 <= hour <= 23)

        # Escalation policy: Risk >= 0.65 and unanswered notifications >= 3
        escalate_to_human = (risk_score >= 0.65 and unanswered_notifs >= 3)

        return {
            "trigger": trigger,
            "primary_reason": primary_reason if trigger else "Öğrenci aktif ve risk eşiği altında",
            "matched_rules": matched_rules,
            "in_peak_window": in_peak_window,
            "delivery_time_recommendation": "20:30 (Veli Akşam Pik Saati)" if in_peak_window else "Bir sonraki 20:00 pik penceresi",
            "escalate_to_human": escalate_to_human,
        }


class LLMPersonalizer:
    """
    Hybrid LLM & Intelligent Pedagogical Message Personalizer.
    Incorporates SHAP mathematical drivers and parent tone calibration.
    """

    SYSTEM_PROMPT = """Sen AI Personal Coach platformunun Pedagojik Veli İletişim Koçusun.
Görevin: Risk tespit edilen LGS/YKS öğrencisinin velisine kısa (maks 140 kelime), yapıcı, yargılayıcı olmayan
ve somut tek bir mikro-aksiyon öneren şefkatli bir mesaj oluşturmaktır.
Asla öğrenciyi şikayet etme, veliyi suçlama. Hedef: Veli-öğrenci çatışmasını önlemek ve öğrenciyi küçük bir adımla masaya döndürmektir."""

    @classmethod
    def generate_prompt(
        cls,
        student_name: str,
        segment: str,
        exam_type: str,
        grade: str,
        risk_score: float,
        shap_drivers: List[Dict[str, Any]],
        tone: str,
    ) -> str:
        drivers_text = ", ".join([f"{d['feature_tr']} (Etki: +{d['shap_value']:.2f})" for d in shap_drivers])
        return f"""
Öğrenci: {student_name} ({exam_type}, Sınıf: {grade})
Risk Skoru: {risk_score:.2f}
Davranış Segmenti: {SEGMENT_NAMES.get(segment, segment)}
Yapay Zeka Risk Tetikleyicileri (SHAP): {drivers_text}
Veli İletişim Tercihi: {tone}

Bu verileri kullanarak veliye WhatsApp/SMS üzerinden gönderilecek samimi ve çözüm odaklı koçluk mesajı üret.
"""

    @classmethod
    def synthesize_message(
        cls,
        student_name: str,
        segment: str,
        rule_result: Dict[str, Any],
        shap_drivers: List[Dict[str, Any]],
        tone_pref: str = "empathetic",
    ) -> str:
        if not rule_result["trigger"]:
            return "Bildirim kuralı tetiklenmedi (Öğrencinin çalışma dinamiği olağan akışında devam ediyor)."

        # Try live OpenAI API if key exists
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                import urllib.request
                prompt = cls.generate_prompt(
                    student_name=student_name,
                    segment=segment,
                    exam_type=rule_result.get("exam_type", "Sınav"),
                    grade=rule_result.get("grade", "Hazırlık"),
                    risk_score=rule_result.get("risk_score", 0.5),
                    shap_drivers=shap_drivers,
                    tone=tone_pref,
                )
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                }
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": cls.SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.6,
                    "max_tokens": 160,
                }
                req = urllib.request.Request(
                    "https://api.openai.com/v1/chat/completions",
                    data=json.dumps(payload).encode("utf-8"),
                    headers=headers,
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    ai_msg = res_data["choices"][0]["message"]["content"].strip()
                    return ai_msg
            except Exception:
                pass  # Fallback gracefully to intelligent synthesizer

        # Intelligent Contextual Synthesizer (incorporating SHAP driver and tone)
        driver_context = ""
        if shap_drivers:
            top_driver = shap_drivers[0]["feature_tr"]
            driver_context = f"AI analizimizde özellikle '{top_driver}' sinyali öne çıkıyor."

        tone_intro = {
            "empathetic": f"Merhaba, {student_name}'in çalışma sürecinde bazen yorulması ve zorlanması çok doğal.",
            "structured": f"Merhaba, {student_name}'in haftalık çalışma ritminde küçük bir optimizasyon fırsatı belirledik.",
            "gentle": f"Merhaba, {student_name} için bu sınav maratonunun getirdiği hassasiyeti ve baskıyı anlıyoruz.",
            "informative": f"Merhaba, {student_name}'in son dönem platform verileri üzerinde bir durum güncellemesi hazırladık.",
        }.get(tone_pref, f"Merhaba, {student_name}'in çalışma akışını desteklemek istiyoruz.")

        segment_action = {
            "baslayamayan": (
                "Büyük hedefler ders başlatma stresini artırabilir. "
                "Bugün için 'Sadece 15 dakikalık tek bir ısınma seti çözelim, bitince mola senin' teklifi "
                "masaya oturma ataletini kıracaktır. [Adım Adım Başarı]"
            ),
            "telefonla_dagilan": (
                "Odak bloğunda bildirimlerin dikkatini böldüğünü gözlemliyoruz. "
                "Yargılamadan destek olmak için: 'Bugünkü 20 dakikalık odak bloğunda telefonu birlikte salona bırakalım mı?' "
                "önerisi odak süresini hemen toparlayacaktır. [Odaklanma Desteği]"
            ),
            "geceye_kayan": (
                "Çalışmaların gece geç saatlere kalması uyku düzenini ve gündüz okul verimini etkileyebilir. "
                "Yarın için ilk çalışma bloğunu akşam 20:30'a planlamasına yardımcı olarak biyolojik saatini dengeleyebilirsiniz. [Ritim Düzenleme]"
            ),
            "yarida_birakan": (
                "Derslere istekli başlıyor fakat oturumu sonuna kadar getirmekte zorlanıyor. "
                "Blokları 40 dakika yerine 20 dakikalık iki mini parçaya bölmek motivasyonunu yüksek tutacaktır. [Mikro Hedef]"
            ),
            "kaygiyla_erteleyen": (
                "Sınav baskısı ve hata yapma endişesi bazen erteleme davranışını tetikleyebilir. "
                "Ona 'Sonuç ne olursa olsun çaban bizim için değerli' güvenini hissettirip, süre tutmadan rahat bir deneme seti çözmesini teklif edebilirsiniz. [Empatik Destek]"
            ),
        }.get(segment, "Bugün 20 dakikalık kısa bir çalışma bloğu ile yeniden başlamayı deneyebilirsiniz.")

        message = f"{tone_intro} {driver_context} {segment_action}"

        if rule_result.get("escalate_to_human"):
            message += (
                "\n\n[Rehberlik Eskalasyonu]: Veli iletişiminde 3 gündür yanıt alınamadı ve risk skoru yüksek. "
                "AI sistemi, veliye 15 dakikalık ücretsiz birebir Rehberlik & Koçluk randevusu daveti yönlendirdi."
            )

        return message

    @classmethod
    def generate_message(
        cls,
        student_name: str,
        segment: str,
        rule_result: Dict[str, Any],
        shap_drivers: Optional[List[Dict[str, Any]]] = None,
        tone_pref: str = "empathetic",
    ) -> str:
        return cls.synthesize_message(
            student_name=student_name,
            segment=segment,
            rule_result=rule_result,
            shap_drivers=shap_drivers or [],
            tone_pref=tone_pref,
        )


# Backward compatibility alias
MessageLayer = LLMPersonalizer


class PersonalCoachPoCPipeline:
    """Master Pipeline orchestrating Risk, SHAP, Segmentation, Rules, and Message Layers."""

    def __init__(self, risk_threshold: float = 0.40):
        self.risk_layer = RiskLayer()
        self.shap_layer = ShapExplainerLayer(self.risk_layer.model)
        self.segment_layer = SegmentationLayer()
        self.rule_engine = RuleEngine(risk_threshold=risk_threshold)
        self.personalizer = LLMPersonalizer()

    def process_student(self, student: Dict[str, Any]) -> Dict[str, Any]:
        student_id = student.get("student_id", "UNKNOWN")
        name = student.get("name", "Öğrenci")
        tone_pref = student.get("parent_tone_preference", "empathetic")

        # Layer 1: Risk Layer
        risk_score, risk_level = self.risk_layer.predict_risk(student)

        # Layer 2: SHAP Explainability Layer
        shap_explanation = self.shap_layer.explain_student(student)

        # Layer 3: Segmentation Layer
        segment_code = self.segment_layer.identify_segment(student)
        segment_display = SEGMENT_NAMES.get(segment_code, segment_code)

        # Layer 4: Deterministic Rule Engine
        rule_result = self.rule_engine.evaluate(student, risk_score, segment_code)
        rule_result["exam_type"] = student.get("exam_type", "N/A")
        rule_result["grade"] = student.get("grade", "N/A")
        rule_result["risk_score"] = risk_score

        # Layer 5: Message Layer (Incorporating SHAP & Tone)
        parent_message = self.personalizer.synthesize_message(
            student_name=name,
            segment=segment_code,
            rule_result=rule_result,
            shap_drivers=shap_explanation["top_risk_drivers"],
            tone_pref=tone_pref,
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
            "shap_explanation": shap_explanation,
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

    shap_info = res.get("shap_explanation", {})
    drivers = shap_info.get("top_risk_drivers", [])
    drivers_str = " | ".join([f"{d['feature_tr']} (+{d['shap_value']:.2f})" for d in drivers[:2]]) if drivers else "Yok"

    card = f"""
{'='*78}
Öğrenci ID     : {res['student_id']} ({res['name']}) | Sınav: {res['exam_type']} (Sınıf {res['grade']})
Risk Skoru     : {res['risk_score']:.4f} [{res['risk_level']}]
Segment        : {res['segment_display']}
SHAP Faktörler : {drivers_str}
Kural Kararı   : {trigger_badge}
Tetik Gerekçesi: {res['primary_reason']}
Teslim Zamanı  : {res['delivery_window']}
Eskalasyon     : {escalate_badge}
{'-'*78}
Kişiselleştirilmiş Veli Koçluk Mesajı:
"{res['parent_message']}"
{'='*78}
"""
    return card


def main():
    parser = argparse.ArgumentParser(description="AI Personal Coach — End-to-End PoC Pipeline CLI with XAI & LLM")
    parser.add_argument("--all", action="store_true", help="Process all students in test fixture")
    parser.add_argument("--student", type=str, default=None, help="Process a specific student ID (e.g. STU_002)")
    parser.add_argument("--risk-threshold", type=float, default=0.40, help="Risk threshold for rule engine trigger (Default 0.40 for operational retention)")
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
            print(" AI PERSONAL COACH — END-TO-END POC PIPELINE RUNNER (K5 + XAI + LLM)")
            print(" Model: LightGBM Baseline | Eşik: 0.40 (Recall %82) | Explainable AI (SHAP)")
            print("="*80)

            table_rows = []
            for r in results:
                drivers = r.get("shap_explanation", {}).get("top_risk_drivers", [])
                top_d = drivers[0]["feature_tr"][:16] if drivers else "-"
                table_rows.append({
                    "ID": r["student_id"],
                    "İsim": r["name"],
                    "Risk": f"{r['risk_score']:.2f}",
                    "Seviye": r["risk_level"].split()[0],
                    "Segment": r["segment_code"][:13],
                    "Baskın Risk Sinyali (SHAP)": top_d,
                    "Tetik": "TRUE" if r["trigger"] else "FALSE",
                    "Eskalasyon": "EVET" if r["escalate_to_human"] else "-",
                })
            df_summary = pd.DataFrame(table_rows)
            print(df_summary.to_string(index=False))

            print("\n" + "="*80)
            print(" DETAYLI ÖĞRENCİ MÜDAHALE VE XAI KARTLARI")
            print("="*80)
            for r in results:
                print(format_card(r))


if __name__ == "__main__":
    main()
