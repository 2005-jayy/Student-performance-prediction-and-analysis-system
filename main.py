import os
import socket

import pandas as pd
from flask import Flask, jsonify, render_template, request

from input_validation import extract_form_values, parse_and_validate
from prediction_config import TARGET_SCALE_MAX
from prediction_logic import apply_reality_adjustments, build_feedback, score_to_grade_and_gpa
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


@app.route("/")
def home():
    return render_template("index.html", form_values={})


@app.route("/predict_form", methods=["POST"])
def predict_form():
    form_values = extract_form_values(request.form)
    input_row, errors = parse_and_validate(request.form)

    if errors:
        return render_template(
            "index.html",
            form_values=form_values,
            error="Please correct the highlighted input values.",
            error_lines=errors,
        )

    input_data = pd.DataFrame([input_row])
    raw_prediction = float(model.predict(input_data)[0])
    raw_prediction = max(0.0, min(TARGET_SCALE_MAX, raw_prediction))

    prediction, penalty_points, adjustment_notes = apply_reality_adjustments(raw_prediction, input_row)
    grade, gpa = score_to_grade_and_gpa(prediction)
    level, feedback_message, improvement_tips = build_feedback(prediction, input_row)

    return render_template(
        "index.html",
        prediction=round(prediction, 2),
        raw_prediction=round(raw_prediction, 2),
        penalty_points=penalty_points,
        adjustment_notes=adjustment_notes,
        grade=grade,
        gpa=round(gpa, 2),
        performance_level=level,
        feedback_message=feedback_message,
        improvement_tips=improvement_tips,
        form_values=form_values,
    )


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    input_row, errors = parse_and_validate(data)

    if errors:
        return jsonify({"error": "Invalid input", "details": errors}), 400

    input_data = pd.DataFrame([input_row])
    raw_prediction = float(model.predict(input_data)[0])
    raw_prediction = max(0.0, min(TARGET_SCALE_MAX, raw_prediction))

    prediction, penalty_points, adjustment_notes = apply_reality_adjustments(raw_prediction, input_row)
    grade, gpa = score_to_grade_and_gpa(prediction)
    level, feedback_message, improvement_tips = build_feedback(prediction, input_row)

    return jsonify(
        {
            "predicted_exam_score": round(prediction, 2),
            "model_raw_score": round(raw_prediction, 2),
            "reality_penalty_points": penalty_points,
            "adjustment_notes": adjustment_notes,
            "estimated_grade": grade,
            "estimated_gpa_10": round(gpa, 2),
            "performance_level": level,
            "motivation_message": feedback_message,
            "improvement_tips": improvement_tips,
        }
    )


if __name__ == "__main__":
    preferred_port = _to_int(os.getenv("PORT"), 5000)
    port = _find_available_port(preferred_port)
    if port != preferred_port:
        print(f"⚠️ Port {preferred_port} is busy. Starting on port {port} instead.")
    app.run(debug=True, port=port)
