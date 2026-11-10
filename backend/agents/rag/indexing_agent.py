from ...services.state import State
from langchain_text_splitters import RecursiveCharacterTextSplitter
from...services.llm_gateway import embedding
from langchain_core.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
def indexing_agent(state:State):
    loader= PyPDFLoader(state['report_path'])
    document=loader.load()
    splitter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=800, separators=["\n\n", "\n", ""," "])
    chunks=splitter.split_documents(document)
    db= Chroma.from_documents(documents=chunks,
    embedding=embedding,
    persist_directory="./chroma_db",
    collection_name="insurance_claim_reports"
    )
    return {
        "indexing_status": "completed"
    }