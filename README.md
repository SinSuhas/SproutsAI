# Candidate Recommendation App

Streamlit URL : https://recommendcandidate.streamlit.app/

# AI-Powered Resume Screening System

**Note:**
1. **Huggingface Token required for AI Summary generation**
2. Backend is deployed on AWS EC2 t2.micro instance and the computation is very slow. Recommend running the app on local
3. Sample resumes and sample Job Description have been provided in data/temp folder. 


## Overview

This system provides an automated solution for screening and ranking job candidates based on resume content and job descriptions. It uses advanced natural language processing and machine learning techniques to analyze resumes, calculate semantic similarity with job requirements, and generate AI-powered summaries for each candidate.

## Architecture & Approach

### Core Components

1. **File Processing Service** (`file_service.py`)
   - Handles multiple file format support (PDF, DOCX)
   - Extracts text content using specialized libraries
   - Manages temporary file operations safely

2. **Similarity Analysis Service** (`similarity_service.py`)
   - Generates semantic embeddings using transformer models
   - Calculates cosine similarity between job descriptions and resumes
   - Provides AI-powered candidate summaries

3. **Upload Handler** (`upload.py`)
   - FastAPI endpoint for file uploads and job description input
   - Orchestrates the analysis pipeline
   - Returns structured results with top candidates

### Technical Approach

#### Semantic Similarity Matching
- **Embedding Model**: BAAI/bge-small-en-v1.5 (BGE - Beijing Academy of Artificial Intelligence)
- **Similarity Metric**: Cosine similarity between normalized embeddings
- **Ranking Strategy**: Top 5 candidates by similarity score

#### Text Processing Pipeline
1. **Document Loading**: 
   - PDF: pdfplumber for robust text extraction
   - DOCX: Docx2txtLoader from LangChain community
2. **Embedding Generation**: Sentence-level semantic representations
3. **Similarity Calculation**: Vector space comparison using cosine similarity
4. **AI Summarization**: LLM-powered candidate analysis

## Key Assumptions

### Technical Assumptions

1. **File Format Support**
   - Only PDF and DOCX formats are supported
   - Files contain extractable text (not image-based PDFs)
   - Resume content is in English

2. **Model Selection**
   - BGE-small-en-v1.5 provides optimal balance of performance and speed
   - Cosine similarity is sufficient for ranking candidates
   - Normalized embeddings ensure consistent similarity scores

3. **Processing Limitations**
   - Maximum file size limits are handled by FastAPI defaults
   - Temporary file system has sufficient space for processing
   - Network connectivity available for model downloads

### Business Assumptions

1. **Candidate Ranking**
   - Top 5 candidates provide sufficient screening results
   - Semantic similarity correlates with job fit
   - Resume content accurately represents candidate capabilities

2. **Job Description Quality**
   - Job descriptions contain sufficient detail for meaningful comparison
   - Requirements are clearly articulated in natural language
   - Job descriptions are comprehensive and not just bullet points

3. **Resume Standards**
   - Resumes follow standard formatting conventions
   - Relevant experience and skills are explicitly mentioned
   - Candidate names can be inferred from filenames

## System Features

### Strengths
- **Multi-format Support**: Handles both PDF and DOCX files seamlessly
- **Semantic Understanding**: Goes beyond keyword matching to understand context and meaning
- **AI-Powered Insights**: Provides detailed summaries explaining candidate fit
- **Scalable Architecture**: Asynchronous processing supports multiple file uploads
- **Error Handling**: Robust exception management and fallback mechanisms

### Limitations
- **File Format Restrictions**: Limited to PDF and DOCX formats
- **Model Dependency**: Requires internet connection for initial model download
- **Processing Time**: Large files or many candidates may impact response time

## Configuration Requirements

### Environment Variables
```bash
HUGGING_FACE_API_BASE=<HuggingFace API endpoint>
HF_API_KEY=<HuggingFace API key>
```

### Dependencies
- `sentence-transformers`: For embedding generation
- `pdfplumber`: PDF text extraction
- `langchain-community`: DOCX processing
- `openai`: AI summary generation
- `fastapi`: Web framework
- `numpy`: Numerical computations

## Usage Workflow

1. **Upload**: Submit resume files (PDF/DOCX) and job description
2. **Processing**: System extracts text from all resume files
3. **Analysis**: Generates embeddings and calculates similarity scores
4. **Ranking**: Sorts candidates by relevance to job requirements
5. **Summarization**: Creates AI-powered insights for each top candidate
6. **Results**: Returns top 5 matches with scores and summaries

## Performance Considerations

- **Caching**: Models are cached locally to improve subsequent processing speed
- **Batch Processing**: Multiple files processed in sequence for memory efficiency
- **Temporary File Management**: Automatic cleanup prevents disk space issues
- **Error Resilience**: Individual file processing failures don't affect other candidates


## Security Considerations

- Temporary files are automatically cleaned up after processing
- No permanent storage of uploaded resume content
- API key management for external service integration
- Input validation and sanitization for job descriptions

This system provides a foundation for AI-powered recruitment screening while maintaining flexibility for future enhancements and customizations.

## Setup on local

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
