#!/usr/bin/env python3
"""
AI Personal Coach — Production REST API (FastAPI & Uvicorn)
Model Serving, XAI Explanation, and Pedagogical Intervention Microservice.
Fulfills Section 3 & 4 of Deployment Submission.

Run:
  uvicorn api:app --host 0.0.0.0 --port 8000 --reload
"""

from __future__ import annotations

import os
from pathlib import Path
import time
from typing import Any, Dict, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from poc_pipeline import (
    FEATURE_COLS,
    FEATURE_TR_NAMES,
    PersonalCoachPoCPipeline,
    SEGMENT_NAMES,
)

# ----------------- FASTAPI INITIALIZATION -----------------
app = FastAPI(
    title="AI Personal Coach — Model Serving API",
    description="""
Production microservice for LGS/YKS Student Churn Risk Prediction,
Explainable AI (SHAP TreeExplainer), and Pedagogical Intervention Generation.

### Features:
- **Fast Inference:** LightGBM serialized binary model (<5ms CPU latency).
- **Explainable AI (XAI):** Real-time SHAP feature contribution decomposition.
- **Rule Engine:** Deterministic pedagogical delivery policies.
- **Tone-Calibrated Messaging:** Adaptive LLM/Synthesized parent coaching messages.
- **KVKK & Privacy Compliant:** Zero persistent PII.
    """,
    version="1.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline as singleton
pipeline = PersonalCoachPoCPipeline(risk_threshold=0.40)


# ----------------- PYDANTIC SCHEMAS -----------------
class StudentFeaturesInput(BaseModel):
    vle_total_clicks: int = Field(..., ge=0, description="Total clicks on LMS / digital materials", example=120)
    avg_focus_duration_mins: float = Field(..., ge=0.0, description="Average completed focus block duration in minutes", example=18.5)
    phone_distraction_10min_count: int = Field(..., ge=0, description="Count of 10+ min phone distraction events during focus blocks", example=4)
    parent_report_open_rate: float = Field(..., ge=0.0, le=1.0, description="Weekly parent report read rate (0.0 to 1.0)", example=0.35)
    assessment_avg_score: float = Field(..., ge=0.0, le=100.0, description="Average homework and mock quiz score", example=65.0)
    late_submission_ratio: float = Field(..., ge=0.0, le=1.0, description="Ratio of overdue assignments (0.0 to 1.0)", example=0.40)
    anxiety_survey_score: float = Field(..., ge=1.0, le=10.0, description="Student exam anxiety survey score (1 to 10)", example=6.5)
    night_study_ratio: float = Field(..., ge=0.0, le=1.0, description="Ratio of study sessions after 22:00 (0.0 to 1.0)", example=0.25)


class FullEvaluationInput(StudentFeaturesInput):
    student_id: str = Field(default="STU_REQ", description="Anonymized student ID", example="STU_1042")
    name: str = Field(default="Öğrenci", description="Student first name for message tokenization", example="Zeynep")
    exam_type: str = Field(default="YKS_TYT_AYT", description="Target exam (LGS or YKS_TYT_AYT)", example="YKS_TYT_AYT")
    grade: str = Field(default="12", description="Grade level (8, 11, 12, Mezun)", example="12")
    sub_segment: Optional[str] = Field(default=None, description="Optional pre-assigned persona", example="telefonla_dagilan")
    inactivity_days: int = Field(default=2, ge=0, description="Consecutive days without platform activity", example=2)
    last_active_time: str = Field(default="20:30", description="Time of last student activity (HH:MM)", example="20:45")
    unanswered_notif_count: int = Field(default=1, ge=0, description="Consecutive unread/unopened parent notifications", example=1)
    parent_tone_preference: str = Field(default="empathetic", description="Preferred tone (empathetic, structured, gentle, informative)", example="empathetic")


# ----------------- SECURITY & LOGGING MIDDLEWARE -----------------
API_KEY_SECRET = os.getenv("API_KEY_SECRET", "dev_sic_ai17_token")


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Validates API Key if environment variable requires enforcement."""
    if os.getenv("ENFORCE_API_KEY", "false").lower() == "true":
        if x_api_key != API_KEY_SECRET:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing X-API-Key header",
            )
    return True


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    print(f"[API Log] {request.method} {request.url.path} - Status: {response.status_code} - Latency: {duration_ms}ms")
    response.headers["X-Inference-Latency-Ms"] = str(duration_ms)
    return response


# ----------------- ENDPOINTS -----------------
@app.get("/", tags=["General"])
def root():
    return {
        "project": "AI Personal Coach — Capstone Group 1",
        "description": "LGS/YKS Student Retention & Churn Prediction Model Serving API",
        "version": "1.2.0",
        "status": "online",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "explain": "/explain",
            "evaluate": "/evaluate",
            "students": "/students",
        }
    }


@app.get("/health", tags=["Monitoring"])
def health_check():
    """Health and model readiness check for container orchestrators (Kubernetes / ECS)."""
    return {
        "status": "healthy",
        "model_loaded": pipeline.risk_layer.model_name,
        "features_count": len(FEATURE_COLS),
        "operational_threshold": pipeline.rule_engine.risk_threshold,
        "xai_explainer": "SHAP TreeExplainer Ready",
        "timestamp": time.time(),
    }


@app.post("/predict", tags=["Inference"], dependencies=[Depends(verify_api_key)])
def predict_risk(data: StudentFeaturesInput):
    """
    Computes continuous churn risk score (0.00 - 1.00) and risk level
    using the optimized LightGBM model.
    """
    feat_dict = data.model_dump()
    risk_score, risk_level = pipeline.risk_layer.predict_risk(feat_dict)
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "operational_threshold": pipeline.rule_engine.risk_threshold,
        "is_at_risk": risk_score >= pipeline.rule_engine.risk_threshold,
    }


@app.post("/explain", tags=["Explainable AI"], dependencies=[Depends(verify_api_key)])
def explain_risk(data: StudentFeaturesInput):
    """
    Returns SHAP mathematical local feature contributions (log-odds impact)
    broken down into risk drivers (+) and protective factors (-).
    """
    feat_dict = data.model_dump()
    risk_score, risk_level = pipeline.risk_layer.predict_risk(feat_dict)
    shap_info = pipeline.shap_layer.explain_student(feat_dict)

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "top_risk_drivers": shap_info["top_risk_drivers"],
        "top_protective_factors": shap_info["top_protective_factors"],
        "all_contributions": shap_info["all_contributions"],
    }


@app.post("/evaluate", tags=["Pipeline"], dependencies=[Depends(verify_api_key)])
def evaluate_student(data: FullEvaluationInput):
    """
    Full End-to-End Evaluation:
    Risk Prediction -> SHAP Explanation -> Persona Segmentation ->
    Deterministic Rule Engine -> Tone-Calibrated Parent Coaching Message.
    """
    student_dict = data.model_dump()
    result = pipeline.process_student(student_dict)
    return result


@app.get("/students", tags=["Data Fixtures"])
def list_fixture_students():
    """Returns the controlled 15-student test cohort used for benchmarking."""
    fixtures_path = Path(__file__).resolve().parent / "data-research" / "fixtures" / "poc_students.json"
    if not fixtures_path.exists():
        raise HTTPException(status_code=404, detail="Fixtures not found")
    import json
    with open(fixtures_path, encoding="utf-8") as f:
        data = json.load(f)
    return {
        "count": len(data),
        "students": data
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
