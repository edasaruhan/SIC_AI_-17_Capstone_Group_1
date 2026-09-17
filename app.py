#!/usr/bin/env python3
"""
AI Personal Coach — Enterprise-Grade PoC & Pedagogical Decision Support Portal
Designed for Teachers, Guidance Counselors, and Educational Leaders.
SIC AI-17 Capstone Project (K1–K5).

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

# ----------------- PAGE SETUP -----------------
st.set_page_config(
    page_title="AI Personal Coach · Rehberlik & Karar Portalı",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- ULTRA-PREMIUM CSS -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #070B14 !important;
        color: #F1F5F9 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0C1222 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    }

    /* Modern Glassmorphic Container */
    .glass-card {
        background: linear-gradient(135deg, rgba(26, 36, 60, 0.55) 0%, rgba(15, 23, 42, 0.75) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 22px;
        backdrop-filter: blur(14px);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 14px 36px -10px rgba(99, 102, 241, 0.15);
    }

    /* KPI Stat Badges */
    .kpi-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-bottom: 6px;
    }
    .kpi-subtext {
        font-size: 0.82rem;
        color: #64748B;
        font-weight: 500;
    }

    /* Custom Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 5px 12px;
        border-radius: 30px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.03em;
    }
    .badge-critical {
        background: rgba(225, 29, 72, 0.18);
        color: #FDA4AF;
        border: 1px solid rgba(225, 29, 72, 0.35);
    }
    .badge-high {
        background: rgba(245, 158, 11, 0.18);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .badge-low {
        background: rgba(16, 185, 129, 0.18);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .badge-segment {
        background: rgba(99, 102, 241, 0.18);
        color: #C7D2FE;
        border: 1px solid rgba(99, 102, 241, 0.35);
    }

    /* Student Banner */
    .student-banner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }
    .student-avatar {
        width: 58px;
        height: 58px;
        border-radius: 16px;
        background: linear-gradient(135deg, #6366F1 0%, #4338CA 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    }

    /* Realistic Phone Mockup */
    .phone-wrapper {
        display: flex;
        justify-content: center;
        padding: 10px 0;
    }
    .phone-device {
        width: 370px;
        background: #0B0E17;
        border: 12px solid #1F2937;
        border-radius: 46px;
        padding: 18px 16px 24px 16px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.85), 0 0 0 1px rgba(255,255,255,0.08);
        position: relative;
    }
    .phone-island {
        width: 110px;
        height: 24px;
        background: #000;
        border-radius: 20px;
        margin: -8px auto 14px auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 10px;
    }
    .phone-status-bar {
        display: flex;
        justify-content: space-between;
        font-size: 0.72rem;
        font-weight: 600;
        color: #94A3B8;
        padding: 0 8px 10px 8px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .chat-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 6px;
        margin-bottom: 14px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .coach-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #10B981, #059669);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    .chat-bubble {
        background: #1E293B;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px 18px 18px 4px;
        padding: 16px;
        color: #F8FAFC;
        font-size: 0.90rem;
        line-height: 1.55;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }
    .chat-timestamp {
        font-size: 0.68rem;
        color: #64748B;
        text-align: right;
        margin-top: 8px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 4px;
    }

    /* Streamlit Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 12px;
        padding: 0 20px;
        background-color: transparent;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.92rem;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.15) !important;
        color: #A5B4FC !important;
        border: 1px solid rgba(99, 102, 241, 0.3) !important;
    }

    /* Custom Progress bar */
    .progress-bar-bg {
        width: 100%;
        height: 10px;
        background: rgba(255,255,255,0.08);
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease-in-out;
    }
</style>
""", unsafe_allow_html=True)


# ----------------- DATA & MODEL LOADERS -----------------
@st.cache_resource
def get_pipeline():
    return PersonalCoachPoCPipeline(risk_threshold=0.40)


@st.cache_data
def get_fixtures():
    fixtures_path = Path(__file__).resolve().parent / "data-research" / "fixtures" / "poc_students.json"
    with open(fixtures_path, encoding="utf-8") as f:
        return json.load(f)


pipeline = get_pipeline()
fixtures = get_fixtures()

