# §1 — Teknoloji Yığını (Tech Stack)

**Proje:** AI Personal Coach  
**Yazar:** K5 — Methodology, Mimari, Stack  
**Hazırlayan:** Berat Erol ÇelİK  
**Tarih:** 2026-08-23  
**Not:** Yalnızca gerçekten kullanılacak araçlar listelenmiştir. Olmayan servisler (Meta Ads, HubSpot, Snowflake vb.) eklenmemiştir.

---

## Teknoloji Tablosu

| Katman | Araç / Teknoloji | Ne İçin | Not |
|--------|-----------------|---------|-----|
| Dil / Ortam | Python 3.10+, Jupyter Notebook | EDA (mevcut), prototip geliştirme, model eğitimi | `data-research/notebooks/oulad_eda.ipynb` |
| Risk Modeli | LightGBM | Öğrenci kopma riski skoru (0.00–1.00) + segment atama | Lojistik regresyon baseline olarak karşılaştırma |
| Açıklanabilirlik | SHAP | Risk skorunun veliye açıklanması (feature importance) | Her yüksek risk skorunda en baskın 2–3 özellik |
| Kural Motoru | Uygulama içi (Python) | 10 dk (600 sn) eşik, günlük bildirim tavanı, sessiz saat | Deterministik IFTTT kuralları |
| LLM — Üslup | OpenAI GPT-3.5 Turbo API | Veli mesajı üslup dönüştürme, profil oluşturma | temperature=0.2; fallback: statik şablon |
| LLM — Rapor | OpenAI GPT-3.5 Turbo API | Haftalık veli raporu kişiselleştirilmiş koçluk cümlesi | Pre-computation: rapor gönderilmeden 1 saat önce |
| LLM — Fallback | Statik şablon (`INTENT_SOFT`) | API çalışmazsa veya zaman aşımı olursa devreye girer | Sıfır maliyet, sıfır gecikme |
| Veri Kaynağı | OULAD (açık) | Proxy veri: tıklama, segment, assessment | UK 2013–14; LGS/YKS'ye genellenemez |
| Veri Kaynağı | Sentetik (`synthetic_data.py`) | Veli mesajları, anket, odak oturumu, telefon olayları | stdlib; PII yok; seed=42 |
| Veri Formatı | CSV dosyaları | Tüm veri akışı CSV üzerinden | `oulad_synthetic_processed.csv` |
| Saklama | Dosya sistemi / basit DB | Sentetik veri, KPI logları | MVP'de CRM yok |
| Demo UI | Flask / basit web çerçevesi (plan) | 5 ekranlık demo arayüzü | Olmayan mobil native stack yazılmamıştır |
| Versiyon Kontrol | Git + GitHub | Branch bazlı iş akışı | Her kişi kendi branch'inde çalışır |

---

## Seçim Gerekçeleri

### Neden LightGBM (XGBoost veya Derin Öğrenme değil)

- **XGBoost:** Histogram tabanlı ayrıştırma ve yaprak odaklı büyüme sayesinde LightGBM, XGBoost'a göre %30–50 daha hızlı eğitim sağlar. Kategorik değişken desteği doğrudan entegredir.
- **Derin Öğrenme (LSTM/Transformer):** "Kara kutu" yapısı veliye açıklama imkanı kısıtlıdır. Oklahoma'da 32.593 öğrencilik veri setinde derin öğrenme için yeterli veri derliği yoktur. CPU tabanlı çıkarım (~4 ms) ile production'da daha dayanıklıdır.

### Neden GPT-3.5 Turbo (GPT-4 değil)

- GPT-4 API maliyeti GPT-3.5'in ~20 katıdır. Abonelik bazlı bir üründe LTV/CAC oranını korumak için maliyet kontrolü kritiktir.
- Kısa ve yönlendirmeli mesajlarda GPT-3.5 Turbo yeterli pedagojik üslup kapasitesine sahiptir.
- Open kaynak modeller (Llama 3, Mistral) MVP'de depolama ve MLOps altyapısı gerektirir; Gelecek aşama olarak planlanmıştır.

### Neden Statik Şablon Fallback

LLM API'sinin çalışmaması (sunucu arızası, rate limit, network kesintisi) durumunda sistem durmaz. Statik şablonlar (`INTENT_SOFT`), K4 tarafından onaylanmış pedagojik dile sahiptir ve sıfır maliyetle çalışır. Bu, **marka güveni** ve **system uptime** için gereklidir.

---

## Olmayanlar (Bu Projede Kullanılmayanlar)

| Araç | Neden yok |
|------|-----------|
| Apache Kafka | MVP'de gerçek zamanlı streaming henüz gerekli değil; sentetik veri CSV ile işlenir |
| Docker / Kubernetes | Mikroservis altyapısı Katman B'de planlanmıştır |
| Redis Cache | MVP'de performans darboğazı henüz yaşanmamıştır |
| Apache Flink / Spark Streaming | Gerçek zamanlı stream processing Katman B'de |
| Meta Ads / HubSpot / Snowflake | Pazarlama ve CRM araçları bu projenin kapsamı dışında |
| Mobil native stack (Swift/Kotlin) | MVP web tabanlıdır; mobil uygulama Katman B'de |
