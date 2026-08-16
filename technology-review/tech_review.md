# Teknoloji Değerlendirmesi ve Mimari Seçim Raporu
### AI Personal Coach · Pazarlamada Yapay Zeka Bitirme Projesi

---

## 1. Yönetici Özeti ve Teknolojik Vizyon

Eğitim teknolojileri (EdTech) sektöründe, özellikle Türkiye'deki Liselere Geçiş Sistemi (LGS) ve Yükseköğretim Kurumları Sınavı (YKS) gibi yüksek baskı ve rekabet içeren merkezi sınavlara hazırlık sürecinde, abonelik tabanlı dijital platformların karşılaştığı en temel ticari zorluk kullanıcı kaybıdır (churn). Sistemimize kayıt olan velilerin önemli bir kısmı, ilk 30 ila 90 gün içinde hizmeti terk etmektedir. AI Personal Coach projesinin teknolojik vizyonu, salt bir öğrenme yönetim sistemi (LMS) veya soru bankası sunmanın ötesine geçerek, doğrudan "90 Günlük Veli Elde Tutma (Retention) Oranı" metriğini maksimize edecek, veri güdümlü, proaktif ve pedagojik bir yapay zeka ekosistemi inşa etmektir. 

Bu rapor, projenin teknolojik temelini oluşturan makine öğrenmesi modellerinin, büyük dil modellerinin (LLM), kural motorlarının (rule engine) ve veri gizliliği mimarilerinin detaylı bir değerlendirmesini sunmaktadır. Sistemimiz, öğrencinin dersten kopma anını gerçek zamanlı olarak tespit edebilmek ve bu riski veliye en doğru, yapıcı ve özerklik destekleyici üslupla iletebilmek için çok katmanlı bir teknoloji yığınına dayanmaktadır.

Değerlendirmemiz sonucunda, platformun üç ana teknolojik bileşeni şu şekilde belirlenmiştir:
1. **Risk Tahmini ve Sınıflandırma Katmanı:** Öğrenci davranış verilerinden (tıklama akışları, oturum süreleri, pasif kalma anları) yola çıkarak anlık kopuş ve uzun vadeli churn riskini hesaplayan LightGBM tabanlı bir makine öğrenmesi modeli. Bu katman, öğrencileri davranışsal olarak ("Başlayamayan", "Yarıda Bırakan", "Telefonla Dağılan", "Kaygıyla Erteleyen", "Geceye Kayan") segmentlere ayırmak için yüksek başarımlı ve yorumlanabilir sonuçlar üretmektedir.
2. **Kural Motoru ve Karar Katmanı:** Makine öğrenmesi modelinden gelen risk skorlarını işleyen, sistem içi deterministik olayları (örneğin 10 dakikalık hareketsizlik) takip eden ve uygun müdahale anlarını tetikleyen düşük gecikmeli bir kural motoru.
3. **Üslup Dönüştürme ve Diyalog Üretim Katmanı (LLM):** Kural motorundan gelen tetikleyicileri alarak, veliye gönderilecek mesajları velinin kaygı düzeyine ve öğrencinin segmentine göre pedagojik olarak yapılandıran OpenAI GPT-3.5 Turbo tabanlı üretimsel yapay zeka katmanı.

Raporun ilerleyen bölümlerinde, neden Derin Öğrenme (Deep Learning) veya XGBoost yerine LightGBM'in seçildiği, LLM maliyetlerinin "LTV / CAC Oranı" bağlamında nasıl optimize edildiği, veri gizliliğinin marka güvenine katkısı ve tüm bu teknolojik kararların pazarlama KPI'ları ("Haftalık Rapor Açılma Oranı", "Bildirim Aksiyonu Tamamlama Oranı", "Veli-Öğrenci Diyalog Benimseme Oranı", "Denemeden Ücretliye Geçiş Oranı") üzerindeki doğrudan etkileri kapsamlı bir şekilde incelenmektedir. Tüm teknolojik seçimlerimiz, teknik mükemmellikten ziyade ticari uygulanabilirlik ve tüketici nezdinde psikolojik güven oluşturma hedefine odaklanmıştır.

---

## 2. Dersten Kopuş ve Risk Tahmini: LightGBM vs. Alternatifler

AI Personal Coach sisteminin kalbinde, öğrencinin sisteme girdiği andan itibaren sergilediği davranışların sürekli olarak analiz edildiği ve bir dersten kopuş (disengagement) ile abonelik iptali (churn) risk skorunun üretildiği makine öğrenmesi modeli yer alır. Bu süreç için çeşitli algoritmalar (Lojistik Regresyon, Rastgele Orman, XGBoost, Derin Sinir Ağları) değerlendirilmiş ve nihai olarak LightGBM (Light Gradient Boosting Machine) algoritmasında karar kılınmıştır.

### 2.1 Model Seçim Süreci ve Alternatiflerin Değerlendirilmesi

Öğrenci davranışları genellikle dengesiz veri setleri (imbalanced data) üretir; çoğu öğrenci dersi normal şekilde tamamlarken, sadece belirli bir azınlık kritik risk sinyalleri gösterir. Bu noktada, geleneksel istatistiksel yöntemler olan Lojistik Regresyon gibi modeller karmaşık doğrusal olmayan (non-linear) ilişkileri modellemekte yetersiz kalmaktadır. 

Öte yandan, LSTM (Long Short-Term Memory) veya Transformer tabanlı Derin Öğrenme algoritmaları, zaman serisi etkileşim verilerinde çok yüksek AUC (Eğri Altında Kalan Alan) ve F1 skorları üretebilse de, "kara kutu" (black-box) yapıları nedeniyle ciddi bir dezavantaja sahiptirler. AI Personal Coach projesinde, modelin neden yüksek risk puanı ürettiğini veliye açıklayabilmek (explainability) hayati önem taşır. Eğer model bir öğrenciye %85 risk skoru verirse, LLM katmanının veliye bu riskin "Telefonla Dağılan" davranışlardan mı yoksa "Kaygıyla Erteleyen" bir profilden mi kaynaklandığını anlatması gerekir. Derin öğrenme modelleri bu düzeyde yorumlanabilirlik sağlamak için karmaşık ekstra katmanlara ihtiyaç duyarken, ağaç tabanlı algoritmalar bu konuda doğal bir avantaja sahiptir.

