from config import TARGET_SLUDGE_CM, MIN_DOSE, MAX_DOSE

LOW_SLUDGE_THRESHOLD = 200.0

def correct_teoretical_sludge(T):
    if T < LOW_SLUDGE_THRESHOLD:
        return T * (T / LOW_SLUDGE_THRESHOLD)
    return T

def recommend_dose(predicted_teoretical_sludge):
    T_corr = correct_teoretical_sludge(predicted_teoretical_sludge)

    dose = T_corr / TARGET_SLUDGE_CM

    dose = max(dose, MIN_DOSE)
    dose = min(dose, MAX_DOSE)

    return round(dose, 2)
