# PoC Fixture Test Veri Seti ve Veri Yönetişimi (K4)

Bu dizin, K5 uçtan uca PoC pipeline'ı (`poc_pipeline.py`) ve testleri için hazırlanan kontrollü, izlenebilir ve sentetik 15 öğrenci/veli test verisini içerir.

## 1. Veri Türleri ve Ayrımı

Repo genelinde veri kaynakları üç katmana ayrılmıştır:

1. **OULAD Proxy Data (`oulad_synthetic_processed.csv`):**
   - Açık kaynaklı İngiltere Açık Üniversitesi (Open University UK) etkileşim kayıtlarının LGS/YKS özelliklerine uyarlanmış vekili (proxy).
   - Türkiye'deki veli abonelik terk verisi değildir; makine öğrenmesi baseline modellerini test etmek için proxy olarak kullanılır.
2. **Sentetik Test Verisi (`poc_students.json` & `poc_students.csv`):**
   - PoC uçtan uca akışının, segmentasyonun ve kural motorunun doğrulanması için hazırlanmış sabit fixture'lardır.
   - Hiçbir gerçek kişisel veri (PII) içermez.
3. **Gerçek Pilot Verisi (Real Pilot Data):**
   - Henüz mevcut değildir; ileride okul veya dershane pilot uygulamalarıyla elde edilecektir.

---

## 2. Test Fixture Persona Dağılımı

15 öğrenci, pedagojik literatürde tanımlanan 5 davranışsal persona üzerinden eşit ve dengeli olarak dağıtılmıştır:

| Segment | Öğrenci ID'leri | Tipik Davranış Kalıbı |
| :--- | :--- | :--- |
| **Başlayamayan** | `STU_001`, `STU_006`, `STU_012` | Düşük VLE tıklaması, kısa odak süresi, yüksek ders başlatma ataleti |
| **Telefonla Dağılan** | `STU_002`, `STU_007`, `STU_011` | 10 dk+ telefon dikkat dağılması yüksek, odak bölünmesi sık |
| **Geceye Kayan** | `STU_003`, `STU_008`, `STU_013` | Gece 22:00 sonrası yüksek aktivite (`night_study_ratio` > 0.75) |
| **Yarıda Bırakan** | `STU_004`, `STU_009`, `STU_014` | Başlangıçta aktif ancak 15 dakikada bloğu terk eden |
| **Kaygıyla Erteleyen** | `STU_005`, `STU_010`, `STU_015` | Yüksek kaygı puanı (`anxiety_survey_score` > 8.0), ödev erteleme |

---

## 3. KVKK ve Veri Gizliliği Güvencesi

- **Sıfır Gerçek PII:** İsimler jenerik Türkçe sentetik isimlerdir (`Ali`, `Zeynep`, `Mert` vb.).
- **Doğrudan Tanımlayıcı Yok:** TC Kimlik No, telefon numarası, IP adresi veya e-posta adresi gibi hiçbir kişisel veri yer almaz.
- **Minimalist Veri Toplama:** Yalnızca churn tahmini ve koçluk mesajı tetiklemesi için gerekli olan davranışsal metrikler işlenir.
