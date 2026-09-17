import json
from pathlib import Path
import sys
import pytest

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from poc_pipeline import (
    FEATURE_COLS,
    MessageLayer,
    PersonalCoachPoCPipeline,
    RiskLayer,
    RuleEngine,
    SegmentationLayer,
)


@pytest.fixture
def sample_student():
    return {
        "student_id": "TEST_001",
        "name": "Barış",
        "exam_type": "LGS",
        "grade": "8",
        "sub_segment": "telefonla_dagilan",
        "vle_total_clicks": 60,
        "avg_focus_duration_mins": 14.0,
        "phone_distraction_10min_count": 5,
        "parent_report_open_rate": 0.30,
        "assessment_avg_score": 62.0,
        "late_submission_ratio": 0.45,
        "anxiety_survey_score": 6.0,
        "night_study_ratio": 0.25,
        "inactivity_days": 2,
        "last_active_time": "20:45",
        "unanswered_notif_count": 1,
    }


def test_risk_layer_prediction(sample_student):
    risk_layer = RiskLayer()
    risk_score, risk_level = risk_layer.predict_risk(sample_student)

    assert isinstance(risk_score, float)
    assert 0.0 <= risk_score <= 1.0
    assert any(lvl in risk_level for lvl in ["Low", "Medium", "High", "Critical"])


def test_segmentation_layer(sample_student):
    segment = SegmentationLayer.identify_segment(sample_student)
    assert segment in [
        "baslayamayan",
        "telefonla_dagilan",
        "geceye_kayan",
        "yarida_birakan",
        "kaygiyla_erteleyen",
    ]


def test_rule_engine_triggers(sample_student):
    rule_engine = RuleEngine(risk_threshold=0.50)
    result = rule_engine.evaluate(sample_student, risk_score=0.65, segment="telefonla_dagilan")

    assert result["trigger"] is True
    assert "RULE_PHONE_DISTRACTION_BURST" in result["matched_rules"]
    assert result["in_peak_window"] is True


def test_rule_engine_low_risk_no_trigger():
    rule_engine = RuleEngine(risk_threshold=0.50)
    student = {
        "inactivity_days": 0,
        "phone_distraction_10min_count": 0,
        "anxiety_survey_score": 3.0,
        "night_study_ratio": 0.10,
        "last_active_time": "19:00",
        "unanswered_notif_count": 0,
    }
    result = rule_engine.evaluate(student, risk_score=0.20, segment="geceye_kayan")
    assert result["trigger"] is False
    assert result["escalate_to_human"] is False


def test_rule_engine_escalation():
    rule_engine = RuleEngine(risk_threshold=0.50)
    student = {
        "inactivity_days": 4,
        "phone_distraction_10min_count": 2,
        "anxiety_survey_score": 7.0,
        "night_study_ratio": 0.20,
        "last_active_time": "21:00",
        "unanswered_notif_count": 4,
    }
    result = rule_engine.evaluate(student, risk_score=0.75, segment="baslayamayan")
    assert result["trigger"] is True
    assert result["escalate_to_human"] is True


def test_message_layer():
    rule_res = {
        "trigger": True,
        "escalate_to_human": False,
    }
    msg = MessageLayer.generate_message("Deniz", "baslayamayan", rule_res)
    assert "Deniz" in msg
    assert "ısınma soru seti" in msg
    assert "Bildirim kuralı tetiklenmedi" not in msg


def test_pipeline_end_to_end(sample_student):
    pipeline = PersonalCoachPoCPipeline()
    result = pipeline.process_student(sample_student)

    required_keys = [
        "student_id",
        "name",
        "risk_score",
        "risk_level",
        "segment_code",
        "segment_display",
        "trigger",
        "primary_reason",
        "delivery_window",
        "escalate_to_human",
        "parent_message",
    ]
    for key in required_keys:
        assert key in result

    assert result["student_id"] == "TEST_001"
    assert result["name"] == "Barış"


def test_pipeline_all_fixtures():
    pipeline = PersonalCoachPoCPipeline()
    fixtures_path = Path(__file__).resolve().parent.parent / "data-research" / "fixtures" / "poc_students.json"
    assert fixtures_path.exists()

    results = pipeline.process_all_fixtures(fixtures_path)
    assert len(results) == 15
    for r in results:
        assert 0.0 <= r["risk_score"] <= 1.0
        assert r["trigger"] in [True, False]
        assert len(r["parent_message"]) > 10
