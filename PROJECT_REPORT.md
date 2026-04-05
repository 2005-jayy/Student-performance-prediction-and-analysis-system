# Student Performance Prediction and Analysis System

## Project Report

### 1. Abstract
The Student Performance Prediction and Analysis System is a machine learning based web application developed to estimate a student's exam performance using behavioral, academic, and lifestyle indicators. The system predicts an exam score on a 0-100 scale and also provides an estimated grade, GPA, risk level, motivational feedback, improvement tips, what-if scenarios, and a short action plan. The project combines a Random Forest regression model with rule-based post-processing to make outputs more realistic and useful for students, teachers, and academic mentors.

### 2. Introduction
Student performance is influenced by multiple factors such as study hours, sleep quality, burnout, productivity, screen time, and internet access. In many academic settings, students are not able to clearly understand how these factors affect outcomes. This project addresses that problem by building a prediction and analysis system that transforms raw student habit data into understandable academic insights.

The system is designed not only to predict marks but also to support decision-making. Instead of showing a score alone, it explains performance level, highlights important factors, and suggests practical ways to improve study habits.

### 3. Problem Statement
Students often struggle to identify the habits and conditions that most strongly affect exam performance. Manual analysis is slow and inconsistent, and students may only realize problems after poor results occur. There is a need for a system that can:

- predict likely exam performance in advance,
- analyze influencing factors,
- provide personalized guidance,
- support early academic intervention.

### 4. Objectives
The main objectives of this project are:

- To build a machine learning system that predicts student exam score.
- To analyze academic, behavioral, and lifestyle factors affecting performance.
- To provide a user-friendly web interface for prediction.
- To generate grade, GPA, feedback, and improvement suggestions.
- To improve prediction reliability using validation and rule-based adjustment logic.

### 5. Scope of the Project
The scope of this project includes:

- data cleaning and exploratory data analysis,
- machine learning model training and evaluation,
- backend input validation,
- prediction through web form and API,
- generation of practical student guidance,
- short-term prediction history tracking.

The project is intended as a decision-support tool and not as a replacement for formal academic evaluation.

### 6. Dataset Description
The project uses the file `data/cleaned_student_dataset.csv` as the main dataset for training and prediction.

Dataset summary:

- Total records: 5000
- Total columns: 22
- Target column: `exam_score`
- Target score range in dataset: 1.0 to 64.09
- Mean exam score: 18.8

The application uses 19 input features:

- `age`
- `gender`
- `academic_level`
- `study_hours`
- `self_study_hours`
- `online_classes_hours`
- `social_media_hours`
- `gaming_hours`
- `sleep_hours`
- `screen_time_hours`
- `exercise_minutes`
- `caffeine_intake_mg`
- `part_time_job`
- `upcoming_deadline`
- `internet_quality`
- `mental_health_score`
- `focus_index`
- `burnout_level`
- `productivity_score`

Two columns, `result` and `grade`, are removed from model training because they are derived from exam score and would cause target leakage.

### 7. System Architecture
The project follows a modular architecture with separate components for interface, validation, model handling, logic, and persistence.

#### Frontend
The frontend is implemented using HTML and CSS in `templates/index.html`. It contains:

- a student input form,
- result display section,
- feedback and statistics cards,
- graphical analysis images from the `static` folder.

#### Backend
The backend is developed using Flask in `main.py`. It provides:

- `/` for loading the dashboard,
- `/predict_form` for form-based prediction,
- `/predict` for JSON API prediction.

#### Supporting Modules
- `prediction_config.py` stores feature lists, paths, limits, defaults, and allowed categories.
- `input_validation.py` handles parsing and backend validation.
- `prediction_model.py` loads or trains the machine learning model.
- `prediction_logic.py` applies business rules, grade mapping, feedback logic, and risk profiling.
- `history_store.py` saves recent prediction history in JSON format.

### 8. Methodology
The project is implemented in the following stages:

#### 8.1 Data Cleaning and Preparation
The raw dataset is processed in `src/data_cleaning_eda.py`. Key steps include:

- reading the raw CSV dataset,
- removing `student_id`,
- checking null values and duplicates,
- generating derived output columns `result` and `grade`,
- saving the cleaned dataset.

#### 8.2 Exploratory Data Analysis
The scripts `src/data_analysis.py` and `src/data_visualization.py` are used to study:

- score distribution,
- correlation with exam score,
- effect of study hours,
- effect of burnout,
- gender-based comparison,
- academic-level comparison,
- internet quality comparison.

The project also generates charts such as:

- histogram of exam score,
- study hours vs exam score scatter plot,
- sleep hours vs exam score scatter plot,
- gender boxplot,
- academic level boxplot,
- correlation heatmap.

