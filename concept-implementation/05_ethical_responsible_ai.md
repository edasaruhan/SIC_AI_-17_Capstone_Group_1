# 5. Ethical and Responsible AI Considerations

**Sahip:** K4  
**Bağlam:** Dual-user abonelik ürünü — ödeyen veli, kullanan çoğu durumda 13–18 yaş öğrenci. Ana KPI 90 günlük veli retention’dır; etik tasarım bu KPI’nın *önkoşuludur*: güven kaybı erken churn üretir.

Bu bölüm hukuki mütalaa değildir. Ürün ve plan kararlarını, 6698 sayılı Kanun ilkeleri ve karşılaştırmalı iyi uygulamalarla hizalar.

---

## 5.1 Privacy, consent, personal data

6698 sayılı Kanun m.4; hukuka uygunluk, dürüstlük, doğru ve gerektiğinde güncel olma, belirli-açık-meşru amaç, amaçla bağlantılı-sınırlı-ölçülü işleme ve ilgili süre kadar saklamayı zorunlu kılar. m.3 açık rızayı “belirli bir konuya ilişkin, bilgilendirmeye dayanan ve özgür iradeyle açıklanan rıza” olarak tanımlar. Kurum rehberliğinde belirli konu ve faaliyet işaret etmeyen **battaniye rızalar geçersizdir**; rıza geri alınabilir ve geri alma ileriye etkilidir; ispat yükü veri sorumlusundadır (Kişisel Verileri Koruma Kurumu, 2018).

AI Personal Coach’ta işleme amaçları ayrılır:

| Amaç | Örnek veri | Hukuki tasarım (MVP) |
|------|------------|----------------------|
| Hesap / abonelik | Veli iletişim, ödeme durumu | Sözleşme ifasına yakın, dar kapsam |
| Öğrenci tanıma | Anket, veli serbest metni | Konuya özgü aydınlatma + açık rıza |
| Odak-içi dikkat sinyali | App *kategorisi* + süre | Ayrı rıza; varsayılan kapalı olabilir |
| Veliye anlık bildirim | Eşik aşımı özeti | Ayrı rıza; günlük tavan |
| Öğrenciye LLM mesajı | Niyet metni → yumuşatılmış aksiyon | Ayrı rıza; veli önizleme |
| Haftalık rapor | Agrega metrikler | Aydınlatılmış amaç; utandırıcı dil yok |

Tek “tüm şartları kabul ediyorum” kutusu kullanılmaz. Rıza geri çekildiğinde ilgili işleme durur; izleme kapalıyken anket ve tek-aksiyon koçluğu sürdürülebilir — böylece mahremiyet tercihi ürünü kullanılamaz kılmaz (retention ile çelişmeyen tasarım).

Saklama: amaç kalınca silme, yok etme veya anonimleştirme (m.7). İlgili kişi hakları (m.10–11) için veli kanalı zorunlu, öğrenciye yaşa uygun bilgilendirme tercih edilir. Bu teslimdeki sentetik katmanda gerçek PII yoktur; OULAD zaten anonimleştirilmiştir (Kuzilek et al., 2017).

## 5.2 Çocuk verisi, rıza belirsizliği, çocuğun üstün yararı

Hedef kitlenin önemli bölümü 18 yaş altındadır. KVKK metninde GDPR m.8 benzeri net bir **dijital rıza yaşı yoktur**. Bu belirsizlik “çocuk kendi başına onay verdi” iddiasıyla kapatılmaz. Proje **temkinli rejim** uygular:

1. Yasal temsilci (veli) aydınlatılır; yüksek riskli faaliyetlerde açık rızası alınır.  
2. Öğrenci, “ne toplanır / kim görür / nasıl kapatılır” sorularına kendi yaşında sade dille cevap alır.  
3. Çocuğun üstün yararı (Birleşmiş Milletler Çocuk Haklarına Dair Sözleşme, m.3) — bildirim ve koçluk utandırma, ceza veya ev içi çatışma aracına dönüşmez.

GDPR m.8, bilgi toplumu hizmetlerinde rıza için kural olarak 16 yaş (üye devletlerce en düşük 13) ve veli onayını doğrulamak için makul çaba öngörür (Regulation (EU) 2016/679, Art. 8). Bu hüküm **doğrudan iç hukuk dayanağı değil**, tasarım benchmark’ıdır. ABD COPPA (13 yaş) da aynı şekilde karşılaştırmalı nottur, uygulanacak rejim değildir.

Ayırt etme gücüne ilişkin doktrin tartışması (kişisel verinin nispi kişiye sıkı sıkıya bağlı hak sayılması) ürünü “yalnızca çocuk onaylasın” noktasına çekmez. Dual-user yapıda veli zaten ödeyen ve bildirim alıcısıdır; bu, velinin çocuğu sınırsız izleme hakkı olduğu anlamına gelmez.

## 5.3 Fairness / bias

