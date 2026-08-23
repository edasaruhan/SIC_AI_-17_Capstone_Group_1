# §4 — Teknik Zorluklar ve Risk Değerlendirmesi (K5 Satırları)

**Proje:** AI Personal Coach  
**Yazar:** K5 — Methodology, Mimari, Stack  
**Hazırlayan:** Berat Erol ÇelİK  
**Tarih:** 2026-08-23  
**Not:** K3 ve K4'ün risk satırları bu dosyada tekrarlanmamıştır. K3'ün挑战ları `04_challenges_k3.md`, K4'ün挑战ları `concept-implementation/04_challenges_k4.md` dosyasındadır.

---

## K5 Risk Tablosu

| Risk | Neden (KPI Etkisi) | Mitigation (Önleyici Tedbir) | Fallback (Çöküş Durumunda) |
|------|---------------------|------------------------------|---------------------------|
| **LLM halüsinasyon / utandırıcı çocuk mesajı** | Brand safety, veli-öğrenci diyalog güveni, hukuki risk. Yargılayıcı veya vaatkar bir mesaj velinin paniklemesine ve aboneliği bırakmasına yol açar. | (a) Temperature=0.2 ile tutarlı üslup; (b) Kural bazlı filtre: "kesin", "garanti", "yüzde yüz" kelimeleri engellenir; (c) Velinin gönderiminden önce insan önizlemesi (editör onayı); (d) LLM çıktıları Validator Agent tarafından 3 kural üzerinden denetlenir (yargılama yok, KVKK aykırılık yok, pazarlama garantisi yok). | Yalnızca statik şablon `INTENT_SOFT` kullanılır. |
| **Over-automation / bildirim yorgunluğu** | Haftalık rapor açılma oranında düşüş, iptal (churn) artışı. Aşırı bildirim, uygulamanın sessize alınmasına veya silinmesine yol açar. | (a) 10 dk eşik + günlük bildirim tavanı (öğrenciye günde en fazla 1); (b) Veliye haftada en fazla 2 proaktif mesaj; (c) Sessiz saat: gece 22:00–09:00 arası veliye bildirim geciktirilir; (d) "Güvenli Liste" (whitelist) ile eğitim uygulamaları bildirim üretmez. | O gün veliye bildirim gönderilmez; öğrenciye yalnızca tek bir nudge. |
| **API maliyeti / latency / vendor bağımlılığı** | Ölçek büyüdükçe maliyet artışı. Demo sırasında API kesintisi veya yavaşlama (GPT-3.5 Turbo'da 2–3 sn gecikme). | (a) Kullanıcı başına aylık maliyet tavanı ($0.05); (b) LLM çağrısı yalnızca gerektiğinde (profil + rapor + bildirim metni, ayda 20–30 çağrı); (c) Pre-computation: haftalık rapor, gönderilmeden 1 saat önce hazırlanır; (d) Gecikme 3 sn'yi aşarsa timeout. | Statik şablon (`INTENT_SOFT`) veya açık kaynak model (fine-tuned Llama 3, Gelecek aşama). |
| **Brand safety (sert veli metninin öğrenciye sızması)** | Veli güveni, platform itibarı, churn riski. Veli皋至孩子写的沉重负罪感的暴力、否定性言论 doğrudan öğrenciye iletilirse ciddi psikolojik ve marka riski doğurur. | (a) Ham veli metni öğrenciye asla doğrudan iletilmez; (b) LLM üslup dönüştürme katmanından geçmeden hiçbir mesaj gönderimi yapılmaz; (c) İnsan onayı (veli önizlemesi) olmadan gönderim gerçekleşmez; (d) Kural bazlı yasaklı kelime filtresi. | Mesaj gönderilmez; veliye yalnızca "Bu haftaki raporunuz hazır" statik bildirimi gider. |
| **Marketing impact ölçememe (saha verisi olmaması)** | Ana KPI (90g retention) bu veri setiyle ölçülemez. Jüri "nasıl kanıtlayacaksınız?" sorusuna yanıt bekler. | (a) Öncesi metrikler tanımlanmıştır (48 saat profil, ≥1 odak bloğu, ≥1 aksiyon, rapor açılma); (b) Korelasyon analizi: `parent_report_open_rate` ile `churn_90d` arasında -0.64 negatif korelasyon (K3 EDA); (c) Bu metrikler "leading indicator" olarak raporlanır. | Simülasyon + dürüst limit beyanı: "Bu bir plan hedefidir, saha doğrulaması Katman B'de yapılacaktır." |
| **Proxy → üretim sıçraması / domain shift** | OULAD (UK 2013–14 yetişkin) ile Türkiye 2026 LGS/YKS arasında yapısal fark. Model canlı veride beklendiği kadar başarılı olmayabilir. Yanlış müdahale riski. | (a) OULAD ile sentetik veri metrikleri **ayrı** raporlanır (birleştirilmez); (b) SHAP yorumlanabilirliği ile hatalı feature'lar tespit edilir; (c) Modelin embarrassingly simple baseline (lojistik regresyon) ile karşılaştırması K3 tarafından sağlanır. | Kural-first MVP: LLM ve LightGBM devre dışı bırakılır, yalnızca 10 dk kural motoru ile minimal bildirim sistemi çalışır. |

---

## Ek Notlar

### Proxy Etiket Uyarısı

Tüm risk modeli sonuçları `final_result` / withdrawal proxy etiketi üzerindedir. Bu etiket:
- **Öğrenme sonucu proxy'sidir**, veli churn değildir.
- OULAD, UK 2013–14 uzaktan yetişkin popülasyonundan elde edilmiştir; LGS/YKS'ye genellenemez.
- Bu sayılar 90 günlük veli retention kanıtı değildir; yalnızca metodoloji demonstrasyonudur.

### ASR (Sesli Görüşme) Notu

ASR modülü P2 aşamasına aittir. Bu 2 aylık MVP'de zorunlu değildir. Detaylı teknik risk değerlendirmesi Katman B'de yapılacaktır.

### İnsan Önizlemesi (Human-in-the-Loop)

LLM'in ürettiği her veli mesajı, gönderilmeden önce bir insan (editör veya ürün yöneticisi) tarafından kontrol edilir. Bu, K4'ün `05_ethical_responsible_ai.md` dosyasında belgelenen "veli gönderim önizlemesi" prensibinin teknik karşılığıdır.
