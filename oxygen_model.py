import joblib
import numpy as np

MODEL_PATH = "models/oxygen_model.pkl"

# Load model once
oxygen_model = joblib.load(MODEL_PATH)

def predict_airflow(cod, flow, temperature):
    X = np.array([[cod, flow, temperature]])
    prediction = oxygen_model.predict(X)[0]
    return float(prediction)
