"""
FastAPI Microservice Integration Tests (Deployment Submission Section 4)
"""

from pathlib import Path
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from api import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "endpoints" in data


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "LightGBM" in data["model_loaded"]


def test_predict_endpoint():
    payload = {
        "vle_total_clicks": 55,
        "avg_focus_duration_mins": 14.5,
        "phone_distraction_10min_count": 5,
        "parent_report_open_rate": 0.25,
        "assessment_avg_score": 60.0,
        "late_submission_ratio": 0.50,
        "anxiety_survey_score": 6.8,
        "night_study_ratio": 0.30
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert 0.0 <= data["risk_score"] <= 1.0
    assert "risk_level" in data
    assert "is_at_risk" in data


def test_explain_endpoint():
    payload = {
        "vle_total_clicks": 30,
        "avg_focus_duration_mins": 10.0,
        "phone_distraction_10min_count": 6,
        "parent_report_open_rate": 0.20,
        "assessment_avg_score": 52.0,
        "late_submission_ratio": 0.65,
        "anxiety_survey_score": 8.0,
        "night_study_ratio": 0.15
    }
    response = client.post("/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "top_risk_drivers" in data
    assert len(data["top_risk_drivers"]) > 0
    assert "all_contributions" in data


def test_evaluate_endpoint():
    payload = {
        "student_id": "STU_API_TEST",
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
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "STU_API_TEST"
    assert data["trigger"] is True
    assert "Zeynep" in data["parent_message"]
    assert "shap_explanation" in data


def test_students_fixture_endpoint():
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 15
    assert len(data["students"]) == 15
