import sqlite3

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt

from services.state import State

# Import your existing agents
from agents.extraction_agent import extraction_agent
from agents.completeness_agent import completeness_agent
from agents.mock_data_validation_agent import mock_data_validation_agent
from agents.damage_validation_agent import damage_validation_agent
from agents.repair_cost_validation_agent import repair_cost_validation_agent
from agents.risk_assessment_agent import risk_assessment_agent
from agents.decision_agent import decision_agent
from agents.report_generation_agent import report_generation_agent


# --------------------------------------------------
# 1. HUMAN REVIEW NODE
# --------------------------------------------------

def human_review_agent(state: State):

    review_request = {
        "claim_id": state.get("claim_id"),
        "recommended_decision": state.get("final_decision"),
        "reason": state.get("decision_reason"),
        "risk_score": state.get("risk_score"),
        "risk_category": state.get("risk_category"),
        "missing_fields": state.get("missing_fields", []),
        "validation_results": {
            "policy": state.get("policy_validation", {}),
            "vehicle": state.get("vehicle_validation", {}),
            "damage": state.get("damage_validation", {}),
            "repair_cost": state.get("repair_cost_validation", {})
        },
        "allowed_actions": [
            "approve",
            "reject",
            "request_more_information"
        ]
    }

    # Pause workflow and wait for human input
    human_response = interrupt(review_request)

    # Validate the human response
    action = human_response.get("action")

    allowed_actions = {
        "approve",
        "reject",
        "request_more_information"
    }

    if action not in allowed_actions:
        raise ValueError("Invalid human review action")

    # Update the claim decision
    if action == "approve":
        final_decision = "APPROVED_BY_HUMAN"

    elif action == "reject":
        final_decision = "REJECTED_BY_HUMAN"

    else:
        final_decision = "MORE_INFORMATION_REQUIRED"

    return {
        "human_decision": human_response,
        "human_review_status": "COMPLETED",
        "final_decision": final_decision
    }


# --------------------------------------------------
# 2. CONDITIONAL ROUTING
# --------------------------------------------------

def route_after_decision(state: State):

    if state.get("human_review_required", False):
        return "human_review"

    return "generate_report"


# --------------------------------------------------
# 3. BUILD STATEGRAPH
# --------------------------------------------------

builder = StateGraph(State)

# Register nodes
builder.add_node("extraction", extraction_agent)
builder.add_node("completeness", completeness_agent)
builder.add_node("mock_data_validation", mock_data_validation_agent)
builder.add_node("damage_validation", damage_validation_agent)
builder.add_node("repair_cost_validation", repair_cost_validation_agent)
builder.add_node("risk_assessment", risk_assessment_agent)
builder.add_node("decision", decision_agent)
builder.add_node("human_review", human_review_agent)
builder.add_node("generate_report", report_generation_agent)


# Define workflow sequence
builder.add_edge(START, "extraction")
builder.add_edge("extraction", "completeness")
builder.add_edge("completeness", "mock_data_validation")
builder.add_edge("mock_data_validation", "damage_validation")
builder.add_edge("damage_validation", "repair_cost_validation")
builder.add_edge("repair_cost_validation", "risk_assessment")
builder.add_edge("risk_assessment", "decision")


# Conditional edge after decision
builder.add_conditional_edges(
    "decision",
    route_after_decision,
    {
        "human_review": "human_review",
        "generate_report": "generate_report"
    }
)

builder.add_edge("human_review", "generate_report")

builder.add_edge("generate_report", END)

connection = sqlite3.connect(
    "insurance_workflow.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(connection)


# Compile graph with persistent checkpointing
graph = builder.compile(
    checkpointer=checkpointer
)