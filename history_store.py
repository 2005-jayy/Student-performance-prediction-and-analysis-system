import json
import os
from datetime import datetime

from prediction_config import HISTORY_FILE

MAX_HISTORY_ITEMS = 25


def _read_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as history_file:
            data = json.load(history_file)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return []


def get_recent_history(limit=8):
    history = _read_history()
    return history[:limit]


def save_prediction_history(input_row, result, source="form"):
    history = _read_history()

    entry = {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": source,
        "predicted_score": result["prediction"],
        "grade": result["grade"],
        "risk_level": result["risk_level"],
        "study_hours": input_row["study_hours"],
        "self_study_hours": input_row["self_study_hours"],
        "sleep_hours": input_row["sleep_hours"],
        "focus_index": input_row["focus_index"],
        "burnout_level": input_row["burnout_level"],
    }

    history.insert(0, entry)
    history = history[:MAX_HISTORY_ITEMS]

    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as history_file:
        json.dump(history, history_file, indent=2)

    return entry