XGBoost ve LightGBM gibi Gradient Boosting algoritmaları, hem yüksek doğruluk oranlarına sahip olmaları hem de SHAP (SHapley Additive exPlanations) değerleri ile entegre çalışarak model kararlarının yorumlanabilmesini sağlamaları açısından öne çıkmıştır. Ancak LightGBM'in XGBoost'a kıyasla tercih edilmesinin üç temel teknik nedeni bulunmaktadır:

1. **Histogram Tabanlı Ayrılma (Histogram-based Splitting):** LightGBM, sürekli değişkenleri ayrık kutulara (bins) böler. Bu yaklaşım, XGBoost'un geleneksel sıralı ayrılma yöntemine göre bellek kullanımını dramatik şekilde azaltır ve eğitim hızını artırır. OULAD gibi büyük tıklama akışı (clickstream) veri setleriyle çalışırken, eğitim sürelerinde %30 ila %50 arasında bir zaman tasarrufu sağlanmıştır.
2. **Yaprak Odaklı Büyüme (Leaf-wise Tree Growth):** Çoğu karar ağacı algoritması seviye odaklı (level-wise) büyürken, LightGBM yaprak odaklı (leaf-wise) büyür ve en fazla kaybı azaltan yaprağı genişletir. Bu özellik, daha az sayıda düğüm ile daha karmaşık asimetrik desenleri ("Geceye Kayan" öğrencilerin aniden oturum kapatması gibi) çok daha yüksek bir doğrulukla yakalamasına olanak tanır.
3. **Kategorik Değişken Desteği:** LightGBM, kategorik değişkenleri One-Hot Encoding işlemine gerek duymadan doğrudan işleyebilir. Sınıf seviyesi, okul türü, seçilen zorluk derecesi gibi kategorik eğitim verileri, veri matrisini büyütmeden ve seyrekliğe (sparsity) yol açmadan doğrudan modele beslenebilmektedir.

### 2.2 Pazarlama KPI'ları ile Entegrasyon ve Davranışsal Segmentasyon

Makine öğrenmesi altyapımız, sadece teknik doğruluk skorlarını (AUC) değil, doğrudan pazarlama başarı metriklerini maksimize edecek şekilde tasarlanmıştır. Modelin ürettiği anlık risk skorları (0.00 - 1.00 arası), kural motoru tarafından anında 5 ana davranışsal segmente atanmaktadır:

*   **Başlayamayan:** İlk 15 dakika içinde sisteme giriş yapıp hiçbir derse tıklamayanlar.
*   **Yarıda Bırakan:** İzleme oranının %40'ın altında kaldığı ve oturumun aniden sonlandırıldığı profiller.
*   **Telefonla Dağılan:** Platform arka plana atıldığında veya odak modundan çıkıldığında kesinti yaşayanlar.
*   **Kaygıyla Erteleyen:** Zorluk derecesi yüksek görevleri sürekli atlayıp kolay sorulara dönenler.
*   **Geceye Kayan:** Etkileşimlerinin %70'ini saat 22:00'den sonra gerçekleştiren ve yanıt süreleri uzayanlar.

Bu davranışsal segmentasyon, sistemimizin kişiselleştirilmiş pazarlama stratejisinin kalbidir. Veliye gönderilecek olan push bildirimlerinin ve SMS'lerin içeriği, bu segmentasyon sayesinde salt bir "öğrenciniz ders çalışmıyor" uyarısından, "öğrenciniz 'Kaygıyla Erteleyen' bir profil sergiliyor, şu pedagojik adımı atabilirsiniz" şeklinde değer katan bir rehberliğe dönüşür. Bu da doğrudan **Bildirim Aksiyonu Tamamlama Oranı** ve **90 Günlük Veli Elde Tutma (Retention) Oranı**'nı artıran en kritik mekanizmadır. Ayrıca, bu özellik "Denemeden Ücretliye Geçiş Oranı" (Trial-to-Paid) açısından da çok güçlü bir satış argümanı (USP) olarak kullanılmaktadır.

## 3. LLM ve Doğal Dil İşleme: Üslup Dönüştürme ve Mesaj Kişiselleştirme

Risk tahmini ve kural tabanlı tetikleyicilerle donatılmış bir sistem tek başına yeterli değildir. Kullanıcılarımız (öğrenciler ve ebeveynler) son derece duygusal ve stresli bir sınav sürecinden geçmektedir. Verilerin veliye ham bir şekilde sunulması (örn. "Çocuğunuz matematikten 40 aldı ve odaklanma süresi düştü"), velinin paniklemesine, öğrenciye baskı kurmasına ve sonucunda ev içi çatışmanın artmasına yol açar. Bu çatışma, platformun "stres kaynağı" olarak algılanmasına ve kısa sürede abonelik iptaliyle (churn) sonuçlanmasına neden olur.

Bu problemi çözmek ve yapıcı bir koçluk ekosistemi yaratmak amacıyla sistemimize, OpenAI'nin GPT-3.5 Turbo modelini merkezine alan bir "Üslup Dönüştürme Katmanı" (Tone Transformation Layer) entegre edilmiştir. Neden GPT-4 veya açık kaynaklı (Llama 3, Mistral) modeller yerine GPT-3.5 Turbo seçilmiştir? Bu sorunun yanıtı LTV / CAC Oranı ve gecikme (latency) gereksinimlerinde yatmaktadır.

### 3.1 LLM Mimari Seçimi ve LTV/CAC Optimizasyonu

