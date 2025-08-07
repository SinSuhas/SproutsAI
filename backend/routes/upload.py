"""
Upload route handler for processing resume files and job descriptions.

This module provides endpoints for:
- Uploading multiple resume files (PDF/DOCX)
- Processing job descriptions
- Analyzing and ranking candidates based on job requirements
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from backend.services import file_service, similarity_service
from backend.models import AnalysisResponse

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
async def upload_and_analyze(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    """
    Process uploaded resume files and match them against a job description.
    
    This endpoint:
    1. Validates the uploaded files and job description
    2. Processes resume files to extract text content
    3. Uses AI to analyze and rank candidates based on job requirements
    4. Returns top matches with similarity scores and AI-generated summaries
    
    Args:
        files: List of resume files (PDF/DOCX format)
        job_description: Text description of the job requirements
        
    Returns:
        AnalysisResponse: Contains list of top candidates with match scores and summaries
        
    Raises:
        HTTPException: If no files provided or job description is empty
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    if not job_description:
        raise HTTPException(status_code=400, detail="Job description is required")
        
    try:
        processed_files = await file_service.process_files(files)
        if not processed_files:
            raise HTTPException(status_code=422, detail="Failed to process files")
            
        results = similarity_service.analyze_candidates(
            processed_files=processed_files,
            job_description=job_description
        )
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))