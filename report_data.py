import pandas as pd
from datetime import datetime, timedelta
import pytz

from sheets_logger import get_worksheet

ITALY_TZ = pytz.timezone("Europe/Rome")

def normalize_numeric_columns(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def load_last_30_days():
    sheet = get_worksheet()
    records = sheet.get_all_records()

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # --- Timestamp ---
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce")

    if df["TIMESTAMP"].dt.tz is None:
        df["TIMESTAMP"] = df["TIMESTAMP"].dt.tz_localize("UTC").dt.tz_convert(ITALY_TZ)
    else:
        df["TIMESTAMP"] = df["TIMESTAMP"].dt.tz_convert(ITALY_TZ)

    cutoff = datetime.now(ITALY_TZ) - timedelta(days=30)
    df = df[df["TIMESTAMP"] >= cutoff]
    df = df.sort_values("TIMESTAMP").reset_index(drop=True)

    # ✅ FIX: normalize numeric columns
    numeric_cols = [
        "COD",
        "SVI",
        "SS",
        "FLOW",
        "SLUDGE",
        "RECOMMENDED_FLOCCULANT_DOSE_L_H"
    ]

    df = normalize_numeric_columns(df, numeric_cols)

    return df