*   **GPT-4 vs. GPT-3.5 Turbo:** GPT-4, kompleks akıl yürütme (reasoning) becerilerinde çok daha üstün olsa da, API maliyeti GPT-3.5'in yaklaşık 20 katıdır ve yanıt süreleri (latency) önemli ölçüde uzundur. Platformumuzdaki mesajlar nispeten kısa, yönlendirmeleri belirli (prompt engineering ile sınırlanmış) ve yüksek hacimli olduğu için GPT-4'ün maliyeti, abonelik bazlı bir sistemde müşteri yaşam boyu değerini (LTV) eritecek düzeydedir. GPT-3.5 Turbo, hem yeterli pedagojik üslubu kopyalama yeteneğine sahip hem de yüksek **LTV / CAC Oranı** hedefimizi destekleyecek kadar ekonomiktir.
*   **Açık Kaynak Modeller (Llama, Mistral vs.):** Açık kaynaklı modeller veri gizliliği açısından avantaj sağlasa da, bu modellerin kendi sunucularımızda (on-premise) yüksek erişilebilirlikle çalıştırılması ve MLOps süreçlerinin yönetimi devasa bir altyapı maliyeti gerektirir. Pazara çıkış süresini (Time-to-Market) kısaltmak ve ilk etapta geliştirme maliyetlerini minimize etmek adına yönetilen API hizmetleri (OpenAI) tercih edilmiştir. Gelecek aşamalarda maliyetleri daha da düşürmek için fine-tune edilmiş küçük açık kaynaklı modellere geçiş bir teknolojik yönelim olarak planlanmaktadır (Bölüm 8).

### 3.2 Prompt Mühendisliği ve Üslup Dönüştürme Katmanının İşleyişi

Üslup dönüştürme katmanımız, veliden gelen veya sisteme kaydedilmiş potansiyel olarak kaygılı, yargılayıcı, otoriter mesaj taslaklarını alır ve bunları **özerklik destekleyici (autonomy-supportive)**, empatik ve koçluk prensiplerine uygun mesajlara dönüştürür. 

LLM'in halüsinasyon (hallucination) görmesini ve mantıksız garantiler (örneğin "Çocuğunuz bu sistemle kesin Boğaziçi'ni kazanacak") vermesini önlemek adına katı sınırlar belirlenmiştir:
1. **Düşük Sıcaklık (Temperature = 0.2):** Modelin yaratıcılığı kısıtlanmış, bunun yerine tutarlı, öngörülebilir ve profesyonel bir rehberlik üslubu benimsemesi sağlanmıştır.
2. **Kural Bazlı Filtreler (Guardrails):** "Kesin", "garanti", "yüzde yüz" gibi hukuki ve pedagojik risk taşıyan kelimelerin çıktıda yer alması kural motoru düzeyinde engellenmiştir.

Bu katmanın pazarlama KPI'larına etkisi büyüktür. Velilere haftalık olarak sunulan ilerleme raporlarında, salt grafikler yerine LLM tarafından o haftanın verisine özel oluşturulmuş "Veli Koçluk Tavsiyeleri" bulunur. Bu sayede, uygulamanın etkileşimi pasif bir okumadan aktif bir koçluk sürecine evrilir. **Haftalık Rapor Açılma Oranı** ve **Veli-Öğrenci Diyalog Benimseme Oranı** doğrudan bu özelleştirilmiş, empatik dilin başarısına dayanmaktadır. Veli uygulamanın sadece bir ders izleme aracı olmadığını, aynı zamanda ev içi huzuru ve iletişimi artıran paha biçilmez bir asistan olduğunu gördüğünde churn ihtimali sıfıra yaklaşır.

## 4. Kural Motoru (Rule Engine) ve Tetikleyici Sistemler

Makine öğrenmesi (LightGBM) tahmin edici içgörüler sunarken, Büyük Dil Modelleri (LLM) zengin içerik üretir. Ancak bu iki yapının doğru zamanda, doğru kanalla ve doğru sıklıkla tüketiciye ulaşmasını sağlayan bir orkestrasyon mekanizmasına ihtiyaç vardır. Bu mekanizma, AI Personal Coach mimarisinin operasyonel beyni olan Kural Motoru (Rule Engine) katmanıdır.

### 4.1 Deterministik Tetikleyicilerin Gücü

Derin öğrenme veya makine öğrenmesi sistemleri probabilistik (olasılıksal) çalışır. Oysa bazı kullanıcı senaryoları kesin kurallara dayalı, anlık ve deterministik tepkiler gerektirir. Örneğin, "Öğrenci videoyu durdurup 10 dakika boyunca ekrana dokunmadıysa" durumu, risk tahmini modelinin değil, anlık bir kural motorunun konusudur.

Kural motorumuz, gerçek zamanlı veri akışını (Apache Kafka tabanlı event stream) dinleyerek önceden tanımlanmış "Eğer-Öyleyse" (If-This-Then-That / IFTTT) senaryolarını işletir. Temel tetikleyicilerimiz şunlardır:
*   **Hareketsizlik Tetikleyicisi (Inactivity Trigger):** Kullanıcı oturumundayken 10 dakikalık bir hareketsizlik saptandığında, sistem "Başlayamayan" veya "Yarıda Bırakan" segment kurallarını devreye sokar ve anında mikro bir dürtükleme (nudge) gönderir.
*   **Terk Etme Eşiği (Abandonment Threshold):** Bir haftada planlanan derslerin %50'si iptal edilmişse, modelin risk skoru yüksek olmasa bile kural motoru "Haftalık Rapor Erken Gönderim" sürecini başlatarak veliyi uyarır.
*   **Escalation (İnsan Desteğine Yönlendirme):** LightGBM modelinin ürettiği churn risk skoru 0.85'in üzerine çıktığında, kural motoru LLM'i devreden çıkararak durumu derhal İnsan Müşteri Başarı (Customer Success) ekibine havale eder (Escalation to Human Success). Yüksek riskli müşterilerin kaybını önlemek için yapay zeka yerine insan empatisinin devreye girmesi, premium müşteri deneyiminin bir parçasıdır.

### 4.2 Bildirim Yorgunluğunun Önlenmesi (Notification Fatigue Prevention)

Kural motorunun en hayati işlevlerinden biri, kullanıcıyı mesaj bombardımanına tutarak "bildirim yorgunluğu" (notification fatigue) yaratmayı önlemektir. Aşırı bildirim, kullanıcının uygulamayı sessize almasına (mute) veya tamamen silmesine yol açar. Bunu engellemek için şu limitler (Rate Limiting) uygulanır:
*   Öğrenciye bir seans içinde en fazla 1 mikro dürtükleme (nudge) gönderilebilir.
*   Veliye acil durumlar haricinde haftada maksimum 2 adet proaktif rehberlik mesajı gönderilir.
*   "Geceye Kayan" profilindeki öğrencilere, veli bildirimleri ertesi sabah 09:00'a kadar geciktirilerek ev içi anlık krizlerin önüne geçilir (Cool-off period).

