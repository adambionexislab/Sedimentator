import joblib
import numpy as np

MODEL_PATH = "flocculant_model.pkl"

class TheoreticalSludgeModel:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, COD, SVI, SS, FLOW):
        X = np.array([[COD, SVI, SS, FLOW]])
        return float(self.model.predict(X)[0])
