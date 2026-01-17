import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "readmission_model.joblib"
)

model = joblib.load(MODEL_PATH)

def predict_readmission(feature_vector: dict) -> float:
    """
    feature_vector must contain all model features
    """
    ordered_features = [
        "time_in_hospital",
        "num_lab_procedures",
        "num_procedures",
        "num_medications",
        "number_outpatient",
        "number_emergency",
        "number_inpatient",
        "number_diagnoses",
        "change",
        "diabetesMed",
    ]

    X = [[feature_vector.get(f, 0) for f in ordered_features]]
    return float(model.predict_proba(X)[0][1])
