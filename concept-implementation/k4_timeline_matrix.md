# Implementation Plan §1–3 — K4 satırları

**Sahip:** K4  
K1 bu dosyayı Technology Stack / Timeline / Milestones bölümlerine yapıştırır.  
Diğer ekip üyelerinin işleri burada **uydurulmaz.**

---

## 1. Technology Stack — K4 bileşeni

| Bileşen | Araç | Amaç | Not |
|---------|------|------|-----|
| Sentetik veri üretici | Python 3.10+, yalnızca stdlib — `data-research/scripts/synthetic_data.py` | Demo event’leri: veli metni, anket, odak bloğu, telefon sinyali, haftalık metrik, niyet→mesaj çifti | `--seed` ile tekrarlanır; `schema_version` 1.0.0; gerçek PII yok |
| Çıktı | CSV + `metadata.json` | K5/K3 pipeline ve haftalık rapor ekranı için girdi | Pilot veri değildir |
| Yönetişim belgesi | Markdown — `data-research/02_governance.md` + bu klasör | Rıza, minimizasyon, sınırlılık | Kod değil, karar kaydı |

K4 yığınına LLM API, vektör DB, CRM veya reklam SDK’sı **eklenmez**. Bunlar K5 / uygulama sprint’idir.

---

## 2. Timeline and Task Distribution — K4

### 2.1 Görev matrisi (K4 satırı)

| Aşama | K4 sorumluluğu | Kanıt |
|-------|----------------|-------|
| Veri erişimi / hazırlık | OULAD’ın sınırını yazmak; sentetik şemayı dondurmak; “gerçek pilot yok” beyanı | `06_data_sources.md`, `synthetic_data.py`, `metadata.json` disclaimer |
| Prototip veri katmanı | Seed’li senaryolar (5 segment, 10 dk `notify_flag`, veli niyeti çifti) | `python3 synthetic_data.py --n 100 --seed 42` |
| Doğrulama | Proxy vs gerçek KPI ayrımı; leakage kontrol listesi | `04_challenges_k4.md` |
| İş akışına entegrasyon | Rıza / odak-sınırlı izleme / veli önizleme kurallarını plana işlemek | `05_ethical_responsible_ai.md` |
| KPI / iş değeri değerlendirmesi | Hangi alanın hangi KPI’ya bağlandığını tablolemek; 90g retention’ın bu veriyle **ölçülmediğini** sabitlemek | `06_data_sources.md` tablo |
| Final belge | K1’e yapıştırma paketi + APA | bu klasör + `references_k4.md` |
| Privacy pass (15–27 Ağu mantığı, yeni ödev) | Diğer bölümlere etik tutarlılık yorumu | PR review notu |

K1, K2, K3, K5 hücreleri: *K1 doldurur.*

### 2.2 K4 Gantt satırları (30 Ağustos 2026 belgesel teslim)

Geçmiş 12–16 Ağustos teslimi (Data Research) **bitmiş iştir**; yeni Gantt’ın tamamı gibi gösterilmez.

| Pencere | K4 işi | Çıktı |
|---------|--------|-------|
| 22–24 Ağustos 2026 | §6 / §4 / §5 / matris / referans taslak | `concept-implementation/` |
| 25–27 Ağustos 2026 | Çapraz privacy pass; K1 birleştirme yorumları | PR yorumu |
| 28–30 Ağustos 2026 | Terminoloji + kaynak son kontrol; final push | Merge-ready K4 paketi |
| Eylül 2026+ (sonraki sprint, bu ödevin teslimi değil) | Prototip gerekirse sentetik v2 / onboarding metinleri | Ayrı görev |

Önerilen günlük ritim (K4, belge haftası): taslak → brief ile grep tutarlılığı → K1’e kısa diff notu. 30 Ağustos 23:59’u tampon bırak; son saat commit yok.

---

## 3. Milestones and Deliverables — K4

| ID | Milestone | Tamamlanma kanıtı | Bu ödevde durum |
|----|-----------|-------------------|-----------------|
| M1 | Data layer documented | Kaynak, alan, KPI bağı, disclaimer tek bölümde | `06_data_sources.md` |
| M2 | Privacy / ethics section ready | Şablon anahtarları (privacy, consent, fairness, transparency, manipulation, brand safety, human oversight) karşılanmış | `05_ethical_responsible_ai.md` |
| M3 | Synthetic generator reproducible | Aşağıdaki komut exit 0; 7 CSV + metadata | mevcut script (16 Ağu teslimi) |
| M4 | Challenges + fallback written | Veri/gizlilik/ölçüm satırları fallback’li | `04_challenges_k4.md` |
| M5 | K1 merge-ready | Yapıştırma haritası + APA | `README.md` + `references_k4.md` |

### M3 doğrulama komutu

```bash
cd data-research/scripts
python3 synthetic_data.py --n 100 --seed 42 --out ./sample_output
```

Beklenen: `students`, `parent_profiles`, `surveys`, `focus_sessions`, `phone_events`, `weekly_metrics`, `parent_intents` + `metadata.json`; `notify_threshold_sec = 600`; disclaimer: sentetik, PII yok, pilot değil.

**Bu ödevde K4 milestone’u olmayanlar:** çalışan mobil izleme, canlı KVKK başvuru süreci, 90g retention ölçümü, yeni ML eğitimi.
