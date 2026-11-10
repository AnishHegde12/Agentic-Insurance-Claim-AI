from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional

from services.workflow_runner import (
    start_claim,
    resume_claim
)

app = FastAPI()


class HumanReviewRequest(BaseModel):

    action: Literal[
        "approve",
        "reject",
        "request_more_information"
    ]

    comments: Optional[str] = None


@app.post("/claims/{claim_id}/process")
def process_claim(claim_id: str):

    try:

        initial_state = {
            "claim_id": claim_id,
            "claim_folder": f"data/incoming/{claim_id}",
            "report_path": (
                f"data/incoming/{claim_id}/claim_form.pdf"
            )
        }

        return start_claim(
            claim_id,
            initial_state
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/claims/{claim_id}/review")
def review_claim(
    claim_id: str,
    request: HumanReviewRequest
):

    try:

        return resume_claim(
            claim_id,
            request.model_dump()
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )