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
