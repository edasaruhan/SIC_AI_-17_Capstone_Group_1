# Machine Learning Project Documentation
## Deployment Phase — AI Personal Coach (Capstone Group 1)

---

### 1. Overview

The deployment phase of the **AI Personal Coach** project operationalizes a multi-stage machine learning system designed to solve customer churn in dual-user EdTech subscription models (LGS and YKS exam preparation platforms in Turkey). 

In this architecture, the student generates behavioral telemetry (focus duration, distraction signals, LMS engagement), while the parent is the economic buyer who decides whether to maintain or cancel the subscription. The deployment phase bridges real-time behavioral data analysis with proactive, constructive parent coaching interventions before customer disengagement leads to churn.

#### Deployment Architecture
The system employs a three-tier deployment structure:
1. **Model Serving REST Microservice (`api.py`):** High-throughput, low-latency FastAPI ASGI microservice exposing prediction, SHAP explanation, and end-to-end decision endpoints for integration with mobile applications, backend LMS platforms, and CRM systems.
2. **Interactive Educator & Guidance Decision Portal (`app.py`):** Enterprise-grade Streamlit web application providing teachers and educational counselors with live student risk cards, SHAP waterfall charts, mobile message previews, and real-time "What-If" simulation capabilities.
3. **Automated Batch Intervention Pipeline (`poc_pipeline.py`):** Command-line batch execution engine for scheduled overnight evaluation of entire student cohorts, generating localized intervention packets and escalating high-risk cases to human counselors.

```
[ Student Telemetry / LMS Logs ]
             ↓
[ FastAPI Serving Layer (/predict, /explain, /evaluate) ]
             ↓
[ Serialized LightGBM Model (Risk Score 0.0 - 1.0) ]
             ↓
[ SHAP TreeExplainer (Feature Attribution: Drivers & Protective Factors) ]
             ↓
[ Behavioral Segmentation Layer (5 Personas) ]
             ↓
[ Deterministic Rule Engine (Timing Window 20:00-23:00, Frequency Cap, Escalation) ]
             ↓
[ LLM Personalization Layer (Tone-Calibrated Parent Coaching Message) ]
             ↓
[ Delivery: WhatsApp / Push Notification / Counselor Dashboard ]
```

---

### 2. Model Serialization

#### Serialization Process & Format
The machine learning models are trained and serialized in Python using `joblib` with zlib compression:
- **Primary Inference Model:** `data-research/modeling/lightgbm_model.joblib` (Trained LightGBM Gradient Boosting Classifier).
- **Linear Benchmark Model:** `data-research/modeling/logistic_model.joblib` (Calibrated Logistic Regression baseline).
- **Explainable AI Engine:** `data-research/modeling/shap_explainer.joblib` (Pre-computed `shap.TreeExplainer` instance optimized for tree-based ensemble decomposition).

#### Efficiency and Storage Considerations
1. **Lightweight Footprint:** The serialized LightGBM binary model occupies **less than 150 KB** of disk space, enabling rapid cold-start container initialization in serverless and containerized environments (< 4 seconds).
2. **Zero GPU Dependency:** LightGBM operates purely on CPU architectures, eliminating high-cost GPU infrastructure and ensuring inference costs remain under **$0.02 per user per month**.
3. **In-Memory Loading Speed:** Model loading via `joblib.load()` takes **< 5 milliseconds**, allowing stateless microservice instances to warm up instantly.
4. **Reproducibility & Versioning:** Every model serialization artifact is pinned with exact dependency versions (`lightgbm==4.6.0`, `scikit-learn==1.6.1`, `joblib==1.4.2`) and logged alongside its training commit hash.

---

### 3. Model Serving

#### Serving Architecture
The serialized models are served using a **FastAPI** web framework executed by the high-performance **Uvicorn** ASGI server.

- **Process Model:** Single-worker or multi-worker asynchronous process model handling concurrent non-blocking I/O requests.
- **Latency Profile:** Individual model inference latency is **< 4 ms** on CPU; full end-to-end pipeline evaluation (including SHAP feature attribution and rule execution) executes within **12 to 18 ms**.
- **Memory Footprint:** The complete serving container requires approximately **85 MB RAM**, allowing cost-efficient multi-container deployment on micro-instances.

#### Deployment Platform Options
1. **Cloud Container Services (Recommended Production Target):**
   - **AWS ECS / Fargate or Google Cloud Run:** Stateless Docker containers running the FastAPI microservice with horizontal autoscaling based on CPU utilization and incoming HTTP request queue depth.
2. **Serverless Function Serving:**
   - Standalone deployment as AWS Lambda or Google Cloud Functions behind an API Gateway for scheduled nightly cohort evaluation.
3. **On-Premises / Private Cloud Deployment:**
   - Kubernetes (EKS/GKE/K3s) deployment for enterprise educational institutions requiring on-premises data locality to comply with strict local educational hosting regulations.

---

### 4. API Integration

The model serving layer is fully integrated into an OpenAPI 3.1-compliant REST API (`api.py`), automatically exposing interactive Swagger documentation at `/docs` and ReDoc at `/redoc`.

#### Core Endpoints