Bu hassas zamanlama (timing) ve frekans kontrolü sayesinde, **Bildirim Aksiyonu Tamamlama Oranı** maksimize edilir. Mesajlar, kullanıcıların en açık ve alıcı oldukları anlarda (örneğin sabah kahvaltısı öncesi veliye, çalışma planı başlangıcında öğrenciye) iletilir. Kural motorunun bu akıllı orkestrasyonu, yapay zekanın tavsiyelerini teoriden çıkarıp, doğru anda tetiklenen kusursuz bir kullanıcı deneyimine (UX) dönüştürmektedir.

---
*(Belgenin devamı için Bölüm 5-8'e geçilecektir.)*


## 5. Veri Gizliliği, KVKK Uyumluluğu ve Şeffaf Takip Mimarisi

Eğitim teknolojilerinde veri toplamak sadece teknik bir gereklilik değil, aynı zamanda ciddi bir güven (trust) ve regülasyon (KVKK/GDPR) meselesidir. Hedef kitlemiz olan 13-18 yaş aralığındaki ergenler, sürekli gözetlenme (surveillance) hissine karşı son derece duyarlıdır. Sistemin sürekli açık kalarak arka planda tüm dijital aktiviteleri izlemesi ("sürekli izleme"), ergen psikolojisinde "kendi özel alanına müdahale" olarak algılanmakta, bu da doğrudan platformun reddedilmesiyle (sistemden kaçış) sonuçlanmaktadır. AI Personal Coach projesinde bu "Kişiselleştirme-Gözetlenme Paradoksu"nu aşmak için "Şeffaf ve Sınırlı Odak Takibi" (Transparent and Bounded Focus Tracking) mimarisi benimsenmiştir.

### 5.1 Şeffaf Sınırlı Odak Takibi ve İzin Yönetimi

Sistemimiz, cihazın arka planında gizlice çalışan bir casus yazılım (spyware) mantığını tamamen reddeder. Veri takibi, yalnızca ve yalnızca öğrencinin kendi iradesiyle "Çalışma Modunu Başlat" (Start Study Session) butonuna bastığı an başlar ve çalışma bloğu bittiğinde kesin olarak sonlanır. Bu sınırlı takip süresi boyunca cihazdaki uygulamalar arası geçişler (context switching) analiz edilir; ancak hangi mesajın yazıldığı veya hangi spesifik içeriğin izlendiği kaydedilmez. 

Bu etik ve mimari tercih, teknik bir sınırlama değil, pazarlama stratejimizin yapıtaşıdır:
*   **Öğrenci Güveni:** Öğrenci, takip edildiği anların tamamen kendi kontrolünde olduğunu bilir. Bu durum özerklik duygusunu destekler ve platformu bir "gardiyan" değil, "asistan" olarak konumlandırır.
*   **Veli Onayı ve KVKK (Kişisel Verilerin Korunması Kanunu):** 18 yaş altı kullanıcıların verilerinin işlenmesi, KVKK kapsamında açık veli rızasına ve katı aydınlatma yükümlülüklerine tabidir. Sınırlı izleme mimarimiz, veliye sistemin sadece akademik sürelerle ilgilendiğini garanti eder. "Güvenli Liste" (Whitelisting) özelliği sayesinde, Wikipedia veya diğer eğitici uygulamalardaki vakit geçirme eylemleri "Telefonla Dağılan" segmentine dahil edilmez ve yanlış pozitif (false positive) uyarıların önüne geçilir.

Veri tabanı katmanımızda, öğrenci kimlik verileri (PII - Personally Identifiable Information) ile davranışsal tıklama verileri ayrı şemalar altında kriptografik olarak hashlenmiş ID'ler üzerinden eşleştirilir. Böylece veri tabanımıza olası bir siber müdahale durumunda bile davranış verilerinin kişisel kimliklerle eşleştirilmesi imkansız hale getirilir. Markaya duyulan bu şeffaf güven, **90 Günlük Veli Elde Tutma (Retention) Oranı**'nın sürdürülebilirliğini koruyan en temel güvencedir.

## 6. API Entegrasyonları ve Gecikme (Latency) Optimizasyonları

Abonelik tabanlı platformlarda kullanıcı deneyiminin (UX) kesintisiz akması, algılanan kalite için vazgeçilmezdir. Hem makine öğrenmesi modelinin hem de LLM'in eş zamanlı çalıştığı mimarilerde, kullanıcıya dönen yanıt sürelerindeki (latency) en ufak bir gecikme, uygulamanın hantal ve kullanışsız olarak değerlendirilmesine yol açar.

### 6.1 Mikroservis Mimarisi ve Asenkron İşlemler

Sistemimiz monolitik (tek parça) bir yapı yerine, hafif ve dağıtık bir mikroservis mimarisi (Microservices Architecture) üzerine inşa edilmiştir. Risk tahmini, mesaj üretimi, kural orkestrasyonu ve kullanıcı arayüzü birbirinden bağımsız konteynerlar (Docker/Kubernetes) içerisinde çalışır.
*   **Asenkron İşleyiş:** Öğrencinin tıklama verileri, doğrudan bir REST API üzerinden değil, Apache Kafka üzerinden asenkron bir olay akışı (event stream) ile kural motoruna iletilir. Bu sayede uygulamanın ana iş parçacığı (main thread) asla bloke edilmez; öğrenci arayüzde donma yaşamaz.
*   **LLM Gecikme Optimizasyonu:** OpenAI GPT-3.5 Turbo'nun yanıt süresi, ağ trafiğine bağlı olarak zaman zaman 2-3 saniyeyi bulabilmektedir. Kullanıcının (velinin) bu süreyi beklememesi için üslup dönüştürme işlemi genellikle arka planda (background worker) önbelleğe alınarak asenkron olarak gerçekleştirilir. Örneğin, "Haftalık Rapor", cuma günü saat 15:00'te teslim edilecekse, LLM bu raporun metnini saat 14:00'te hazırlamaya başlar. Bu *pre-computation* tekniği ile son kullanıcı için latency pratikte sıfıra indirilmiştir.

### 6.2 Redis Cache ve Edge Computing (Uç Bilişim) Kullanımı

Sık erişilen statik verilerin (örneğin kural motorundaki eşik değerleri, güvenli liste içerikleri) ve bazı popüler LLM çıktılarının (genel motivasyon şablonları) tekrar tekrar hesaplanmasını önlemek için Redis tabanlı bir in-memory cache (bellek içi önbellekleme) katmanı kullanılmıştır. Ayrıca, uygulamanın "Zamanlayıcı" (Timer) ve "Anlık Mikro Dürtükleme" bileşenleri doğrudan kullanıcının cihazında (Edge Computing) çalıştırılarak sunucuya git-gel süreleri tamamen ortadan kaldırılmıştır.

## 7. Ölçeklenebilirlik, MLOps ve Sürekli Öğrenme (Scalability & CI/CD)

Platformun lansman sonrası hızla büyüyecek bir kullanıcı tabanına (örneğin 100.000 aktif kullanıcıya) hizmet verebilmesi için altyapının yatayda (horizontal scaling) kolayca büyütülebilir olması gerekir.

### 7.1 MLOps Süreçleri ve Modelin Yaşlanması (Model Drift)

Makine öğrenmesi modelleri zamanla eskir. Öğrenci davranışları, sınav sistemindeki müfredat değişiklikleri, mevsimsel etkiler (bahar yorgunluğu vs.) gibi faktörler, LightGBM modelimizin doğruluk oranının zamanla düşmesine (Model Drift / Concept Drift) yol açabilir. 
Bunu engellemek için kurduğumuz MLOps boru hattı (pipeline) şu adımları içerir:
1.  **Sürekli İzleme:** Modelin sahadaki başarımı, kullanıcıların gerçekten derse dönüp dönmediği üzerinden (Bildirim Aksiyonu Tamamlama Oranı verisiyle) sürekli takip edilir.
2.  **Otomatik Yeniden Eğitim (Automated Retraining):** Modelin başarımı belirlenen bir eşiğin altına düştüğünde, sistem son 30 günün yeni verilerini alarak gözetimli bir şekilde (human-in-the-loop gözetiminde) modeli otomatik olarak yeniden eğitir.
3.  **A/B Testi Dağıtımı:** Yeni model, trafiğin yalnızca %10'luk bir kesimine (Canary Release) açılarak eski modelle kıyaslanır. Yeni model **Denemeden Ücretliye Geçiş Oranı**'nda artış sağlarsa tüm sisteme yaygınlaştırılır.

Bu sürekli öğrenme döngüsü, AI Personal Coach'un durağan bir yazılım değil, organik olarak evrilen ve kullanıcıyı tanıdıkça akıllanan bir asistan olmasını sağlar.

## 8. Sonuç ve Gelecek Teknolojik Yönelimler

Bu raporda detaylandırılan teknolojik mimari kararları, AI Personal Coach projesinin pazarlama hedefleriyle tam bir uyum içinde tasarlanmıştır. LightGBM'in yüksek doğruluk ve yorumlanabilirlik kapasitesi, kural motorunun asenkron ve düşük gecikmeli orkestrasyonu, OpenAI GPT-3.5 Turbo'nun pedagojik üslup dönüştürme gücü ile birleşerek veli elde tutma (retention) problemini teknolojik olarak çözmüştür.

**Kısa ve Orta Vadeli Teknolojik Planlarımız:**
1.  **Açık Kaynak Modellerine Geçiş (R&D Phase):** OpenAI maliyetlerini sıfırlamak ve veri gizliliğini maksimuma çıkarmak amacıyla, Llama 3 (veya muadili Mistral) modellerinin yalnızca "pedagojik koçluk" verisiyle eğitilerek (Fine-Tuning) kendi sunucularımızda barındırılması planlanmaktadır. Bu sayede **LTV / CAC Oranı**'nda marjinal bir artış yakalanacaktır.
2.  **Sesli Etkileşim (Speech-to-Text):** Projenin AR-GE safhasında, öğrencilerin duygusal durumunu analiz edebilmek için OpenAI Whisper (veya muadili açık kaynak modeller) kullanılarak sesli notlardan duygu analizi yapılması düşünülmektedir. Ses analizi, öğrencinin metinle ifade edemediği sınav kaygısını tonlamasından anlayarak risk modelini (LightGBM) çok daha erken uyarabilecektir. Ancak bu modül, KVKK uyumluluğu gözetilerek yalnızca aktif öğrenci onayıyla (opt-in) devreye alınacaktır.

Özetle, teknolojiyi bir amaç değil, ebeveyn ile öğrenci arasındaki iletişimsizliği çözen, ticari abonelik metriklerini iyileştiren güvenilir bir "araç" olarak konumlandırdık. AI Personal Coach, salt analitik doğrulukla değil, insani duyguları anlayan, empati kuran ve özerkliği destekleyen bütüncül mimarisiyle EdTech pazarında yeni bir standart belirlemektedir.


## 9. Derinlemesine Mimari Analiz: Matematiksel Modeller ve Veri Akışı

Bu bölümde, AI Personal Coach sisteminin kalbini oluşturan makine öğrenmesi algoritmalarının matematiksel temelleri ve veri işleme (data pipeline) süreçleri detaylı bir şekilde incelenecektir. Modelin teknik doğruluğu, doğrudan "90 Günlük Veli Elde Tutma (Retention) Oranı" metriğine etki ettiği için, hiperparametre optimizasyonundan kayıp fonksiyonlarına (loss functions) kadar her detayın pazarlama çıktısı düşünülerek tasarlanması gerekmiştir.

### 9.1 LightGBM Matematiksel Temelleri ve Hiperparametre Optimizasyonu

Dersten kopuş (churn) riski, doğası gereği ikili bir sınıflandırma (binary classification) problemidir. Öğrenci ya dersten kopar ($y=1$) ya da eğitime devam eder ($y=0$). Ancak pazarlama müdahaleleri için sadece $0$ veya $1$ tahmini yeterli değildir; sistemin, öğrencinin kopma "ihtimalini" (risk score) sürekli ve güncellenen bir olasılık fonksiyonu $P(y=1|x)$ olarak hesaplaması gerekir.

LightGBM algoritması, bu olasılığı gradyan artırma (gradient boosting) yaklaşımıyla optimize eder. Modelin temel amacı, aşağıdaki lojistik kayıp (logistic loss - logloss) fonksiyonunu minimize etmektir:

$$ \mathcal{L}(y, p) = -\frac{1}{N} \sum_{i=1}^{N} \left[ y_i \log(p_i) + (1 - y_i) \log(1 - p_i) \right] $$

Burada:
*   $N$: Analiz edilen toplam öğrenci oturumu sayısı.
*   $y_i$: Öğrencinin gerçek durumu (1: churn, 0: aktif).
*   $p_i$: Modelin öğrencinin churn yapacağına dair tahmini olasılığı.

LightGBM'i XGBoost'tan ayıran en temel fark, Eğitim verisini histogram tabanlı ağaçlara bölmesidir. Karar ağaçlarının bölünme (split) noktalarında kazancı (Information Gain) maksimize etmek için GOSS (Gradient-based One-Side Sampling) algoritması kullanılır. GOSS, yüksek gradyana (yani modelin henüz doğru tahmin edemediği, büyük hataya sahip) sahip örneklere odaklanırken, düşük gradyanlı veri noktalarını rastgele örnekleyerek eğitim setinden çıkarır. 

**Modelin Mimarisine Entegre Edilen Hiperparametreler:**
*   `learning_rate` (0.01 - 0.05): Modelin çok hızlı ezberlemesini (overfitting) önlemek için düşük tutulmuştur. Bu, özellikle "Kaygıyla Erteleyen" öğrenci profillerinde zamanla değişen yavaş davranışsal sinyallerin daha doğru yakalanmasını sağlar.
*   `num_leaves` (31 - 63): Yaprak odaklı (leaf-wise) büyüme algoritması gereği, `num_leaves` değeri ağacın ne kadar karmaşıklaşacağını belirler. Derinlik sınırlandırılmadığında aşırı uyuma (overfitting) yatkınlık oluşur, bu nedenle `max_depth` parametresi ile sınırlandırılarak genelleştirme yeteneği artırılmıştır.
*   `scale_pos_weight`: Dersten kopan öğrenci (churn) sayısının, derse devam eden öğrenci sayısına oranı genellikle çok düşüktür (örneğin %5 churn, %95 aktif). Modelin sadece çoğunluk sınıfına (aktif) odaklanıp churn olaylarını kaçırmaması için, bu parametre azınlık sınıfı lehine ağırlıklandırılmıştır. Bu ince ayar, doğrudan "Bildirim Aksiyonu Tamamlama Oranı" KPI'sını hedefler çünkü model yanlış alarm (false positive) verirse velide "bildirim yorgunluğu" oluşur, alarmı kaçırırsa (false negative) abone kaybedilir.

### 9.2 SHAP (SHapley Additive exPlanations) ve Yorumlanabilirlik

Modelin ürettiği risk skoru, veliye açıklanabilir (explainable) olmak zorundadır. "Neden çocuğumun risk skoru %85?" sorusunun teknik değil, eyleme dönüştürülebilir pedagojik bir cevabı olmalıdır. Bu noktada SHAP değerleri devreye girer.

Oyun teorisi (Game Theory) temelli SHAP değerleri, modele giren her bir özelliğin (feature), o anki risk tahminine ne kadar katkı (pozitif veya negatif) sağladığını hesaplar:

$$ \phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|! (|F| - |S| - 1)!}{|F|!} \left[ f_x(S \cup \{i\}) - f_x(S) \right] $$

