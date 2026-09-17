# SIC AI-17 Capstone – Yapılması Gereken İşler

**Proje:** AI Personal Coach  
**Repo:** https://github.com/edasaruhan/SIC_AI_-17_Capstone_Group_1  
**Amaç:** Araştırma ve dokümantasyon ağırlıklı mevcut yapıyı, ölçülebilir ve çalışan bir Proof-of-Concept (PoC) seviyesine taşımak.

---

## Öncelikli Sprint Hedefi

İlk hedef tam uygulama geliştirmek değildir. Önce aşağıdaki uçtan uca akışın çalışan bir PoC olarak kurulması gerekir:

```text
Öğrenci davranış verisi
        ↓
Risk tahmin modeli
        ↓
Risk skoru
        ↓
Davranış segmenti
        ↓
Deterministik kural motoru
        ↓
Kişiselleştirilmiş veli mesajı
```

Bu akış terminal/CLI seviyesinde çalışsa bile ilk sprint için yeterlidir.

---

# K1 – Literature Lead & Editor

## Sorumluluklar

- Proje genel README ve dokümantasyonunu güncellemek.
- Eski tarih, durum ve teslim bilgilerini temizlemek.
- K3, K4 ve K5 tarafından üretilen yeni çıktıları ana dokümantasyona işlemek.
- Repo genelindeki model, KPI ve performans iddialarının ifade biçimlerini standardize etmek.
- Gerçek ölçüm olmayan değerleri gerçek sonuç gibi göstermemek.

## Özellikle Güncellenmesi Gerekenler

- Eski sprint ve deadline tarihleri
- `Last Updated` alanları
- Model performans iddiaları
- Retention ve CTR gibi henüz saha verisiyle doğrulanmamış değerler
- Tasarım varsayımı ile gerçek deney sonucunun ayrımı

## Kullanılabilecek Etiketler

```text
Target
Design assumption
Proxy result
Synthetic result
Pilot validated
Not yet validated
```

## Tamamlanma Kriteri

- README güncel proje durumunu doğru göstermeli.
- Repo içinde birbirleriyle çelişen performans ifadeleri kalmamalı.
- Gerçek olmayan hiçbir metrik "doğrulanmış sonuç" gibi sunulmamalı.

---

# K2 – Literature Analyst

## Sorumluluklar

Yeni literatür toplamaktan çok mevcut iddiaların kaynak kontrolünü yapmak.

Kontrol edilmesi gereken başlıca konular:

- Churn prediction
- Retention
- Parent engagement
- Personalized messaging
- Notification timing
- Nudge interventions
- CTR / engagement artışı
- Eğitim teknolojilerinde personalization

## Yapılacaklar

1. Repo içindeki sayısal iddiaları listelemek.
2. Her iddianın gerçek akademik/teknik kaynağı olup olmadığını kontrol etmek.
3. Kaynağı olmayan iddiaları:
   - kaldırmak,
   - yeniden ifade etmek,
   - veya "target / assumption" olarak etiketlemek.
4. `references.bib` dosyasını güncellemek.

## Tamamlanma Kriteri

- Sayısal veya nedensel önemli iddiaların kaynağı açık olmalı.
- Kaynaksız iddialar gerçek bulgu gibi görünmemeli.
- `references.bib` ile doküman içi atıflar tutarlı olmalı.

---

# K3 – Data Lead / EDA

## En Kritik Görev

Baseline modelleri yeniden ve tekrarlanabilir biçimde değerlendirmek.

## Karşılaştırılacak Modeller

En az:

- Logistic Regression
- LightGBM

İstenirse mevcut LSTM proxy sonucu ayrıca raporlanabilir ancak aynı deney koşullarına dahil edilmeden doğrudan karşılaştırılmamalıdır.

## Değerlendirme Koşulları

Her model:

- aynı veri seti,
- aynı train/test split,
- aynı random seed,
- aynı target tanımı

ile değerlendirilmelidir.

## Üretilecek Metrikler

- ROC-AUC
- F1 Score
- Precision
- Recall
- Confusion Matrix

İsteğe bağlı:

- Accuracy
- PR-AUC

## Önerilen Dosya Yapısı

```text
data-research/
└── modeling/
    ├── baseline_models.py
    ├── baseline_results.csv
    ├── confusion_matrix_logistic.png
    ├── confusion_matrix_lightgbm.png
    └── README.md
```

## Düzeltilmesi Gereken Nokta

Mevcut EDA dokümanındaki model performans tabloları yeniden kontrol edilmeli.

Model seçiminde tablo değerleri ile metindeki "en iyi model" yorumu birbiriyle uyumlu olmalıdır.

## Tamamlanma Kriteri

- Kod tek komutla yeniden çalıştırılabilmeli.
- Sonuçlar CSV veya Markdown tablo olarak kaydedilmeli.
- Hangi modelin neden seçildiği açıkça yazılmalı.
- Performans rakamları README ve methodology dokümanlarıyla tutarlı hale getirilmeli.

---

# K4 – Data Governance & Synthetic Data

## Sorumluluklar

PoC'de kullanılan verinin kaynağını, niteliğini ve sınırlarını açık hale getirmek.

## Veri Türleri Net Ayrılmalı

### 1. OULAD Proxy Data
Gerçek bir eğitim veri setidir ancak doğrudan Türkiye'deki LGS/YKS abonelik churn verisi değildir.

