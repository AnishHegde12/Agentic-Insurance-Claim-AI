import os
from langgraph.checkpoint.sqlite import SqliteSaver

def get_memory():

    os.makedirs("./checkpoints", exist_ok=True)

    return SqliteSaver.from_conn_string(
        "./checkpoints/rag_memory.db"
    )