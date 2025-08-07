# Candidate Recommendation App

A FastAPI and Streamlit application for matching resumes with job descriptions using AI.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Start the backend:
cd backend
uvicorn main:app --reload

3. Start the frontend
cd frontend
streamlit run app.py