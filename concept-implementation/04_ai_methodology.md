# §4 — AI Metodolojisi: Hibrit Risk, Kural ve Üslup Katmanı

**Proje:** AI Personal Coach  
**Yazar:** K5 — Methodology, Mimari, Stack  
**Hazırlayan:** Berat Erol ÇelİK  
**Tarih:** 2026-08-23  
**Kullanılan Veri:** OULAD (proxy) + sentetik; **gerçek pilot verisi yoktur.**

---

## 4.1 Yaklaşım ve Pazarlama Hedefi

AI Personal Coach, öğrencilerin dijital davranışlarını yorumlayarak velilere ölçülebilir erken değer üreten üç katmanlı bir yapay zeka sistemi üzerine kurulmuştur. Her katman, pazarlama hunisinin (funnel) farklı bir aşamasına ve bir KPI'ya doğrudan hizmet eder.

**Birinci Katman — LightGBM Risk Modeli.** LightGBM (Light Gradient Boosting Machine), öğrenci davranışlarından (tıklama akışları, oturum süreleri, pasif kalma anları) yola çıkarak kopma riskini ve beş davranış segmentini (başlayamayan, yarıda bırakan, telefonla dağılan, kaygıyla erteleyen, geceye kayan) sınıflandırır. Amaç, müdahale zamanlamasını optimize ederek 90 günlük veli retention oranını artırmaktır. Model, SHAP (SHapley Additive exPlanations) değerleriyle veliye "neden yüksek risk?" sorusunu eyleme dönüştürülebilir şekilde yanıtlar. Örneğin, SHAP analizi `phone_distraction_10min_count` değişkeninin risk skoruna %34 katkı sağladığını gösterirse, sistem bu bilgiyi LLM katmanına "Telefonla Dağılan" segment etiketi olarak aktarır.

**İkinci Katman — Kural Motoru (Rule Engine).** Belirli eşik değerleri doğrudan tetikleyen deterministik bir karar katmanıdır. Ana kural: öğrenci odak bloğunda dikkat dağıtıcı kategoride (sosyal medya, oyun vb.) **≥10 dakika (600 saniye)** kaldığında bildirim adayı üretilir. Bu süre, "casusluk" algısını önlemek ve orantılı bir uyarı sunmak için belirlenmiştir. Kural motoru ayrıca günlük bildirim tavanını kontrol eder; bir öğrenciye günde birden fazla bildirim gönderilmez. Gece 22:00–09:00 arasında veliye bildirim gönderilmez (cool-off periyodu). Bu katman, **Bildirim Aksiyonu Tamamlama Oranı** metriğini doğrudan etkiler.

**Üçüncü Katman — LLM Üslup Dönüştürme.** OpenAI GPT-3.5 Turbo tabanlı büyük dil modeli, üç görevi yerine getirir: (a) veli anketi ve sistem içi verilerle kısa öğrenci profili üretir; (b) velinin potansiyel olarak yargılayıcı veya baskıcı niyetini tek aksiyonlu, özerklik destekleyici (autonomy-supportive) motive mesaja dönüştürür; (c) haftalık veli raporu için kişiselleştirilmiş koçluk cümlesi oluşturur. Temperature 0.2 ile sabit, tutarlı ve pedagojik bir üslup hedeflenir; "kesin", "garanti", "yüzde yüz" gibi hukuki risk taşıyan kelimeler kural filtresiyle engellenir. LLM, **Diyalog Benimseme Oranı** ve **Haftalık Rapor Açılma Oranı** metriklerini artırmak için tasarlanmıştır.

**Sesli Görüşme (ASR):** Öğrencinin sesli notlarından duygu analizi, OpenAI Whisper kullanılarak planlanmıştır ancak bu modül **P2 aşamasına** aittir; 2 aylık MVP'de zorunlu değildir. KVKK uyumluluğu gözetilerek yalnızca aktif opt-in ile devreye alınacaktır.

---

## 4.2 Bileşen → KPI Eşlemesi

| Bileşen | Pazarlama İşi | Birincil KPI | İkincil KPI |
|---------|---------------|-------------|-------------|
| LightGBM risk modeli | Erken risk tespiti → doğru zamanda müdahale | 90g veli retention (tasarım) | Aksiyon tamamlama oranı |
| Kural motoru (10 dk eşiği) | Orantılı dikkat uyarısı | Bildirim aksiyonu tamamlama | Rapor `distraction_count` |
| LLM üslup dönüştürme | Çatışmasız iletişim | Veli-öğrenci diyalog benimseme | Trial→paid (değer algısı) |
| LLM rapor metni | Haftalık görünürlük ve değer kanıtı | Haftalık rapor açılma oranı | 90g retention |
| İnsan önizleme (veli gönderim onayı) | Brand safety ve yanlış tonu önleme | (Koruyucu) | Churn'ü artıran skandalı engeller |

Her bileşen, pazarlama KPI'sına bağlıdır. AI, salt bir analitik araç değil, abonelik retention döngüsünün her aşamasında ölçülebilir değer üreten bir pazarlama mekanizması olarak konumlandırılmıştır.

---

## 4.3 Neden Bu Stack

