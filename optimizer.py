import numpy as np
from config import CONTROL_TARGET_CM, DOSE_MIN, DOSE_STEP

def recommend_dose(model, COD, SVI, SS, FLOW, max_dose):
    doses = np.arange(DOSE_MIN, max_dose + DOSE_STEP, DOSE_STEP)

    for dose in doses:
        sludge = model.predict_sludge(
            COD=COD,
            SVI=SVI,
            SS=SS,
            FLOW=FLOW,
            FLOCCULANT=dose
        )

        if sludge <= CONTROL_TARGET_CM:
            return {
                "dose": round(dose, 2),
                "predicted_sludge": round(sludge, 1)
            }

    return None
