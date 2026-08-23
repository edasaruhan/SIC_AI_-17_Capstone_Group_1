# 1. Baseline Notu (Baseline Numbers for Methodology)

Aşağıdaki tablo, `data-research/notebooks/oulad_eda.ipynb` dosyasındaki mevcut model sonuçlarını göstermektedir:

| Model | Etiket (Proxy) | n / split | Metrik | Sayı | Kaynak (Figür / Cell) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Lojistik Regresyon | churn_90d (olumsuz / withdrawal proxy) | %75 train / %25 test | ROC-AUC / F1 | Koşulmadı | Cell 4 |
| LightGBM | churn_90d (olumsuz / withdrawal proxy) | %75 train / %25 test | ROC-AUC / F1 | Koşulmadı | Cell 4 |

*(Not: Notebook henüz veri seti ile çalıştırılmadığı için AUC/F1 çıktıları boştur. Kural gereği veriler uydurulmamış, "Koşulmadı" olarak raporlanmıştır.)*

**Zorunlu Veri Kısıtı Uyarıları:**
* `final_result` / `withdrawal` veli churn değildir; öğrenme sonucu proxy'sidir (vekil veri).
* OULAD UK 2013–14 uzaktan yetişkin popülasyonudur; LGS/YKS'ye genellenmez.
* Bu sayılar 90 günlük veli retention kanıtı değildir.

**Kullanılan Temel Feature'lar (5-8 adet):**
`vle_total_clicks`, `avg_focus_duration_mins`, `phone_distraction_10min_count`, `date_registration`, `gender`, `highest_education`, `studied_credits`.

**Engagement ve Olumsuz Sonuç İlişkisi Özeti:**
Öğrencinin platform içindeki etkileşimi (engagement) ile dersi bırakma (withdrawal) veya başarısız olma durumu arasında ters bir orantı gözlemlenmiştir. Özellikle ilk haftalardaki düşük `vle_total_clicks` (tıklama sayısı) değerleri, olumsuz sonucun en güçlü erken uyarı sinyallerinden biridir. Sisteme geç kayıt olan veya başlangıçta etkileşimi düşük kalan kullanıcıların etiketlerinin olumsuz olma ihtimali daha yüksektir. Ancak bu durum doğrudan velinin abonelikten çıkma (churn) sebebi olarak kesinleştirilemez, sadece erken risk tespitinde matematiksel bir temel oluşturur.

---

# 2. Implementation Plan §4 Challenges (K3 Katkısı)

Projenin veri ve modelleme aşamasında karşılaşılan riskler aşağıda özetlenmiştir:

| Risk | Sayısal Gerekçe | Mitigation (Önlem) | Fallback (B/C Planı) |
| :--- | :--- | :--- | :--- |
| **Sınıf dengesizliği / Seyrek tıklama** | Churn (Withdrawal) sınıfı, tüm veri setinin yaklaşık %30'unu oluşturmaktadır. | Model eğitiminde sınıf ağırlıklarını (class weights) dengelemek veya SMOTE kullanmak. | Aşırı dengesizlik aşılamazsa yalnızca "yüksek riskli" küçük bir segmenti hedeflemek. |
| **Proxy etiket gürültüsü** | OULAD'daki etiketler, gerçek LGS/YKS veli churn'ünü yansıtmadığı için modelin F1 veya AUC skoru suni olarak şişebilir. | Modelin amacı 90 günlük retention kanıtlamak değil, sadece "riskli grubu ayrıştırmak" olarak çerçevelenecek. | Kural bazlı sisteme ağırlık vermek (Örn: 10 dk kuralı). |
| **Figürlerin yanlış okunması (Saha sonucu sanılması)** | AUC değerlerinin, "retention kanıtlanmış" gibi hatalı bir algı yaratması. | Plana en fazla 2 figür koymak ve her figürün altına "Bunun bir proxy verisi olduğu" uyarısını mutlaka yazmak. | Karmaşık grafikler yerine kural bazlı (10 dk) metrikleri ön plana çıkarmak. |

---

# 3. Figür Seçkisi (K1'in Kullanımı İçin)

Aşağıdaki grafikler `data-research/figures/` dizininden seçilmiştir ve yalnızca ilk 2 figürün nihai rapora dahil edilmesi önerilmektedir.

| Figür | Path | Plana girsin mi? | Alt Yazı Önerisi |
| :--- | :--- | :--- | :--- |
| Engagement Dağılımı | `data-research/figures/fig1_engagement_distribution.png` | Evet (1) | *OULAD veri setindeki etkileşim dağılımı. Erken uyarının temel dayanağı.* |
| Dropout / Churn Proxy | `data-research/figures/fig3_dropout_rates.png` | Evet (2) | *Withdrawal (proxy churn) durumu. (Uyarı: Bu veriler 90 günlük veli retention kanıtı değildir).* |
| VLE Click Timeseries | `data-research/figures/fig2_vle_click_timeseries.png` | Hayır | (Ek raporlar / Appendix için saklanabilir) |
| Baseline Model Performance | `data-research/figures/fig6_baseline_model_performance.png` | Hayır | (Ek raporlar / Appendix için saklanabilir) |
