# AI Personal Coach — Proje Özeti ve Uyum Rehberi
### (Tüm Ekip Üyeleri İçin Referans Belgesi) · Pazarlamada Yapay Zeka Bitirme Projesi

---

## 1. Yönetici Özeti ve Pazarlama Çerçevesi

* **Ürün Adı:** AI Personal Coach
* **Alan:** Pazarlamada Yapay Zeka / Eğitim Teknolojisi (EdTech) Abonelik Pazarlaması
* **Hedef Sınav Bağlamı:** LGS ve YKS Hazırlık Süreci (Türkiye)
* **Temel Pazarlama Problemi:** Öğrencinin dersten kopması, ev içi iletişim çatışması ve velinin pedagojik rehberlik eksikliği nedeniyle ilk 30–90 gün içinde yaşanan yüksek veli abonelik iptali (erken churn).
* **İkili Kullanıcı Yapısı:**
  * **Ödeyen Müşteri (Ekonomik Alıcı):** Veli (çoğunlukla ailedeki eğitim harcamalarını yöneten ve sınav başarısı konusunda yüksek kaygı yaşayan ebeveynler).
  * **Kullanan (Öğrenci):** Sınav stresi, ders erteleme ve dijital dikkat dağıtıcılarla mücadele eden 13–18 yaş arası gençler.

---

## 2. Temel Başarı Metrikleri (KPI'lar)

*Tüm ekip üyeleri raporlarında kesinlikle bu standart KPI isimlerini kullanmalıdır:*

* **Birincil Ticari Metrik:**
  * **90 Günlük Veli Elde Tutma (Retention) Oranı:** Kritik ilk 3 aylık dönemi tamamlayıp aboneliğini sürdüren velilerin yüzdesi.
* **İkincil Metrikler:**
  * **Denemeden Ücretliye Geçiş Oranı (Trial-to-Paid):** Ücretsiz deneme kullanıcılarının ücretli aylık aboneliğe geçiş oranı.
  * **Haftalık Rapor Açılma Oranı:** Velilerin haftalık elde tutma raporlarıyla etkileşim oranı.
  * **Bildirim Aksiyonu Tamamlama Oranı:** Yapay zeka dürtüklemesi sonrası öğrenci/velinin aksiyonu tamamlama oranı (ör. duraksayan dersi 10 dk içinde başlatma).
  * **Veli-Öğrenci Diyalog Benimseme Oranı:** Velilerin sistemin önerdiği yapıcı iletişim kalıplarını kullanma sıklığı.
  * **LTV / CAC Oranı:** Müşteri Yaşam Boyu Değerinin Müşteri Edinme Maliyetine oranı.

---

## 3. Standart Davranışsal Segmentler (5 Alt Segment)

*Öğrenci profillerinden ve segmentasyondan bahsederken bu 5 kategoriyi kullanın:*

1. **Başlayamayan (Cannot Start):** Planlanan çalışma seansına başlamakta zorlanan, başlama felci yaşayan öğrenciler.
2. **Yarıda Bırakan (Abandons Midway):** Derse başlayıp odaklanmasını sürdüremeyen ve süreyi tamamlamadan bırakanlar.
3. **Telefonla Dağılan (Phone-Distracted):** Çalışma blokları esnasında sık sık uygulamalar arası geçiş yapan ve dikkatini dağıtanlar.
4. **Kaygıyla Erteleyen (Anxiety-Driven Procrastinator):** Başarısızlık korkusuyla zor dersleri sürekli erteleyenler.
5. **Geceye Kayan (Night-Shifted):** Çalışma saatlerini gece geç saatlere kaydıran ve zihinsel yorgunluk yaşayanlar.

---

## 4. Teknik ve Veri Esasları (Kilit Kararlar)

* **Risk Tahmin Modeli:** Tıklama ve zaman serisi verilerinden dersten kopuş ve churn riskini tahmin eden LightGBM sınıflandırıcısı.
* **Doğal Dil İşleme (NLP) / Üslup Dönüştürme Katmanı:** Kaygılı/baskıcı veli mesajlarını özerklik destekleyici yapıcı koçluk önerilerine dönüştüren LLM mimarisi.
* **Kural Motoru:** Deterministik tetikleyiciler (ör. 10 dakikalık hareketsizlik durumunda devreye giren aktivasyon dürtüklemeleri).
* **Veri Kaynakları:**
  * **OULAD (Açık Veri):** Davranışsal tıklama verileri ve dersten kopuş modellemesi için kullanılır.
  * **Sentetik Veri Seti:** Türkiye sınav ortamı, veli mesajları, anket profilleri ve odak bloğu telefon kullanım verileri için kullanılır.

---

## 5. Gizlilik ve Veri Yönetişimi İlkeleri

* **Sınırlı Odak Takibi:** Veri toplama işlemi *yalnızca* öğrencinin başlattığı planlı ders blokları esnasında aktiftir.
* **Güvenli Liste (Whitelisting):** Eğitici uygulamalar dikkat dağınıklığı uyarısı üretmez.
* **Çocuk Verisi Koruması:** KVKK standartlarına uygun veli açık rızası ve şeffaf çocuk verisi koruma politikası.
```[cite: 1]
