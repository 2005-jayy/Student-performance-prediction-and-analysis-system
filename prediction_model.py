import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from prediction_config import (
    CSV_FILE,
    INPUT_FEATURES,
    LEAKAGE_COLUMNS,
    MODEL_FILE,
    TARGET_COLUMN,
    TARGET_SCALE_MAX,
)


def train_and_save_model():
    print("📂 Loading dataset...")
    df = pd.read_csv(CSV_FILE)

    print("✅ Dataset Loaded Successfully!")
    print("Shape:", df.shape)

    if "student_id" in df.columns:
        df.drop(columns=["student_id"], inplace=True)

    drop_cols = [TARGET_COLUMN] + [col for col in LEAKAGE_COLUMNS if col in df.columns]
    X = df.drop(columns=drop_cols)
    y_raw = df[TARGET_COLUMN]

    source_target_max = float(y_raw.max())
    if source_target_max <= 0:
        raise ValueError("Invalid exam_score max value. Cannot scale target.")
    y = (y_raw / source_target_max) * TARGET_SCALE_MAX

    missing_features = [col for col in INPUT_FEATURES if col not in X.columns]
    if missing_features:
        raise ValueError(f"Missing required feature columns in dataset: {missing_features}")
    X = X[INPUT_FEATURES]

    categorical_features = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numerical_features = X.select_dtypes(exclude=["object", "string"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numerical_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
    )

    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("\n🚀 Training model...")
    pipeline.fit(X_train, y_train)
    print("✅ Model Training Completed!")

    y_pred = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\n================ MODEL PERFORMANCE ================")
    print(f"R2 Score   : {r2:.4f}")
    print(f"MAE        : {mae:.4f}")
    print(f"RMSE       : {rmse:.4f}")
    print(f"Target Scale: 0-{TARGET_SCALE_MAX:.0f} (source max was {source_target_max:.2f})")
    print("==================================================")

    pipeline.target_scale_max_ = TARGET_SCALE_MAX
    pipeline.source_target_max_ = source_target_max
    joblib.dump(pipeline, MODEL_FILE)
    print(f"\n💾 Model saved as '{MODEL_FILE}'")
    return pipeline


def is_model_compatible(loaded_model):
    feature_names = getattr(loaded_model, "feature_names_in_", None)
    if feature_names is None:
        return False
    if list(feature_names) != INPUT_FEATURES:
        return False
    model_scale = getattr(loaded_model, "target_scale_max_", None)
    return model_scale == TARGET_SCALE_MAX


def load_or_train_model():
    try:
        loaded_model = joblib.load(MODEL_FILE)
        print(f"📦 Loading existing model from '{MODEL_FILE}'...")
        if is_model_compatible(loaded_model):
            print("✅ Model Loaded Successfully!")
            return loaded_model
        print("♻️ Existing model is outdated (old feature schema). Retraining...")
    except FileNotFoundError:
        pass
    return train_and_save_model()