Sistemimiz, her risk skoru yükseldiğinde LightGBM modelinden SHAP değerlerini çeker. Örneğin, bir öğrenci için en yüksek SHAP değerine sahip olan değişken `idle_time_last_10m` (son 10 dakikadaki boşta kalma süresi) ise, sistem bu durumu "Başlayamayan" veya "Yarıda Bırakan" segmenti olarak etiketler. Bu etiket, LLM katmanına ("Üslup Dönüştürme") prompt parametresi olarak geçer. Böylece LLM veliye, "Öğrencinin son günlerde derslere başlama süresinde gecikmeler yaşanıyor (Başlayamayan profil), lütfen şu yaklaşımla konuşmayı deneyin..." diyebilir. Yorumlanabilirlik (Explainability), teknik bir zorunluluk değil, doğrudan "Veli-Öğrenci Diyalog Benimseme Oranı"nı artıran stratejik bir karar mekanizmasıdır.

## 10. API Mimarisi, Payload Yapıları ve Sistem Entegrasyonu

Platformumuz, modüler ve yüksek erişilebilirlikli (High Availability - HA) bir mikroservis yapısı (Microservices Architecture) üzerine inşa edilmiştir. Risk tahmini, Kural Motoru, LLM orkestrasyonu ve İletişim Servisleri arasındaki tüm haberleşme JSON tabanlı RESTful API'ler ve Apache Kafka üzerinden asenkron event-driven (olay güdümlü) mimari ile sağlanır.

