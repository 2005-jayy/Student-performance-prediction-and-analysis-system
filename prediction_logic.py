from prediction_config import TARGET_SCALE_MAX


def score_to_grade_and_gpa(score):
    if score >= 90:
        return "O", 10.0
    if score >= 80:
        return "A+", 9.0
    if score >= 70:
        return "A", 8.0
    if score >= 60:
        return "B+", 7.0
    if score >= 50:
        return "B", 6.0
    if score >= 40:
        return "C", 5.0
    return "F", 0.0


def apply_reality_adjustments(raw_score, input_row):
    max_penalty = 35.0
    penalty = 0.0
    notes = []

    if input_row["study_hours"] < 2:
        penalty += 16
        notes.append("Very low study hours reduced the final score.")
    elif input_row["study_hours"] < 4:
        penalty += 9
        notes.append("Low study hours reduced the final score.")

    if input_row["self_study_hours"] < 1:
        penalty += 6
        notes.append("No self-study time reduced the final score.")

    if input_row["social_media_hours"] > 5:
        penalty += 8
        notes.append("High social media usage reduced the final score.")
    elif input_row["social_media_hours"] > 3:
        penalty += 4

    if input_row["gaming_hours"] > 4:
        penalty += 8
        notes.append("High gaming hours reduced the final score.")
    elif input_row["gaming_hours"] > 2:
        penalty += 4

    if input_row["caffeine_intake_mg"] > 500:
        penalty += 7
        notes.append("Very high caffeine intake reduced the final score.")
    elif input_row["caffeine_intake_mg"] > 300:
        penalty += 3

    if input_row["burnout_level"] > 7:
        penalty += 7
        notes.append("High burnout level reduced the final score.")
    elif input_row["burnout_level"] > 5:
        penalty += 3

    if input_row["sleep_hours"] < 6:
        penalty += 5
    if input_row["screen_time_hours"] > 6:
        penalty += 3

    if input_row["productivity_score"] >= 85 and input_row["study_hours"] < 3:
        penalty += 8
        notes.append("Very high productivity with very low study hours was treated as inconsistent.")

    penalty = min(penalty, max_penalty)
    adjusted_score = max(0.0, min(TARGET_SCALE_MAX, raw_score - penalty))
    return adjusted_score, round(penalty, 2), notes


def build_feedback(score, input_row):
    if score >= 85:
        level = "Excellent"
        message = "Outstanding work. Your consistency is paying off, so keep this momentum."
    elif score >= 70:
        level = "Good"
        message = "Great progress. You are on a strong path, and a few improvements can lift you higher."
    elif score >= 50:
        level = "Average"
        message = "You have a solid base. With focused adjustments, you can move into the good range."
    else:
        level = "Needs Improvement"
        message = "Do not lose confidence. Small daily changes can improve your score steadily."

    tips = []
    if input_row["study_hours"] < 6:
        tips.append("Increase total study hours to at least 6-8 with a fixed daily plan.")
    if input_row["self_study_hours"] < 2:
        tips.append("Add self-study time for revision and practice, not only classes.")
    if input_row["sleep_hours"] < 7:
        tips.append("Improve sleep to around 7-8 hours for better memory and concentration.")
    if input_row["focus_index"] < 7:
        tips.append("Work in distraction-free blocks to raise your focus index.")
    if input_row["burnout_level"] > 6:
        tips.append("Reduce burnout with short breaks, realistic targets, and lighter late-night workload.")
    if input_row["productivity_score"] < 60:
        tips.append("Track daily goals and complete high-priority tasks first to increase productivity.")
    if input_row["social_media_hours"] > 2:
        tips.append("Cut social media time and shift that time to revision practice.")
    if input_row["gaming_hours"] > 2:
        tips.append("Limit gaming hours on study days and schedule it only after key tasks are done.")
    if input_row["screen_time_hours"] > 6:
        tips.append("Reduce non-study screen time to protect attention and sleep quality.")
    if input_row["caffeine_intake_mg"] > 300:
        tips.append("Lower caffeine intake to avoid sleep and focus disruption.")
    if input_row["exercise_minutes"] < 20:
        tips.append("Add at least 20-30 minutes of physical activity for better energy and mood.")
    if input_row["internet_quality"] == "Poor":
        tips.append("Improve internet reliability or download materials early to avoid study interruptions.")
    if input_row["upcoming_deadline"] == 1:
        tips.append("Break upcoming deadline tasks into smaller steps and start earlier.")

    if not tips:
        tips.append("Maintain this routine and review weak subjects weekly to keep improving.")

    return level, message, tips[:4]