# ----------------- TOP NAVBAR -----------------
nav_col1, nav_col2, nav_col3 = st.columns([3, 2, 2])
with nav_col1:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 8px;">
        <span style="font-size: 2.2rem; filter: drop-shadow(0 2px 8px rgba(99,102,241,0.5));">✦</span>
        <div>
            <h2 style="margin: 0; font-size: 1.55rem; font-weight: 800; letter-spacing: -0.02em;">AI Personal Coach</h2>
            <p style="margin: 0; font-size: 0.82rem; color: #94A3B8;">Öğretmen & Rehberlik Karar Destek Portalı (LGS & YKS)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_col2:
    st.markdown("""
    <div style="text-align: right; padding-top: 10px;">
        <span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3);">
            ● Sistem Aktif: LightGBM v1.2
        </span>
        <span class="badge" style="background: rgba(99, 102, 241, 0.15); color: #A5B4FC; border: 1px solid rgba(99, 102, 241, 0.3);">
            XAI: SHAP Explainer
        </span>
    </div>
    """, unsafe_allow_html=True)

with nav_col3:
    st.markdown("""
    <div style="text-align: right; padding-top: 10px;">
        <span class="badge" style="background: rgba(148, 163, 184, 0.12); color: #CBD5E1; border: 1px solid rgba(148, 163, 184, 0.25);">
            🛡️ %100 KVKK & Açık Rıza Uyumlu
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 12px 0 24px 0;'>", unsafe_allow_html=True)


# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("### 🔍 Öğrenci Dizini")

# Fast Filter Pills
filter_choice = st.sidebar.radio(
    "Filtrele:",
    ["Tümü (15)", "🔴 Yüksek & Kritik Risk", "⚡ Bildirim Tetiklenenler", "⚠️ Eskalasyon Bekleyenler"],
    horizontal=True,
    label_visibility="collapsed",
)

# Filter fixtures based on choice
filtered_fixtures = []
for s in fixtures:
    score, _ = pipeline.risk_layer.predict_risk(s)
    rule_eval = pipeline.rule_engine.evaluate(s, score, s.get("sub_segment", "baslayamayan"))
    
    if filter_choice == "🔴 Yüksek & Kritik Risk" and score < 0.50:
        continue
    if filter_choice == "⚡ Bildirim Tetiklenenler" and not rule_eval["trigger"]:
        continue
    if filter_choice == "⚠️ Eskalasyon Bekleyenler" and not rule_eval["escalate_to_human"]:
        continue
    filtered_fixtures.append(s)

if not filtered_fixtures:
    filtered_fixtures = fixtures
    st.sidebar.warning("Filtreye uyan öğrenci bulunamadı, tüm liste gösteriliyor.")

student_options = {f"{s['student_id']} · {s['name']} ({s['exam_type']} - Sınıf {s['grade']})": s for s in filtered_fixtures}
selected_label = st.sidebar.selectbox("Öğrenci Seçiniz:", list(student_options.keys()))
current_student = student_options[selected_label]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Karar Eşiği (Threshold)")
risk_thresh = st.sidebar.slider(
    "Operasyonel Terk Eşiği:",
    min_value=0.25,
    max_value=0.65,
    value=0.40,
    step=0.05,
    help="0.40 eşiği, churn vakalarının %82'sini yakalamak üzere optimize edilmiştir."
)
pipeline.rule_engine.risk_threshold = risk_thresh

st.sidebar.markdown("### 🎭 Veli İletişim Tonu")
tone_choice = st.sidebar.selectbox(
    "Mesaj İletişim Tarzı:",
    ["empathetic", "structured", "gentle", "informative"],
    index=["empathetic", "structured", "gentle", "informative"].index(
        current_student.get("parent_tone_preference", "empathetic")
    ),
    format_func=lambda x: {
        "empathetic": "Empatik & Destekleyici (Önerilen)",
        "structured": "Yapılandırılmış & Net Hedefli",
        "gentle": "Şefkatli & Kaygı Azaltıcı",
        "informative": "Veri Odaklı & Bilgilendirici"
    }.get(x, x)
)
current_student["parent_tone_preference"] = tone_choice

st.sidebar.markdown("---")
st.sidebar.caption("SIC AI-17 Capstone · AI in Marketing · Group 1")


# ----------------- EVALUATE CURRENT STUDENT -----------------
res = pipeline.process_student(current_student)

# ----------------- STUDENT BANNER HEADER -----------------
exam_color = "#38BDF8" if res["exam_type"] == "LGS" else "#F472B6"
avatar_char = res["name"][0] if res["name"] else "Ö"

st.markdown(f"""
<div class="student-banner">
    <div style="display: flex; align-items: center; gap: 18px;">
        <div class="student-avatar">{avatar_char}</div>
        <div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <h3 style="margin: 0; font-size: 1.4rem; font-weight: 700;">{res['name']}</h3>
                <span class="badge" style="background: rgba(255,255,255,0.08); color: #E2E8F0;">ID: {res['student_id']}</span>
                <span class="badge" style="background: rgba(56, 189, 248, 0.15); color: {exam_color};">{res['exam_type']} · Sınıf {res['grade']}</span>
            </div>
            <p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #94A3B8;">
                Davranışsal Kategori: <strong style="color: #C7D2FE;">{res['segment_display']}</strong> · 
                Son İnaktivite: <strong style="color: #F8FAFC;">{current_student.get('inactivity_days', 0)} gün</strong>
            </p>
        </div>
    </div>
    <div>
        <span class="badge {'badge-critical' if res['risk_score'] >= 0.50 else ('badge-high' if res['risk_score'] >= 0.40 else 'badge-low')}" style="font-size: 0.95rem; padding: 8px 18px;">
            {'🔴 Yüksek Churn Riski' if res['risk_score'] >= 0.50 else ('🟡 Orta Risk (İzleniyor)' if res['risk_score'] >= 0.40 else '🟢 Düşük Risk')}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


# ----------------- MAIN PORTAL TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Rehberlik & Karar Paneli",
    "📱 Veli Mesajlaşma Stüdyosu",
    "🧪 Müdahale & What-If Simülatörü",
    "📊 Sınıf Rosteri & Model Benchmark",
])