- **Az etiketli Türkçe veri problemi:** Türkiye'de eğitim alanında etiketlenmiş,(segmentlenmiş) büyük ölçekli veri setleri sınırlıdır. LightGBM, küçük ve orta ölçekli veri setlerinde yüksek performans gösteren, hiperparametre ayarlaması kolay bir algoritmadır.
- **İki aylık MVP zaman baskısı:** Derin öğrenme (Transformer, LSTM) modellerinin eğitilmesi, ince ayarlanması ve production'a alınması daha uzun sürer. LightGBM, CPU tabanlı çıkarım ile ~4 ms gecikme süresinde çalışarak zaman kazandırır.
- **Veliye açıklanabilirlik:** LightGBM, doğal yorumlanabilirlik (feature importance + SHAP) sunar. "Neden çocuğumun risk skoru yüksek?" sorusu, veliye "telefon dağıtıcı kullanım 10 dakikayı aştı" gibi somut, eyleme geçirilebilir bir gerekçeyle yanıtlanabilir.
- **Maliyet optimizasyonu:** GPT-3.5 Turbo, GPT-4'ün yaklaşık 1/20 maliyetine çalışır. Abonelik bazlı bir üründe LTV/CAC oranını korumak için maliyet kontrolü kritiktir.
- **Domain shift riski:** OULAD (2013–14 İngiltere) ile Türkiye 2026 LGS/YKS arasındaki yapısal fark, derin öğrenmenin avantajını azaltır; basit ve yorumlanabilir modeller production'da daha dayanıklıdır.

---

## 4.4 Değerlendirme Planı

### Teknik Değerlendirme

| Bileşen | Metrik | Kaynak | Not |
|---------|--------|--------|-----|
| LightGBM | PR-AUC veya ROC-AUC, F1 | K3 baseline tablosu (K3 `04_challenges_k3.md`) | Proxy etiket (`final_result` / withdrawal) üzerinde |
| Kural motoru | Precision of notify (eşik 600 sn) | Sentetik `phone_events` verisi | `notify_flag` sütunu |
| LLM üslup | Türkçe rubrik: suçlama yok, tek aksiyon, yaşa uygun | İnsan değerlendirmesi (3 evaluator) | + latency (hedef <3 sn) + maliyet/kullanıcı/ay |

**Kural motoru precision'ı:** Odak bloğunda ≥10 dakika dikkat dağıtıcı kullanım durumlarında bildirim gönderme hassasiyeti (precision) hesaplanır. Yanlış pozitif (okul uygulamasını "telefon" olarak algılama) oranı düşük tutulmalıdır; bu amaçla "Güvenli Liste" (whitelist) mekanizması devreye alınır.

**LLM maliyet tahmini:** Kullanıcı başına aylık ortalama 20–30 LLM çağrısı (haftalık rapor + profil + bildirim metni) ile maliyet kullanıcı başına aylık < $0.05 olarak hesaplanmaktadır.

### Pazarlama Değerlendirme

Bu teslimde saha A/B testi yoktur. **90 günlük veli retention bu veri setiyle ölçülemez.** Öncesi metrikler (önceki sprintlerde tanımlanmıştır):
- 48 saatte öğrenci profili oluşturulma oranı
- ≥1 odak bloğu başlatma oranı
- ≥1 aksiyon tamamlama oranı
- Haftalık rapor açılma oranı

Bu metrikler, retention'ın "ön göstergeleri" (leading indicators) olarak tasarlanmıştır; son göstergeler (lagging indicators) Katman B'deki saha verisiyle doğrulanacaktır.

---

## 4.5 Baseline / Karşılaştırma

### Risk Modeli Karşılaştırması

K3 tarafından sağlanan baseline sonuçları (K3 `04_challenges_k3.md` tablosu) esas alınmıştır. K3 henüz tam tabloyu teslim etmediyse, aşağıdaki satırlar "önceki taslak / plan hedefi" olarak işaretlenir:

| Model | Etiket | n / split | Metrik | Sayı | Durum |
|-------|--------|-----------|--------|------|-------|
| Lojistik Regresyon | `final_result` olumsuz / withdrawal (proxy) | K3 tarafından belirlenecek | ROC-AUC, F1 | K3 tarafından sağlanacak | K3'e bağlı |
| LightGBM | aynı proxy etiket | aynı split | aynı metrik | K3 tarafından sağlanacak | K3'e bağlı |

**Önemli not:** `final_result` / withdrawal etiketi **veli churn değildir**; öğrenme sonucu proxy'sidir. OULAD, UK 2013–14 uzaktan yetişkin popülasyonundan elde edilmiştir; LGS/YKS'ye genellenemez. Bu nedenle Lojistik Regresyon'un LightGBM'i geçtiği durumlarda bile LightGBM tercih edilir; çünkü asıl avantaj metriklerde değil, SHAP yorumlanabilirliğinde ve segment atama kapasitesindedir.

README'deki "AUC ~0.78" gibi cümleler, K3 tarafından doğrulanmadığı sürece "önceki taslak / plan hedefi" olarak işlenir.

### LLM Karşılaştırması

| Yöntem | avantaj | dezavantaj |
|--------|---------|------------|
| `parent_intents` şablon çifti (statik) | Sıfır maliyet, sıfır gecikme | Kişiselleştirme yok, tekdüze dil |
| GPT-3.5 Turbo API | Kişiselleştirilmiş üslup, segment-duyarlı | API maliyeti, gecikme, halüsinasyon riski |

 MVP'de her iki yöntem de kullanılabilir: statik şablon fallback olarak hazır bekletilir, LLM API çağrılamazsa veya zaman aşımı olursa devreye girer.

### ASR Karşılaştırması

ASR (sesli görüşme) modülü P2'de değerlendirileceğinden, bu aşamada detaylı karşılaştırma yapılmamıştır. Tek cümle: "Sesli veli görüşmesi, ileri aşamada Whisper tabanlı duygu analiziyle zenginleştirilebilir; MVP'de zorunlu değildir."
