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
from report_pdf import generate_pdf_report
import os
from report_data import build_summary
from report_llm import generate_llm_report
from schemas import OxygenRequest, OxygenResponse
from oxygen_model import predict_airflow
from sheets_logger import log_oxygen_prediction
from compressor_lookup import get_compressor_setup

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

@app.post("/report/generate")
def generate_full_report():
    df = load_last_30_days()

    if df.empty:
        return {"error": "No data available for report"}

    # Charts
    charts_dir = "static/reports/charts"
    chart_paths = {
        "dose": plot_flocculant_dose(df, charts_dir),
        "sludge": plot_sludge_height(df, charts_dir),
        "cod_vs_dose": plot_cod_vs_dose(df, charts_dir)
    }

    # Excel
    excel_path = export_last_30_days_to_excel(df)

    # LLM text
    summary = build_summary(df)
    report_text = generate_llm_report(summary)

    # PDF
    pdf_path = generate_pdf_report(chart_paths, report_text)

    return {
        "status": "ok",
        "pdf": pdf_path,
        "excel": excel_path
    }

@app.post("/oxygen/recommend", response_model=OxygenResponse)
def recommend_oxygen(request: OxygenRequest):

    base_airflow = predict_airflow(
        cod=request.COD,
        flow=request.FLOW,
        temperature=request.TEMPERATURE
    )

    correction_factor = request.TARGET_OXYGEN / 2.0
    recommended_airflow = base_airflow * correction_factor

    compressor_data = get_compressor_setup(recommended_airflow)

    response = {
        "BASE_AIRFLOW": round(base_airflow, 2),
        "TARGET_OXYGEN": request.TARGET_OXYGEN,
        "RECOMMENDED_AIRFLOW": round(recommended_airflow, 2),
        "COMPRESSORS": compressor_data["COMPRESSORS"],
        "INVERTER_PERCENT": compressor_data["INVERTER_PERCENT"],
        "CONSUMPTION_KW": compressor_data["CONSUMPTION_KW"]
    }

    # 🔹 Log to Google Sheets
    log_oxygen_prediction({
        "COD": request.COD,
        "FLOW": request.FLOW,
        "TEMPERATURE": request.TEMPERATURE,
        "TARGET_OXYGEN": request.TARGET_OXYGEN,
        "BASE_AIRFLOW": response["BASE_AIRFLOW"],
        "RECOMMENDED_AIRFLOW": response["RECOMMENDED_AIRFLOW"]
    })

    return response


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

@app.get("/debug/generate-pdf")
def debug_generate_pdf():
    df = load_last_30_days()

    if df.empty:
        return {"status": "no data"}

    output_dir = "static/reports/charts"

    chart_paths = {
        "dose": os.path.join(output_dir, "flocculant_dose.png"),
        "sludge": os.path.join(output_dir, "sludge_height.png"),
        "cod_vs_dose": os.path.join(output_dir, "cod_vs_dose.png")
    }

    path = generate_pdf_report(chart_paths)

    return {
        "status": "ok",
        "file": path
    }