# Concept Note and Implementation Plan — K4 teslim paketi

**Ödev:** AI in Marketing Capstone — Concept Note and Implementation Plan  
**Deadline:** 30 Ağustos 2026, 23:59 (İstanbul)  
**Rol:** Kişi 4 — Data Governance + Synthetic Data + Responsible AI  
**Ürün:** AI Personal Coach  
**Branch:** `feat/data-governance-k4`

Bu klasör, şablonun **K4’e düşen bölümlerini** merge-ready metin olarak içerir. Ortak tek dosyaya yazılmamıştır; K1 final belgeyi birleştirir.

---

## K1 yapıştırma haritası

| Bu dosya | Şablondaki yer |
|----------|----------------|
| [`06_data_sources.md`](06_data_sources.md) | Concept Note **§6 Data Sources** (tam bölüm) |
| [`04_challenges_k4.md`](04_challenges_k4.md) | Implementation Plan **§4 Challenges** — yalnızca veri / gizlilik / ölçüm / fallback satırları |
| [`05_ethical_responsible_ai.md`](05_ethical_responsible_ai.md) | Implementation Plan **§5 Ethical and Responsible AI** (tam bölüm) |
| [`k4_timeline_matrix.md`](k4_timeline_matrix.md) | **§1** tech stack satırı + **§2** K4 matris/Gantt satırları + **§3** K4 milestone’ları |
| [`references_k4.md`](references_k4.md) | **§6 References** — K4 kaynakları (APA) |

K4 **yazmaz:** Concept Note §1–3, §4 AI Methodology, §5 mimari diyagram, §7 Literature. Bu bölümler K1 / K2 / K5 sorumluluğundadır.

---

## Kilitli terminoloji (brief ile aynı)

- Ana KPI: **90 günlük veli retention**
- Dual-user: ödeyen = veli; kullanan = öğrenci
- Segmentler: başlayamayan / yarıda bırakan / telefonla dağılan / kaygıyla erteleyen / geceye kayan
- Veri: OULAD + sentetik; **gerçek pilot verisi yok**
- İzleme: yalnızca odak bloğunda; eğitim uygulamaları uyarı üretmez; eşik 10 dakika (600 sn)

---

## Önceki teslimle ilişki

Metinler `data-research/02_governance.md` ve `data-research/scripts/synthetic_data.py` üzerine **sıkıştırılıp plan diline** çevrilmiştir. Yeni saha verisi üretilmemiştir.

---

## AI disclosure

K4 bölümleri AI destekli taslak + insan düzenlemesi ve kaynak kontrolü ile hazırlanmıştır. Şablonun “If this document is created directly by AI please highlight” maddesi gereği final belgede bu not korunmalıdır.
