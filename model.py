import joblib
import numpy as np

MODEL_PATH = "flocculant_model.pkl"

class SludgeModel:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict_sludge(self, COD, SVI, SS, FLOW, FLOCCULANT):
        X = np.array([[COD, SVI, SS, FLOW, FLOCCULANT]])
        prediction = self.model.predict(X)[0]
        return float(prediction)
