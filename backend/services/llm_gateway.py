from langchain_cohere import ChatCohere, CohereEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()
llm= ChatCohere(
    api_key= os.getenv("API_KEY"),
    model= os.getenv("FOUNDATION_MODEL"),
    temperature=0.7
    )
embedding= CohereEmbeddings(
    api_key= os.getenv("API_KEY"),
    model= os.getenv("EMBEDDING_MODEL")
)
