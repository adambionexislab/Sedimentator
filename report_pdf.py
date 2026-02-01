import os
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from pytz import timezone


OUTPUT_DIR = "static/reports/pdf"
ITALY_TZ = timezone("Europe/Rome")


def generate_pdf_report(chart_paths, days=30):
    """
    Generates a PDF report with charts and static text.
    Returns the file path.
    """

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    timestamp = datetime.now(ITALY_TZ).strftime("%Y-%m-%d_%H-%M")
    file_path = os.path.join(
        OUTPUT_DIR,
        f"flocculant_report_last_{days}_days.pdf"
    )

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    story = []

    # --- Title ---
    story.append(Paragraph(
        f"<b>Flocculant Dosing Report – Last {days} Days</b>",
        styles["Title"]
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        f"Generated on: {datetime.now(ITALY_TZ).strftime('%d/%m/%Y %H:%M')} (Italy)",
        styles["Normal"]
    ))
    story.append(Spacer(1, 20))

    # --- Executive summary (placeholder) ---
    story.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "This report summarizes flocculant dosing performance over the last 30 days. "
        "It is intended to support operational decision-making and cost optimization. "
        "The analysis is based on real plant data logged by the dosing recommendation system.",
        styles["Normal"]
    ))
    story.append(Spacer(1, 20))

    # --- Charts ---
    story.append(Paragraph("<b>Process Trends</b>", styles["Heading2"]))
    story.append(Spacer(1, 12))

    for title, path in [
        ("Flocculant Dose (L/h)", chart_paths["dose"]),
        ("Sludge Height (cm)", chart_paths["sludge"]),
        ("COD vs Flocculant Dose", chart_paths["cod_vs_dose"])
    ]:
        story.append(Paragraph(title, styles["Heading3"]))
        story.append(Spacer(1, 8))

        img = Image(path, width=16 * cm, height=9 * cm)
        story.append(img)
        story.append(Spacer(1, 20))

    # --- Footer note ---
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<i>Model version: v1.0 – Operator-facing dose displayed in L/h.</i>",
        styles["Normal"]
    ))

    doc.build(story)

    return file_path
