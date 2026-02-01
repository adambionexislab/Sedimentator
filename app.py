from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from schemas import FlocculantRequest, FlocculantResponse
from model import TheoreticalSludgeModel
from optimizer import recommend_dose
from config import TARGET_SLUDGE_CM
from sheets_logger import log_prediction
from report_data import load_last_30_days
from report_charts import (
    plot_flocculant_dose,
    plot_sludge_height,
    plot_cod_vs_dose
)
from report_excel import export_last_30_days_to_excel

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

@app.get("/debug/last-30-days")
def debug_last_30_days():
    df = load_last_30_days()
    return {
        "rows": len(df),
        "columns": list(df.columns)
    }


@app.get("/debug/generate-charts")
def debug_generate_charts():
    df = load_last_30_days()

    if df.empty:
        return {"status": "no data"}

    output_dir = "static/reports/charts"

    print(df.columns.tolist())

    # --- temporary ---
    print(
        df[[
            "FLOW",
            "RECOMMENDED_FLOCCULANT_DOSE_L_H"
        ]].head(10)
    )
    # --- temporary ---
    
    paths = {
        "dose": plot_flocculant_dose(df, output_dir),
        "sludge": plot_sludge_height(df, output_dir),
        "cod_vs_dose": plot_cod_vs_dose(df, output_dir)
    }

    return {
        "status": "ok",
        "charts": paths
    }


@app.get("/debug/export-excel")
def debug_export_excel():
    df = load_last_30_days()

    if df.empty:
        return {"status": "no data"}

    path = export_last_30_days_to_excel(df)

    return {
        "status": "ok",
        "file": path
    }