### 2. Synthetic Data
Sentetik olarak üretilmiş test/geliştirme verisidir.

### 3. Real Pilot Data
Şu anda mevcut değildir.

Bu üç kategori repo genelinde birbirine karıştırılmamalıdır.

## Yapılacaklar

- PoC için küçük ve kontrollü test veri seti hazırlamak.
- Verinin provenance bilgisini tutmak.
- Sentetik veriyi açık biçimde etiketlemek.
- KVKK açısından kullanılan alanları yeniden kontrol etmek.
- Gereksiz kişisel veri alanlarını kaldırmak.
- Risk modelinin hangi veri ile üretildiğini dokümante etmek.

## Önerilen PoC Test Verisi

10–20 öğrencilik sabit fixture hazırlanabilir.

Örnek:

```text
student_001 → Başlayamayan
student_002 → Telefonla Dağılan
student_003 → Geceye Kayan
student_004 → Düzenli ama Düşük Performanslı
```

Bu veri K5 tarafından pipeline testi için kullanılabilir.

## Tamamlanma Kriteri

- Her veri dosyasının synthetic / proxy / real statüsü belli olmalı.
- Test verileri yeniden üretilebilir olmalı.
- PoC veri akışında hassas kişisel veri kullanılmamalı.
- Veri kaynakları ve kısıtları açıkça dokümante edilmiş olmalı.

---

# K5 – Technology / Methodology / Architecture

## Ana Görev

Çalışan ilk uçtan uca PoC'nin teknik sahibi olmak.

## Kurulacak Pipeline

```text
Student Data
    ↓
Risk Model
    ↓
Risk Score
    ↓
Behavior Segment
    ↓
Rule Engine
    ↓
Parent Message
```

## İlk Sürüm İçin UI Gerekli Değildir

CLI veya Python script yeterlidir.

Örnek çıktı:

```text
Student ID: 1042

Risk Score: 0.76
Risk Level: High
Segment: Telefonla Dağılan
Trigger: TRUE

Parent Message:
"Son günlerde çalışma sırasında odak süresinde düşüş görüldü.
Bugün 20 dakikalık kısa bir çalışma bloğu ile yeniden başlamayı deneyebilirsiniz."
```

## Teknik Katmanlar

### 1. Risk Layer
K3 tarafından doğrulanan baseline model kullanılmalı.

### 2. Segmentation Layer
Öğrenci davranışına göre segment üretmeli.

### 3. Rule Engine
LLM'den bağımsız ve deterministik olmalı.

Örnek:

```text
IF risk_score > 0.70
AND inactivity_days >= 3
THEN trigger_parent_message = TRUE
```

### 4. Message Layer

İlk sürümde iki alternatif kullanılabilir:

- Template-based mesaj üretimi
- LLM tabanlı kişiselleştirme

LLM kullanılıyorsa model yalnızca mesajın ifade biçimini kişiselleştirmeli; risk kararı veya kritik iş mantığı LLM'e bırakılmamalıdır.

## Tamamlanma Kriteri

Tek komutla aşağıdaki çıktılar üretilebilmeli:

1. Risk score
2. Risk level
3. Segment
4. Rule trigger sonucu
5. Parent message

---

# Çalışma Sırası

K3 ve K4 paralel başlayabilir.

```text
K3 – Baseline model doğrulama
          ↓
K5 – Risk model entegrasyonu
          ↓
K5 – Segment + Rule Engine + Message
```

Aynı anda:

```text
K4 – Test verisi + provenance + governance
```

Sonrasında:

```text
K2 – Claim ve kaynak doğrulama
          ↓
K1 – README ve genel repo finalizasyonu
```

---

# Bir Sonraki Haftalık Rapora Kadar Minimum Hedef

Aşağıdaki üç iş tamamlanırsa proje yeterli seviyede ilerlemiş kabul edilebilir:

## 1. Baseline Model Validation

- Logistic Regression
- LightGBM
- Ortak değerlendirme pipeline'ı
- ROC-AUC / F1 / Precision / Recall

## 2. Temiz PoC Veri Seti

- Synthetic veya proxy olduğu açıkça belirtilmiş
- 10–20 örnek öğrenci
- Tekrarlanabilir

## 3. Çalışan End-to-End PoC

```text
data
→ risk
→ segment
→ rule
→ personalized message
```

---

# Bu Sprintte Yapılmaması Gerekenler

Şimdilik aşağıdaki işler düşük önceliklidir:

- Full frontend geliştirme
- Mobil uygulama
- Production backend
- Authentication
- Deployment
- Dashboard tasarımı
- Büyük ölçekli API entegrasyonu
- Yeni ve geniş literature review
- Fine-tuning
- Gerçek zamanlı notification sistemi

Önce sistemin temel AI mantığının gerçekten çalıştığı kanıtlanmalıdır.

---

# Sprint Sonunda Beklenen Repo Durumu

Repo yalnızca araştırma/dokümantasyon içeren bir proje olmaktan çıkıp şu üç bileşeni göstermelidir:

1. **Doğrulanmış baseline model**
2. **İzlenebilir ve tanımlı test verisi**
3. **Çalışan AI intervention pipeline'ı**

Bu üç çıktı tamamlandıktan sonra frontend, backend ve ürünleştirme aşamasına geçmek anlamlı hale gelir.
