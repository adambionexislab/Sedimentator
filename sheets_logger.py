import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import json
import pytz

SPREADSHEET_NAME = "Flocculant_Predictions"
WORKSHEET_NAME = "data"

ITALY_TZ = ZoneInfo("Europe/Rome")

SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

def get_client():
    creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_json:
        raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON env var")

    creds_dict = json.loads(creds_json)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

    return gspread.authorize(creds)

def log_prediction(data: dict):
    client = get_client()
    sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)

    timestamp = datetime.now(ITALY_TZ).isoformat(timespec="seconds")

    row = [
        timestamp,
        data["COD"],
        data["SVI"],
        data["SS"],
        data["FLOW"],
        data["SLUDGE_CM"],
        data["RECOMMENDED_DOSE_L_M3"]
    ]

    sheet.append_row(row, value_input_option="USER_ENTERED")

def get_gspread_client():
    service_account_info = json.loads(
        os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    )

    creds = Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    return gspread.authorize(creds)

def get_worksheet():
    client = get_gspread_client()
    sh = client.open(SPREADSHEET_NAME)
    try:
        return sh.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        return sh.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=20)
    
def log_oxygen_prediction(data: dict):
    tz = pytz.timezone("Europe/Rome")
    timestamp = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    client = get_client()
    sheet = client.open(SPREADSHEET_NAME).worksheet("oxygen_data")

    row = [
        timestamp,
        data["COD"],
        data["FLOW"],
        data["TEMPERATURE"],
        data["TARGET_OXYGEN"],
        data["BASE_AIRFLOW"],
        data["RECOMMENDED_AIRFLOW"]
    ]

    sheet.append_row(row, value_input_option="USER_ENTERED")