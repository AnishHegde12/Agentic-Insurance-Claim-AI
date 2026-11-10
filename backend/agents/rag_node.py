from rag.rag_main import build_rag_graph
def rag_node(question:str):
    app= build_rag_graph()
    answer= app.invoke({"question":question})
    return answer['answer']
