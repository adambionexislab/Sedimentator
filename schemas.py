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