### 10.1 Veri Akış Mimarisi (Data Pipeline)
1.  **Event Ingestion (Olay Alımı):** Mobil veya web istemcisi (Client), öğrencinin tıklamalarını, sayfada kalma süresini ve ders başlama/bitirme olaylarını şifrelenmiş paketler halinde bir API Gateway'e iletir.
2.  **Stream Processing (Akan Veri İşleme):** Veri paketleri Apache Kafka topic'lerine yazılır. Apache Flink veya Spark Streaming kullanılarak (sistem ihtiyacına göre), bu veriler gerçek zamanlı (real-time) olarak zaman pencerelerine (time windows) bölünür (ör. son 10 dakika, son 1 saat, son 1 hafta).
3.  **Feature Store:** İşlenmiş metrikler (ör. `average_response_time`, `skip_rate`) düşük gecikmeli bir Feature Store'a (ör. Redis tabanlı bir önbelleğe) yazılır.
4.  **Inference (Tahmin):** Kural motoru, her 5 dakikada bir veya belirli bir tetikleyici oluştuğunda Feature Store'dan güncel durumu çeker ve LightGBM API'sine gönderir. Model, anlık risk skorunu ve en baskın SHAP özelliklerini döndürür.

### 10.2 JSON Payload Örnekleri

Sistem entegrasyonunu ve veri formatını daha iyi anlamak için, Model-Kural Motoru-LLM zinciri arasındaki JSON mesajlaşma yapıları aşağıda örneklendirilmiştir.

