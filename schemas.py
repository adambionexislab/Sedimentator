from pydantic import BaseModel

class FlocculantRequest(BaseModel):
    COD: float
    SVI: float
    SS: float
    FLOW: float
    SLUDGE_CM: float

class FlocculantResponse(BaseModel):
    predicted_teoretical_sludge: float
    recommended_dose_l_m3: float
    target_sludge_cm: float

class OxygenRequest(BaseModel):
    COD: float
    FLOW: float
    TEMPERATURE: float
    TARGET_OXYGEN: float


class OxygenResponse(BaseModel):
    BASE_AIRFLOW: float
    TARGET_OXYGEN: float
    RECOMMENDED_AIRFLOW: float
