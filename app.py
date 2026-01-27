from fastapi import FastAPI, HTTPException
from schemas import FlocculantRequest, FlocculantResponse
from model import SludgeModel
from optimizer import recommend_dose
from config import CONTROL_TARGET_CM, HARD_LIMIT_CM, DEFAULT_MAX_DOSE

app = FastAPI(
    title="Flocculant Optimization API",
    description="Predicts sludge height and recommends flocculant dose",
    version="1.0"
)

model = SludgeModel()

@app.post("/flocculant/recommend", response_model=FlocculantResponse)
def recommend_flcoagulant(request: FlocculantRequest):
    result = recommend_dose(
        model=model,
        COD=request.COD,
        SVI=request.SVI,
        SS=request.SS,
        FLOW=request.FLOW,
        max_dose=DEFAULT_MAX_DOSE
    )

    if result is None:
        raise HTTPException(
            status_code=422,
            detail="No safe flocculant dose found under current conditions"
        )

    return FlocculantResponse(
        recommended_dose_l_m3=result["dose"],
        predicted_sludge_cm=result["predicted_sludge"],
        target_cm=CONTROL_TARGET_CM,
        hard_limit_cm=HARD_LIMIT_CM,
        confidence="medium"
    )