**A. Kural Motorundan LightGBM Tahmin Servisine Giden İstek (Request):**
```json
{
  "student_id": "c8x9d2k4",
  "session_id": "ses_90123",
  "timestamp": "2026-08-16T14:30:00Z",
  "features": {
    "total_session_duration_min": 45,
    "idle_time_last_10m": 8.5,
    "difficulty_level_chosen": "easy",
    "historical_completion_rate": 0.65,
    "time_of_day": 23.5
  }
}
```

**B. LightGBM Servisinin Kural Motoruna Döndüğü Yanıt (Response):**
```json
{
  "risk_score": 0.82,
  "predicted_segment": "Geceye Kayan",
  "top_shap_features": [
    {"feature": "time_of_day", "contribution": 0.45},
    {"feature": "idle_time_last_10m", "contribution": 0.30}
  ],
  "action_required": true,
  "confidence_interval": [0.75, 0.88]
}
```

**C. Kural Motorundan LLM (GPT-3.5 Turbo) Servisine Giden Prompt İsteği:**
```json
{
  "model": "gpt-3.5-turbo",
  "temperature": 0.2,
  "messages": [
    {
      "role": "system",
      "content": "Sen özerkliği destekleyen uzman bir eğitim pedagojisi koçusun. Hedefin, kaygılı ebeveynlere çocuklarının 'Geceye Kayan' profiline uygun, yargılamadan uzak, yapıcı iletişim önerileri sunmaktır. 'Kesin', 'garanti', 'yüzde yüz' kelimelerini asla kullanma. LGS/YKS bağlamında kal."
    },
    {
      "role": "user",
      "content": "Veli profili: Yüksek kaygılı anne. Öğrenci segmenti: Geceye Kayan. Risk skoru: 0.82. Son 10 dakikada 8.5 dakika hareketsiz kaldı ve saat çok geç. Veliye gönderilecek 150 kelimeyi aşmayan, empati odaklı ve eyleme geçirilebilir bir SMS/Bildirim metni oluştur."
    }
  ]
}
```

Bu yapısal JSON akışı, gecikmeyi (latency) en aza indirerek sistemin her bir parçasının birbirinden bağımsız şekilde ölçeklenmesine olanak tanır. Kural motoru, LLM yanıtını aldıktan sonra, velinin saat dilimini ve iletişim tercihlerini (SMS, Push Notification, Email) kontrol ederek mesajın doğru zamanda iletilmesini sağlar. Örneğin, "Geceye Kayan" profilinde saat gece 01:00 ise, kural motoru bu LLM çıktısını "Cool-off queue" (bekleme kuyruğu) içine atar ve mesaj veliye sabah 09:00'da gönderilir. Bu durum doğrudan "Bildirim Aksiyonu Tamamlama Oranı"nı ve sistemin organik entegrasyon algısını yükseltir.

## 11. LLM Prompt Mühendisliği ve Model Güvenliği (Guardrails)

LLM katmanı, marka itibarını ve güvenliğini doğrudan etkileyen bir dışa vurum (output) noktasıdır. Üretilen hatalı bir içerik (halüsinasyon), velinin uygulamaya güvenini derhal sıfırlayarak anında churn ile sonuçlanabilir. Bu yüzden GPT-3.5 Turbo ile etkileşime girerken çok katmanlı bir Prompt Mühendisliği (Prompt Engineering) ve Çıktı Doğrulama (Guardrails) yapısı geliştirilmiştir.

### 11.1 Çoklu Ajan Çerçevesi (Multi-Agent Framework) ve Çıktı Doğrulaması

AI Personal Coach, sadece tek bir LLM çağrısı yapmak yerine, doğruluğu artırmak için zincirleme bir Doğrulama Ajanı (Validation Agent) kullanır:
1.  **Üretici Ajan (Generator Agent):** Kural motorundan gelen metriklerle veliye yönelik ilk taslağı oluşturur.
2.  **Denetleyici Ajan (Critic / Guardrail Agent):** Üretilen taslağı alır ve 3 katı kural üzerinden denetler:
    *   Kural 1: Yargılayıcı bir dil içeriyor mu? (Örn. "Çocuğunuz ders çalışmıyor")
    *   Kural 2: KVKK'ya veya veri gizliliğine aykırı bir ifşa var mı? (Örn. "Arkadaşıyla mesajlaştı" yerine "Platform dışında vakit geçirdi" kullanılmalı).
    *   Kural 3: Pazarlama garantisi veren yasaklı kelimeler (kesin, garanti, kazanacak) geçiyor mu?

Eğer Denetleyici Ajan "Geçti" (Pass) yanıtı verirse, mesaj kullanıcıya iletilir. Aksi takdirde "Reddedildi" (Fail) yanıtı döner ve önceden yazılmış, statik olarak onaylanmış standart bir pedagojik şablon (fallback template) veliye gönderilir. Bu güvenlik ağı, marka riskini sıfıra indirirken **Denemeden Ücretliye Geçiş Oranı** (Trial-to-Paid) açısından sistemin "güvenilir ve profesyonel" algısını (Brand Trust) radikal biçimde pekiştirir.


## 12. MLOps, Sürekli Entegrasyon ve Sürekli Dağıtım (CI/CD) Altyapısı

Pazarlama odaklı makine öğrenmesi projelerinde, bir modelin laboratuvar (Jupyter Notebook) ortamında gösterdiği performans ile canlı (production) ortamda gösterdiği performans arasında ciddi bir uçurum olabilir. Bu uçurum, eğitim verisi ile canlı veri arasındaki yapısal veya anlamsal farklardan (Data Skew / Concept Drift) kaynaklanır. AI Personal Coach projesinde bu riski minimize etmek için uçtan uca, tamamen otomatikleştirilmiş bir MLOps ve CI/CD (Sürekli Entegrasyon / Sürekli Dağıtım) boru hattı kurulmuştur.

### 12.1 Veri Sürümleme (Data Versioning) ve Model Kayıt Defteri (Model Registry)

Aylık bazda binlerce yeni kullanıcının sisteme katıldığı bir senaryoda, her hafta toplanan tıklama verilerinin karakteristiği değişebilir. Örneğin, deneme sınavlarının yaklaştığı bir ayda "Kaygıyla Erteleyen" profil sayısında anormal bir artış gözlemlenebilir. 
Sistemimizde verilerin tutarlılığını sağlamak için DVC (Data Version Control) aracı kullanılarak her eğitim verisi (dataset) tıpkı bir kod bloğu gibi Git üzerinden sürümlenmektedir (versioning).

