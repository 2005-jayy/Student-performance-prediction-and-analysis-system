import os
import socket

import pandas as pd
from flask import Flask, jsonify, render_template, request

from history_store import get_recent_history, save_prediction_history
from input_validation import extract_form_values, parse_and_validate
from prediction_config import TARGET_SCALE_MAX
from prediction_logic import (
    apply_reality_adjustments,
    build_action_plan,
    build_feedback,
    explain_prediction_factors,
    get_risk_profile,
    score_to_grade_and_gpa,
)
from prediction_model import load_or_train_model

app = Flask(__name__)
model = load_or_train_model()


def _find_available_port(preferred_port, max_tries=50):
    for port in range(preferred_port, preferred_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return preferred_port


def _to_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return int(default)


def _predict_details(input_row):
    input_data = pd.DataFrame([input_row])
    raw_prediction = float(model.predict(input_data)[0])
    raw_prediction = max(0.0, min(TARGET_SCALE_MAX, raw_prediction))

    prediction, penalty_points, adjustment_notes = apply_reality_adjustments(raw_prediction, input_row)
    grade, gpa = score_to_grade_and_gpa(prediction)
    level, feedback_message, improvement_tips = build_feedback(prediction, input_row)
    risk_level, risk_message = get_risk_profile(prediction)
    action_plan = build_action_plan(input_row)
    score_factors = explain_prediction_factors(input_row)

    return {
        "prediction": round(prediction, 2),
        "raw_prediction": round(raw_prediction, 2),
        "adjustment_points": penalty_points,
        "adjustment_notes": adjustment_notes,
        "grade": grade,
        "gpa": round(gpa, 2),
        "performance_level": level,
        "feedback_message": feedback_message,
        "improvement_tips": improvement_tips,
        "risk_level": risk_level,
        "risk_message": risk_message,
        "action_plan": action_plan,
        "score_factors": score_factors,
    }


def _build_scenarios(input_row):
    scenario_specs = [
        (
            "Balanced Routine",
            {
                "study_hours": max(input_row["study_hours"], 6.0),
                "self_study_hours": max(input_row["self_study_hours"], 2.0),
                "sleep_hours": max(input_row["sleep_hours"], 7.0),
                "social_media_hours": min(input_row["social_media_hours"], 2.0),
                "gaming_hours": min(input_row["gaming_hours"], 1.0),
                "screen_time_hours": min(input_row["screen_time_hours"], 5.0),
            },
        ),
        (
            "Focus Boost",
            {
                "focus_index": max(input_row["focus_index"], 8.0),
                "productivity_score": max(input_row["productivity_score"], 75.0),
                "burnout_level": min(input_row["burnout_level"], 4.0),
                "social_media_hours": min(input_row["social_media_hours"], 1.5),
            },
        ),
        (
            "Wellbeing Reset",
            {
                "sleep_hours": max(input_row["sleep_hours"], 8.0),
                "mental_health_score": max(input_row["mental_health_score"], 7.0),
                "burnout_level": min(input_row["burnout_level"], 3.0),
                "exercise_minutes": max(input_row["exercise_minutes"], 30),
                "caffeine_intake_mg": min(input_row["caffeine_intake_mg"], 200),
            },
        ),
    ]

    base_prediction = _predict_details(input_row)["prediction"]
    scenarios = []

    for name, overrides in scenario_specs:
        scenario_row = dict(input_row)
        scenario_row.update(overrides)
        scenario_result = _predict_details(scenario_row)
        scenarios.append(
            {
                "name": name,
                "predicted_score": scenario_result["prediction"],
                "delta": round(scenario_result["prediction"] - base_prediction, 2),
                "changes": [
                    f"{field.replace('_', ' ').title()}: {value}"
                    for field, value in overrides.items()
                    if input_row.get(field) != value
                ][:4],
            }
        )

    return scenarios


@app.route("/")
def home():
    return render_template(
        "index.html",
        form_values={},
        prediction=None,
        scenarios=[],
        action_plan=[],
        score_factors=[],
        prediction_history=get_recent_history(),
    )


@app.route("/predict_form", methods=["POST"])
def predict_form():
    form_values = extract_form_values(request.form)
    input_row, errors = parse_and_validate(request.form)

    if errors:
        return render_template(
            "index.html",
            form_values=form_values,
            prediction=None,
            scenarios=[],
            action_plan=[],
            score_factors=[],
            prediction_history=get_recent_history(),
            error="Please correct the highlighted input values.",
            error_lines=errors,
        )

    result = _predict_details(input_row)
    scenarios = _build_scenarios(input_row)
    save_prediction_history(input_row, result, source="form")

    return render_template(
        "index.html",
        form_values=form_values,
        scenarios=scenarios,
        prediction_history=get_recent_history(),
        **result,
    )


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    input_row, errors = parse_and_validate(data)

    if errors:
        return jsonify({"error": "Invalid input", "details": errors}), 400

    result = _predict_details(input_row)
    scenarios = _build_scenarios(input_row)
    saved_entry = save_prediction_history(input_row, result, source="api")

    return jsonify(
        {
            "predicted_exam_score": result["prediction"],
            "model_raw_score": result["raw_prediction"],
            "reality_adjustment_points": result["adjustment_points"],
            "adjustment_notes": result["adjustment_notes"],
            "estimated_grade": result["grade"],
            "estimated_gpa_10": result["gpa"],
            "performance_level": result["performance_level"],
            "motivation_message": result["feedback_message"],
            "improvement_tips": result["improvement_tips"],
            "risk_level": result["risk_level"],
            "risk_message": result["risk_message"],
            "action_plan": result["action_plan"],
            "score_factors": result["score_factors"],
            "what_if_scenarios": scenarios,
            "saved_history_entry": saved_entry,
            "recent_history": get_recent_history(),
        }
    )


if __name__ == "__main__":
    preferred_port = _to_int(os.getenv("PORT"), 5000)
    port = _find_available_port(preferred_port)
    if port != preferred_port:
        print(f"⚠️ Port {preferred_port} is busy. Starting on port {port} instead.")
    app.run(debug=True, port=port)
