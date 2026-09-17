#!/usr/bin/env python3
"""
AI Personal Coach — Streamlit Live PoC & XAI Decision Support Dashboard
Interactive Web Application for Capstone Presentation and Demonstration.

Run:
  streamlit run app.py
"""

from __future__ import annotations

import json
from pathlib import Path
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from poc_pipeline import (
    FEATURE_COLS,
    FEATURE_TR_NAMES,
    PersonalCoachPoCPipeline,
    SEGMENT_NAMES,
)

# Page configuration
st.set_page_config(
    page_title="AI Personal Coach — Live PoC",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for rich aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 18px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .metric-title {
        font-size: 0.85rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    /* Phone Mockup Styling */
    .phone-frame {
        max-width: 380px;
        margin: 0 auto;
        border: 10px solid #2d3748;
        border-radius: 36px;
        padding: 20px;
        background: #1a202c;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        color: #fff;
    }
    .phone-header {
        text-align: center;
        font-size: 0.75rem;
        color: #a0aec0;
        border-bottom: 1px solid #2d3748;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .phone-notch {
        width: 120px;
        height: 16px;
        background: #2d3748;
        border-radius: 0 0 12px 12px;
        margin: -20px auto 14px auto;
    }
    .notif-bubble {
        background: #2b6cb0;
        border-radius: 16px 16px 16px 4px;
        padding: 14px;
        font-size: 0.92rem;
        line-height: 1.45;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .notif-time {
        font-size: 0.7rem;
        color: #cbd5e0;
        text-align: right;
        margin-top: 6px;
    }
    .badge-tag {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_pipeline():
    return PersonalCoachPoCPipeline(risk_threshold=0.40)


@st.cache_data
def load_fixtures():
    fixtures_path = Path(__file__).resolve().parent / "data-research" / "fixtures" / "poc_students.json"
    with open(fixtures_path, encoding="utf-8") as f:
        return json.load(f)


pipeline = load_pipeline()
fixtures = load_fixtures()

# ----------------- SIDEBAR -----------------
st.sidebar.title("🎓 AI Personal Coach")
st.sidebar.caption("Pazarlamada Yapay Zeka · Capstone PoC Demo")

student_options = {f"{s['student_id']} — {s['name']} ({s['exam_type']})": s for s in fixtures}
selected_label = st.sidebar.selectbox("Öğrenci Seçiniz:", list(student_options.keys()))
selected_student = student_options[selected_label]

st.sidebar.divider()
st.sidebar.subheader("⚙️ Karar Motoru Parametreleri")

risk_thresh = st.sidebar.slider(
    "Operasyonel Risk Eşiği (Threshold):",
    min_value=0.20,
    max_value=0.70,
    value=0.40,
    step=0.05,
    help="Varsayılan 0.40 eşiği, churn vakalarının %82'sini yakalamak üzere optimize edilmiştir."
)
pipeline.rule_engine.risk_threshold = risk_thresh

tone_choice = st.sidebar.selectbox(
    "Veli İletişim Tonu Tercihi:",
    ["empathetic", "structured", "gentle", "informative"],
    index=["empathetic", "structured", "gentle", "informative"].index(
        selected_student.get("parent_tone_preference", "empathetic")
    ),
    format_func=lambda x: {
        "empathetic": "Empatik & Destekleyici",
        "structured": "Yapılandırılmış & Hedef Odaklı",
        "gentle": "Nazik & Kaygı Giderici",
        "informative": "Bilgilendirici & Veri Odaklı"
    }.get(x, x)
)
selected_student["parent_tone_preference"] = tone_choice

st.sidebar.info("""
💡 **PoC Özeti:**
- Baseline Model: **LightGBM**
- Açıklanabilir AI: **SHAP TreeExplainer**
- Karar Motoru: **Deterministik Kural Motoru**
- Mesaj Üretimi: **LLM Kişiselleştirme Katmanı**
""")

# ----------------- MAIN TABS -----------------
tab1, tab2, tab3 = st.tabs([
    "📊 Canlı Öğrenci & Karar Analizi",
    "🧪 'What-If' Canlı Senaryo Simülatörü",
    "📈 Baseline Model Kıyaslama & Metrikler",
])

# ----------------- TAB 1: STUDENT DECISION ANALYSIS -----------------
with tab1:
    res = pipeline.process_student(selected_student)
    
    st.markdown(f"### 👤 {res['name']} ({res['student_id']}) — Karar ve Müdahale Paneli")
    st.caption(f"Hedef Sınav: **{res['exam_type']}** | Sınıf: **{res['grade']}** | Tanımlı Segment: **{res['segment_display']}**")

    # Top KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_color = "#e53e3e" if res["risk_score"] >= 0.50 else ("#dd6b20" if res["risk_score"] >= 0.40 else "#38a169")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Churn Risk Skoru</div>
            <div class="metric-value" style="color: {risk_color};">%{res['risk_score']*100:.1f}</div>
            <span class="badge-tag" style="background: rgba(255,255,255,0.1);">{res['risk_level']}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        seg_color = "#805ad5"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Davranışsal Segment</div>
            <div class="metric-value" style="color: {seg_color}; font-size: 1.3rem;">{res['segment_code'].replace('_', ' ').title()}</div>
            <span class="badge-tag" style="background: rgba(128, 90, 213, 0.2); color: #b794f4;">5 Persona Tespiti</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        trig_color = "#e53e3e" if res["trigger"] else "#38a169"
        trig_text = "MÜDAHALE GEREKLİ" if res["trigger"] else "NORMAL AKIŞ"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Kural Motoru Kararı</div>
            <div class="metric-value" style="color: {trig_color}; font-size: 1.3rem;">{trig_text}</div>
            <span class="badge-tag" style="background: rgba(255,255,255,0.1);">{res['delivery_window']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        esc_color = "#d69e2e" if res["escalate_to_human"] else "#718096"
        esc_text = "CANLI KOÇ DAVETİ" if res["escalate_to_human"] else "STANDART AI"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Rehberlik Eskalasyonu</div>
            <div class="metric-value" style="color: {esc_color}; font-size: 1.3rem;">{esc_text}</div>
            <span class="badge-tag" style="background: rgba(255,255,255,0.1);">{'>0.65 Risk & 3+ Cevapsız' if res['escalate_to_human'] else 'Gerek Yok'}</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Split: Left XAI SHAP, Right Phone Preview
    col_left, col_right = st.columns([1.1, 0.9])
    
    with col_left:
        st.subheader("🧠 Açıklanabilir Yapay Zeka (SHAP Analizi)")
        st.caption("Bu öğrencinin risk skorunu hangi faktörlerin artırdığını veya azalttığını matematiksel olarak gösterir:")
        
        shap_data = res["shap_explanation"]["all_contributions"]
        df_shap = pd.DataFrame(shap_data)
        df_shap["Yön"] = df_shap["shap_value"].apply(lambda x: "Riski Artıran (+)" if x > 0 else "Riski Azaltan (-)")
        df_shap["Etki"] = df_shap["shap_value"].abs()
        
        # Altair horizontal bar chart
        chart = alt.Chart(df_shap).mark_bar().encode(
            x=alt.X("shap_value:Q", title="SHAP Etki Değeri (Log-Odds)"),
            y=alt.Y("feature_tr:N", sort="-x", title="Özellik (Feature)"),
            color=alt.Color(
                "Yön:N",
                scale=alt.Scale(domain=["Riski Artıran (+)", "Riski Azaltan (-)"], range=["#e53e3e", "#38a169"])
            ),
            tooltip=["feature_tr", "student_value", "shap_value"]
        ).properties(height=320)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Bullet callouts
        drivers = res["shap_explanation"]["top_risk_drivers"]
        if drivers:
            st.markdown(f"**🔴 En Baskın Risk Faktörü:** `{drivers[0]['feature_tr']}` (Değer: {drivers[0]['student_value']}, Katkı: +{drivers[0]['shap_value']:.2f})")
        protect = res["shap_explanation"]["top_protective_factors"]
        if protect:
            st.markdown(f"**🟢 Koruyucu Faktör:** `{protect[0]['feature_tr']}` (Değer: {protect[0]['student_value']}, Katkı: {protect[0]['shap_value']:.2f})")

    with col_right:
        st.subheader("📱 Veli Mesajı Önizlemesi (Mobile Mockup)")
        st.caption("Kural tetiklendiğinde veliye giden hiper-kişiselleştirilmiş koçluk bildirimi:")
        
        st.markdown(f"""
        <div class="phone-frame">
            <div class="phone-notch"></div>
            <div class="phone-header">WhatsApp · AI Koçluk Asistanı</div>
            <div style="font-size: 0.72rem; color: #a0aec0; text-align: center; margin-bottom: 10px;">
                📅 Bugün · {res['delivery_window']}
            </div>
            <div class="notif-bubble">
                {res['parent_message']}
                <div class="notif-time">20:30 ✓✓</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ----------------- TAB 2: WHAT-IF SIMULATOR -----------------
with tab2:
    st.subheader("🧪 Canlı Senaryo Simülatörü (What-If Simulation)")
    st.caption("Öğrenci davranış parametrelerini değiştirerek riskin ve mesajın nasıl değiştiğini anlık test edin:")
    
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    
    with sim_col1:
        sim_clicks = st.slider("Platform Tıklaması (vle_total_clicks):", 5, 800, int(selected_student["vle_total_clicks"]))
        sim_focus = st.slider("Ortalama Odak Süresi dk (avg_focus_duration_mins):", 5.0, 60.0, float(selected_student["avg_focus_duration_mins"]))
        sim_phone = st.slider("10dk+ Telefon Dağılma Sayısı:", 0, 15, int(selected_student["phone_distraction_10min_count"]))

    with sim_col2:
        sim_open_rate = st.slider("Haftalık Veli Raporu Açılma Oranı:", 0.0, 1.0, float(selected_student["parent_report_open_rate"]))
        sim_score = st.slider("Deneme Sınavı Puanı (assessment_avg_score):", 20.0, 100.0, float(selected_student["assessment_avg_score"]))
        sim_late = st.slider("Geç Teslim Oranı:", 0.0, 1.0, float(selected_student["late_submission_ratio"]))

    with sim_col3:
        sim_anxiety = st.slider("Kaygı Anketi Skoru (1-10):", 1.0, 10.0, float(selected_student["anxiety_survey_score"]))
        sim_night = st.slider("Gece Çalışma Oranı (>22:00):", 0.0, 1.0, float(selected_student["night_study_ratio"]))
        sim_inact = st.slider("Son İnaktivite Gün Sayısı:", 0, 10, int(selected_student["inactivity_days"]))

    # Reconstruct student for simulation
    sim_student = dict(selected_student)
    sim_student.update({
        "vle_total_clicks": sim_clicks,
        "avg_focus_duration_mins": sim_focus,
        "phone_distraction_10min_count": sim_phone,
        "parent_report_open_rate": sim_open_rate,
        "assessment_avg_score": sim_score,
        "late_submission_ratio": sim_late,
        "anxiety_survey_score": sim_anxiety,
        "night_study_ratio": sim_night,
        "inactivity_days": sim_inact,
    })

    sim_res = pipeline.process_student(sim_student)

    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 2])
    with res_col1:
        st.markdown(f"#### Simülasyon Sonucu:")
        st.metric("Tahmin Edilen Risk Skoru", f"%{sim_res['risk_score']*100:.1f}", delta=f"{(sim_res['risk_score'] - selected_student.get('risk_score', sim_res['risk_score']))*100:.1f}%")
        st.markdown(f"**Segment:** `{sim_res['segment_display']}`")
        st.markdown(f"**Kural Kararı:** `{'TETIKLENDI (Bildirim Gönder)' if sim_res['trigger'] else 'NORMAL (Gönderilmedi)'}`")
        st.markdown(f"**Gerekçe:** *{sim_res['primary_reason']}*")
    
    with res_col2:
        st.markdown(f"#### Dinamik Üretilen Veli Mesajı:")
        st.info(sim_res["parent_message"])


# ----------------- TAB 3: BENCHMARK & MODEL PERFORMANCE -----------------
with tab3:
    st.subheader("📈 Baseline Modeller ve Eşik Optimizasyonu (K3 Çıktıları)")
    
    base_dir = Path(__file__).resolve().parent / "data-research" / "modeling"
    results_csv = base_dir / "baseline_results.csv"
    thresh_csv = base_dir / "threshold_tuning_results.csv"

    if results_csv.exists():
        df_base = pd.read_csv(results_csv)
        st.markdown("##### 1. Doğrulanmış Model Kıyaslama Tablosu (N=813 Test Seti)")
        st.dataframe(df_base, use_container_width=True)
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("##### 2. Karışıklık Matrisleri (Confusion Matrices)")
        sub_c1, sub_c2 = st.columns(2)
        cm_lr = base_dir / "confusion_matrix_logistic.png"
        cm_lgb = base_dir / "confusion_matrix_lightgbm.png"
        if cm_lr.exists():
            sub_c1.image(str(cm_lr), caption="Logistic Regression CM")
        if cm_lgb.exists():
            sub_c2.image(str(cm_lgb), caption="LightGBM Classifier CM")

    with col_g2:
        st.markdown("##### 3. Eşik Optimizasyonu (Precision vs Recall)")
        thresh_img = base_dir / "threshold_tuning_plot.png"
        if thresh_img.exists():
            st.image(str(thresh_img), caption="Eşik = 0.40 ile Recall %82'ye Ulaşmaktadır.")

    if thresh_csv.exists():
        st.markdown("##### 4. Eşik Analiz Verileri (Operational Retention Impact)")
        df_th = pd.read_csv(thresh_csv)
        st.dataframe(df_th, use_container_width=True)

    st.markdown("""
    > [!NOTE]
    > **Pazarlama Çıkarımı:** Churn tahmininde yanlış alarm maliyeti (False Positive), kaybedilen müşterinin maliyetinden (False Negative) düşüktür. 
    > Bu sebeple eşiğin 0.50'den 0.40'a çekilmesi yakalanan terk vakalarını %51'den **%82'ye** çıkarmıştır.
    """)
