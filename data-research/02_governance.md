# Data Research — Data Governance, Quality, Privacy and Limitations

**Project:** AI Personal Coach  
**Author role:** K4 — Data Governance + Synthetic Data  
**Version:** 1.2 (final for submission package)  
**Date:** 2026-08-15  

---

## 1. Introduction

AI Personal Coach, LGS ve YKS sürecindeki öğrencilere kişiselleştirilmiş tek aksiyon sunan; **ödeyen müşterisi veli**, **kullananı öğrenci** olan ikili kullanıcılı (dual-user) bir abonelik ürünüdür. Pazarlama problemi, velinin ürün değerini göremeden ilk bir-iki ayda aboneliği bırakmasıdır (erken churn). Ana KPI **90 günlük veli retention**’dır. Destekleyici metrikler trial→paid dönüşümü, haftalık rapor açılma oranı, bildirim yanıt oranı ve aksiyon tamamlama oranını kapsar.

Bu KPI’lar yalnızca tahmin modelinin F1 skoruna değil; **güvenilir, hukuka uygun ve şeffaf veri pratiğine** bağlıdır. Yanlış risk skoru, orantısız bildirim veya “casus uygulama” algısı güveni aşındırır ve retention’ı bozar. Bu nedenle veri katmanı iki parçalıdır:

1. **OULAD (Open University Learning Analytics Dataset)** — açık ve anonimleştirilmiş learning-analytics benchmark’ı; VLE engagement ile olumsuz sonuç (`final_result` / withdrawal) ilişkisi üzerinden risk modellemesi metodolojisi için (Kuzilek et al., 2017).
2. **Sentetik veri** — OULAD’da olmayan veli serbest metni, anket cevapları, odak oturumları ve odak bloğu içi telefon/dikkat sinyalleri; beş davranış segmentine (başlayamayan, yarıda bırakan, telefonla dağılan, kaygıyla erteleyen, geceye kayan) göre üretilir.

**Gerçek pilot verisi bu teslimde yoktur.** Ürün-spesifik akışlar sentetiktir; OULAD proxy ve tekrarlanabilir deney omurgasıdır. Bu bölümün amacı, hangi verinin neden gerekli olduğunu; kalite ve bias risklerini; KVKK ve çocuk verisi bağlamında mahremiyet tasarımını; genelleme sınırlarını ortaya koymaktır.

---

## 3. Data Quality, Privacy and Limitations

### 3.1 Data quality

**OULAD.** 2013–2014 döneminde 22 module-presentation, 32.593 öğrenci ve 10.655.280 günlük VLE tıklama özeti (`studentVle`) içerir; demografi (`studentInfo`), kayıt, assessment ve VLE tabloları kimlik alanlarıyla birleştirilir (Kuzilek et al., 2017). Kalite riskleri: (i) seyrek tıklama ve eksik/genelleştirilmiş demografi bantları; (ii) `final_result` sınıflarında dengesizlik; (iii) **günlük aggregate** `sum_click` alanının, ürünün 10 dakikalık uygulama eşiği gibi ince taneli dikkat olaylarını temsil edememesi; (iv) `final_result` / withdrawal etiketinin “erteleme alt segmenti” veya “veli churn” ile özdeş olmaması (proxy label gürültüsü); (v) 2013–14 VLE davranışının 2026 mobil dikkat örüntülerinden zamansal kayması; (vi) seçim bias’ı (OU uzaktan yetişkin popülasyonu). Önlemler: eksik veri ve sınıf dağılımı raporlama (K3 EDA), sınıf ağırlığı veya PR-AUC odaklı değerlendirme, proxy etiketlerin şeffaf beyanı, OULAD ile sentetik özellik uzaylarının **karıştırılmaması**. Adil ve yanlı model riskleri için bias literatürü, özellik ve etiket seçiminin popülasyon kaymasıyla birleşebileceğini hatırlatır (Mehrabi et al., 2021).

