from langgraph.graph import StateGraph, START, END
from rag.rag_state import State
from rag.memory import get_memory

from rag.retrieval_agent import retrieval_agent
from rag.augmentation_agent import augmentation_agent
from rag.generation_agent import generation_agent
from rag.reflection_agent import reflection_agent


def reflection_router(state: State):

    if state["is_grounded"]:
        return "end"

    if state["attempts"] >= 2:
        return "end"

    return "retry"


def build_rag_graph():

    workflow = StateGraph(State)

    workflow.add_node("retrieval", retrieval_agent)
    workflow.add_node("augmentation", augmentation_agent)
    workflow.add_node("generation", generation_agent)
    workflow.add_node("reflection", reflection_agent)

    workflow.add_edge(START, "retrieval")
    workflow.add_edge("retrieval", "augmentation")
    workflow.add_edge("augmentation", "generation")
    workflow.add_edge("generation", "reflection")

    workflow.add_conditional_edges(
        "reflection",
        reflection_router,
        {
            "retry": "augmentation",
            "end": END
        }
    )

    app=workflow.compile()
    return app