LightGBM modellerinin her bir yeni versiyonu eğitildiğinde (retraining), MLflow tabanlı bir "Model Kayıt Defteri"ne (Model Registry) kaydedilir. MLflow üzerinde:
*   Modelin hiperparametreleri (learning rate, max depth).
*   Performans metrikleri (Validation LogLoss, F1 Score).
*   En önemlisi, Pazarlama Etki Metrikleri (O modelin önceki versiyonuna kıyasla simüle edilmiş **90 Günlük Veli Elde Tutma (Retention) Oranı**).
loglanmaktadır. Eğer yeni eğitilen model, doğruluk metriklerinde bir önceki versiyonu geçemezse veya yanlış pozitif (false positive) oranı artarsa, CI/CD boru hattı (GitHub Actions veya GitLab CI) modelin canlı ortama (production) geçmesini otomatik olarak durdurur (rollback).

### 12.2 A/B Testleri ve Gölge Dağıtım (Shadow Deployment)

Yeni bir kural motoru senaryosu veya yeni bir LightGBM versiyonu geliştirildiğinde, doğrudan tüm kullanıcı tabanına sunulmaz. Sistem, algoritmik güncellemeleri pazarlama KPI'ları üzerinde kanıtlamak için iki katmanlı bir dağıtım stratejisi izler:

1.  **Shadow Deployment (Gölge Dağıtım):** Yeni model canlı ortama alınır ancak verdiği kararlar kullanıcılara gösterilmez (sadece veritabanına loglanır). Gölge modelin ürettiği risk skorları ile mevcut modelin skorları arka planda karşılaştırılır. Eğer yeni model "Yarıda Bırakan" bir öğrenciyi eski modelden 5 dakika daha erken tespit edebiliyorsa, ikinci aşamaya geçilir.
2.  **A/B Testi (Canary Release):** Kullanıcı tabanının rastgele seçilmiş %10'u "B Grubu"na (yeni model), %90'ı ise "A Grubu"na (eski model) atanır. 14 günlük bir sprint sonunda, B grubundaki **Bildirim Aksiyonu Tamamlama Oranı** ve **Haftalık Rapor Açılma Oranı** istatistiksel olarak anlamlı bir (p < 0.05) iyileşme gösteriyorsa, yeni model tüm sisteme (100%) açılır. 

Bu veri güdümlü ve son derece ihtiyatlı MLOps süreçleri, **LTV / CAC Oranı** üzerinde dramatik düşüşlere yol açabilecek "hatalı bir güncelleme" (bad release) senaryosunu tamamen engeller. Teknoloji ekibinin her kodu, doğrudan pazarlama departmanının churn oranlarıyla senkronize edilmiştir.

## 13. Edge Computing (Uç Bilişim) ve Mobil İstemci Optimizasyonu

Günümüzde pek çok EdTech platformu yoğun hesaplama (heavy computation) gerektiren işlemleri bulut sunucularına (Cloud) yaptırır. Ancak sürekli sunucuya ping atmak, hem bulut maliyetlerini (AWS/GCP faturalarını) şişirir hem de kullanıcının internet bağlantısının zayıf olduğu durumlarda bildirimlerin gecikmesine neden olur. Bu durumu çözmek için AI Personal Coach projesinde Edge Computing (Uç Bilişim) mimarisinden faydalanılmıştır.

Öğrencinin anlık odaklanma süreleri, cihazın kilit ekranına geçip geçmediği veya aktif uygulamadan ne kadar koptuğu gibi yüksek frekanslı sinyaller (high-frequency signals), buluta saniyede bir veri göndermek yerine, doğrudan iOS veya Android işletim sisteminin arka plan worker'ları (lokal cihaz) üzerinde hesaplanır.
*   **Lokal Kural Motoru:** Öğrencinin "Başlayamayan" bir döngüde olup olmadığı cihazın kendisinde hesaplanır. Yalnızca 10 dakikalık eşik (threshold) aşıldığında buluta tek bir JSON paketi gönderilir. Bu, sunucu trafiğini %80 oranında azaltarak muazzam bir maliyet optimizasyonu (**LTV / CAC Oranı** iyileştirmesi) sağlar.
*   **Çevrimdışı Çalışabilirlik (Offline Graceful Degradation):** İnternet koptuğunda cihaz içi lokal yapay zeka (On-device ML), öğrencinin çalışma performansını kaydetmeye devam eder ve internet geldiğinde asenkron olarak verileri senkronize eder. Böylece veri kaybı önlenir ve haftalık veli raporlarının doğruluğu tehlikeye atılmaz.

## 14. Sonuç ve Stratejik Değerlendirme

AI Personal Coach projesinin teknolojik değerlendirmesi sonucunda, sistemin donanımsal ve yazılımsal her bir bileşeninin (LightGBM, GPT-3.5 Turbo, Kural Motoru, Kafka), platformun asıl varoluş amacı olan "churn problemini çözmek" hedefine hizalandığı açıkça görülmektedir.

*   LightGBM'in hızı ve SHAP yorumlanabilirliği; siyah kutu (black-box) modellerinin aksine veliye güven ve şeffaflık sunmaktadır.
*   GPT-3.5 Turbo'nun pedagojik üslup dönüştürme yeteneği, velinin baskıcı mesajlarını özerklik destekleyici koçluk iletişimine çevirerek ev içi çatışmayı azaltmaktadır.
*   Kafka ve mikroservis tabanlı asenkron veri akışı, bildirimlerin tam zamanında (Just-in-Time) ulaşmasını sağlayarak **Bildirim Aksiyonu Tamamlama Oranı**nı maksimize etmektedir.
*   Şeffaf ve sınırlı izleme mimarisi ise, KVKK uyumluluğunun yanı sıra genç kullanıcılar nezdinde platformun kabul görmesini sağlamaktadır.

Neticede, bu projedeki teknoloji seçimi sadece "en modern aracı kullanmak" (hype-driven development) değil; psikolojik bir bariyeri aşmak, güven inşa etmek ve **90 Günlük Veli Elde Tutma Oranını** sürdürülebilir kılmak için yapılmış stratejik bir yatırımdır.


