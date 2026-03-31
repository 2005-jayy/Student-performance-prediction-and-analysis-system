import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "data", "cleaned_student_dataset.csv")
MODEL_FILE = os.path.join(BASE_DIR, "student_exam_model.pkl")

TARGET_COLUMN = "exam_score"
TARGET_SCALE_MAX = 100.0
LEAKAGE_COLUMNS = ["result", "grade"]

INPUT_FEATURES = [
    "age",
    "gender",
    "academic_level",
    "study_hours",
    "self_study_hours",
    "online_classes_hours",
    "social_media_hours",
    "gaming_hours",
    "sleep_hours",
    "screen_time_hours",
    "exercise_minutes",
    "caffeine_intake_mg",
    "part_time_job",
    "upcoming_deadline",
    "internet_quality",
    "mental_health_score",
    "focus_index",
    "burnout_level",
    "productivity_score",
]

DEFAULT_INPUTS = {
    "age": 18,
    "gender": "Male",
    "academic_level": "Undergraduate",
    "study_hours": 0.0,
    "self_study_hours": 0.0,
    "online_classes_hours": 0.0,
    "social_media_hours": 0.0,
    "gaming_hours": 0.0,
    "sleep_hours": 0.0,
    "screen_time_hours": 0.0,
    "exercise_minutes": 0,
    "caffeine_intake_mg": 0,
    "part_time_job": 0,
    "upcoming_deadline": 0,
    "internet_quality": "Average",
    "mental_health_score": 0.0,
    "focus_index": 0.0,
    "burnout_level": 0.0,
    "productivity_score": 1.0,
}

ALLOWED_CATEGORIES = {
    "gender": {"Male", "Female"},
    "academic_level": {"Undergraduate", "Postgraduate"},
    "internet_quality": {"Poor", "Average", "Good"},
}

NUMERIC_LIMITS = {
    "age": (15, 60),
    "study_hours": (0, 16),
    "self_study_hours": (0, 16),
    "online_classes_hours": (0, 16),
    "social_media_hours": (0, 16),
    "gaming_hours": (0, 16),
    "sleep_hours": (0, 12),
    "screen_time_hours": (0, 24),
    "exercise_minutes": (0, 300),
    "caffeine_intake_mg": (0, 1000),
    "mental_health_score": (0, 10),
    "focus_index": (0, 10),
    "burnout_level": (0, 10),
    "productivity_score": (1, 100),
}

INT_BOOLEAN_FIELDS = {"part_time_job", "upcoming_deadline"}