# =========================================================================
# TAB 1: REHBERLİK & KARAR PANELI
# =========================================================================
with tab1:
    # 4 Top KPI Cards
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    with col_kpi1:
        risk_pct = res["risk_score"] * 100
        bar_color = "#F43F5E" if risk_pct >= 50 else ("#F59E0B" if risk_pct >= 40 else "#10B981")
        st.markdown(f"""
        <div class="glass-card kpi-container">
            <div>
                <div class="kpi-label">📊 Tahmin Edilen Churn Riski</div>
                <div class="kpi-value" style="color: {bar_color};">%{risk_pct:.1f}</div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" style="width: {min(risk_pct, 100)}%; background: {bar_color};"></div>
                </div>
            </div>
            <div class="kpi-subtext">Model Güvenilirlik Eşiği: <strong>%{risk_thresh*100:.0f}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi2:
        seg_icons = {
            "baslayamayan": "⏳",
            "telefonla_dagilan": "📱",
            "geceye_kayan": "🌙",
            "yarida_birakan": "⚡",
            "kaygiyla_erteleyen": "💔"
        }
        icon = seg_icons.get(res["segment_code"], "📌")
        st.markdown(f"""
        <div class="glass-card kpi-container">
            <div>
                <div class="kpi-label">🧠 Davranışsal Persona</div>
                <div class="kpi-value" style="font-size: 1.35rem; color: #A5B4FC; margin-top: 6px;">
                    {icon} {res['segment_code'].replace('_', ' ').title()}
                </div>
            </div>
            <div style="margin-top: 14px;">
                <span class="badge badge-segment">Öğretmen Aksiyonu: {res['segment_code'][:10]}...</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi3:
        trig_status = "BİLDİRİM TETİKLENDİ" if res["trigger"] else "NORMAL (BEKLEMEDE)"
        trig_color = "#F43F5E" if res["trigger"] else "#10B981"
        st.markdown(f"""
        <div class="glass-card kpi-container">
            <div>
                <div class="kpi-label">⚡ Deterministik Kural Kararı</div>
                <div class="kpi-value" style="font-size: 1.25rem; color: {trig_color}; margin-top: 6px;">
                    {'🔴 ' + trig_status if res['trigger'] else '🟢 ' + trig_status}
                </div>
            </div>
            <div class="kpi-subtext" style="color: #94A3B8; margin-top: 8px;">
                Zaman: <strong>{res['delivery_window']}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi4:
        esc_status = "CANLI REHBERLİK DAVETİ" if res["escalate_to_human"] else "STANDART AI KOÇLUK"
        esc_color = "#F59E0B" if res["escalate_to_human"] else "#64748B"
        st.markdown(f"""
        <div class="glass-card kpi-container">
            <div>
                <div class="kpi-label">📞 İnsan Desteği Eskalasyonu</div>
                <div class="kpi-value" style="font-size: 1.25rem; color: {esc_color}; margin-top: 6px;">
                    {'⚠️ ' + esc_status if res['escalate_to_human'] else '✓ ' + esc_status}
                </div>
            </div>
            <div class="kpi-subtext">Kriter: Risk > 0.65 ve 3+ Cevapsız Bildirim</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # Two-Column Layout: Left Pedagogical Drivers (SHAP), Right Intervention Plan
    col_plan_left, col_plan_right = st.columns([1.1, 0.9])

    with col_plan_left:
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin: 0 0 4px 0; font-size: 1.15rem; font-weight: 700;">
                🧠 Açıklanabilir Yapay Zeka (SHAP Risk Analizi)
            </h4>
            <p style="margin: 0 0 16px 0; font-size: 0.84rem; color: #94A3B8;">
                Modelin kara kutu tahminlerini pedagojik gerekçelere dönüştüren matematiksel etki analizi:
            </p>
        """, unsafe_allow_html=True)

        shap_info = res["shap_explanation"]
        df_shap = pd.DataFrame(shap_info["all_contributions"])
        df_shap["Yön"] = df_shap["shap_value"].apply(lambda x: "Riski Artıran (+)" if x > 0 else "Riski Azaltan (-)")
        df_shap["Etki"] = df_shap["shap_value"].abs()

        # Altair Horizontal Divergent Bar Chart
        chart = alt.Chart(df_shap).mark_bar(cornerRadius=6).encode(
            x=alt.X("shap_value:Q", title="SHAP Etki Değeri (Log-Odds)", axis=alt.Axis(gridColor="rgba(255,255,255,0.06)", titleColor="#94A3B8")),
            y=alt.Y("feature_tr:N", sort="-x", title="", axis=alt.Axis(labelColor="#CBD5E1", labelFontSize=11)),
            color=alt.Color(
                "Yön:N",
                scale=alt.Scale(domain=["Riski Artıran (+)", "Riski Azaltan (-)"], range=["#F43F5E", "#10B981"]),
                legend=alt.Legend(title="", orient="top", labelColor="#E2E8F0")
            ),
            tooltip=[
                alt.Tooltip("feature_tr:N", title="Özellik"),
                alt.Tooltip("student_value:Q", title="Öğrencinin Değeri"),
                alt.Tooltip("shap_value:Q", title="SHAP Etkisi", format="+.4f")
            ]
        ).properties(height=280, background="transparent")
        
        st.altair_chart(chart, use_container_width=True)

        # High Impact Driver Callouts
        drivers = shap_info.get("top_risk_drivers", [])
        protectives = shap_info.get("top_protective_factors", [])

        st.markdown("<div style='margin-top: 14px;'>", unsafe_allow_html=True)
        if drivers:
            d = drivers[0]
            st.markdown(f"""
            <div style="background: rgba(244, 63, 94, 0.12); border-left: 4px solid #F43F5E; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;">
                <strong style="color: #FDA4AF;">🚨 Öncelikli Risk Kaynağı:</strong> 
                <span style="color: #F8FAFC;">{d['feature_tr']}</span> 
                (Öğrenci Değeri: <strong>{d['student_value']}</strong> · Risk Katkısı: <strong>+{d['shap_value']:.2f}</strong>)
            </div>
            """, unsafe_allow_html=True)
        if protectives:
            p = protectives[0]
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.12); border-left: 4px solid #10B981; padding: 10px 14px; border-radius: 8px;">
                <strong style="color: #6EE7B7;">🛡️ Koruyucu Güçlü Yön:</strong> 
                <span style="color: #F8FAFC;">{p['feature_tr']}</span> 
                (Öğrenci Değeri: <strong>{p['student_value']}</strong> · Koruma Katkısı: <strong>{p['shap_value']:.2f}</strong>)
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_plan_right:
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin: 0 0 4px 0; font-size: 1.15rem; font-weight: 700;">
                🎯 Öğretmen / Koç Aksiyon Notu
            </h4>
            <p style="margin: 0 0 14px 0; font-size: 0.84rem; color: #94A3B8;">
                Rehberlik birimi için önerilen pedagojik strateji ve kural tetik gerekçesi:
            </p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
            <div style="font-size: 0.78rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;">Tetik Gerekçesi (Kural Motoru)</div>
            <div style="font-size: 0.95rem; color: #F8FAFC; font-weight: 600; margin-top: 4px;">{res['primary_reason']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Quick action tips based on segment
        pedagogical_tips = {
            "baslayamayan": "📌 <strong>Tavsiye:</strong> Öğrenciye masaya oturma ataletini kırmak için 'sadece 15 dk tek bir konu' kuralını hatırlatın. Büyük hedefler donma tepkisi yaratır.",
            "telefonla_dagilan": "📌 <strong>Tavsiye:</strong> Odak bloğu telefon bölünmesini engellemek için veliye cihazı farklı bir odaya bırakma teklifini 'ceza değil, oyun/odak desteği' olarak sunun.",
            "geceye_kayan": "📌 <strong>Tavsiye:</strong> Biyolojik saatin geceye kayması ertesi gün okulda konsantrasyonu düşürür. Çalışma bloğunu kademeli olarak 20:30'a çekin.",
            "yarida_birakan": "📌 <strong>Tavsiye:</strong> Oturumları 40 dakika yerine 20+20 dakika olarak bölün. Erken başarı hissi sürdürülebilirliği artırır.",
            "kaygiyla_erteleyen": "📌 <strong>Tavsiye:</strong> Hata yapma korkusu nedeniyle test başlatmıyor. Süresiz deneme ve yanlışların 'öğrenme adımı' olduğu vurgusu yapılmalıdır."
        }
        tip = pedagogical_tips.get(res["segment_code"], "📌 Öğrenci ile haftalık 15 dakikalık değerlendirme planlayın.")
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 12px; padding: 14px; margin-bottom: 16px; font-size: 0.88rem; line-height: 1.5; color: #E2E8F0;">
            {tip}
        </div>
        """, unsafe_allow_html=True)

        if res["escalate_to_human"]:
            st.error("⚠️ Dikkat: Bu öğrenci velisi 3 gündür sistem bildirimlerine yanıt vermedi. Doğrudan veli telefon araması önerilmektedir.")
            if st.button("📞 Veliyi Arama Listesine Ekle (Randevu Oluştur)", use_container_width=True):
                st.success(f"✓ {res['name']}'in velisi için rehberlik görüşmesi takvime eklendi.")
        else:
            st.success("✓ Standart AI döngüsü aktif. Veli akşam saat 20:30'da koçluk bildirimi alacak.")

        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================================
# TAB 2: VELI MESAJLAŞMA STÜDYOSU
# =========================================================================
with tab2:
    st.markdown("### 📱 Veli İletişim ve Bildirim Simülatörü")
    st.caption("AI Koçluk motorunun veliye akşam saat 20:30'da ilettiği kişiselleştirilmiş koçluk mesajının gerçek zamanlı önizlemesi:")

    col_phone_left, col_phone_right = st.columns([1, 1])

    with col_phone_left:
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin: 0 0 12px 0; font-size: 1.1rem; font-weight: 700;">⚙️ Mesajlaşma Ayarları & Kontrol</h4>
        """, unsafe_allow_html=True)
        
        st.write(f"**Öğrenci:** {res['name']} ({res['exam_type']})")
        st.write(f"**Hedef Veli Personası:** {tone_choice.capitalize()} Ton")
        st.write(f"**Teslim Zamanı Penceresi:** {res['delivery_window']}")
        st.write(f"**Tetik Durumu:** `{'AKTİF' if res['trigger'] else 'PASİF'}`")

        st.markdown("---")
        st.markdown("#### ✏️ Mesajı Özelleştir (Canlı Düzenleme):")
        custom_msg = st.text_area("Veliye İletilecek Metin:", value=res["parent_message"], height=140)
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("📋 Panoya Kopyala", use_container_width=True):
                st.toast("✓ Mesaj panoya kopyalandı!")
        with c_btn2:
            if st.button("📲 Velinin WhatsApp'ına İlet", use_container_width=True):
                st.toast(f"✓ {res['name']}'in velisine WhatsApp iletisi gönderildi!")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_phone_right:
        # Authentic iPhone Mockup
        st.markdown(f"""
        <div class="phone-wrapper">
            <div class="phone-device">
                <div class="phone-island">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #22c55e;"></span>
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: #1f2937;"></span>
                </div>
                <div class="phone-status-bar">
                    <span>20:30</span>
                    <span>5G 📶 100% 🔋</span>
                </div>
                <div class="chat-header">
                    <div class="coach-avatar">🤖</div>
                    <div>
                        <div style="font-weight: 700; font-size: 0.9rem; color: #F8FAFC;">AI Personal Coach</div>
                        <div style="font-size: 0.70rem; color: #34D399;">● Çevrimiçi · Rehberlik Asistanı</div>
                    </div>
                </div>
                <div style="text-align: center; margin-bottom: 12px;">
                    <span class="badge" style="background: rgba(255,255,255,0.06); color: #94A3B8; font-size: 0.68rem;">
                        Bugün · {res['delivery_window']}
                    </span>
                </div>
                <div class="chat-bubble">
                    {custom_msg}
                    <div class="chat-timestamp">
                        20:30 <span style="color: #38BDF8;">✓✓</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================================
# TAB 3: MÜDAHALE & WHAT-IF SIMÜLATÖRÜ
# =========================================================================
with tab3:
    st.markdown("### 🧪 Canlı Müdahale & 'What-If' Senaryo Laboratuvarı")
    st.caption("Öğrencinin çalışma parametrelerine pedagojik müdahale yapıldığında (örneğin telefon kullanımı azaldığında veya veli rapor okuduğunda) risk skorunun ve sistem kararlarının nasıl değiştiğini anında simüle edin:")

    sim_c1, sim_c2, sim_c3 = st.columns(3)

    with sim_c1:
        s_clicks = st.slider("Platform Etkileşimi (VLE Tıklama):", 5, 800, int(current_student["vle_total_clicks"]), help="Toplam tıklama sayısı")
        s_focus = st.slider("Ortalama Odak Süresi (dk):", 5.0, 60.0, float(current_student["avg_focus_duration_mins"]), step=1.0)
        s_phone = st.slider("10dk+ Telefon Dağılma Sayısı:", 0, 15, int(current_student["phone_distraction_10min_count"]))

    with sim_c2:
        s_report = st.slider("Haftalık Veli Raporu Açılma Oranı:", 0.0, 1.0, float(current_student["parent_report_open_rate"]), step=0.05)
        s_score = st.slider("Deneme Sınavı Puan Ortalaması:", 20.0, 100.0, float(current_student["assessment_avg_score"]), step=1.0)
        s_late = st.slider("Geç Ödev Teslim Oranı:", 0.0, 1.0, float(current_student["late_submission_ratio"]), step=0.05)

    with sim_c3:
        s_anxiety = st.slider("Kaygı Anketi Puanı (1-10):", 1.0, 10.0, float(current_student["anxiety_survey_score"]), step=0.5)
        s_night = st.slider("Gece Çalışma Oranı (>22:00):", 0.0, 1.0, float(current_student["night_study_ratio"]), step=0.05)
        s_inact = st.slider("Son İnaktivite Gün Sayısı:", 0, 10, int(current_student.get("inactivity_days", 0)))

    # Compute Simulated Student
    sim_data = dict(current_student)
    sim_data.update({
        "vle_total_clicks": s_clicks,
        "avg_focus_duration_mins": s_focus,
        "phone_distraction_10min_count": s_phone,
        "parent_report_open_rate": s_report,
        "assessment_avg_score": s_score,
        "late_submission_ratio": s_late,
        "anxiety_survey_score": s_anxiety,
        "night_study_ratio": s_night,
        "inactivity_days": s_inact,
    })

    sim_res = pipeline.process_student(sim_data)
    delta_risk = (sim_res["risk_score"] - res["risk_score"]) * 100

    st.markdown("---")
    res_c1, res_c2 = st.columns([1, 2])

    with res_c1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin: 0 0 10px 0; font-size: 1.1rem; font-weight: 700;">📊 Simülasyon Kıyaslama</h4>
        """, unsafe_allow_html=True)
        
        st.metric(
            label="Simüle Edilen Risk Skoru",
            value=f"%{sim_res['risk_score']*100:.1f}",
            delta=f"{delta_risk:+.1f}%",
            delta_color="inverse"
        )
        st.write(f"**Yeni Seviye:** `{sim_res['risk_level']}`")
        st.write(f"**Tespit Edilen Persona:** `{sim_res['segment_display']}`")
        st.write(f"**Kural Kararı:** `{'MÜDAHALE TETİKLENDİ' if sim_res['trigger'] else 'GÜVENLİ (TETİKLENMEDİ)'}`")
        st.markdown("</div>", unsafe_allow_html=True)

    with res_c2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin: 0 0 10px 0; font-size: 1.1rem; font-weight: 700;">💬 Yeni Şartlara Göre Dinamik Üretilen Mesaj</h4>
        """, unsafe_allow_html=True)
        st.info(sim_res["parent_message"])
        st.caption(f"Gerekçe: {sim_res['primary_reason']}")
        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================================
