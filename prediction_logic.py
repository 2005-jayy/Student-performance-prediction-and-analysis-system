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
    max_bonus = 12.0
    penalty = 0.0
    bonus = 0.0
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

    if input_row["study_hours"] >= 6:
        bonus += 6
        notes.append("Consistent study hours improved the final score.")
    elif input_row["study_hours"] >= 5:
        bonus += 3

    if input_row["self_study_hours"] >= 2:
        bonus += 3
        notes.append("Healthy self-study time improved the final score.")

    if input_row["sleep_hours"] >= 7:
        bonus += 2
        notes.append("Good sleep habits improved the final score.")

    if input_row["focus_index"] >= 7:
        bonus += 2

    if input_row["productivity_score"] >= 70:
        bonus += 2

    if input_row["burnout_level"] <= 4:
        bonus += 1

    if input_row["social_media_hours"] <= 2 and input_row["gaming_hours"] <= 2:
        bonus += 1

    penalty = min(penalty, max_penalty)
    bonus = min(bonus, max_bonus)
    net_adjustment = round(bonus - penalty, 2)
    adjusted_score = max(0.0, min(TARGET_SCALE_MAX, raw_score + net_adjustment))
    return adjusted_score, net_adjustment, notes


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


def build_action_plan(input_row):
    plan = []

    if input_row["study_hours"] < 6:
        gap = max(1, round(6 - input_row["study_hours"], 1))
        plan.append(f"Add about {gap} more daily study hours and keep them on a fixed timetable.")
    if input_row["self_study_hours"] < 2:
        plan.append("Reserve at least 2 hours for self-study, revision, and practice tests.")
    if input_row["sleep_hours"] < 7:
        plan.append("Move toward 7-8 hours of sleep to improve recall, focus, and energy.")
    if input_row["social_media_hours"] > 2 or input_row["gaming_hours"] > 2:
        plan.append("Set a distraction cap for social media and gaming before starting study sessions.")
    if input_row["burnout_level"] > 6 or input_row["mental_health_score"] < 5:
        plan.append("Add recovery blocks during the week and reduce overload on the toughest days.")
    if input_row["exercise_minutes"] < 20:
        plan.append("Include 20-30 minutes of movement each day to support concentration and mood.")
    if input_row["focus_index"] < 7:
        plan.append("Study in short distraction-free blocks with one clear goal per session.")
    if input_row["upcoming_deadline"] == 1:
        plan.append("Split deadline work into smaller milestones so pressure does not spike at the end.")

    if not plan:
        plan.append("Keep your current routine stable and review weaker subjects once a week.")

    return plan[:5]


def get_risk_profile(score):
    if score >= 80:
        return "Low Risk", "Current habits suggest a strong chance of staying on track."
    if score >= 60:
        return "Moderate Risk", "Performance looks recoverable, but consistency will matter."
    return "High Risk", "This profile may need early intervention to prevent further decline."


def explain_prediction_factors(input_row):
    factors = []

    def add_factor(direction, impact, label, detail):
        factors.append(
            {
                "direction": direction,
                "impact": impact,
                "label": label,
                "detail": detail,
            }
        )

    study_hours = input_row["study_hours"]
    self_study_hours = input_row["self_study_hours"]
    sleep_hours = input_row["sleep_hours"]
    burnout_level = input_row["burnout_level"]
    focus_index = input_row["focus_index"]
    productivity_score = input_row["productivity_score"]
    social_media_hours = input_row["social_media_hours"]
    gaming_hours = input_row["gaming_hours"]
    screen_time_hours = input_row["screen_time_hours"]
    caffeine_intake_mg = input_row["caffeine_intake_mg"]
    mental_health_score = input_row["mental_health_score"]

    if study_hours >= 6:
        add_factor("positive", 6, "Strong study time", f"{study_hours} hours of study is supporting the score.")
    elif study_hours < 4:
        add_factor("negative", 7, "Low study time", f"{study_hours} study hours is limiting performance.")

    if self_study_hours >= 2:
        add_factor("positive", 4, "Healthy self-study", f"{self_study_hours} hours of self-study adds useful revision time.")
    elif self_study_hours < 1:
        add_factor("negative", 5, "Low self-study", "Independent revision time is currently too low.")

    if sleep_hours >= 7:
        add_factor("positive", 3, "Good sleep routine", f"{sleep_hours} hours of sleep supports attention and memory.")
    elif sleep_hours < 6:
        add_factor("negative", 5, "Low sleep", f"{sleep_hours} hours of sleep may be hurting concentration.")

    if burnout_level <= 4:
        add_factor("positive", 2, "Burnout is under control", f"Burnout level {burnout_level} is in a healthier range.")
    elif burnout_level > 6:
        add_factor("negative", 6, "High burnout", f"Burnout level {burnout_level} is dragging the score down.")

    if focus_index >= 7:
        add_factor("positive", 3, "Good focus", f"Focus index {focus_index} is helping study quality.")
    elif focus_index < 5:
        add_factor("negative", 4, "Weak focus", f"Focus index {focus_index} suggests concentration problems.")

    if productivity_score >= 70:
        add_factor("positive", 3, "Good productivity", f"Productivity score {productivity_score} supports stronger output.")
    elif productivity_score < 60:
        add_factor("negative", 4, "Low productivity", f"Productivity score {productivity_score} is holding the score back.")

    if social_media_hours > 3:
        add_factor("negative", 4, "High social media time", f"{social_media_hours} hours on social media may reduce effective study time.")

    if gaming_hours > 2:
        add_factor("negative", 4, "High gaming time", f"{gaming_hours} gaming hours is adding distraction pressure.")

    if screen_time_hours > 6:
        add_factor("negative", 3, "High screen time", f"{screen_time_hours} total screen hours may affect focus and sleep.")

    if caffeine_intake_mg > 300:
        add_factor("negative", 2, "High caffeine", f"{caffeine_intake_mg} mg of caffeine may disrupt sleep quality.")

    if mental_health_score >= 7:
        add_factor("positive", 2, "Mental wellbeing", f"Mental health score {mental_health_score} is helping consistency.")
    elif mental_health_score < 5:
        add_factor("negative", 3, "Mental strain", f"Mental health score {mental_health_score} suggests extra strain.")

    factors.sort(key=lambda item: (-item["impact"], item["direction"]))
    return factors[:5]
