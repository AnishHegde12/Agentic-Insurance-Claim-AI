import json
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from ..services.state import State


def report_generation(state: State):
    claim_id = state["claim_id"]
    normalised_data = state["normalised_claim"]
    completeness = state["completeness_list"]
    api_list = state["mock_api_list"]
    risk_score = state["risk_score"]
    risk_indicator = state["risk_category"]
    risk_description = state["risk_description"]
    if isinstance(normalised_data, str):
        normalised_data = json.loads(normalised_data)

    # Create reports folder
    os.makedirs("reports", exist_ok=True)

    pdf_path = f"reports/{claim_id}_assessment_report.pdf"

    # Create PDF
    pdf = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph(
            "Insurance Claim Assessment Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    def add_section(title, data):

        story.append(
            Paragraph(
                title,
                styles["Heading2"]
            )
        )

        table_data = []

        for key, value in data.items():

            if isinstance(value, list):
                value = ", ".join(map(str, value))

            elif isinstance(value, dict):
                value = json.dumps(value, indent=2)

            if value in [None, "", []]:
                value = "N/A"

            table_data.append(
                [
                    Paragraph(
                        key.replace("_", " ").title(),
                        styles["BodyText"]
                    ),
                    Paragraph(
                        str(value),
                        styles["BodyText"]
                    )
                ]
            )

        table = Table(
            table_data,
            colWidths=[
                2.2 * inch,
                4.5 * inch
            ]
        )

        table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.append(table)
        story.append(Spacer(1, 20))

    add_section(
        "Claim Details",
        {
            "claim_id": claim_id,

            "policy_id": normalised_data.get(
                "policy_id",
                "N/A"
            ),

            "customer": normalised_data.get(
                "customer",
                "N/A"
            ),

            "vehicle": normalised_data.get(
                "vehicle",
                "N/A"
            ),

            "accident_date": normalised_data.get(
                "accident_date",
                "N/A"
            ),

            "accident_location": normalised_data.get(
                "accident_location",
                "N/A"
            )
        }
    )


    add_section(
        "Document Validation",
        {
            "missing_fields": completeness,
            "extraction_status": "Completed"
        }
    )


    add_section(
        "Backend Data Validation",
        {
            "discrepancies": api_list
        }
    )

    add_section(
        "Damage Assessment",
        {
            "reported_damage": normalised_data.get(
                "claimed_damage",
                "N/A"
            ),

            "image_detected_damage": normalised_data.get(
                "damage_image",
                "N/A"
            ),

            "garage_requested_repairs": normalised_data.get(
                "garage_requested_repairs",
                "N/A"
            )
        }
    )

    add_section(
        "Financial Assessment",
        {
            "garage_estimate": normalised_data.get(
                "garage_estimate",
                "N/A"
            ),

            "reference_repair_amount": normalised_data.get(
                "reference_repair_amount",
                "N/A"
            ),

            "cost_anomalies": api_list
        }
    )


    add_section(
        "Risk Assessment",
        {
            "risk_score": risk_score,
            "risk_category": risk_indicator,
            "risk_description": risk_description
        }
    )

    story.append(
        Paragraph(
            "Final Recommendation",
            styles["Heading2"]
        )
    )

    if str(risk_indicator).upper() == "LOW":
        recommendation = "RECOMMENDED FOR APPROVAL"

    elif str(risk_indicator).upper() == "MEDIUM":
        recommendation = "RECOMMENDED FOR MANUAL REVIEW"

    else:
        recommendation = "NOT RECOMMENDED FOR APPROVAL"

    story.append(
        Paragraph(
            f"<b>Recommendation:</b> {recommendation}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"<b>Reason:</b> {risk_description}",
            styles["BodyText"]
        )
    )

    pdf.build(story)

    return {
        "report_path": pdf_path
    }