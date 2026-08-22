# 4. Challenges and Mitigation Strategies — K4 satırları

**Sahip:** K4 (yalnızca veri kalitesi, gizlilik, ölçüm, fallback).  
Model/LLM mimarisi, ASR ve tam ürün entegrasyonu K5 satırlarına bırakılır.  
K1 bu tabloyu Implementation Plan §4’e yapıştırır; diğer kişilerin satırlarını buradan uydurmaz.

| Risk | Neden kritik (KPI / pazarlama) | Mitigation | Fallback |
|------|--------------------------------|------------|----------|
| Gerçek LGS/YKS pilot verisi yok | 90 günlük veli retention, trial→paid ve rapor açılma oranı bu aşamada gözlemlenemez; sahte “kanıt” jüri ve marka güvenini bozar | Açık beyan: OULAD + sentetik. Proxy ile gerçek KPI’yı ayır. Datasheet disiplini (Gebru et al., 2021) | Demo ve plan, saha A/B’siz ilerler. Hedef %’ler *plan hedefi*dir, ölçülmüş lift değildir |
| OULAD domain + zaman kayması | UK 2013–14 uzaktan yetişkin OU ≠ 2026 TR ergen + veli aboneliği. Yanlış genelleme yanlış segment ve yanlış müdahale üretir | OULAD yalnızca engagement→olumsuz sonuç *metodolojisi* için. Sentetik ile özellik uzayı karıştırılmaz | LightGBM yoksa kural + segment prior ile risk proxy’si; “TR’de kanıtlandı” iddiası yok |
| Proxy etiket gürültüsü ve sınıf dengesizliği | `final_result` / withdrawal ≠ veli churn. Dengesiz sınıflar şişirilmiş F1 ile yanıltır | PR-AUC / sınıf ağırlığı; etiket sözlüğü; K3 EDA’da dağılım raporu | Basit kural baseline (düşen tıklama, kaçırılan blok, ≥10 dk dağıtıcı) pazarlama anlatısının omurgası olur |
| Sentetik tasarımcı bias’ı ve evaluation leakage | Prior gerçeği yansıtmaz; `segment_label` özelliğe sızarsa metrik şişer; veli mesaj çeşitliliği sınırlıdır | Sabit `seed`, yazılı prior, `metadata.json`, segment’i özellik olarak kullanmama | Küçük elle yazılmış senaryo seti (5 segment × 1 veli metni) demo için yeterli |
| Çocuk verisi + KVKK rıza belirsizliği | Hedef kitlenin önemli bölümü 18 yaş altı. KVKK’de GDPR m.8 benzeri dijital rıza yaşı yok. Hatalı rıza = yasal ve “casus uygulama” churn riski | Temkinli rejim: veli aydınlatması + konuya özgü açık rıza; öğrenciye sade dil; battaniye rıza yok (KVKK Kurumu, 2018) | İzleme kapalıyken anket + tek aksiyon koçluğu çalışır; izleme zorunlu aktivasyon şartı değildir |
| OS-level telefon telemetrisi / mağaza politikası | Gerçek app-süresi izleme Android/iOS ve store kurallarına takılır; 24 saat algısı retention’ı düşürür | Ürün ilkesi: yalnızca odak bloğu; kategori + süre; içerik/URL/ekran yok; eğitim app whitelist | Self-report “dağıldım” + sentetik `phone_events` + 10 dk kuralının demo stub’ı |
| 90 günlük retention’ı bu aşamada ölçememe | Ana KPI’nın sahadaki hareketi yoksa “AI marketing impact” iddiası boş kalır | Öncesi metrikleri tanımla: 48s profil tamamlandı mı, ≥1 odak bloğu, ≥1 aksiyon, rapor açıldı mı | Simüle edilmiş `weekly_metrics` ile rapor *ekranı* gösterilir; lift iddiası ertelenir |
| Yurt dışı LLM aktarımı + çocuğa giden mesajda halüsinasyon | Yanlış “çocuğunuz başarısız” veya utandırıcı dil brand safety ve diyalog benimseme oranını bozar; m.9 aktarım riski | Veli önizlemeli gönderim; suçlayıcı dil yasağı; üretimde aktarım güvencesi yoksa API kapalı | Şablonlu yumuşatma (`parent_intents` çiftleri) + insan onayı; kapalı model sonraya |

### K4 için kritik fallback özeti

1. **Veri:** OULAD (açık, anonim) + seed’li sentetik; uydurma pilot yok.  
2. **İzleme:** Gerçek OS casusluğu yok; odak-içi kural + stub/self-report.  
3. **Model:** LightGBM yoksa kural motoru (10 dk, kaçırılan blok, başlamama) yeterli MVP sinyalidir.  
4. **LLM:** API veya aktarım sorunu varsa kural tabanlı üslup şablonları.  
5. **KPI:** Bu teslimde retention *tasarlanır ve simüle edilir*, ölçülmez.
