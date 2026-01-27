from pydantic import BaseModel, Field

class FlocculantRequest(BaseModel):
    COD: float = Field(..., example=400)
    SVI: float = Field(..., example=170)
    SS: float = Field(..., example=3.2)
    FLOW: float = Field(..., example=1300)

class FlocculantResponse(BaseModel):
    recommended_dose_l_m3: float
    predicted_sludge_cm: float
    target_cm: float
    hard_limit_cm: float
    confidence: str