# TAB 4: SINIF ROSTERI & MODEL BENCHMARK
# =========================================================================
with tab4:
    st.markdown("### 📋 Sınıf Genel Bakışı (15 Öğrenci Kohortu)")
    st.caption("Tüm test fixture öğrencilerinin churn riski, persona segmenti ve müdahale durum özeti:")

    cohort_rows = []
    for s in fixtures:
        r_item = pipeline.process_student(s)
        cohort_rows.append({
            "Öğrenci ID": r_item["student_id"],
            "İsim": r_item["name"],
            "Sınav": r_item["exam_type"],
            "Sınıf": r_item["grade"],
            "Risk Skoru (%)": round(r_item["risk_score"] * 100, 1),
            "Risk Seviyesi": r_item["risk_level"].split()[0],
            "Davranış Segmenti": r_item["segment_code"].replace('_', ' ').title(),
            "Müdahale Tetik": "EVET" if r_item["trigger"] else "HAYIR",
            "Canlı Destek": "VAR" if r_item["escalate_to_human"] else "YOK",
            "Pik Saati": r_item["delivery_window"][:5]
        })
    
    df_cohort = pd.DataFrame(cohort_rows)
    st.dataframe(df_cohort, use_container_width=True, height=360)

    st.markdown("---")
    st.markdown("### 📈 Makine Öğrenmesi Baseline Raporu (K3)")

    base_dir = Path(__file__).resolve().parent / "data-research" / "modeling"
    results_csv = base_dir / "baseline_results.csv"

    if results_csv.exists():
        df_base = pd.read_csv(results_csv)
        st.markdown("##### 1. Doğrulanmış Model Benchmark Tablosu ($N=813$ Test Seti)")
        st.dataframe(df_base, use_container_width=True)

    g_col1, g_col2 = st.columns(2)
    with g_col1:
        cm_lgb = base_dir / "confusion_matrix_lightgbm.png"
        if cm_lgb.exists():
            st.image(str(cm_lgb), caption="LightGBM Karışıklık Matrisi (Düşük Yanlış Alarm = 120 FP)")

    with g_col2:
        th_plot = base_dir / "threshold_tuning_plot.png"
        if th_plot.exists():
            st.image(str(th_plot), caption="Eşik 0.40 Optimizasyonu: Recall %51'den %82'ye yükseltildi.")
