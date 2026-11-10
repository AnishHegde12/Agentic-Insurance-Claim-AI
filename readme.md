# Agentic AI-Based Motor Insurance Claim Assessment

## Project Description
An Agentic AI system that automates motor insurance claim assessment using **LangChain, LangGraph, FastAPI, and RAG**.

The system processes claim documents in PDF, TXT, JSON, and PNG formats, extracts relevant information, validates it against mock insurance APIs, detects inconsistencies, calculates risk scores, and generates claim assessment reports.

It also supports Human-in-the-Loop (HITL) review and RAG-based question answering over processed claims.

## Tech Stack
- Python
- LangChain & LangGraph
- FastAPI
- Streamlit
- ChromaDB
- Pydantic
- LangSmith

## How to Run

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file and configure the required LLM API key and LangSmith settings.

### 5. Start FastAPI Backend
```bash
cd backend
uvicorn main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### 6. Start Streamlit Application

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run app.py
```

Open the URL displayed in the terminal to access the application.

## Project Workflow
1. Monitor incoming claim documents.
2. Extract and normalize claim information.
3. Validate claim completeness and backend records.
4. Perform damage and repair-cost validation.
5. Calculate claim risk scores.
6. Generate claim decisions and route cases for HITL review.
7. Generate assessment reports and index them for RAG-based Q&A.