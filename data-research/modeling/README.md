# Baseline Modeling Pipeline (K3: Data Lead)

Bu modül, AI Personal Coach projesinde veli churn/retention risk tahminlemesi için eğitilen baseline makine öğrenmesi modellerini içerir.

## 1. Çalıştırma Talimatı

Baseline modelleme scripti tek bir komutla uçtan uca çalıştırılabilir:

```bash
python data-research/modeling/baseline_models.py
```

Bu komut:
1. `data-research/oulad_synthetic_processed.csv` veri setini yükler ($N=3,250$, 8 feature).
2. Veriyi %75 train / %25 test olarak stratified ve sabit seed (`random_state=42`) ile böler.
3. **Logistic Regression** ve **LightGBM Classifier** modellerini eğitir.
4. `baseline_results.csv` dosyasını oluşturur.
5. `confusion_matrix_logistic.png` ve `confusion_matrix_lightgbm.png` grafiklerini kaydeder.
6. Eğitilen modelleri (`lightgbm_model.joblib`, `logistic_model.joblib`) K5 pipeline'ı için serialize eder.

---

## 2. Karşılaştırmalı Model Metrikleri

`oulad_synthetic_processed.csv` veri seti üzerinde $N=813$ test örneği ile elde edilen doğrulanmış sonuçlar:

| Model | ROC-AUC | PR-AUC | F1-Score | Precision | Recall | Accuracy | LogLoss | TN | FP | FN | TP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **0.6490** | 0.6124 | **0.6172** | 0.6179 | **0.6164** | **0.6322** | **0.6595** | 273 | 149 | 150 | 241 |
| **LightGBM Classifier** | 0.6426 | **0.6118** | 0.5666 | **0.6273** | 0.5166 | 0.6199 | 0.6668 | **302** | **120** | 189 | 202 |

*(Proxy etiket: `churn_90d` | Split: 75/25 Stratified | Random Seed: 42)*

---

## 3. Model Seçimi ve Analiz

### 3.1 Neden LightGBM Tercih Edildi?
1. **Daha Düşük Yanlış Pozitif (False Positive - FP):**
   - LightGBM, 120 FP üretirken Logistic Regression 149 FP üretmiştir. Veli iletişiminde "yanlış alarm" (öğrenci çalışırken gereksiz veli uyarısı göndermek) veli güvenini zedeleyebileceğinden, yüksek Precision (%62.7) ve düşük FP oranı kritik bir avantajdır.
2. **Açıklanabilir Yapay Zeka (XAI) ve Feature Importance:**
   - LightGBM ağaç yapısı sayesinde her tahminin hangi özelliklerden (örneğin `parent_report_open_rate` ve `phone_distraction_10min_count`) kaynaklandığını kural motoruna iletebilir.
3. **Doğrusal Olmayan Dinamikler:**
   - Gece çalışma oranı ve odak süresi gibi etkileşimli özellikler gerçek sahada doğrusal olmayan eşik değerlerine (non-linear thresholds) sahiptir.

### 3.2 Metrik Düzeltme Notu (Consistency Note)
Önceki taslak dokümanlarda LightGBM'in ROC-AUC skoru için teorik/tahmini olarak "~0.78" ifadesi yer almış ve EDA tablosunda LR skoru daha yüksek olmasına rağmen metinde LightGBM "en yüksek skor" olarak nitelendirilmiştir. Bu tutarsızlık giderilmiş olup, yukarıdaki tabloda yer alan **0.6426 ROC-AUC** ve **%62.7 Precision** değerleri projenin resmi doğrulanmış baseline metrikleri olarak belirlenmiştir.

---

## 4. Veri Sınırlılıkları Beyanı

> [!WARNING]
> - `churn_90d` etiketi, OULAD açık verisindeki terk (withdrawal) proxy'si ve sentetik davranış özelliklerinin birleşimidir.
> - Bu sonuçlar **gerçek bir LGS/YKS pilot denemesi sonucu değildir**, PoC seviyesinde matematiksel akışın çalıştığını gösteren **sentetik/proxy baseline** niteliğindedir.
