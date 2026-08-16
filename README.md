# AI Personal Coach — Pazarlama Teknoloji Değerlendirmesi

[![Status: In Progress](https://img.shields.io/badge/Status-In_Progress-yellow.svg)](#) [![Deadline: Aug 16](https://img.shields.io/badge/Deadline-Aug_16-red.svg)](#) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#)

## 🎓 Proje Özeti

**AI Personal Coach**, LGS ve YKS (Türkiye'deki lise ve üniversite giriş sınavları) hazırlığı yapan öğrenciler ve velileri için özel olarak tasarlanmış abonelik tabanlı, yapay zeka destekli bir e-learning (e-öğrenme) platformudur. Bu proje, eğitim teknolojileri platformlarının en büyük ticari sorunu olan **erken veli churn (müşteri kaybı) problemini (1–2 ay içinde abonelik iptali)** çözmek amacıyla yapay zeka ve modern pazarlama teknolojilerinin nasıl entegre edilebileceğini akademik bir derinlikte değerlendirmektedir. 

Proje, **pazarlama bağlamında** proaktif veri analizi (Predictive ML), doğal dil işleme tabanlı kişiselleştirme (LLM-based Personalization), olay güdümlü otomasyon (Rule Engines) ve duygu analizi (Speech-to-Text) teknolojilerini stratejik olarak incelemektedir. Sistemimizin temel ticari hedefi, eğitim sektöründe ortalama %40–50 bandında seyreden 90 günlük veli elde tutma (retention) oranını (KPI) %65'in (target) üzerine kalıcı olarak yükseltmektir.

### Pazarlama Problemi ve İnovatif Çözüm

Abonelik tabanlı eğitim platformlarında yaşanan en kritik sorun asimetrik değer algısıdır: **Ödeme yapan müşteri (veli), uygulamanın işe yaradığına dair somut bir öğrenme sinyali (deneme sınavı başarısı gibi) görmeden çok önce aboneliği iptal etmektedir.**

**Neden?** Çocuğun akademik sınav performansının ölçülebilir bir şekilde artması genellikle 4 ila 6 hafta sürer. Ancak velinin sabır ve karar verme penceresi çoğunlukla ilk 30 günde, en geç Hafta 4–6 arasında kapanır. 
**Temel Fark:** Veli aboneliği iptal etme kararı aldığında, öğrenci henüz ilerleme kaydedebilecek zamanı dahi bulamamıştır.

**Çözüm:** Platformumuz bu kopukluğu, AI destekli proaktif elde tutma (retention) mesajlaşması, anlık davranışsal zamanlama optimizasyonu (timing) ve hiper-kişiselleştirilmiş pedagojik rehberlik (LLM) ile çözmektedir. Veliye, salt "öğrenciniz ders çalışmadı" gibi kriz tetikleyici uyarılar yerine, yapay zeka destekli yapılandırıcı koçluk tavsiyeleri sunularak sistemin "değeri" sınav sonucundan çok önce kanıtlanmaktadır.

---

## 📊 Pazarlama Metrikleri

Platformun tüm teknolojik mimarisi, aşağıdaki temel başarı metriklerini (KPI'lar) maksimize etmek üzere kurgulanmıştır.

### Ana KPI: 90-Günlük Veli Retention (Elde Tutma) Oranı

| Metrik | Tanım | Hedef (Target) | Sektör Ortalaması |
|--------|-------|----------------|-------------------|
| **90-Gün Veli Retention** | 90. günün sonunda aktif kalan abonelerin, başlayanlara oranı | **65%+** | %40–50 |
| **30-Gün Retention** | Kritik ilk ayın sonunda (30. gün) aktif kalan aboneler | **80%+** | %50–60 |
| **Trial → Paid Conversion** | Ücretsiz deneme (Free Trial) sürecinden ücretli pakete geçiş | **25%+** | %15–20 |
| **Haftalık Rapor Açılma** | Push bildirimlerine tıklanarak haftalık detaylı rapora erişim oranı | **35%+** | %20–25 |
| **Bildirim Yanıt Oranı** | Veliye gönderilen aksiyon odaklı Push Notification CTR (Tıklama) oranı | **18%+** | %8–12 |

---

## 🎯 Hedef Müşteri (Dual-User Model / İkili Kullanıcı)

EdTech platformlarında karar alıcı ile son kullanıcı genellikle farklıdır. Bu durum karmaşık bir pazarlama dinamiği yaratır.

| Rol | Tanım | Pazarlama Bağlantısı |
|-----|-------|----------------------|
| **Ödeyen** (Veli) | Lise veya ortaokul öğrencisinin ebeveyni (çoğunlukla anne) | Ana pazarlama personasi; abonelik karar alıcısı, temel mesajlaşma hedefi |
| **Kullanan** (Öğrenci) | LGS/YKS sınavlarına hazırlanan ergenlik çağındaki öğrenci (14–17 yaş) | Etkileşim (engagement) ve risk skorunu oluşturan birincil veri kaynağı |

> **Pazarlama Paradoksu**: İletişim ve bildirimler ödeme yapan veliye gitmektedir; ancak veliye ne söyleneceğini (Aktivasyon metriklerini) öğrencinin dijital ayak izi belirler. Öğrencinin aktivitesi → Yapay zeka tabanlı veli mesajı → Churn riskinin sıfırlanması döngüsü, ürünün temel büyüme motorudur.

---

### Segmentler (5 Davranışsal Profil Segmenti)

Öğrenci davranışları homojen değildir. Makine öğrenmesi modelimiz (LightGBM), etkileşim verilerini analiz ederek kullanıcıları otomatik olarak aşağıdaki 5 segmentten birine atar:

1. **Başlayamayan (Cannot Start)** — Sisteme kayıt olduktan sonraki ilk 3 gün içinde toplam 1 saatten az aktivite gösterenler (Oryantasyon eksikliği).
2. **Yarıda Bırakan (Abandons Midway)** — 1. haftada güçlü başlayıp, 2. haftada ardışık 2'den fazla gün sisteme hiç giriş yapmayanlar.
3. **Telefonla Dağılan (Phone-Distracted)** — 2–3 hafta boyunca düzenli çalışırken, son 5 günde (uygulama içi veya arka planda) ciddi odaklanma kaybı yaşayanlar.
4. **Kaygıyla Erteleyen (Anxiety-Driven)** — Sisteme giriş yapan ancak yalnızca sınav teknikleri/rehberlik videolarını izleyip asıl konu anlatımlarına/testlere girmeyenler.
5. **Geceye Kayan (Night-Shifted)** — Sisteme ağırlıklı olarak saat 22:00'den sonra giriş yapan, sabah motivasyonunu tamamen yitirmiş profiller.

> **Her segment tamamen farklı bir mesajlaşma stratejisi gerektirir.** "Başlayamayan" bir öğrencinin velisine motive edici (onboarding) içerikler iletilirken, "Telefonla Dağılan" öğrencinin velisine yapıcı disiplin/odaklanma (engagement) taktikleri sunulur.

---

## 🤖 Teknoloji Stack (Kısa Özet)

Teknoloji yığınımız, veri toplamadan mesaj iletimine kadar uçtan uca pürüzsüz bir pazarlama makinesi yaratmak için tasarlanmıştır.

| Bileşen | Teknik / Araç | Temel Amaç | Pazarlama Etkisi (KPI) |
|---------|---------------|------------|------------------------|
| **Risk Skoru Tahmini** | LightGBM ML | Son 30 günlük öğrenci davranışından churn riskini (%0-100) anlık tahmin etmek | Doğru zamanda (timing) hedefli churn müdahalesi |
| **Mesaj Kişiselleştirme** | OpenAI GPT-3.5 Turbo | Soğuk risk skorunu (0.85) velinin anlayacağı sıcak, empatik bir mesaja dönüştürmek | %3–5x Bildirim açılma (CTR) artışı |
| **Trigger & Timing** | Kural Motoru (Rule Engine) | 10 dk hareketsizlik gibi deterministik eylemleri izlemek ve Peak-hour teslimatı yapmak | "Doğru mesajı doğru saatte" ulaştırarak bildirim yorgunluğunu önlemek |
| **Feedback Toplama** | Whisper ASR (R&D) | Odak gruplarında veli sesli geri bildirimini (voice feedback) analiz etmek | Engelleri (barrier) tespit edip modeli ve iletişimi iyileştirmek |

**Daha derinlemesine mimari analiz için:** Projedeki tüm makine öğrenmesi algoritmaları, JSON payload'ları ve mimari detaylar için lütfen [`technology-review/tech_review.md`](./technology-review/tech_review.md) dosyasını inceleyiniz.

---

## 📈 Veri Kaynağı ve Metodoloji

### OULAD Dataset + Sentetik Veri Yaklaşımı

**Neden?** Türk LGS-YKS eğitim bağlamında açık kaynaklı, gerçek ve kapsamlı bir pilot davranışsal veri seti (real pilot data) bulunmamaktadır.
**Çözüm:** Dünyaca kabul görmüş açık veri setleri ile Türkiye'ye özgü sentetik verilerin melez (hybrid) kullanımı.

| Veri Türü | Kaynak | Kullanım Amacı | Temel Sınırlılık |
|-----------|--------|----------------|------------------|
| **OULAD** | UK Open University | Makine öğrenmesi modelinin davranışsal özellikleri (behavioral features) öğrenmesi için temel eğitim verisi | İngiltere akademik bağlamı; tam zamanlı olmayan (part-time) öğrenici davranışı |
| **Sentetik** | Python + Realistic Distributions | Türk LGS-YKS öğrenci/veli davranışı, saat tercihleri ve sınav stresi simülasyonu | Gerçek dünya verisi olmadığı için doğrudan genellenemez; lansman sonrası cross-validation gerektirir |

### Temel Veri Özellikleri (Features)

Makine öğrenmesi modelimize (LightGBM) giren temel **Veli (Parent) Davranış Özellikleri** şunlardır:
- `login_frequency_30d` — Son 30 gün içindeki sisteme başarılı giriş sayısı.
- `report_opened_count` — Haftalık ilerleme raporlarının açılma frekansı.
- `notification_clicked_rate` — Push bildirimlerine tıklama (CTR) eğilimi.
- `session_duration_mean` — Ortalama günlük oturum süresi.
- `time_of_day_variance` — Giriş saati değişkenliği (Geceye Kayan segment tespiti için kritik).
- `engagement_trend` — Son 7 günün aktivitesinin, önceki 7-14 günlük aktiviteyle kıyaslanması (trend).
- `day_since_signup` — Başlangıçtan itibaren geçen abonelik süresi (Churn riski penceresi).

**KVKK Uyum ve Çocuk Verisi Hassasiyeti:** Tüm veri işleme süreçleri Türk Kişisel Verilerin Korunması Kanunu'na (KVKK) %100 uyumludur. 18 yaş altı çocukların verileri için "Açık Veli Rızası" mekanizması işletilir ve veriler ekstra kriptografik korumaya tabi tutulur. Amaç gözetleme (surveillance) değil, tamamen 90 günlük retention hedeflerini gerçekleştirmektir. Daha detaylı analiz için [`data-research/02_governance.md`](./data-research/02_governance.md) dosyasına bakınız.

---

## 👥 Ekip Rolü ve Doküman Dağılımı

Projemiz, spesifik sorumluluklara sahip 5 kişilik bir takım tarafından 3 ana dokümantasyon klasöründe koordineli olarak yürütülmektedir:

### Kişi 1: Literature Lead & Editor
**Sorumlu Olduğu Dokümanlar**: [`literature-review/01_intro_gap_conclusion.md`](./literature-review/01_intro_gap_conclusion.md), [`00_project_brief.md`](./00_project_brief.md)
**Sorumluluklar**:
- **Literature Review §1:** Pazarlama problemi, asimetrik ikili kullanıcı (hedef müşteri) modelinin tanımlanması, KPI'ların kurgusu.
- **Literature Review §2:** Araştırmanın tematik yapısının ve gerekçesinin kurulması.
- **Literature Review §4:** Akademik literatürdeki boşlukların (gap) analizi ve projemizin bu boşluğu nasıl kapattığının (pazarlama ilgisi) gösterilmesi.
- **Literature Review §5:** Sonuç ve genel sentezin oluşturulması.
- **Ek Görev:** Üç ana dokümanda yer alan terminoloji tutarlılığının sağlanması, KPI ve segment isimlerinin standardize edilmesi, final PR merge işlemlerinin yürütülmesi.

### Kişi 2: Literature Analyst
**Sorumlu Olduğu Dokümanlar**: [`literature-review/02_source_summaries.md`](./literature-review/02_source_summaries.md), [`references.bib`](./references.bib)
**Sorumluluklar**:
- **Literature Review §3:** Aşağıdaki 4 tema altında 10-12 temel endüstriyel ve akademik kaynağın analiz edilmesi:
  1. Davranış bazlı kullanıcı segmentasyonu.
  2. SaaS ve abonelik bağlamında churn (iptal) tahmini.
  3. Kişiselleştirme paradoksu & Recommender (öneri) sistemleri.
  4. Bildirim (Nudge) zamanlaması ve mesaj çerçeveleme (framing).
- Her kaynak için: Araştırma amacı, veri seti, kullanılan yöntem, ana bulgu ve "pazarlama katkısının" incelenmesi.
- **Çıktı:** Literatürü sistematik olarak karşılaştıran detaylı bir matris/tablo oluşturmak (dataset | method | metric | marketing context | limitations).

### Kişi 3: Data Lead (EDA - Keşifsel Veri Analizi)
**Sorumlu Olduğu Dokümanlar**: [`data-research/01_scope_eda.md`](./data-research/01_scope_eda.md), [`data-research/notebooks/oulad_eda.ipynb`](./data-research/notebooks/oulad_eda.ipynb)
**Sorumluluklar**:
- **Data §2:** OULAD veri kaynağının erişim, format, boyut ve değişkenlerinin (features) detaylı haritalanması.
- **Data §4:** Keşifsel Veri Analizi (Exploratory Data Analysis - EDA).
  - Kritik betimsel istatistikler.
  - 5-6 kapsamlı görselleştirme (Engagement dağılımı, VLE clickstream, dropout/churn oranları, 5 ana segmentin dağılımı, korelasyon matrisleri).
  - Kullanıcı etkileşim (engagement) düşüşünün, "abonelik iptali" (churn) proxy'si olarak analiz edilmesi.
  - Bu bulguların doğrudan pazarlama metriklerine bağlanması.
- **Deliverable:** Makine öğrenmesi (Baseline) model sonuçlarının oluşturulması ve Teknoloji incelemesi için (Kişi 5) paslanması.

### Kişi 4: Data Governance & Synthetic Data
**Sorumlu Olduğu Dokümanlar**: [`data-research/02_governance.md`](./data-research/02_governance.md), [`data-research/scripts/synthetic_data.py`](./data-research/scripts/synthetic_data.py)
**Sorumluluklar**:
- **Data §1:** Sentetik veri ve OULAD kullanım gerekçelerinin bilimsel temelleri.
- **Data §3:** Veri kalitesi, privacy (gizlilik) ve sınırlılıklar. Eksik veri (missing data), sınıf dengesizliği (class imbalance) ve temsil sorununun çözümü.
- **KVKK + Çocuk Verisi + Açık Rıza:** Sistemdeki en hassas konuların etik standartlarda projelendirilmesi (18 yaş altı verilerin ekstra korunması).
- **Sınırlılıklar Analizi:** OULAD veri setinin Türkiye bağlamına uymayan noktalarının saptanması ve sentetik verinin limitlerinin dürüstçe belirtilmesi.
- **Deliverable:** Sentetik veri üretimi için kapsamlı bir şema (schema) tasarlanması ve Python üretim betiğinin (`synthetic_data.py`) yazılması. *(Not: KVKK ve çocuk mahremiyeti bölümü projenin en vizyoner farklılaştırıcısıdır.)*

### Kişi 5: Technology Review
**Sorumlu Olduğu Dokümanlar**: [`technology-review/tech_review.md`](./technology-review/tech_review.md)
**Sorumluluklar**: 
8 bölümden oluşan, son derece derin ve kapsamlı teknoloji mimarisi değerlendirmesi:
1. **Giriş** — Neden teknoloji değerlendirmesi gerekli.
2. **Teknoloji Genel Bakışı** — LightGBM, LLM, Kural Motoru, ASR incelemesi.
3. **Pazarlama KPI Mapping** — Her bileşenin KPI'ya nasıl katkı sağladığı.
4. **Karşılaştırma Analizi** — Risk modeli (LightGBM vs LSTM vs Lojistik Regresyon), LLM (GPT-3.5 vs Llama vs Claude) ve ASR (Whisper vs Google Cloud).
5. **Kullanım Örnekleri** — Duolingo, Khanmigo, Netflix vaka analizleri (case studies).
6. **Riskler** — Halüsinasyon, over-automation, KVKK, model yaşlanması (drift).
7. **Sonuç** — Hedefe yönelik teknoloji stack'inin nihai özeti.
8. **Kaynaklar** — 10-14 adet APA formatında güncel teknik literatür entegrasyonu.

---

## 📁 Repo Yapısı

Proje dosyaları mantıksal bir klasör yapısı içerisinde GitHub'da organize edilmiştir:

```text
SIC_AI_-17_Capstone_Group_1/
├── README.md                              # Bu genel proje dokümantasyon dosyası
├── 00_project_brief.md                    # K1: Proje stratejisi ve özet brief
├── references.bib                         # Ortak Kullanım: Tüm ekip kaynaklarını bu APA/BibTeX dosyasına ekler
│
├── literature-review/
│   ├── 01_intro_gap_conclusion.md         # K1: Literatür giriş, boşluk (gap) analizi ve sonuç
│   └── 02_source_summaries.md             # K2: Seçilen 10-12 kaynağın detaylı özeti ve matriksi
│
├── data-research/
│   ├── 01_scope_eda.md                    # K3: Veri kapsamı ve EDA sonuç raporu
│   ├── 02_governance.md                   # K4: Veri yönetişimi, KVKK, rıza süreçleri ve sentetik veri temelleri
│   ├── notebooks/
│   │   └── oulad_eda.ipynb                # K3: Etkileşimli EDA ve görselleştirme Jupyter defteri
│   ├── scripts/
│   │   └── synthetic_data.py              # K4: Simülasyon ve sentetik veri üretim betiği
│   └── figures/                           # K3: Raporlarda kullanılan çıktı grafikler ve dağılımlar
│
└── technology-review/
    └── tech_review.md                     # K5: MLOps, algoritmalar ve kapsamlı teknoloji değerlendirmesi
```

**Git Workflow (Ekip Çalışma Akışı):**
- Her takım üyesi kendi özellik dalında (feature branch) çalışır (örneğin: `feat/lit-review-k1`, `feat/tech-review-k5`, vb.).
- Değişiklikler günlük olarak uzak sunucuya (origin) itilir (Push).
- Geliştirme tamamlandığında Pull Request (PR) açılır ve Ana (Main) dala K1'in koordinatörlüğünde dahil edilir (Merge).
- Son gün çatışmalar (conflict resolution) çözülerek nihai sürüm birleştirilir.

---

## 🔧 Teknoloji Detayları

Projenin arkasında çalışan yapay zeka ajanlarının mimari anatomisi.

### 1. Churn Risk Prediction (Churn Tahmini - LightGBM)
- **Model:** LightGBM (Gradient Boosting Decision Tree)
- **Girdi (Input):** Son 30 günlük veli/öğrenci davranışını betimleyen 7 temel feature.
- **Çıktı (Output):** 0 ile 1 arasında sürekli bir Risk Skoru (0 = Çok düşük risk, 1 = Kesin iptal riski).
- **Risk Skoru Dağılımı ve Aksiyonlar:**
  - `0.0–0.2`: Düşük Risk (Müdahaleye gerek yok - no intervention).
  - `0.2–0.5`: Orta Risk (Yakından izleme - monitor).
  - `0.5–0.8`: Yüksek Risk (Kişiselleştirilmiş mesaj gönder - send personalized message).
  - `0.8–1.0`: Kritik Risk (İnsan desteği teklif et - human support offer).
- **Neden LightGBM Tercih Edildi?**
  - **Yorumlanabilirlik:** Modelin kararları (feature importance) veliye anlaşılır bir dille açıklanabilir.
  - **Hız:** Tahmin süresi <100ms seviyesindedir. Günde 100.000'den fazla öğrenciyi analiz edebilecek kapasitededir.
  - **Maliyet:** Açık kaynaklıdır ve GPU gerektirmez (no GPU).
  - **Doğruluk:** Pazarlama müdahaleleri için oldukça yeterli olan ~0.78 AUC skoruna sahiptir.

### 2. Message Personalization (Mesaj Kişiselleştirme - LLM)
- **Model:** OpenAI GPT-3.5 Turbo
- **Girdi (Input):** Risk Skoru, Segment, Öğrencinin Zayıf Konuları, Velinin İletişim Stili.
- **Çıktı (Output):** Veliye iletilecek, 140 karakteri aşmayan Türkçe Push Bildirimi.
- **Örnek Çıktı:**
  > **Input**: Risk 0.73, Disengaged (Yarıda Bırakan), English weak (İngilizce zayıf), Impatient parent (Sabırsız veli).
  > **Output**: "Emre'nin İngilizce'de 3×20dk/hafta blokları yapması yeterli. Bugün küçük bir başlangıç yapsak mı? 💪"
- **Neden GPT-3.5 Turbo Tercih Edildi?**
  - Türkçe dil hakimiyeti anadil (native-level) seviyesindedir.
  - Gecikme süresi (Latency) <500ms bandında olup gerçek zamanlı kullanıma (real-time viable) olanak tanır.
  - Mesaj başına maliyet ~$0.001 seviyesindedir (scale'de verimli).
  - Halüsinasyon (hallucination) riski katı şablonlar (template + validation) sayesinde tamamen kontrol edilebilir.

### 3. Timing & Trigger (Zamanlama ve Kural Motoru)
- **Core Rule (Ana Kural):** Eğer veli uygulamada son 10 dakika içinde aktif değilse **AND** saat 20:00–23:00 arasındaysa $\rightarrow$ send message.
- **Diğer Kritik Kurallar:**
  - **Time Window Optimization:** Velilerin telefonlarını en yoğun kontrol ettikleri akşam (parent peak-check) saati optimizasyonu.
  - **Segment-Based Routing:** Öğrenci "Başlayamayan" ise sisteme alıştırma (onboarding) mesajı; "Yarıda Bırakan" (disengaged) ise kanıt (proof) mesajı iletilir.
  - **Escalation:** Risk skoru >0.85 ise ve 3 gündür hiçbir yanıt (no-response) yoksa $\rightarrow$ canlı insan desteğine (human support) bilet açılır.
  - **Frequency Cap:** Maksimum 2 günde 3 mesaj (max 3 msg/2 days) gönderim limiti ile bildirim yorgunluğu engellenir.

### 4. Voice Feedback (Sesli Geri Bildirim - Optional R&D)
- **Technology:** Whisper (OpenAI) $\rightarrow$ Google Cloud Speech (production).
- **Use:** Odak grubu (Focus group) çalışmalarında veli sesli geri bildirimi (parent feedback) toplama.
- **Output:** Transkriptler (Transcripts) $\rightarrow$ Uygulama önündeki engellerin çıkarılması (barrier extraction) $\rightarrow$ Modelin sürekli iyileştirilmesi (model improvement).

---

## ⏰ Timeline (Zaman Çizelgesi)

| Tarih | Milestone | Sorumluluk |
|-------|-----------|------------|
| **12 Ağu** | Proje kick-off | Ekip toplantısı, brief lock (proje kilitlenmesi) |
| **13 Ağu** | İlk checkpoints | Kaynak listesi, veri indir, schema taslak |
| **14 Ağu** | İlk taslaklar | Herkes draft push yapar |
| **15 Ağu** | Cross-review (Çapraz inceleme) | K1↔K5, K2↔K3 çapraz okuması, K4 privacy pass (gizlilik onayı) |
| **16 Ağu 18:00** | Final push deadline | Tüm commit'ler `main` dalında (branch) toplanmalı |
| **16 Ağu 23:59** | Teslim deadline | GitHub'da eksiksiz görünmeli |

---

## 🎓 Proje Değerlendirme Çerçevesi

Bu proje, temel eksen olarak bir **"AI in Marketing" (Pazarlamada Yapay Zeka)** çalışmasıdır (Birleşmiş Milletler Sürdürülebilir Kalkınma Hedeflerine uyum zorunlu tutulmamıştır).

**Jüri ve Değerlendirme Beklentileri:**
- Pazarlama problemi net olarak ifade edilmeli ve çözümü ticari olarak ölçülebilir olmalıdır.
- Mimari teknoloji seçimleri, doğrudan pazarlama KPI'larına (LTV, CAC vb.) hizmet etmelidir.
- Veri gizliliği (KVKK), özellikle çocuk verisinin (reşit olmayan) analizi en üst düzeyde yapılmalıdır.
- Akademik derinlik ve endüstri uygunluğu (industry relevance) arasında sağlam bir denge kurulmalıdır.
- Tüm dokümanlar arasında (all 3 docs) kavramsal ve yazım tutarlılığı sağlanmalıdır.

**Başarı Metrikleri (Success Metrics):**
- 90-gün retention KPI'ının pazarlama bağlamında nasıl artırılacağı ikna edici şekilde ele alınmıştır.
- Risk ve fırsat analizi somut olarak haritalanmıştır.
- Teknoloji stack seçimi, İşletme (Business) + Teknik (Technical) uyumunu göstermektedir.
- Reşit olmayan veri işleme hassasiyetleri (properly addressed) doğru bir şekilde çözülmüştür.

---

## 👨‍💼 Ekip Üyeleri

| Kişi | Rol | GitHub | Sorumluluk |
|------|-----|--------|------------|
| **Berat Erol ÇELİK** | Kişi 5 | [@BeratCelikk](https://github.com/BeratCelikk) | Technology Review |
| [K1 Adı] | Kişi 1 | @[username] | Literature Lead + Editor |
| [K2 Adı] | Kişi 2 | @[username] | Literature Analyst |
| [K3 Adı] | Kişi 3 | @[username] | Data Lead (EDA) |
| [K4 Adı] | Kişi 4 | @[username] | Data Governance |

---

## 💬 İletişim Koordinasyonu

- **Proje Lead:** [K1 Adı] (@[username])
- **GitHub Issues:** Teknik sorular, kod hataları ve dokümantasyon koordinasyonu (coordination).
- **Slack/Discord:** Anlık (Real-time) günlük koordinasyon.
- **Deadline Questions:** Teslimat ile ilgili acil soruları K1'e ulaştırın.

---

## 📚 Kaynaklar ve Referanslar

Tüm akademik ve sektörel kaynaklar APA formatında ortak [`references.bib`](./references.bib) dosyasında toplanmıştır:
- LightGBM paper (Ke et al., 2017)
- Churn prediction literature (SaaS/subscription pazar bağlamı)
- Message personalization research (Mesaj kişiselleştirme araştırmaları)
- KVKK & GDPR child data safeguards (Çocuk verisi koruma yönergeleri)
- Duolingo, Khanmigo, Netflix case studies (Vaka çalışmaları)

**Total Hedef:** Doküman başına ortalama 10–14 kaynakça entry × 3 ana doküman = Toplamda ~30–40 unique source (farklı kaynak).

---

## 📝 Lisans & Etik Çerçeve

Bu proje, tamamen **akademik amaçlarla** yapay zeka tabanlı pazarlama teknolojisinin değerlendirilmesi için oluşturulmuştur.
**KVKK Uyum Beyanı:** Tasarlanan tüm veri işleme süreçleri Türk Kişisel Verileri Koruma Kanunu'na uygundur.
**Çocuk Verisi Beyanı:** 18 yaş altı kullanıcıların (çocuk) veri işleme adımlarında ekstra veri güvenliği ve açık rıza gereklilikleri gözetilmektedir.

---

## 🚀 Nasıl Başlanılır?

### Dosyaları Okuma Sırası
Sistemin genel bağlamını kavramak için önerilen okuma sırası:
1. **Bu README** — Tüm projenin ve mimarinin genel özeti (overview).
2. **[`00_project_brief.md`](./00_project_brief.md)** — Pazarlama problemi ve Ana KPI'ların tanımlanması.
3. **[`literature-review/`](./literature-review/)** — Teorik ve akademik temeller.
4. **[`data-research/`](./data-research/)** — Veri altyapısı ve metodoloji.
5. **[`technology-review/tech_review.md`](./technology-review/tech_review.md)** — Teknoloji değerlendirmesi (Technology evaluation).

### Kontribüsyon (Katkı Sağlama)
- Kendinize atanmış bir özellik dalı (branch) oluşturun (`feat/[görev]-[kişi]`).
- Kendi dosyanız veya klasörünüz üzerinde geliştirme yapın.
- Günlük düzenli olarak uzak sunucuya itme (push) gerçekleştirin.
- Çalışmanız tamamlandığında Ana (Main) dala Pull Request (PR) açın (K1'in merge etmesini bekleyin).

### Quality Checklist (Kalite Kontrol)
PR açmadan önce aşağıdaki listeyi onaylayın:
- [ ] Bütün projede aynı terminoloji (KPI adları, segmentler, ürün adları) kullanıldı mı?
- [ ] Atıflar APA formatında `references.bib` içerisine eklendi mi?
- [ ] Pazarlama bağlantısı net bir şekilde açıklandı mı?
- [ ] KVKK compliance (uyumluluk) denetimi (check) yapıldı mı?
- [ ] Dosyalar UTF-8 encoding ile (Türkçe karakter sorunsuz) kaydedildi mi?

---

## 📞 Sorular?

Herhangi bir soru, öneri veya iş akışı problemi (issue) için:
1. GitHub depomuz üzerinden **Issues** bölümünde kayıt açın.
2. Yazılan kod veya metin üzerine PR kısmında **comment** bırakın.
3. Team Slack kanalımız üzerinden doğrudan ekip üyesine mesaj atın.

---
**Last Updated**: 16 Ağustos 2026
**Status**: In Progress → Submission Aug 16, 23:59
