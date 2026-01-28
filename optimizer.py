from config import TARGET_SLUDGE_CM, MIN_DOSE, MAX_DOSE

def recommend_dose(predicted_teoretical_sludge):
    dose = predicted_teoretical_sludge / TARGET_SLUDGE_CM

    dose = max(dose, MIN_DOSE)
    dose = min(dose, MAX_DOSE)

    return round(dose, 2)
