from ..rag.rag_state import State
from ...services.llm_gateway import llm
def generation_agent(state: State):
    response = llm.invoke(
        state["augmented_prompt"]
    )
    return {
        "answer": response.content,
        "attempts": state.get("attempts", 0) + 1
    }