**Sentetik katman.** Veli metni, anket, odak oturumu ve telefon olayları kontrollü prior’larla üretilir. Kalite riskleri: tasarımcı bias’ı (prior gerçeği yansıtmaz), evaluation leakage (`segment_label`’ın özelliğe sızması), sentetik üzerinde şişirilmiş metrikler ve sınırlı metin çeşitliliği. Önlemler: sabit `seed`, `schema_version` ve üretim `metadata.json`, segment üretim kurallarının yazılı olması, gerçek PII üretmeme, OULAD ve sentetik metriklerin **ayrı** raporlanması. Bu yaklaşım, veri setinin motivation–composition–recommended uses–limitations ekseninde belgelenmesi gerektiğini savunan datasheet disipliniyle uyumludur (Gebru et al., 2021).

### 3.2 Privacy and legal-ethical design

**KVKK genel ilkeler ve rıza.** 6698 sayılı Kanun m.4; hukuka uygunluk, amaçla bağlantılı–sınırlı–ölçülü işleme ve gerekli süre kadar saklamayı zorunlu kılar. m.3 açık rızayı “belirli bir konuya ilişkin, bilgilendirmeye dayanan ve özgür iradeyle açıklanan rıza” olarak tanımlar. Kurum rehberliğinde battaniye (genel) rızalar geçersizdir; rıza geri alınabilir ve geri alma ileriye etkilidir; ispat yükü veri sorumlusundadır (Kişisel Verileri Koruma Kurumu, 2018). m.5 kural olarak açık rıza arar; sözleşme ifası ve meşru menfaat gibi istisnalar vardır. AI Personal Coach’ta abonelik hesabı dar anlamda sözleşme ifası ile ilişkilendirilebilir; buna karşılık **odak-içi dikkat sinyali, veliye anlık bildirim ve LLM ile öğrenciye mesaj iletimi** konuya özgü açık rıza ve ayrı aydınlatma gerektirir. Tek “tüm şartları kabul ediyorum” kutusu kullanılmaz.

**Çocuk verisi.** Hedef kitlenin önemli bölümü 18 yaş altındadır. KVKK metninde GDPR m.8 benzeri net bir dijital rıza yaşı yoktur. Belirsizlik karşısında proje **temkinli rejim** önerir: (1) yasal temsilci (veli) aydınlatması ve gerekli faaliyetlerde açık rızası; (2) öğrenciye yaşına uygun bilgilendirme (“ne toplanır, kim görür, nasıl kapatılır”); (3) çocuğun üstün yararı — bildirim ve koçluk dilinin utandırma veya ceza aracına dönüşmemesi. Karşılaştırmalı iyi uygulama olarak GDPR m.8, bilgi toplumu hizmetlerinde rıza için kural olarak 16 yaş (üye devletlerce en düşük 13) ve veli onayının teknolojiye uygun doğrulanması için makul çaba öngörür (Regulation (EU) 2016/679, Art. 8). Bu hüküm doğrudan iç hukuk dayanağı değil, tasarım benchmark’ıdır.

**Telefon / odak izleme.** App kategorisi ve süre, m.6 özel nitelikli kişisel veri listesine otomatik girmez; yine de yüksek riskli davranışsal izlemedir. İlkeler: (i) yalnızca öğrencinin başlattığı **odak bloğunda** kayıt — blok dışı izleme yok; (ii) minimizasyon — içerik, URL ve ekran kaydı yok, tercihen kategori düzeyi; (iii) eğitim uygulamaları uyarı üretmez; (iv) **≥10 dakika** dikkat dağıtıcı kullanım veli bildirimi adayıdır; (v) günlük bildirim tavanı ve yargısız dil; (vi) rıza geri çekme ve izlemeyi kapatma — izleme kapalıyken anket ve aksiyon koçluğu sürer. Böylece “24 saat casusluk” algısı hem hukuken hem churn riski olarak sınırlanır.

**Aktarım, silme ve ilgili kişi hakları.** m.7, işleme sebebi kalkınca silme, yok etme veya anonimleştirmeyi öngörür. m.10–11 çerçevesinde aydınlatma ve erişim/silme talepleri için veli kanalı (ve mümkünse öğrenci bilgilendirmesi) tasarlanmalıdır. LLM API’leri yurt dışındaysa m.9 kapsamında yeterlilik kararı veya uygun güvenceler (ör. standart sözleşme) olmadan üretim aktarımı yapılmamalıdır. MVP’de veli önizlemeli gönderim (human-in-the-loop) yanlış ton ve brand safety riskini azaltır.

### 3.3 Limitations

