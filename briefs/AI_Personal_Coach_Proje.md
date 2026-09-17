# AI Personal Coach — Proje Dokümanı (Güncel)

> Hocanın geri bildirimine göre güncellendi:  
> **Asıl müşteri = LGS / YKS velileri**  
> **Kullanıcı = öğrenci**  
> **Davranış bazlı segmentasyon**  
> **Veli metin + sesli AI görüşmesi**  
> **Anketlerle öğrenci tanıma**  
> **Odak bloğunda telefon izleme (10 dk+) + veli bildirimi**  
> **Haftalık veli raporu**  
> **Veli niyetini AI’nın motive edici mesaja çevirmesi**  
> Süre: **2 ay (MVP)**

---

## 1) Proje özeti

**AI Personal Coach**, LGS ve YKS sürecindeki öğrencilerin erteleme ve odak kaybı riskini önceden tespit eden bir yapay zeka sistemidir.

Sistem öğrenciyi şu yollarla tanır:
1. velinin serbest metinle girdiği bilgiler  
2. veli–AI sesli görüşmesi  
3. öğrenciye / veliye uygulanan kısa anketler  
4. öğrenci rutin kayıtları  
5. odak bloğundaki telefon / dikkat dağılma sinyalleri  

Sonra:
- öğrenciye kişiselleştirilmiş tek aksiyon üretir  
- velinin kızdırabilecek sert uyarısını yumuşak ve motive edici mesaja çevirir  
- veliye anlık dikkat bildirimi + **haftalık rapor** sunar  

- **Kullanan:** öğrenci  
- **Ödeyen müşteri:** veli (özellikle LGS / YKS anneleri)  
- **SKA:** 4, 8  
- **Yöntem:** ML + LLM + kural motoru (10 dk eşiği)

---

## 2) Roller

| Rol | Kim | Ne ister? |
|-----|-----|-----------|
| Kullanıcı | LGS / YKS öğrencisi | Net aksiyon, motivasyon, ertelemeyi kırmak |
| Müşteri | Veli (özellikle anne) | Çocuğu tanımak, riski görmek, doğru şekilde yönlendirmek |
| Değer | İkisi birlikte | Zamanında koçluk + görünürlük + çatışmasız iletişim |

---

## 3) Problem

- Öğrenci ertelemeyi geç fark eder  
- Veli çocuğu iyi tanısa da sisteme aktaramaz  
- Ders sırasında telefon dikkat dağıtır  
- Anne bazen doğru şeyi yanlış dille söyler; çocuk küsür, motivasyon düşer  
- İki öğrenci aynı sınava hazırlansa bile kopma sebepleri farklıdır  

---

## 4) Çözüm akışı

1. **Veli metin girişi** — çocuğu serbest yazıyla anlatır  
2. **Veli–AI sesli görüşme** — profil derinleşir  
3. **Anketler** — öğrenciyi farklı boyutlardan tanır  
4. **Öğrenci rutin kaydı** — ders/tekrar/odak blokları  
5. **Telefon izleme (odak bloğunda)** — app + süre; 10 dk+ olursa veliye bildirim  
6. **ML risk skoru** — erteleme / odak kaybı tahmini  
7. **LLM kişiselleştirme** — öğrenciye özel aksiyon + velinin mesajını motive edici forma çevirme  
8. **Haftalık veli raporu** — özet PDF/ekran  

---

## 5) Haftalık veli raporu

Her hafta veliye sade bir özet gider (ekran + istenirse PDF).

**Raporda olacaklar:**
- ortalama / son risk skoru  
- tamamlanan aksiyon sayısı  
- kaçırılan ders/odak bloğu sayısı  
- dikkat dağılma sayısı (10 dk+ telefon uyarıları)  
- en sık dağıtan uygulama grubu (sosyal, oyun vb.)  
- öne çıkan alt segment (başlayamayan / yarıda bırakan / telefonla dağılan…)  
- gelecek hafta için 1–2 öneri  

**Örnek cümle:**  
“Bu hafta risk ortalaması orta. 12 aksiyondan 7’si tamamlandı. Dikkat dağılma uyarısı: 4. En çok kopma: gece sosyal medya. Öneri: gündüz 2 kısa blok.”

---

## 6) Anketlerle öğrenciyi tanıma

Farklı kısa anket setleri olur; hepsi uzun psikoloji testi değil, hızlı tanıma amaçlıdır.

### 6.1 Veli anketleri
- çocuğun güçlü yanı / zorlandığı yer  
- en çok ertelenen ders  
- evdeki çalışma düzeni  
- neyin işe yaradığı / yaramadığı  
- motivasyon tetikleyicileri  

### 6.2 Öğrenci anketleri
- sabah mı akşam mı daha iyi çalışıyorum  
- başlamak mı zor, sürdürmek mi  
- telefonu en çok ne için açıyorum  
- hangi ödül/hedef beni hareket ettiriyor  
- kaygı yükselince ne oluyor  

