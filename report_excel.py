import os

OUTPUT_DIR = "static/reports/excel"


def export_last_30_days_to_excel(df):
    """
    Exports the given DataFrame to an Excel file.
    Returns the file path.
    """

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    file_path = os.path.join(
        OUTPUT_DIR,
        "flocculant_raw_data_last_30_days.xlsx"
    )

    # Ensure Excel-friendly timestamp
    df_export = df.copy()
    if "TIMESTAMP" in df_export.columns:
        df_export["TIMESTAMP"] = df_export["TIMESTAMP"].dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    df_export.to_excel(
        file_path,
        index=False,
        sheet_name="data",
        engine="openpyxl"
    )

    return file_path