| Method | Endpoint | Description | Input Schema | Response Schema |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | Liveness & Readiness check for orchestrators | None | Status, model name, threshold |
| `POST` | `/predict` | Rapid churn risk scoring | `StudentFeaturesInput` | `risk_score`, `risk_level`, `is_at_risk` |
| `POST` | `/explain` | SHAP feature contribution decomposition | `StudentFeaturesInput` | `top_risk_drivers`, `top_protective_factors` |
| `POST` | `/evaluate` | Full end-to-end pipeline execution | `FullEvaluationInput` | Risk, Segment, Trigger, Escalation, Message |
| `GET` | `/students` | Benchmark fixture cohort listing | None | List of 15 sample student profiles |

#### Input Schema Example (`POST /evaluate`)
```json
{
  "student_id": "STU_002",
  "name": "Zeynep",
  "exam_type": "YKS_TYT_AYT",
  "grade": "12",
  "vle_total_clicks": 85,
  "avg_focus_duration_mins": 18.0,
  "phone_distraction_10min_count": 6,
  "parent_report_open_rate": 0.35,
  "assessment_avg_score": 68.0,
  "late_submission_ratio": 0.40,
  "anxiety_survey_score": 5.0,
  "night_study_ratio": 0.30,
  "inactivity_days": 2,
  "last_active_time": "20:45",
  "unanswered_notif_count": 1,
  "parent_tone_preference": "empathetic"
}
```

#### Output Schema Example (`POST /evaluate`)
```json
{
  "student_id": "STU_002",
  "name": "Zeynep",
  "risk_score": 0.5735,
  "risk_level": "High (Yüksek)",
  "segment_code": "telefonla_dagilan",
  "segment_display": "Telefonla Dağılan (Phone Distracted)",
  "trigger": true,
  "primary_reason": "Odak bloklarında 6 kez 10 dk+ telefon kullanım uyarısı",
  "delivery_window": "20:30 (Veli Akşam Pik Saati)",
  "escalate_to_human": false,
  "shap_explanation": {
    "top_risk_drivers": [
      {
        "feature_tr": "Platform Etkileşimi (VLE Tıklama)",
        "shap_value": 0.4124,
        "student_value": 85
      },
      {
        "feature_tr": "Sınav Kaygısı Anketi",
        "shap_value": 0.1312,
        "student_value": 5.0
      }
    ]
  },
  "parent_message": "Merhaba, Zeynep'in haftalık çalışma ritminde küçük bir optimizasyon fırsatı belirledik. AI analizimizde özellikle 'Platform Etkileşimi (VLE Tıklama)' sinyali öne çıkıyor. Odak bloğunda bildirimlerin dikkatini böldüğünü gözlemliyoruz. Yargılamadan destek olmak için: 'Bugünkü 20 dakikalık odak bloğunda telefonu birlikte salona bırakalım mı?' önerisi odak süresini hemen toparlayacaktır. [Odaklanma Desteği]"
}
```

---

### 5. Security Considerations

#### KVKK & Underage Data Protection
1. **Zero Real PII:** In strict accordance with Turkish Personal Data Protection Law (KVKK No. 6698) and comparative international standards (GDPR Art. 8), the system never processes national IDs, phone numbers, email addresses, or biometric data in the machine learning layer. Identifiers are strictly anonymized tokens (`STU_XXXX`).
2. **Explicit Parental Consent:** Telemetry processing and AI message delivery operate exclusively on explicitly granted, revocable parental consent.
3. **Data Minimization:** Only aggregated behavioral features (e.g. distraction counts, focus minutes) are captured; raw device telemetry, browsing history, and camera/screen recordings are strictly prohibited by system design.

#### Authentication & Authorization
- **API Security:** All REST endpoints are protected via an API Key authentication mechanism (`X-API-Key` header).
- **Transport Layer Security:** All communications enforce HTTPS over TLS 1.3, mitigating man-in-the-middle risks.

#### Responsible AI Guardrails
- **Notification Frequency Capping:** The deterministic rule engine enforces a hard cap of maximum 3 messages per 48-hour window, eliminating notification fatigue and parental anxiety.
- **Human-in-the-Loop Escalation:** Students with critical risk (>0.65) and 3+ consecutive unread notifications trigger a counselor escalation flag, transferring communication from automated AI to a licensed guidance professional.

---

### 6. Monitoring and Logging

#### Real-Time Telemetry & Request Logging
The FastAPI deployment includes custom middleware logging every incoming request with structured attributes:
- HTTP Method, URL path, and Client IP.
- HTTP status code and response payload size.
- Exact end-to-end execution latency in milliseconds (`X-Inference-Latency-Ms` header).

#### Data & Model Drift Tracking
1. **Feature Drift Monitoring:** The system tracks rolling distribution metrics (mean, variance, quartiles) for key predictive features (`avg_focus_duration_mins`, `phone_distraction_10min_count`). If the population Kolmogorov-Smirnov test diverges from the baseline training distribution ($p < 0.05$), a retraining alert is raised.
2. **Prediction Drift Monitoring:** The daily average predicted risk score and the proportion of students categorized into each of the 5 behavioral segments are logged to detect seasonal shifts (e.g., examination week behavioral spikes).

#### Alerting Mechanisms
- **Operational Health Alerts:** Health-check failures (`/health` returning non-200) trigger automated orchestrator restarts.
- **High-Risk Cohort Alerts:** Webhook notifications to school guidance teams when more than 35% of a cohort enters the "Critical Risk" category in a single evaluation cycle.
- **Latency Alerts:** P99 inference latency exceeding 50 ms triggers automated horizontal container scale-out.