### 6.3 Periyodik mini anket
Haftada 1–2 soru:  
“Bu hafta en çok nerede koptun?”  
“Yarın için tek hedefin ne?”

Anket çıktıları profil bilgisene yazılır ve mesaj tonunu etkiler.

---

## 7) Veli niyeti → AI motive edici mesaj (yeni)

### Problem
Anne bazen doğru uyarıyı sert söyler:  
“Yine telefon, yine boş; böyle YKS kazanılmaz.”  
Çocuk kızar / kapanır; motivasyon düşer.

### Çözüm
Veli niyetini AI’ya yazar veya sesli söyler.  
AI bunu öğrenciye **kızdırmayan, motive eden, aksiyonlu** mesaja çevirir.

**Veli girişi:**  
“Telefonu bırakmadı, dersi yine böldü, çok kızgınım.”

**AI’nın öğrenciye mesajı:**  
“Dikkatin dağıldığını gördük. Sorun değil, şimdi toparlanabilirsin. 20 dakikalık tek bir soru bloğu yap; bitince kısa mola senin.”

### Kurallar
- suçlayıcı dil yok  
- tek net aksiyon var  
- velinin endişesi korunur, üslup yumuşatılır  
- amaç baskı değil, harekete geçirme  

Bu özellik pazarlamada çok güçlüdür:  
“Sizin yerinize bağırmadan, çocuğunuza doğru dille ulaşır.”

---

## 8) Telefon / dikkat izleme

Odak/ders bloğu açıkken:
- telefon açıldı mı  
- hangi app  
- kaç dakika  

**10 dakikadan fazla** dikkat dağıtıcı app = veliye bildirim  
Örnek: “Çocuğunuzun dikkati dağılmış olabilir. Instagram’da 12 dakikadır.”

- 24 saat casusluk değil  
- sadece odak bloğunda  
- eğitim app’leri uyarı üretmez  

---

## 9) Segmentasyon farkı

| Alt segment | Sinyal | Mesaj farkı |
|-------------|--------|-------------|
| Başlayamayan | hiç başlamaz | “25 dk başlat” |
| Yarıda bırakan | kısa süre sonra bırakır | “bloğu bitir” |
| Telefonla dağılan | app >10 dk | “uygulamayı kapat, geri dön” |
| Kaygıyla erteleyen | deneme öncesi kaçırma | “küçük ısınma seti” |
| Geceye kayan | gündüz boş / gece yığılma | “gündüz kısa blok” |

Veli anlatımı + anket + davranış + telefon sinyali birlikte iki benzer öğrenciyi ayırır.

---

## 10) Veri

1. OULAD (açık veri)  
2. Öğrenci rutin logları  
3. Veli metin + sesli görüşme  
4. Anket cevapları  
5. Telefon dikkat sinyalleri  
6. Haftalık rapor metrikleri  
7. Veli niyeti → AI mesaj dönüşüm logları  

---

## 11) Yöntem

- **ML:** risk skoru / tipi  
- **LLM:** profil, anket özeti, öğrenci mesajı, veli mesajını yumuşatma, haftalık rapor metni  
- **Kural:** 10 dk dikkat eşiği  
- **Deep Learning:** zorunlu değil  

---

## 12) 2 aylık plan

| Hafta | İş |
|------|-----|
| 1–2 | Model, segmentler, veri şeması, proposal |
| 3–4 | Risk modeli (OULAD + sentetik) |
| 5 | Veli metin/ses + anket → profil |
| 6 | 10 dk dikkat kuralı + veli bildirimi + mesaj yumuşatma |
| 7 | Haftalık rapor demo + küçük pilot |
| 8 | Rapor / sunum |

### 2 ay teslimi
- veli metin/ses + anket ile öğrenci tanıma  
- risk modeli  
- odak bloğunda 10 dk dikkat uyarısı  
- veli niyetini motive edici mesaja çevirme  
- haftalık veli raporu  
- demo  

---

## 13) Gelir modeli

- Ödeyen: veli  
- Aylık abonelik  
- Neden öder: erken uyarı + kişiselleştirme + çatışmasız iletişim + haftalık görünürlük  

---

## 14) Riskler

| Risk | Önlem |
|------|-------|
| Baskı / casusluk algısı | Sadece odak bloğu, yargısız dil |
| Aşırı bildirim | 10 dk eşiği + günlük limit |
| Sert veli mesajı | AI üslup dönüştürücü zorunlu |
| Kapsam şişmesi | 2 ayda demo seviyesinde tut |

---

## 15) Tek cümlelik tanım

**AI Personal Coach; LGS/YKS velisinin anlatımı ve anketleriyle öğrenciyi tanıyan, ders sırasında dikkat dağılınca veliye bildiren, velinin sert uyarısını motive edici mesaja çeviren ve haftalık rapor sunan 2 aylık yapay zeka MVP’sidir.**
