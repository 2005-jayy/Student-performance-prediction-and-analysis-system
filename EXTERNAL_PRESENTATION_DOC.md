# Student Performance Prediction and Analysis System
## External Presentation + Viva Guide

### 1. Project Title
**Student Performance Prediction and Analysis System**

### 2. One-Line Pitch
This project predicts a student’s exam score (0-100), estimates grade and GPA, and gives personalized motivational feedback with practical improvement tips.

---

## 3. Problem Statement
Students often do not know how daily habits like study time, sleep, burnout, focus, and distractions affect academic outcomes.  
This system helps by:
- Predicting likely exam score
- Showing grade and GPA estimate
- Giving customized feedback and improvement areas

---

## 4. Objectives
- Build an ML-based prediction system for student exam performance
- Provide an easy web interface for input and results
- Add practical feedback for real student guidance
- Improve reliability using backend validation and reality-adjustment rules

---

## 5. Dataset Used
- File: `data/cleaned_student_dataset.csv`
- Main target: `exam_score`
- Input features include:
  - Academic behavior: `study_hours`, `self_study_hours`, `online_classes_hours`
  - Lifestyle: `sleep_hours`, `exercise_minutes`, `screen_time_hours`, `caffeine_intake_mg`
  - Distractions: `social_media_hours`, `gaming_hours`
  - Contextual: `internet_quality`, `upcoming_deadline`, `part_time_job`
  - Psychological: `mental_health_score`, `focus_index`, `burnout_level`
  - Output-support: `productivity_score`

---

## 6. System Architecture
### Frontend
- `templates/index.html`
- Premium responsive UI
- Sticky form (values remain after submit)
- Displays score, grade, GPA, feedback, and adjustment notes

### Backend (Flask)
- `main.py`: routes and app orchestration
- `/predict_form`: form submission (HTML response)
- `/predict`: JSON API response

### Modular Backend Design
- `prediction_config.py`: constants, feature list, limits
- `input_validation.py`: parsing + backend validation
- `prediction_model.py`: training/loading model
- `prediction_logic.py`: grade/GPA mapping, reality adjustment, motivational feedback

---

## 7. ML Pipeline
- Algorithm: `RandomForestRegressor`
- Preprocessing:
  - Numeric: median imputation + standard scaling
  - Categorical: most-frequent imputation + one-hot encoding
- Data split: train/test
- Metrics:
  - R2 Score
  - MAE
  - RMSE

### Important Model Improvements Done
- Removed target leakage fields from training: `result`, `grade`
- Added model compatibility checks for schema changes
- Target scaling to 0-100 output for user-friendly interpretation

---

## 8. Validation and Reliability Features
Backend checks now prevent unrealistic inputs:
- Category checks (gender, academic level, internet quality)
- Numeric range checks (focus 0-10, productivity 1-100, etc.)
- Boolean checks (`part_time_job`, `upcoming_deadline` must be 0/1)
- Cross-field sanity checks

If invalid input is given:
- Form route shows clear error list
- API route returns HTTP `400` with detailed validation messages

---

## 9. Reality Adjustment Layer (Post-Model)
To avoid unrealistically high scores in contradictory habits:
- Applies capped penalty for patterns like:
  - Very low study + very high productivity
  - High social media/gaming
  - Very high caffeine
  - High burnout
- Shows transparency:
  - Raw model score
  - Penalty points
  - Reason notes

This improves trust and practical realism in output.

---

## 10. User Output
For each prediction, system displays:
- Predicted Exam Score (/100)
- Estimated Grade
- Estimated GPA (10-point)
- Performance Level (Excellent/Good/Average/Needs Improvement)
- Motivational message
- Personalized top improvement tips

---

## 11. Demo Flow (Live Presentation)
1. Open app in browser
2. Enter normal student profile and predict
3. Explain score + grade + GPA
4. Show motivational feedback section
5. Enter contradictory profile (e.g., low study + high distraction)
6. Show reality adjustment and explain penalty notes
7. Show that inputs stay in form (better UX)

---

## 12. Suggested 8-10 Minute Presentation Script
### Slide 1: Introduction
"Our project predicts student exam performance and gives actionable guidance, not just a number."

### Slide 2: Problem
"Students struggle to connect daily behavior with academic performance."

### Slide 3: Solution
"We built a machine learning + rule-assisted web system that predicts score, grade, GPA, and gives targeted improvement tips."

### Slide 4: Dataset and Features
"We use academic, lifestyle, and mental-wellbeing indicators to model student outcomes."

### Slide 5: ML Pipeline
"Random Forest with preprocessing pipeline, trained on cleaned dataset, evaluated using R2, MAE, RMSE."

### Slide 6: Engineering Improvements
"We modularized code, added validation, removed leakage features, and made output scale 0-100."

### Slide 7: Reality Layer
"To avoid unrealistic predictions, we apply transparent post-model penalties for contradictory habits."

### Slide 8: Product Demo
"Show score, grade, GPA, feedback, and improvement suggestions in live app."

### Slide 9: Impact
"Students get understandable and practical guidance for improving habits."

### Slide 10: Future Scope
"Add university-specific SGPA/CGPA rules, explainable AI, authentication, and student progress tracking."

---

## 13. Likely Viva Questions with Strong Answers
### Q1: Why Random Forest?
Because it handles mixed features well, is robust to non-linearity, and performs reliably without heavy tuning.

### Q2: How did you avoid leakage?
We removed `result` and `grade` from model input because they are derived from exam score and can inflate prediction quality.

### Q3: Why add rule-based penalties after ML?
Pure ML can sometimes give unrealistic scores for contradictory inputs. Rule layer improves practical realism and trust.

### Q4: How do you ensure data validity?
Backend validation enforces ranges, category correctness, boolean constraints, and sanity checks before inference.

### Q5: Is this clinically/academically final advice?
No. It is a decision-support tool to guide habits, not a replacement for formal academic evaluation.

---

## 14. Limitations
- Performance depends on dataset quality and representativeness
- Current GPA mapping is generic, not university-specific
- Reality adjustment is heuristic and can be further calibrated

---

## 15. Future Enhancements
- Institution-specific SGPA/CGPA engine
- Feature contribution explainability (SHAP)
- User login + progress history
- Personalized weekly action plan generation
- Deploy on cloud with analytics dashboard

---

## 16. Closing Statement
"This project combines ML prediction with practical educational guidance. The key value is not just predicting marks, but helping students understand what to improve and how."

---

## 17. Team Presentation Split (for 3 members)
- Member 1: Problem, Objectives, Dataset, EDA
- Member 2: ML pipeline, model training, metrics, architecture
- Member 3: UI, feedback system, validation, demo, future scope

