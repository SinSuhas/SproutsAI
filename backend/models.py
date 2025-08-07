from pydantic import BaseModel
from typing import List, Dict, Optional

class ResumeContent(BaseModel):
    filename: str
    content: str

class CandidateResult(BaseModel):
    name: str
    similarity: float
    summary: str

class AnalysisRequest(BaseModel):
    job_description: str
    resume_texts: List[ResumeContent]

class AnalysisResponse(BaseModel):
    candidates: List[CandidateResult]