#### 8.3 Model Building
The machine learning pipeline is implemented in `prediction_model.py`.

Model details:

- Algorithm used: `RandomForestRegressor`
- Numeric preprocessing: median imputation + standard scaling
- Categorical preprocessing: most frequent imputation + one-hot encoding
- Data split: 80% training and 20% testing
- Random seed: 42

The target score is rescaled to a 0-100 range to make output easier to interpret in the user interface.

#### 8.4 Prediction Enhancement Logic
After the model generates a raw score, the system applies a reality-adjustment layer. This improves practical reliability by reducing unrealistic scores when the input pattern is contradictory.

Examples of penalty conditions:

- very low study hours,
- zero or low self-study,
- high social media usage,
- high gaming time,
- very high caffeine intake,
- high burnout,
- inconsistent combinations such as high productivity with very low study time.

Examples of bonus conditions:

- strong study hours,
- healthy self-study,
- good sleep,
- good focus and productivity,
- low burnout,
- controlled distraction levels.

This layer produces:

- adjusted score,
- adjustment points,
- adjustment notes.

### 9. Input Validation
The project validates all user input before prediction. Validation includes:

- category checks for `gender`, `academic_level`, and `internet_quality`,
- numeric range limits for each measurable field,
- 0/1 validation for boolean-style fields such as `part_time_job` and `upcoming_deadline`,
- sanity check on total learning hours.

If validation fails:

- the form route redisplays the page with error messages,
- the API route returns HTTP 400 with a detailed error response.

### 10. Features of the System
The developed system provides the following features:

- score prediction on a 0-100 scale,
- estimated grade and GPA,
- performance level classification,
- motivation message,
- personalized improvement tips,
- risk profile generation,
- action plan creation,
- explanation of key positive and negative factors,
- what-if scenario predictions,
- recent prediction history,
- browser-based interface and JSON API support.

### 11. Model Evaluation
The model was evaluated on the test split during training. The recorded performance is:

- R2 Score: 0.8156
- MAE: 6.1675
- RMSE: 7.8206

These values indicate that the model captures a strong amount of variance in the target and provides reasonably accurate predictions for a student-support application.

### 12. Output Generated by the System
For each valid student input, the system returns:

- predicted exam score,
- raw model score,
- reality adjustment points,
- grade,
- GPA on a 10-point scale,
- performance level,
- motivational feedback,
- improvement tips,
- risk level,
- action plan,
- important score factors,
- alternative what-if scenarios.

This makes the project more informative than a standard prediction-only model.

### 13. Tools and Technologies Used
- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Joblib
- HTML
- CSS
- Matplotlib
- JSON storage

### 14. Advantages of the Project
- Easy to use through both web form and API.
- Combines machine learning with practical rule-based reasoning.
- Provides actionable feedback instead of only a numeric output.
- Includes validation for safer and more realistic predictions.
- Maintains recent prediction history for quick review.
- Modular code structure improves maintainability.

### 15. Limitations
- The prediction quality depends on the quality and representativeness of the dataset.
- The target scores in the original dataset are relatively low and are rescaled for user presentation.
- The grade and GPA mapping are generic and may not match every institution.
- The reality-adjustment rules are heuristic and may require further calibration.
- There is no user authentication or long-term per-student progress tracking.

### 16. Future Enhancements
The following improvements can be made in future versions:

- institution-specific grading and GPA calculation,
- student login and profile management,
- long-term performance tracking dashboard,
- explainable AI techniques such as SHAP,
- support for more advanced model comparison,
- cloud deployment with analytics,
- teacher or counselor reporting features.

### 17. Conclusion
The Student Performance Prediction and Analysis System successfully demonstrates how machine learning can be combined with academic analytics to support students in a practical way. The project goes beyond score prediction by adding validation, interpretability, personalized feedback, scenario analysis, and risk identification. With further refinement and expansion, this system can become a valuable academic decision-support tool for institutions and learners.

### 18. File Structure Summary
Important files in the project are:

- `main.py` - Flask application entry point and routes
- `prediction_model.py` - model training and loading
- `prediction_logic.py` - grading, feedback, and reality adjustments
- `input_validation.py` - parsing and validation
- `history_store.py` - prediction history persistence
- `prediction_config.py` - configuration and feature definitions
- `templates/index.html` - frontend dashboard
- `src/data_cleaning_eda.py` - cleaning and preprocessing script
- `src/data_analysis.py` - EDA and insights
- `src/data_visualization.py` - graph generation

### 19. References
- Flask Documentation
- Scikit-learn Documentation
- Pandas Documentation
- NumPy Documentation
- Matplotlib Documentation
