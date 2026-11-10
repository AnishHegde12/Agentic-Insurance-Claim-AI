import os
import requests
import streamlit as st
import pandas as pd

from pathlib import Path


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Motor Insurance Claim Assessment",
    page_icon="🚗",
    layout="wide"
)


# --------------------------------------------------
# 2. CONFIGURATION
# --------------------------------------------------

API_BASE_URL = os.getenv(
    "INSURANCE_API_URL",
    "http://127.0.0.1:8000"
)

CLAIM_IDS = [
    "CLM001",
    "CLM002",
    "CLM003",
    "CLM004"
]


# --------------------------------------------------
# 3. SESSION STATE
# --------------------------------------------------

if "workflow_response" not in st.session_state:
    st.session_state.workflow_response = None

if "selected_claim" not in st.session_state:
    st.session_state.selected_claim = None

if "review_response" not in st.session_state:
    st.session_state.review_response = None


# --------------------------------------------------
# 4. API FUNCTIONS
# --------------------------------------------------

def start_claim_processing(claim_id):

    url = f"{API_BASE_URL}/claims/{claim_id}/process"

    response = requests.post(
        url,
        timeout=300
    )

    response.raise_for_status()

    return response.json()


def submit_human_review(claim_id, action, comments):

    url = f"{API_BASE_URL}/claims/{claim_id}/review"

    payload = {
        "action": action,
        "comments": comments
    }

    response = requests.post(
        url,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# 5. HELPER FUNCTIONS
# --------------------------------------------------

def get_review_details(response):

    if not response:
        return {}

    review_request = response.get("review_request", [])

    if isinstance(review_request, list) and review_request:
        return review_request[0]

    if isinstance(review_request, dict):
        return review_request

    return {}


def get_result(response):

    if not response:
        return {}

    return response.get("result", {})


def show_json_section(title, data):

    with st.expander(title, expanded=False):

        if data:
            st.json(data)
        else:
            st.info("No information available.")


def show_status(status):

    if status == "COMPLETED":
        st.success("Claim workflow completed.")

    elif status == "HUMAN_REVIEW_REQUIRED":
        st.warning("Human review is required.")

    else:
        st.info(status or "No workflow status available.")


# --------------------------------------------------
# 6. SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🚗 Insurance Claims")

    st.caption("Agentic AI Claim Assessment System")

    st.divider()

    selected_claim = st.selectbox(
        "Select Claim ID",
        CLAIM_IDS
    )

    # st.caption(f"Backend API: {API_BASE_URL}")

    if st.button("Reset current screen"):
        st.session_state.workflow_response = None
        st.session_state.review_response = None
        st.session_state.selected_claim = None
        st.rerun()


# --------------------------------------------------
# 7. MAIN DASHBOARD
# --------------------------------------------------

st.title("Motor Insurance Claim Assessment")

st.write(
    "Automated insurance claim extraction, validation, "
    "risk assessment and human review using Agentic AI."
)

st.divider()


# --------------------------------------------------
# 8. CLAIM PROCESSING
# --------------------------------------------------

st.subheader("Claim Processing")

col1, col2 = st.columns([2, 1])

with col1:

    st.write(f"Selected Claim: **{selected_claim}**")

with col2:

    process_button = st.button(
        "▶ Process Claim",
        type="primary",
        use_container_width=True
    )


if process_button:

    try:

        with st.spinner("Processing claim using LangGraph agents..."):

            response = start_claim_processing(selected_claim)

            st.session_state.workflow_response = response
            st.session_state.selected_claim = selected_claim
            st.session_state.review_response = None

        st.rerun()

    except requests.exceptions.ConnectionError:

        st.error(
            "Unable to connect to FastAPI. "
            "Make sure your backend is running."
        )

    except requests.exceptions.HTTPError as error:

        st.error(f"Backend returned an error: {error}")

        if error.response is not None:
            st.code(error.response.text)

    except Exception as error:

        st.error(f"Unexpected error: {error}")


# --------------------------------------------------
# 9. DISPLAY WORKFLOW RESPONSE
# --------------------------------------------------

response = st.session_state.workflow_response

if response and st.session_state.selected_claim == selected_claim:

    st.divider()

    st.subheader("Workflow Status")

    status = response.get("status", "UNKNOWN")

    show_status(status)

    st.write(f"Claim ID: **{selected_claim}**")

    # --------------------------------------------------
    # HUMAN REVIEW REQUIRED
    # --------------------------------------------------

    if status == "HUMAN_REVIEW_REQUIRED":

        review_details = get_review_details(response)

        st.divider()

        st.subheader("🧑 Human-in-the-Loop Review")

        st.warning(
            "The LangGraph workflow is paused. "
            "Review the assessment before submitting your decision."
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Risk Score",
                review_details.get("risk_score", "N/A")
            )

        with col2:

            st.metric(
                "Risk Category",
                review_details.get("risk_category", "N/A")
            )

        with col3:

            st.metric(
                "Recommended Decision",
                review_details.get(
                    "recommended_decision",
                    "N/A"
                )
            )

        st.write("**Reason for review**")

        st.info(
            review_details.get(
                "reason",
                "Additional verification is required."
            )
        )

        # Missing fields
        missing_fields = review_details.get(
            "missing_fields",
            []
        )

        if missing_fields:

            st.write("**Missing Information**")

            for field in missing_fields:
                st.write(f"- {field}")

        # Validation results
        st.write("**Validation Results**")

        validation_results = review_details.get(
            "validation_results",
            {}
        )

        if validation_results:

            for agent, result in validation_results.items():

                show_json_section(
                    agent.replace("_", " ").title(),
                    result
                )

        # --------------------------------------------------
        # HUMAN REVIEW FORM
        # --------------------------------------------------

        st.divider()

        st.subheader("Submit Review Decision")

        with st.form("human_review_form"):

            action = st.selectbox(
                "Select your decision",
                options=[
                    "approve",
                    "reject",
                    "request_more_information"
                ],
                format_func=lambda value: {
                    "approve": "Approve Claim",
                    "reject": "Reject Claim",
                    "request_more_information":
                        "Request More Information"
                }[value]
            )

            comments = st.text_area(
                "Reviewer Comments",
                placeholder="Enter your observations or reason..."
            )

            submit_review = st.form_submit_button(
                "Submit Decision",
                type="primary",
                use_container_width=True
            )

            if submit_review:

                if action == "request_more_information" and not comments.strip():

                    st.error(
                        "Please provide comments when requesting more information."
                    )

                else:

                    try:

                        with st.spinner("Resuming LangGraph workflow..."):

                            review_result = submit_human_review(
                                selected_claim,
                                action,
                                comments
                            )

                            st.session_state.review_response = review_result
                            st.session_state.workflow_response = review_result

                        st.rerun()

                    except requests.exceptions.ConnectionError:

                        st.error("Unable to connect to the backend.")

                    except requests.exceptions.HTTPError as error:

                        st.error(f"Review submission failed: {error}")

                        if error.response is not None:
                            st.code(error.response.text)

                    except Exception as error:

                        st.error(f"Unexpected error: {error}")


    # --------------------------------------------------
    # COMPLETED WORKFLOW
    # --------------------------------------------------

    elif status == "COMPLETED":

        result = get_result(response)

        st.divider()

        st.subheader("Final Claim Assessment")

        decision = result.get(
            "final_decision",
            "Not available"
        )

        risk_category = result.get(
            "risk_category",
            "Not available"
        )

        risk_score = result.get(
            "risk_score",
            "N/A"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Final Decision",
                decision
            )

        with col2:

            st.metric(
                "Risk Category",
                risk_category
            )

        with col3:

            st.metric(
                "Risk Score",
                risk_score
            )

        st.write("**Decision Reason**")

        st.info(
            result.get(
                "decision_reason",
                "No decision reason available."
            )
        )

        # --------------------------------------------------
        # VALIDATION SUMMARY
        # --------------------------------------------------

        st.divider()

        st.subheader("Validation Summary")

        validation_keys = [
            "completeness_result",
            "policy_validation",
            "customer_validation",
            "vehicle_validation",
            "claim_history_validation",
            "damage_validation",
            "repair_cost_validation"
        ]

        for key in validation_keys:

            if key in result:

                show_json_section(
                    key.replace("_", " ").title(),
                    result[key]
                )

        # --------------------------------------------------
        # RISK DETAILS
        # --------------------------------------------------

        st.divider()

        st.subheader("Risk Assessment")

        risk_indicators = result.get(
            "risk_indicators",
            []
        )

        if risk_indicators:

            st.dataframe(
                pd.DataFrame(risk_indicators),
                use_container_width=True
            )

        else:

            st.info("No risk indicators available.")

        # --------------------------------------------------
        # REPORT DETAILS
        # --------------------------------------------------

        st.divider()

        st.subheader("Generated Assessment Report")

        report_path = result.get("report_path_output")

        if report_path:

            report_file = Path(report_path)

            if report_file.exists():

                st.success("Assessment report generated.")

                if report_file.suffix.lower() == ".pdf":

                    st.download_button(
                        "Download PDF Report",
                        data=report_file.read_bytes(),
                        file_name=report_file.name,
                        mime="application/pdf"
                    )

                elif report_file.suffix.lower() in [".html", ".json"]:

                    mime_type = (
                        "text/html"
                        if report_file.suffix.lower() == ".html"
                        else "application/json"
                    )

                    st.download_button(
                        "Download Assessment Report",
                        data=report_file.read_bytes(),
                        file_name=report_file.name,
                        mime=mime_type
                    )

            else:

                st.warning(
                    "Report path was returned, but the file "
                    "is not accessible from the Streamlit application."
                )

        else:

            st.info(
                "No report path was returned by the backend."
            )

        # --------------------------------------------------
        # COMPLETE WORKFLOW OUTPUT
        # --------------------------------------------------

        show_json_section(
            "Complete Workflow Output",
            result
        )


elif not response:

    st.info(
        "Select a claim and click Process Claim to begin."
    )