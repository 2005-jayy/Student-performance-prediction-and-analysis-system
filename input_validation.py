from prediction_config import (
    ALLOWED_CATEGORIES,
    DEFAULT_INPUTS,
    INPUT_FEATURES,
    INT_BOOLEAN_FIELDS,
    NUMERIC_LIMITS,
)


def _to_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return int(default)


def _to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def build_input_row(raw_data):
    row = {}
    row["age"] = _to_int(raw_data.get("age"), DEFAULT_INPUTS["age"])
    row["gender"] = raw_data.get("gender", DEFAULT_INPUTS["gender"])
    row["academic_level"] = raw_data.get("academic_level", DEFAULT_INPUTS["academic_level"])
    row["study_hours"] = _to_float(raw_data.get("study_hours"), DEFAULT_INPUTS["study_hours"])
    row["self_study_hours"] = _to_float(raw_data.get("self_study_hours"), DEFAULT_INPUTS["self_study_hours"])
    row["online_classes_hours"] = _to_float(raw_data.get("online_classes_hours"), DEFAULT_INPUTS["online_classes_hours"])
    row["social_media_hours"] = _to_float(raw_data.get("social_media_hours"), DEFAULT_INPUTS["social_media_hours"])
    row["gaming_hours"] = _to_float(raw_data.get("gaming_hours"), DEFAULT_INPUTS["gaming_hours"])
    row["sleep_hours"] = _to_float(raw_data.get("sleep_hours"), DEFAULT_INPUTS["sleep_hours"])
    row["screen_time_hours"] = _to_float(raw_data.get("screen_time_hours"), DEFAULT_INPUTS["screen_time_hours"])
    row["exercise_minutes"] = _to_int(raw_data.get("exercise_minutes"), DEFAULT_INPUTS["exercise_minutes"])
    row["caffeine_intake_mg"] = _to_int(raw_data.get("caffeine_intake_mg"), DEFAULT_INPUTS["caffeine_intake_mg"])
    row["part_time_job"] = _to_int(raw_data.get("part_time_job"), DEFAULT_INPUTS["part_time_job"])
    row["upcoming_deadline"] = _to_int(raw_data.get("upcoming_deadline"), DEFAULT_INPUTS["upcoming_deadline"])
    row["internet_quality"] = raw_data.get("internet_quality", DEFAULT_INPUTS["internet_quality"])
    row["mental_health_score"] = _to_float(raw_data.get("mental_health_score"), DEFAULT_INPUTS["mental_health_score"])
    row["focus_index"] = _to_float(raw_data.get("focus_index"), DEFAULT_INPUTS["focus_index"])
    row["burnout_level"] = _to_float(raw_data.get("burnout_level"), DEFAULT_INPUTS["burnout_level"])
    row["productivity_score"] = _to_float(raw_data.get("productivity_score"), DEFAULT_INPUTS["productivity_score"])
    return row


def validate_input_row(row):
    errors = []

    for field, allowed in ALLOWED_CATEGORIES.items():
        if row[field] not in allowed:
            errors.append(f"{field} must be one of: {sorted(allowed)}")

    for field, (low, high) in NUMERIC_LIMITS.items():
        value = row[field]
        if value < low or value > high:
            errors.append(f"{field} must be between {low} and {high}")

    for field in INT_BOOLEAN_FIELDS:
        if row[field] not in (0, 1):
            errors.append(f"{field} must be 0 or 1")

    total_learning_hours = row["study_hours"] + row["self_study_hours"] + row["online_classes_hours"]
    if total_learning_hours > 20:
        errors.append("study/self-study/online class combined hours look unrealistic (>20)")

    if row["screen_time_hours"] < row["study_hours"]:
        # Not always wrong, but this catches obvious typing mistakes.
        pass

    return errors


def parse_and_validate(raw_data):
    row = build_input_row(raw_data)
    errors = validate_input_row(row)
    return row, errors


def extract_form_values(raw_data):
    values = {}
    for key in INPUT_FEATURES:
        values[key] = raw_data.get(key, "")
    return values
