from langgraph.types import Command

from workflow.graph import graph


def get_config(claim_id: str):

    return {
        "configurable": {
            "thread_id": claim_id
        },
        "run_name": "motor-insurance-claim-workflow",
        "tags": [
            "motor-insurance",
            "claim-assessment"
        ],
        "metadata": {
            "claim_id": claim_id
        }
    }


def start_claim(claim_id: str, initial_state: dict):

    config = get_config(claim_id)

    result = graph.invoke(
        initial_state,
        config=config
    )

    if result.get("__interrupt__"):
        return {
            "status": "HUMAN_REVIEW_REQUIRED",
            "claim_id": claim_id,
            "review_request": [
                item.value for item in result["__interrupt__"]
            ]
        }

    return {
        "status": "COMPLETED",
        "claim_id": claim_id,
        "result": result
    }


def resume_claim(claim_id: str, human_response: dict):

    config = get_config(claim_id)

    result = graph.invoke(
        Command(resume=human_response),
        config=config
    )

    if result.get("__interrupt__"):
        return {
            "status": "HUMAN_REVIEW_REQUIRED",
            "claim_id": claim_id
        }

    return {
        "status": "COMPLETED",
        "claim_id": claim_id,
        "result": result
    }