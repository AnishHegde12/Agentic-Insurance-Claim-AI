from ...services.llm_gateway import llm, embedding
from ..rag.rag_state import State
from langchain_community.vectorstores import Chroma
def retrieval_agent(state:State):
    msg= state['messages']
    history="\n".join(f"{message.type}:{message.content}" for message in msg[:-1])
    question= state['question']
    if history.strip():
        prompt=f"""
        Convert the current question into a standalone
        search query using the conversation history.

        Conversation History:
        {history}

        Current Question:
        {question}

        Return only the standalone search query.
    """
        response=llm.invoke(prompt)
        search_query=response.content.strip()
    else:
        search_query=question
    db = Chroma(
        collection_name="insurance_claim_reports",
        embedding_function=embedding,
        persist_directory="./chroma_db"
    )
    retriever=db.as_retriever(search_type="similarity", search_kwargs={"k":3})
    documents=retriever.invoke(search_query)
    return {"search_query":search_query,"documents":documents}

