/**
 * AI PERSONAL COACH — FRONTEND INTERACTIVITY & LOGIC
 * Samsung Innovation Campus (SIC) Capstone
 * Fully aligned with AI_Personal_Coach_Proje.md
 */

// 15 PoC Fixture Students with Deep Weekly Report Metrics & Personas (§5, §9, §10)
const STUDENTS_DB = [
  {
    student_id: "STU_001",
    name: "Ali",
    exam_type: "LGS",
    grade: "8",
    sub_segment: "baslayamayan",
    segment_label: "Başlayamayan (Cannot Start)",
    vle_total_clicks: 28,
    avg_focus_duration_mins: 12.5,
    phone_distraction_10min_count: 2,
    inactivity_days: 4,
    assessment_avg_score: 54.0,
    studied_credits: 60,
    unstudied_credits: 30,
    risk_score: 0.68,
    shap_drivers: [
      { feature: "Hareketsiz Gün (inactivity_days)", impact: 0.28, direction: "up", val: "4 gün" },
      { feature: "10 Dk+ Dağılma (phone_distraction)", impact: 0.18, direction: "up", val: "2 kez" },
      { feature: "Deneme Başarısı (assessment_score)", impact: -0.12, direction: "down", val: "%54" },
      { feature: "Tıklama Yoğunluğu (total_clicks)", impact: 0.14, direction: "up", val: "28 tık" }
    ],
    coach_script: "Ali bu hafta ders masasına oturmakta biraz zorlanıyor. Ona 'Neden ders çalışmıyorsun?' yerine, 'Sadece 5 dakikalık eğlenceli bir ısınma testine bakalım mı?' diyerek başlamasını kolaylaştırabilirsiniz.",
    action_text: "Masaya oturma felcini kırmak için 5 dakikalık tek soru testi başlatın.",
    digest: "Ali'nin çalışma hevesi mevcut ancak başlangıç adımı destek istiyor. Küçük ısınma seanslarıyla ritim oturacaktır.",
    // Weekly Report §5 specific data
    weekly_report: {
      risk_avg: "Yüksek",
      actions_done: "5 / 12",
      missed_blocks: "4 Blok",
      distract_alerts: "3 Uyarı",
      top_app: "Brawl Stars (Oyun)",
      segment: "Başlayamayan",
      official_sentence: "Bu hafta risk ortalaması yüksek. 12 aksiyondan 5'i tamamlandı. Dikkat dağılma uyarısı: 3. En çok kopma: derse başlama anında oyun bildirimi. Öneri: 5 dakikalık tek soru seansı ile başlayın."
    }
  },
  {
    student_id: "STU_002",
    name: "Zeynep",
    exam_type: "YKS (TYT/AYT)",
    grade: "12",
    sub_segment: "telefonla_dagilan",
    segment_label: "Telefonla Dağılan (Phone-Distracted)",
    vle_total_clicks: 85,
    avg_focus_duration_mins: 18.0,
    phone_distraction_10min_count: 6,
    inactivity_days: 1,
    assessment_avg_score: 68.0,
    studied_credits: 90,
    unstudied_credits: 20,
    risk_score: 0.76,
    shap_drivers: [
      { feature: "10 Dk+ Dağılma (phone_distraction)", impact: 0.36, direction: "up", val: "6 kez" },
      { feature: "Deneme Başarısı (assessment_score)", impact: -0.21, direction: "down", val: "%68" },
      { feature: "Hareketsiz Gün (inactivity_days)", impact: -0.15, direction: "down", val: "1 gün" },
      { feature: "Çalışma Yükü (studied_credits)", impact: -0.10, direction: "down", val: "90 kredi" }
    ],
    coach_script: "Zeynep'in konu kavrayışı güçlü fakat telefon bildirimleri odak süresini bölüyor. Ona telefonunu yasaklamak yerine, '25 dakikalık odak bloğunda telefonu salondaki kutuya koyup seans bitince mola çayı içelim mi?' teklifinde bulunabilirsiniz.",
    action_text: "Pomodoro seansı boyunca telefonu görüş alanından çıkaracak 'Mola Kutusu' uygulayın.",
    digest: "Zeynep'in potansiyeli yüksek; dikkat dağıtıcıları kontrol altına aldığında haftalık netleri hızla sıçrayacaktır.",
    weekly_report: {
      risk_avg: "Orta-Yüksek",
      actions_done: "7 / 12",
      missed_blocks: "2 Blok",
      distract_alerts: "6 Uyarı",
      top_app: "Instagram (Sosyal)",
      segment: "Telefonla Dağılan",
      official_sentence: "Bu hafta risk ortalaması orta. 12 aksiyondan 7'si tamamlandı. Dikkat dağılma uyarısı: 6. En çok kopma: akşam sosyal medya. Öneri: odak bloğunda telefonu salondaki kutuya koyun."
    }
  },
  {
    student_id: "STU_003",
    name: "Mert",
    exam_type: "YKS (Mezun)",
    grade: "Mezun",
    sub_segment: "geceye_kayan",
    segment_label: "Geceye Kayan (Night-Shifted)",
    vle_total_clicks: 140,
    avg_focus_duration_mins: 38.0,
    phone_distraction_10min_count: 1,
    inactivity_days: 0,
    assessment_avg_score: 76.5,
    studied_credits: 120,
    unstudied_credits: 0,
    risk_score: 0.32,
    shap_drivers: [
      { feature: "Deneme Başarısı (assessment_score)", impact: -0.32, direction: "down", val: "%76.5" },
      { feature: "Hareketsiz Gün (inactivity_days)", impact: -0.24, direction: "down", val: "0 gün" },
      { feature: "Tıklama Yoğunluğu (total_clicks)", impact: -0.18, direction: "down", val: "140 tık" },
      { feature: "Gece Çalışma Oranı (night_ratio)", impact: 0.15, direction: "up", val: "%82" }
    ],
    coach_script: "Mert düzenli ve yüksek tempoda çalışıyor. Tek risk faktörü çalışmalarının gece geç saatlere kayması. Sabah denemelerinde zihin berraklığı için uyku düzenini kademeli olarak 1 saat öne çekmesini rica edebilirsiniz.",
    action_text: "Yatmadan 30 dakika önce mavi ışık maruziyetini kesip dinlenme seansına geçin.",
    digest: "Mert için retention riski çok düşük; sistemde güvenle ilerliyor. Tebrik ve uyku dengesi yeterlidir.",
    weekly_report: {
      risk_avg: "Düşük",
      actions_done: "11 / 12",
      missed_blocks: "0 Blok",
      distract_alerts: "1 Uyarı",
      top_app: "YouTube (Gece)",
      segment: "Geceye Kayan",
      official_sentence: "Bu hafta risk ortalaması çok düşük. 12 aksiyondan 11'i tamamlandı. Dikkat dağılma uyarısı: 1. En çok kopma: gece geç saat YouTube. Öneri: gündüz 2 kısa blok ekleyin, uyku saatini öne çekin."
    }
  },
  {
    student_id: "STU_004",
    name: "Elif",
    exam_type: "LGS",
    grade: "8",
    sub_segment: "yarida_birakan",
    segment_label: "Yarıda Bırakan (Abandons Midway)",
    vle_total_clicks: 45,
    avg_focus_duration_mins: 14.0,
    phone_distraction_10min_count: 4,
    inactivity_days: 3,
    assessment_avg_score: 58.0,
    studied_credits: 60,
    unstudied_credits: 30,
    risk_score: 0.62,
    shap_drivers: [
      { feature: "Hareketsiz Gün (inactivity_days)", impact: 0.22, direction: "up", val: "3 gün" },
      { feature: "10 Dk+ Dağılma (phone_distraction)", impact: 0.19, direction: "up", val: "4 kez" },
      { feature: "Deneme Başarısı (assessment_score)", impact: -0.11, direction: "down", val: "%58" },
      { feature: "Çalışma Yükü (studied_credits)", impact: 0.08, direction: "up", val: "60 kredi" }
    ],
    coach_script: "Elif derse büyük bir hevesle başlıyor fakat 15. dakikadan sonra zihinsel yorgunluk hissedip seansı kapatıyor. Seansları 40 dakika yerine 20 dakikalık iki mini parçaya bölmek motivasyonunu korumasını sağlayacaktır.",
    action_text: "Çalışma bloklarını 20'şer dakikalık iki mini aşamaya bölün.",
    digest: "Elif'in devamlılığı için blok süreleri optimize edildi; erken pes etme davranışı kırılıyor.",
    weekly_report: {
      risk_avg: "Orta",
      actions_done: "6 / 12",
      missed_blocks: "3 Blok",
      distract_alerts: "4 Uyarı",
      top_app: "TikTok (Video)",
      segment: "Yarıda Bırakan",
      official_sentence: "Bu hafta risk ortalaması orta. 12 aksiyondan 6'sı tamamlandı. Dikkat dağılma uyarısı: 4. En çok kopma: blok ortasında sıkılma. Öneri: blokları 20 dakikaya indirin ve aralarda su molası verin."
    }
  },
  {
    student_id: "STU_005",
    name: "Can",
    exam_type: "YKS (Sayısal)",
    grade: "11",
    sub_segment: "kaygiyla_erteleyen",
    segment_label: "Kaygıyla Erteleyen (Anxiety Procrastinator)",
    vle_total_clicks: 52,
    avg_focus_duration_mins: 22.0,
    phone_distraction_10min_count: 3,
    inactivity_days: 5,
    assessment_avg_score: 62.0,
    studied_credits: 90,
    unstudied_credits: 40,
    risk_score: 0.71,
    shap_drivers: [
      { feature: "Hareketsiz Gün (inactivity_days)", impact: 0.31, direction: "up", val: "5 gün" },
      { feature: "Bırakılan Dersler (unstudied_credits)", impact: 0.16, direction: "up", val: "40 kredi" },
      { feature: "10 Dk+ Dağılma (phone_distraction)", impact: 0.12, direction: "up", val: "3 kez" },
      { feature: "Deneme Başarısı (assessment_score)", impact: -0.14, direction: "down", val: "%62" }
    ],
    coach_script: "Can'ın erteleme davranışı tembellikten değil, zorlandığı fizik konusundaki hata yapma korkusundan kaynaklanıyor. Ona 'Önemli olan test sonucu değil, sadece 3 soruya cesaretle bakman' diyerek baskıyı azaltabilirsiniz.",
    action_text: "Süre veya net baskısı olmadan yalnızca 3 soru çözme hedefi koyun.",
    digest: "Kaygı bazlı kaçınma davranışı tespit edildi. Destekleyici dil ile derse dönüşü tetiklendi.",
    weekly_report: {
      risk_avg: "Yüksek",
      actions_done: "4 / 12",
      missed_blocks: "5 Blok",
      distract_alerts: "3 Uyarı",
      top_app: "WhatsApp (Sohbet)",
      segment: "Kaygıyla Erteleyen",
      official_sentence: "Bu hafta risk ortalaması yüksek. 12 aksiyondan 4'ü tamamlandı. Dikkat dağılma uyarısı: 3. En çok kopma: zor dersler öncesi erteleme. Öneri: sıfır hata baskısı olmadan sadece 3 soru hedefi koyun."
    }
  }
];