OULAD seçim bias’ı taşır: uzaktan, ağırlıklı yetişkin, 2013–14 VLE. Mobil 2026 dikkat dağılması, sınav kaygısı ve TR ev içi dinamik temsil edilmez (Kuzilek et al., 2017; Mehrabi et al., 2021). Sentetik katman kontrollü prior ile üretilir; prior tasarımcı varsayımıdır, saha dağılımı değildir. Riskler:

- Segment etiketinin damgalayıcı kullanımı (“bu çocuk tembel”).  
- `segment_label`’ın modele özellik olarak sızması (evaluation leakage).  
- Kaygıyla erteleyen / geceye kayan profillerde aşırı bildirim.  
- OULAD + sentetik metriklerin birleştirilerek “kanıt” gibi sunulması.

Önlem: iki kaynağı ayrı raporlamak; segmenti koçluk *hipotezi* olarak tutmak; özellik ve etiket sözlüğünü yazmak (Gebru et al., 2021); üretim iddiası taşımamak.

## 5.4 Transparency / explainability

Veliye giden risk veya uyarı kara kutu skor olamaz. Her dikkat bildirimi ve haftalık özet **1–2 sade gerekçe** taşır: örneğin “odak bloğunda sosyal kategoride 12 dakika” — teşhis koymaz, niyet okumaz. Öğrenci aynı olayı “velin X’i görür” şeffaflığıyla bilir. Yorumlanabilirlik hem etik hem pazarlamadır: veli neden ödediğini anlamazsa 90 gün kalmaz.

## 5.5 Manipulation risk and brand safety

Ürünün pazarlama vaadi “sizin yerinize bağırmadan ulaşır”dır. Bu, velinin kaygısını **ölçekleyerek baskı uygulamak** için kullanılamaz.

Kurallar:

- Suçlayıcı, kıyaslayan, tehdit eden dil yok.  
- Öğrenciye giden çıktıda **tek net aksiyon** vardır.  
- Velinin endişesi korunur, üslup yumuşatılır.  
- “Çocuğunuz YKS’yi kaybedecek” gibi spekülatif kehanet yok.  
- Plan belgesindeki sektör kıyasları ve hedef yüzdeler **plan hedefidir**; üretimde kanıtlanmış lift gibi sunulmaz.

LLM halüsinasyonu burada marka ve çocuk güvenliği riskidir. Ham model çıktısı öğrenciye otomatik gitmez.

## 5.6 Human oversight

İnsan devrede kalır:

- Veli, AI’nın ürettiği öğrenci mesajını **göndermeden önce görür**.  
- 10 dakika eşiği + günlük bildirim tavanı + sessiz saat.  
- Eğitim uygulamaları whitelist; odak dışı log yok.  
- İzleme kapatılabilir; koçluk (anket + aksiyon) sürer.  
- Yüksek riskli veya belirsiz vakada sistem sessiz kalmayı tercih eder (fail-safe), ek baskı üretmez.

## 5.7 Zararlı veya yanıltıcı pazarlama çıktısından kaçınma

Retention döngüsü (haftalık rapor, bildirim, üslup dönüştürme) **görünür değer** üretmek içindir, korku pazarlaması için değil. Yasak örnekler: sahte ilerleme grafiği, uydurma “uzman teşhisi”, çocuğu velinin önünde teşhir, 24 saat izleme vaadi. İzinli örnek: “Bu hafta 12 aksiyondan 7’si tamamlandı. Dikkat uyarısı: 4. Öneri: gündüz 2 kısa blok.”

## 5.8 Odak-sınırlı izleme ilkeleri (özet kutu)

| İlke | Uygulama |
|------|----------|
| Amaç bağları | Yalnızca öğrencinin başlattığı odak/ders bloğu |
| Minimizasyon | Kategori + süre; içerik, URL, mesaj, ekran, konum yok |
| Whitelist | Eğitim (ve iletişim) uygulamaları uyarı üretmez |
| Eşik | Dikkat dağıtıcı kategoride ≥10 dakika (600 sn) |
| Orantılılık | Günlük tavan; yargısız dil; önce öğrenci nudge, sonra veli özeti |
| Kapatılabilirlik | Rıza geri alma; izlemesiz koçluk yolu |
| Demo gerçeği | Bu teslimde `phone_events` sentetiktir; OS casusluğu yoktur |

## 5.9 Aktarım ve üçüncü taraf modeller

Üretimde LLM API’si yurt dışındaysa m.9 kapsamında yeterlilik veya uygun güvence (ör. standart sözleşme) olmadan çocuk/veli içeriği gönderilmez. Fallback: şablonlu yumuşatma + insan onayı; API kapalı demo.

## 5.10 AI disclosure

Bu K4 bölümleri AI destekli taslak ve insan düzenlemesiyle yazılmıştır. Yasal atıflar birincil metinlere (6698 sayılı Kanun; KVKK açık rıza duyurusu; GDPR m.8; OULAD makalesi) dayandırılmış, uydurma kurul kararı eklenmemiştir. Final birleştirmede bu satır korunmalıdır.
