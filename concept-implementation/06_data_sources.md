# 6. Data Sources

**Sahip:** K4 — Data Governance + Synthetic Data  
**Kaynak teslim:** `data-research/02_governance.md`, `data-research/scripts/synthetic_data.py`  
**Durum:** Gerçek saha / pilot verisi **yoktur.**

---

AI Personal Coach’un pazarlama problemi — velinin ürün değerini görmeden ilk 30–90 günde aboneliği bırakması — iki katmanlı bir veri omurgasına bağlanır. Birinci katman **OULAD (Open University Learning Analytics Dataset)**’tır: 2013–2014 döneminde 22 module-presentation, 32.593 öğrenci ve 10.655.280 günlük VLE tıklama özetini (`studentVle`) demografi, kayıt ve değerlendirme tablolarıyla birleştiren, CC-BY 4.0 lisanslı açık bir learning-analytics benchmark’ıdır (Kuzilek et al., 2017). Format tablo/CSV’dir; kritik alanlar günlük `sum_click` engagement’ı, assessment sonuçları ve `final_result` / withdrawal etiketleridir. Bu katman, LightGBM risk skorunun **metodolojik omurgasını** taşır: düşük ve düşen etkileşim, olumsuz öğrenme sonucu için proxy’dir ve abonelik dilinde erken churn *risk tasarımına* çevrilir. OULAD, İngiltere’de uzaktan öğrenen ağırlıklı olarak yetişkin bir popülasyonu tanımlar; LGS/YKS ergeni, TR aile yapısı, veli metni, anket veya uygulama düzeyi telefon sinyali içermez. Bu nedenle `final_result` **veli churn’ü ölçmez**; proxy etikettir ve 90 günlük veli retention bu setle kanıtlanamaz.

İkinci katman, OULAD’da olmayan ürün akışlarını dolduran **sentetik veri**dir. `data-research/scripts/synthetic_data.py` (Python 3.10+, yalnızca standart kütüphane) sabit `--seed` ile tekrarlanabilir CSV üretir; kimlikler `stu_0001` / `par_0001` biçimindedir, gerçek PII yoktur. Beş kilitli davranış segmentine (başlayamayan, yarıda bırakan, telefonla dağılan, kaygıyla erteleyen, geceye kayan) göre prior’lar uygulanır. Ön işleme bilinçli olarak dardır: OULAD ve sentetik özellik uzayları **karıştırılmaz**; sentetik `segment_label` değerlendirme sızıntısını önlemek için model özelliği değil üretim etiketidir; `notify_flag` ancak odak bloğu içinde, dikkat dağıtıcı kategoride ve `duration_sec >= 600` (10 dakika) iken true olur; eğitim ve iletişim uygulamaları uyarı üretmez. Çıktılar pazarlama KPI’larına şöyle bağlanır: veli serbest metni ve anketler segment + üslup çerçevesini (kişiselleştirme, diyalog benimseme); odak oturumları aksiyon tamamlama oranını; `phone_events.notify_flag` bildirim yanıtı / dikkat uyarısı döngüsünü; `weekly_metrics` haftalık rapor açılma loop’unun metrik iskeletini taşır. Trial→paid ve LTV/CAC bu aşamada gözlemlenmez.

Erişim, rıza ve sorumlu kullanım bu teslimde **tasarım kararı** olarak belgelenir, saha onamı olarak değil. OULAD zaten anonimleştirilmiş açık veridir. Sentetik katman gerçek öğrenci/veli kaydı üretmez. Üretim senaryosunda abonelik hesabı dar sözleşme ifasıyla ilişkilendirilebilir; buna karşılık odak-içi dikkat sinyali, veliye anlık bildirim ve LLM ile öğrenciye mesaj iletimi konuya özgü açık rıza ve ayrı aydınlatma gerektirir (Kişisel Verileri Koruma Kurumu, 2018; 6698 sayılı Kanun). İzleme yalnızca öğrencinin başlattığı odak bloğunda aktiftir; blok dışı kayıt yoktur. Ayrıntı Implementation Plan §5’tedir.

| Kaynak | Tip / format | Kritik alanlar | Pazarlama / KPI bağı | Ana sınır |
|--------|----------------|----------------|----------------------|-----------|
| OULAD (Kuzilek et al., 2017) | Açık, anonim tablo; günlük VLE aggregate | `sum_click`, assessment, `final_result` / withdrawal | Risk modeli metodolojisi; engagement → olumsuz sonuç proxy’si → erken müdahale tasarımı | UK 2013–14 yetişkin OU; TR LGS/YKS ve veli churn değil |
| Sentetik ürün katmanı (`synthetic_data.py`, şema 1.0.0) | Seed’li CSV + `metadata.json` | `segment_label`, anket, `planned_min`/`completed_min`, `app_category`, `duration_sec`, `notify_flag`, `risk_avg`, `raw_text_tr`/`softened_text_tr` | Segmentasyon, mesaj framing, bildirim eşiği, haftalık rapor iskeleti, üslup dönüştürme demo’su | Tasarımcı prior’ı; saha dağılımını temsil etmez; retention kanıtı değildir |

### Sentetik çıktı envanteri

| Dosya | Rol |
|-------|-----|
| `students.csv` | `exam_track` (LGS/YKS), `age_band`, `chronotype`, `segment_label`, `risk_prior` |
| `parent_profiles.csv` | Veli serbest metni (`free_text_tr`), `tone_hint` |
| `surveys.csv` | Öğrenci ve veli maddeleri + haftalık mini anket |
| `focus_sessions.csv` | Planlanan / tamamlanan dakika, `start_hour`, `abandoned` |
| `phone_events.csv` | Kategori + süre; `in_focus_block`; `notify_flag` (≥600 sn dağıtıcı) |
| `weekly_metrics.csv` | `risk_avg`, `actions_done` / `actions_missed`, `distraction_count`, `top_distractor_category` |
| `parent_intents.csv` | Sert veli niyeti → yumuşatılmış, tek aksiyonlu mesaj çifti |
| `metadata.json` | `seed`, `schema_version`, sayımlar, **pilot değildir** uyarısı |

**Ön işleme özeti.** OULAD tarafında (K3 EDA ile hizalı) eksik değer ve sınıf dağılımı raporlanır; dengesiz `final_result` için sınıf ağırlığı veya PR-AUC tercih edilir; proxy etiket şeffaf beyan edilir. Sentetik tarafta üretim kuralı yazılıdır, `schema_version` sabittir, gerçek ad/telefon/konum üretilmez. İki kaynaktan gelen metrikler ayrı raporlanır; birleşik “kanıtlanmış retention lift” tablosu kurulmaz.

**Sonuç cümlesi.** Bu teslim için veri, demo ve plan belgesi düzeyinde yeterlidir: risk pipeline’ı tekrarlanabilir, ürün şeması uçtan uca gösterilebilir, gizlilik kısıtları belgelenebilir. **90 günlük veli retention, trial→paid dönüşümü veya bildirim yanıt oranı bu veriyle ölçülmez**; sonraki etik/onamlı dar pilot olmadan pazarlama etkisi iddiası taşınmaz.
