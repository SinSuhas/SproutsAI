from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from pathlib import Path
import os
import requests
from openai import OpenAI

class SimilarityService:
    """
    A service that handles resume-to-job matching using AI embeddings and similarity calculations.
    
    This service uses the BAAI/bge-small-en-v1.5 model for generating text embeddings and compares
    resumes with job descriptions. It provides methods for:
    - Generating embeddings from text
    - Calculating similarity between embeddings
    - Analyzing candidates by comparing their resumes to job descriptions
    - Generating AI-powered summaries of candidate matches
    """
    def __init__(self):
        cache_dir = Path("data/cache/models")
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize the model using sentence-transformers
        self.model_name = "BAAI/bge-small-en-v1.5"#'infgrad/stella-base-en-v5' #'sentence-transformers/all-MiniLM-L6-v2'
        self.model = SentenceTransformer(self.model_name, cache_folder=str(cache_dir))
        
    def get_embedding(self, text: str) -> np.ndarray:
        """
        Generate an embedding vector for the input text using the sentence transformer model.
        
        Args:
            text (str): The input text to generate embeddings for
            
        Returns:
            np.ndarray: A normalized embedding vector representing the semantic meaning of the text
        """
        return self.model.encode(text, normalize_embeddings=True)

    def calculate_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        Calculate the cosine similarity between two embedding vectors.
        
        Args:
            emb1 (np.ndarray): First embedding vector
            emb2 (np.ndarray): Second embedding vector
            
        Returns:
            float: Cosine similarity score between 0 and 1, where 1 means perfect similarity
        """
        
        # Calculate cosine similarity between the two embeddings
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))

    def analyze_candidates(self, processed_files: List[Dict], job_description: str):
        """
        Analyze a list of candidate resumes against a job description.
        
        This method:
        1. Generates embeddings for the job description
        2. Processes each resume and generates its embedding
        3. Calculates similarity scores between job and resume embeddings
        4. Generates AI summaries for each candidate
        5. Returns top 5 candidates sorted by similarity score
        
        Args:
            processed_files (List[Dict]): List of dictionaries containing resume file data
            job_description (str): The job description to match against
            
        Returns:
            Dict: Contains a 'candidates' key with a list of top 5 matches, each with name, 
                 similarity score, and AI-generated summary
        """
        # Generate job description embedding
        job_embedding = self.get_embedding(job_description)
        print(f"Job description: {job_description[:100]}...") #DEBUG
        # Process each resume
        results = []
        for file in processed_files:
            resume_text = file["content"]

            # DEBUG: Print actual resume content
            print(f"File: {file['filename']}")
            print(f"Content length: {len(resume_text)}")
            print(f"Content preview: {resume_text[:200]}...")
            print("---")

            resume_embedding = self.get_embedding(resume_text)
            
            similarity_score = self.calculate_similarity(job_embedding, resume_embedding)
            
            results.append({
                "name": file["filename"],
                "similarity": float(similarity_score),
                "summary": self._generate_summary(resume_text, job_description)
            })
        
        # Sort by similarity score
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return {"candidates": results[:5]}
    
    def _generate_summary(self, resume_text: str, job_description: str) -> str:      
        try:
            prompt = (
                "You are an expert HR recruiter. Given the following job description and candidate resume, "
                "write a concise 2-3 sentence summary focusing on the candidate's strongest matches to the requirements"
                " and highlight these matches in your summary. Provide your summary in the form of bullet points."
                "If the candidate does not match the requirements, provide a brief explanation as to why he or she is not a good fit.\n\n"
                f"Job Description:\n{job_description}...\n\n"
                f"Candidate Resume:\n{resume_text}...\n"
            )
            
            client = OpenAI(
            base_url=os.getenv("HUGGING_FACE_API_BASE"),  
            api_key=os.getenv("HF_API_KEY")    
            )
            response = client.chat.completions.create(
                model="Qwen/Qwen3-Coder-30B-A3B-Instruct:fireworks-ai",
                messages=[{"role": "user", "content": prompt}],
                
            )
            return response.choices[0].message.content 
        except Exception as e:
            print(f"Summary generation failed: {e}")
            return "Summary could not be generated due to an internal error."

        

similarity_service = SimilarityService()