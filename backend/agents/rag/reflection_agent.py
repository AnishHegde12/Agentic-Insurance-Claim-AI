from ..rag.rag_state import State
from ...services.llm_gateway import llm
from langchain_core.messages import AIMessage
def reflection_agent(state: State):
    prompt = f"""
    You are an answer evaluation agent.
    Evaluate the generated answer against
    the retrieved context.
    Question:
    {state["question"]}
    Retrieved Context:
    {state["context"]}
    Generated Answer:
    {state["answer"]}
    Check:
    1. Is the answer relevant to the question?
    2. Is the answer supported by the context?
    3. Does the answer contain unsupported claims?
    Return exactly:
    VERDICT: PASS or FAIL
    FEEDBACK: Explanation of your evaluation.
    """
    response = llm.invoke(prompt).content
    verdict_line = next(
        (
            line for line in response.splitlines()
            if line.strip().upper().startswith("VERDICT:")
        ),
        ""
    )
    is_grounded = (
        verdict_line.split(":", 1)[-1].strip().upper() == "PASS"
    )
    attempts = state["attempts"]
    messages = []
    if is_grounded or attempts >= 2:
        messages.append(
            AIMessage(content=state["answer"])
        )
    return {
        "is_grounded": is_grounded,
        "feedback": response,
        "messages": messages
    }