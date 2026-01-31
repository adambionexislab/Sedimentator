from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from schemas import FlocculantRequest, FlocculantResponse
from model import TheoreticalSludgeModel
from optimizer import recommend_dose
from config import TARGET_SLUDGE_CM
from sheets_logger import log_prediction


app = FastAPI(title="Flocculant Recommendation API")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

model = TheoreticalSludgeModel()

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/flocculant/recommend", response_model=FlocculantResponse)
def recommend(request: FlocculantRequest):

    predicted_teoretical_sludge = model.predict(
        COD=request.COD,
        SVI=request.SVI,
        SS=request.SS,
        FLOW=request.FLOW
    )

    dose = recommend_dose(predicted_teoretical_sludge)

# 🔹 Log everything
    log_prediction({
        "COD": request.COD,
        "SVI": request.SVI,
        "SS": request.SS,
        "FLOW": request.FLOW,
        "SLUDGE_CM": request.SLUDGE_CM,
        "RECOMMENDED_DOSE_L_M3": dose
    })

    return FlocculantResponse(
        predicted_teoretical_sludge=round(predicted_teoretical_sludge, 2),
        recommended_dose_l_m3=dose,
        target_sludge_cm=TARGET_SLUDGE_CM
    )
