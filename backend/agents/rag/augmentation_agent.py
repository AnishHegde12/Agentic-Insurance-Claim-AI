from ..rag.rag_state import State
def augmentation_agent(state: State):
    documents = state["documents"]
    context = "\n\n".join(
        doc.page_content
        for doc in documents
    )
    feedback = state.get("feedback", "")
    augmented_prompt = f"""
    You are a RAG-based question answering assistant.
    Answer the user's question using only the
    retrieved document context.
    Retrieved Context:
    {context}
    User Question:
    {state["question"]}
    Previous Reflection Feedback:
    {feedback}
    Instructions:
    1. Use the retrieved context to answer.
    2. Do not invent information.
    3. Correct the issues mentioned in reflection feedback.
    4. If information is unavailable, mention it clearly.
    5. Give a clear and concise answer.
    """
    return {
        "context": context,
        "augmented_prompt": augmented_prompt
    }