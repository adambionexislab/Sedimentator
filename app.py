from fastapi import FastAPI
from schemas import FlocculantRequest, FlocculantResponse
from model import TheoreticalSludgeModel
from optimizer import recommend_dose
from config import TARGET_SLUDGE_CM

app = FastAPI(title="Flocculant Recommendation API")

model = TheoreticalSludgeModel()

@app.post("/flocculant/recommend", response_model=FlocculantResponse)
def recommend(request: FlocculantRequest):

    predicted_teoretical_sludge = model.predict(
        COD=request.COD,
        SVI=request.SVI,
        SS=request.SS,
        FLOW=request.FLOW
    )

    dose = recommend_dose(predicted_teoretical_sludge)

    return FlocculantResponse(
        predicted_teoretical_sludge=round(predicted_teoretical_sludge, 2),
        recommended_dose_l_m3=dose,
        target_sludge_cm=TARGET_SLUDGE_CM
    )
