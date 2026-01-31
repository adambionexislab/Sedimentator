import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo   # Python 3.9+

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "predictions.csv")

FIELDS = [
    "timestamp",
    "COD",
    "SVI",
    "SS",
    "FLOW",
    "SLUDGE_CM",
    "RECOMMENDED_DOSE_L_M3"
]

ITALY_TZ = ZoneInfo("Europe/Rome")

def log_prediction(data: dict):
    os.makedirs(LOG_DIR, exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    now_italy = datetime.now(ITALY_TZ).isoformat(timespec="seconds")

    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": now_italy,
            **data
        })
