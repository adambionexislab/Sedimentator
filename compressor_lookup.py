import pandas as pd

COMPRESSOR_TABLE_PATH = "data/compressors.csv"

# Load once
compressor_df = pd.read_csv(COMPRESSOR_TABLE_PATH)
compressor_df = compressor_df.sort_values("AIRFLOW").reset_index(drop=True)


def get_compressor_setup(required_airflow: float) -> dict:
    """
    Returns compressor configuration for required airflow
    Uses nearest higher airflow (conservative choice)
    """

    match = compressor_df[compressor_df["AIRFLOW"] >= required_airflow]

    if match.empty:
        # If airflow exceeds table, use max available
        row = compressor_df.iloc[-1]
    else:
        row = match.iloc[0]

    return {
        "COMPRESSORS": int(row["COMPRESSORS"]),
        "INVERTER_PERCENT": round(float(row["INVERTER"]) * 100, 2),
        "CONSUMPTION_KW": float(row["CONSUMPTION"])
    }
