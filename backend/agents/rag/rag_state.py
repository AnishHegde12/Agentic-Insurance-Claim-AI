from typing import TypedDict, List, Annotated
from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    question: str
    search_query: str
    documents: List[Document]
    context: str
    augmented_prompt: str
    answer: str
    feedback: str
    is_grounded: bool
    attempts: int