| Sınır | Sonuç |
|-------|--------|
| OULAD = UK yetişkin uzaktan yükseköğretim | LGS/YKS ergen + TR aile bağlamına birebir genellenemez |
| OULAD’da veli / anket / app-level sinyal yok | Ürün omurgası sentetik ile tamamlanır |
| Sentetik veri | Saha dağılımını temsil etmez; production iddiası taşımaz |
| Gerçek pilot yok | 90 günlük retention bu veri ile **ölçülmez**; yalnızca tasarlanır ve simüle edilir |
| OS-level telefon telemetrisi yok | Bu teslimde `phone_events` sentetik/demo; mağaza ve platform kısıtları ayrı risk |
| Domain ve zaman kayması | 2013–14 VLE ≠ 2026 mobil dikkat |

### 3.4 PoC Test Fixtures ve Kontrollü Test Seti (`data-research/fixtures/`)

Uçtan uca PoC pipeline'ının (K5) güvenle test edilebilmesi için 15 öğrencilik sentetik test veri seti (`poc_students.json` / `poc_students.csv`) hazırlanmıştır.
- **Sıfır Gerçek PII:** İsimler sembolik ve sentetiktir; kimlik numarası, telefon veya IP verisi toplanmaz.
- **5 Segment Temsili:** Her pedagojik profil (Başlayamayan, Yarıda Bırakan, Telefonla Dağılan, Kaygıyla Erteleyen, Geceye Kayan) için 3 adet temsili öğrenci barındırır.
- **Deterministik Kural Testi:** Model risk skoru, telefon dikkat dağılma olayları ve inaktivite günleri gibi deterministik kural motoru girdilerini izole ve tekrarlanabilir biçimde simüle eder.

Bu sınırlar bilerek şeffaf bırakılmıştır: uydurma pilot iddiası akademik dürüstlüğü zedeler. Verinin sonraki aşama değeri; (a) OULAD üzerinde tekrarlanabilir risk pipeline’ı, (b) ürün şeması ve etik kısıtların sentetikle uçtan uca gösterimi, (c) privacy-by-design kararlarının belgelenmesidir — sahada A/B ile kanıtlanmış retention lift iddiası değildir.

---

## 5. Conclusion

OULAD açık benchmark’ı ile şema-uyumlu sentetik veli/anket/odak/telefon katmanı birlikte, **ödev ve MVP demo kapsamı için yeterlidir**: pazarlama KPI’sına bağlı özellik tasarımı, kalite risklerinin tanınması, çocuk ve izleme odaklı mahremiyet rejimi ve model karşılaştırması için ortak zemin sağlar. Buna karşılık **üretim kararı ve 90 günlük retention kanıtı için yeterli değildir.** Sonraki adımlar: dar kapsamlı etik/onamlı pilot; konuya özgü rıza ve aydınlatma akışlarının ürünleştirilmesi; yurt dışı aktarım değerlendirmesi; OS izinleri ve mağaza politikasına uyumlu (veya bilinçli self-report) dikkat sinyali; OULAD’dan bağımsız TR bağlamı validasyonu. Özetle governance, AI Personal Coach’un “daha çok izle” değil “daha doğru, daha az ve daha güvenli veriyle veliye görünür değer üret” stratejisinin parçasıdır; bu da abonelik retention probleminin veri katmanındaki karşılığıdır.

---

## 6. Proper Citations

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM, 64*(12), 86–92. https://doi.org/10.1145/3458723

Kişisel Verileri Koruma Kurumu. (2018). *Açık rıza alırken dikkat edilecek hususlar*. https://www.kvkk.gov.tr/Icerik/2037/Acik-Riza-Alirken-Dikkat-Edilecek-Hususlar

Kişisel Verilerin Korunması Kanunu, 6698 sayılı Kanun. (2016). *Resmî Gazete* (Sayı: 29677). https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6698&MevzuatTur=1&MevzuatTertip=5

Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. *Scientific Data, 4*, Article 170171. https://doi.org/10.1038/sdata.2017.171

Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A. (2021). A survey on bias and fairness in machine learning. *ACM Computing Surveys, 54*(6), Article 115. https://doi.org/10.1145/3457607

Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data (General Data Protection Regulation). *Official Journal of the European Union, L 119*, 1–88. (See especially Art. 8.)