// Active State
let currentStudent = STUDENTS_DB[0];
let timerSeconds = 18 * 60 + 42; // 18:42

// Initialize on DOM Load
document.addEventListener("DOMContentLoaded", () => {
  populateStudentSelect();
  loadStudentData(currentStudent.student_id);
  calculateROI();
  startFocusTimer();
});

// View Switcher Navigation
function switchView(viewName) {
  document.querySelectorAll(".view-panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".switch-btn").forEach(b => b.classList.remove("active"));

  const targetPanel = document.getElementById(`view-${viewName}`);
  const targetBtn = document.getElementById(`btn-view-${viewName}`);

  if (targetPanel) targetPanel.classList.add("active");
  if (targetBtn) targetBtn.classList.add("active");

  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Populate Student Selector
function populateStudentSelect() {
  const selectEl = document.getElementById("studentSelect");
  if (!selectEl) return;

  selectEl.innerHTML = "";
  STUDENTS_DB.forEach(s => {
    const opt = document.createElement("option");
    opt.value = s.student_id;
    opt.textContent = `${s.name} (${s.exam_type} - ${s.segment_label.split(' ')[0]})`;
    selectEl.appendChild(opt);
  });
}

// Load Specific Student Data
function loadStudentData(studentId) {
  const s = STUDENTS_DB.find(item => item.student_id === studentId) || STUDENTS_DB[0];
  currentStudent = s;

  // 1. Update KPI Cards
  const kpiRisk = document.getElementById("kpi-risk-val");
  const kpiRiskLbl = document.getElementById("kpi-risk-label");
  const kpiRiskCard = document.getElementById("kpi-card-risk");

  const riskPct = Math.round(s.risk_score * 100);
  kpiRisk.textContent = `%${riskPct}`;

  if (s.risk_score >= 0.40) {
    kpiRisk.className = "kpi-num red";
    kpiRiskLbl.textContent = "Yüksek Kopma Riski (Tetiklendi)";
    kpiRiskCard.className = "kpi-card alert";
  } else {
    kpiRisk.className = "kpi-num green";
    kpiRiskLbl.textContent = "Düşük Risk (Güvenli Alan)";
    kpiRiskCard.className = "kpi-card safe";
  }

  document.getElementById("kpi-focus-val").textContent = `${s.avg_focus_duration_mins} dk`;
  document.getElementById("kpi-distract-val").textContent = `${s.phone_distraction_10min_count} kez`;

  // 2. Render SHAP Bars
  renderShapBars(s.shap_drivers);

  // 3. Update Sliders for What-If
  document.getElementById("sim-inactivity").value = s.inactivity_days;
  document.getElementById("val-sim-inactivity").textContent = `${s.inactivity_days} gün`;

  document.getElementById("sim-distraction").value = s.phone_distraction_10min_count;
  document.getElementById("val-sim-distraction").textContent = `${s.phone_distraction_10min_count} kez`;

  document.getElementById("sim-clicks").value = s.vle_total_clicks;
  document.getElementById("val-sim-clicks").textContent = `${s.vle_total_clicks} tık`;

  document.getElementById("sim-score").value = Math.round(s.assessment_avg_score);
  document.getElementById("val-sim-score").textContent = `%${Math.round(s.assessment_avg_score)}`;

  // 4. Update Virtual Phone Mockup
  document.getElementById("phone-bubble-tag").textContent = s.segment_label;
  document.getElementById("phone-message-body").textContent = s.coach_script;
  document.getElementById("phone-action-text").textContent = s.action_text;

  // 5. Update Mini Digest
  document.getElementById("portal-digest-text").textContent = s.digest;

  // 6. Update Official Weekly Report (§5)
  if (s.weekly_report) {
    document.getElementById("rep-student-name").textContent = s.name;
    document.getElementById("rep-risk-avg").textContent = s.weekly_report.risk_avg;
    document.getElementById("rep-actions-done").textContent = s.weekly_report.actions_done;
    document.getElementById("rep-missed-blocks").textContent = s.weekly_report.missed_blocks;
    document.getElementById("rep-distract-alerts").textContent = s.weekly_report.distract_alerts;
    document.getElementById("rep-top-app").textContent = s.weekly_report.top_app;
    document.getElementById("rep-segment").textContent = s.weekly_report.segment;
    document.getElementById("rep-official-sentence").textContent = `"${s.weekly_report.official_sentence}"`;
  }

  // Update focus block app alert indicator
  const alertPill = document.getElementById("focus-alert-pill");
  if (alertPill) {
    if (s.phone_distraction_10min_count >= 1) {
      alertPill.style.display = "inline-flex";
      alertPill.innerHTML = `<span>⚠️</span> ${s.weekly_report.top_app}: 12 Dk (>10 dk eşiği aşıldı)`;
    } else {
      alertPill.style.display = "none";
    }
  }
}

// Render SHAP Bars with Divergent Progress
function renderShapBars(drivers) {
  const container = document.getElementById("shap-bars-list");
  if (!container) return;

  container.innerHTML = "";

  drivers.forEach(d => {
    const row = document.createElement("div");
    row.className = "shap-row";

    const isUp = d.direction === "up";
    const widthPct = Math.min(100, Math.round(Math.abs(d.impact) * 200));

    row.innerHTML = `
      <div class="shap-label" title="${d.feature}">${d.feature.split('(')[0].trim()}</div>
      <div class="shap-track">
        <div class="shap-fill ${isUp ? 'risk-up' : 'risk-down'}" style="width: ${widthPct}%;"></div>
      </div>
      <div class="shap-val" style="color: ${isUp ? '#f43f5e' : '#10b981'};">
        ${isUp ? '+' : '-'}${Math.abs(d.impact).toFixed(2)}
      </div>
    `;

    container.appendChild(row);
  });
}

// What-If Dynamic Live Update
function updateWhatIf() {
  const inact = parseInt(document.getElementById("sim-inactivity").value);
  const distract = parseInt(document.getElementById("sim-distraction").value);
  const clicks = parseInt(document.getElementById("sim-clicks").value);
  const score = parseInt(document.getElementById("sim-score").value);

  // Update labels
  document.getElementById("val-sim-inactivity").textContent = `${inact} gün`;
  document.getElementById("val-sim-distraction").textContent = `${distract} kez`;
  document.getElementById("val-sim-clicks").textContent = `${clicks} tık`;
  document.getElementById("val-sim-score").textContent = `%${score}`;

  // Approximate simulated LightGBM risk logit
  let baseLogit = -0.5;
  baseLogit += (inact * 0.22);
  baseLogit += (distract * 0.18);
  baseLogit -= (clicks * 0.008);
  baseLogit -= ((score - 50) * 0.02);

  const simRisk = 1 / (1 + Math.exp(-baseLogit));
  const simRiskPct = Math.round(simRisk * 100);

  // Update KPI card
  const kpiRisk = document.getElementById("kpi-risk-val");
  const kpiRiskLbl = document.getElementById("kpi-risk-label");
  const kpiRiskCard = document.getElementById("kpi-card-risk");

  kpiRisk.textContent = `%${simRiskPct}`;

  if (simRisk >= 0.40) {
    kpiRisk.className = "kpi-num red";
    kpiRiskLbl.textContent = "Yüksek Kopma Riski (Simüle)";
    kpiRiskCard.className = "kpi-card alert";
  } else {
    kpiRisk.className = "kpi-num green";
    kpiRiskLbl.textContent = "Düşük Risk (Simüle)";
    kpiRiskCard.className = "kpi-card safe";
  }

  // Update dynamic SHAP approximation
  const dynamicDrivers = [
    { feature: "Hareketsiz Gün", impact: (inact * 0.06), direction: inact > 1 ? "up" : "down" },
    { feature: "Telefon Dağılması", impact: (distract * 0.07), direction: distract > 1 ? "up" : "down" },
    { feature: "Deneme Başarısı", impact: ((score - 50) * -0.006), direction: score >= 60 ? "down" : "up" },
    { feature: "Tıklama Yoğunluğu", impact: (clicks * -0.002), direction: clicks > 50 ? "down" : "up" }
  ];
  renderShapBars(dynamicDrivers);

  // Dynamic Phone message update
  if (simRisk >= 0.40) {
    document.getElementById("phone-message-body").textContent = 
      `${currentStudent.name} için son verilerde ${inact} gündür hareketsizlik ve ${distract} kez dikkat dağınıklığı görüldü. Akşam onu yargılamadan, '10 dakikalık keyifli bir mola verip ardından kısa bir soruya bakalım mı?' önerisinde bulunabilirsiniz.`;
  } else {
    document.getElementById("phone-message-body").textContent = 
      `${currentStudent.name} harika bir çalışma ritmi yakaladı! Son denemesinde %${score} başarı gösterdi. Bu akşam çabasını takdir edip motive edebilirsiniz.`;
  }
}

// Reset What-If
function resetWhatIf() {
  loadStudentData(currentStudent.student_id);
}

// Select Persona from Landing Page
function selectPersonaDemo(subSegment) {
  const match = STUDENTS_DB.find(s => s.sub_segment === subSegment) || STUDENTS_DB[0];
  switchView('portal');
  document.getElementById("studentSelect").value = match.student_id;
  loadStudentData(match.student_id);
}

// ============================================================
// LIVE PARENT TONE REFRAMER (§7)
// ============================================================
function setQuickPrompt(text) {
  const inputEl = document.getElementById("parentToneInput");
  if (inputEl) {
    inputEl.value = text;
    inputEl.focus();
  }
}

function reframeToneLive() {
  const inputEl = document.getElementById("parentToneInput");
  const rawText = inputEl.value.trim() || "Telefonu bırakmadı, dersi yine böldü, çok kızgınım.";

  // Rule & Tone Reframing Engine (Deci & Ryan 2000 - Self Determination Theory)
  let transformedMsg = "";
  let microAction = "";

  if (rawText.toLowerCase().includes("telefon") || rawText.toLowerCase().includes("böl")) {
    transformedMsg = `Dikkatin dağıldığını ve zorlandığını gördük. Sorun değil, şimdi toparlanabilirsin. 20 dakikalık tek bir soru bloğu yap; bitince mola çayı senin.`;
    microAction = `20 dakikalık tek soru bloğu başlat ve telefonu mola kutusuna koy.`;
  } else if (rawText.toLowerCase().includes("otur") || rawText.toLowerCase().includes("başla")) {
    transformedMsg = `Masaya oturmak bazen günün en zor adımıdır. Hiç canını sıkma, sadece 5 dakikalık tek bir ısınma sorusuna bakıp kalkabilirsin.`;
    microAction = `Sadece 5 dakikalık 1 soru çöz ve başarı butonuna bas.`;
  } else if (rawText.toLowerCase().includes("net") || rawText.toLowerCase().includes("deneme") || rawText.toLowerCase().includes("hata")) {
    transformedMsg = `Deneme netleri inişli çıkışlı olabilir; bu sürecin çok doğal bir parçası. Bugün yanlışlarına kızmak yerine sadece 1 konunun püf noktasına bakalım.`;
    microAction = `Son denemeden sadece 1 yanlış sorunun video çözümünü incele.`;
  } else {
    transformedMsg = `Bugün çalışma ritminde küçük bir dalgalanma hissettik. Seni çok iyi anlıyoruz; derin bir nefes alıp 15 dakikalık mini bir blokla günün kapanışını yapabilirsin.`;
    microAction = `15 dakikalık hafif tekrar bloğu tamamla.`;
  }

  // Update phone screen with animation
  const phoneBody = document.getElementById("phone-message-body");
  const phoneAction = document.getElementById("phone-action-text");
  const phoneBubble = document.getElementById("phone-message-bubble");

  phoneBubble.style.transform = "scale(0.96)";
  phoneBubble.style.opacity = "0.6";

  setTimeout(() => {
    phoneBody.textContent = transformedMsg;
    phoneAction.textContent = microAction;
    document.getElementById("phone-bubble-tag").textContent = "AI Motive Edici Koçluk Mesajı";
    phoneBubble.style.transform = "scale(1)";
    phoneBubble.style.opacity = "1";
    phoneBubble.style.transition = "all 0.3s ease";
  }, 250);

  // Switch focus or smooth scroll to phone screen
  document.querySelector(".dash-col-right").scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// Simulate Parent Action
function simulateParentAction() {
  alert(`✓ Harika! ${currentStudent.name} için önerilen koçluk diyaloğu veli tarafından uygulandı olarak kaydedildi. Sistem 90 günlük retention skorunu güncelledi!`);
}

// Print Weekly Report (§5)
function printWeeklyReport() {
  alert(`📄 [Resmi Rapor Çıktısı] ${currentStudent.name} için Haftalık Veli Güven Karnesi PDF formatında hazırlanıyor. Yazdırma penceresi açılıyor.`);
  window.print();
}

// Focus Tracker Timer countdown
function startFocusTimer() {
  const clockEl = document.getElementById("focus-timer-clock");
  if (!clockEl) return;

  setInterval(() => {
    if (timerSeconds > 0) {
      timerSeconds--;
      const mins = Math.floor(timerSeconds / 60).toString().padStart(2, '0');
      const secs = (timerSeconds % 60).toString().padStart(2, '0');
      clockEl.textContent = `${mins}:${secs}`;
    }
  }, 1000);
}

// Onboarding & Survey Choice Toggle
function toggleSurveyChoice(btn) {
  const parent = btn.parentElement;
  parent.querySelectorAll(".survey-choice-btn").forEach(b => b.classList.remove("selected"));
  btn.classList.add("selected");
}

function saveOnboardingProfile() {
  const freeText = document.getElementById("onboard-free-text").value;
  alert(`✅ Öğrenci profili başarıyla güncellendi!\n\nVeli Anlatımı ve Anket analiz edildi. Öğrenci modeli 'Telefonla Dağılan' alt segmentine kalibre edildi. Veli Portalı güncel verilerle hazır.`);
  switchView('portal');
}

// ROI & LTV/CAC Calculator Logic
function calculateROI() {
  const subs = parseInt(document.getElementById("calc-subs").value);
  const price = parseInt(document.getElementById("calc-price").value);
  const churnRate = parseInt(document.getElementById("calc-churn").value) / 100;
  const reductionRate = parseInt(document.getElementById("calc-reduction").value) / 100;

  // Update slider label texts
  document.getElementById("lbl-calc-subs").textContent = `${subs.toLocaleString('tr-TR')} abone`;
  document.getElementById("lbl-calc-price").textContent = `${price} ₺`;
  document.getElementById("lbl-calc-churn").textContent = `%${Math.round(churnRate * 100)}`;
  document.getElementById("lbl-calc-reduction").textContent = `%${Math.round(reductionRate * 100)} (Hedef)`;

  // Calculations
  const savedStudents = Math.round(subs * churnRate * reductionRate);
  const extraArr = savedStudents * price * 12;

  let arrFormatted = "";
  if (extraArr >= 1000000) {
    arrFormatted = (extraArr / 1000000).toFixed(2) + "M ₺";
  } else {
    arrFormatted = Math.round(extraArr / 1000) + "K ₺";
  }

  document.getElementById("res-saved-arr").textContent = arrFormatted;
  document.getElementById("res-saved-students").textContent = `${savedStudents.toLocaleString('tr-TR')} Aile`;

  const ltvCac = (1.8 + (reductionRate * 7)).toFixed(1) + "x";
  document.getElementById("res-ltv-cac").textContent = ltvCac;
}
