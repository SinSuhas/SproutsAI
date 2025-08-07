import os
from typing import List, Dict
import io
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from tempfile import NamedTemporaryFile

class FileService:
    """
    A service that handles file processing operations for resume files.
    
    This service provides functionality to:
    - Process multiple resume files asynchronously
    - Extract text content from PDF and DOCX files
    - Handle temporary file operations safely
    """
    
    async def process_files(self, files: List[UploadFile]) -> List[Dict]:
        """
        Process a list of uploaded resume files and extract their text content.
        
        Args:
            files (List[UploadFile]): List of FastAPI UploadFile objects containing resumes
            
        Returns:
            List[Dict]: List of dictionaries containing filename and extracted text content
        """
        results = []
        for file in files:
            content = await file.read()
            text = await self._extract_text(file.filename, content)
            results.append({
                "filename": file.filename,
                "content": text
            })
        return results
    
    async def _extract_text(self, filename: str, content: bytes) -> str:
        """
        Extract text content from a file using appropriate document loader.
        
        This method:
        1. Creates a temporary file from the uploaded content
        2. Uses pdfplumber for PDF files and Docx2txtLoader for DOCX files
        3. Extracts and returns the text content
        4. Handles cleanup of temporary files
        
        Args:
            filename (str): Name of the uploaded file
            content (bytes): Binary content of the file
            
        Returns:
            str: Extracted text content from the file
        """
        # Create a temporary file to store the content
        with NamedTemporaryFile(delete=False, suffix=self._get_suffix(filename)) as temp_file:
            temp_file.write(content)
            temp_file.flush()
            
            try:
                if filename.lower().endswith('.pdf'):
                    #loader = PyPDFLoader(temp_file.name)
                    #pages = loader.load()
                    #return "\n".join(page.page_content for page in pages)
                    import pdfplumber
                    with pdfplumber.open(temp_file.name) as pdf:
                        text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                    return text
                    
                elif filename.lower().endswith('.docx'):
                    loader = Docx2txtLoader(temp_file.name)
                    pages = loader.load()
                    return "\n".join(page.page_content for page in pages)
                    
                return ""
                
            except Exception as e:
                print(f"Error extracting text from {filename}: {str(e)}")
                return ""
            
            finally:
                temp_file.close()
                os.unlink(temp_file.name)  # Delete the temporary file
            
    def _get_suffix(self, filename: str) -> str:
        if filename.lower().endswith('.pdf'):
            return '.pdf'
        elif filename.lower().endswith('.docx'):
            return '.docx'
        return ''

file_service = FileService()