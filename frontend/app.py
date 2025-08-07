import streamlit as st
import requests
import json
from pathlib import Path
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API endpoint URL, defaulting to localhost if not specified in .env
API_URL = os.getenv("API_URL", "http://localhost:8000")

def main():
    """
    Main function that runs the Streamlit web application.
    
    This application:
    1. Provides a form to input job descriptions
    2. Allows uploading multiple resumes (PDF/DOCX)
    3. Sends the data to the backend API for processing
    4. Displays matched candidates with their similarity scores and AI-generated summaries
    """
    #center the title and description of the app

    st.set_page_config(page_title="Candidate Recommender", layout="wide")
    st.markdown("""
        <style>
            div[data-testid="stMarkdownContainer"] > div:first-child h1 {
                text-align: center;
            }
            div[data-testid="stMarkdownContainer"] > p {
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Candidate Recommender")
    st.markdown("Enter your job description and upload resumes to get best candidate recommendations.")

    # Job Description Input
    st.header("Job Description")
    job_description = st.text_area("Enter Job Description", height=100)

    # Multiple Resume Upload
    #st.header("Resume Upload")
    col1, col2, col3 = st.columns([8, 2, 1])
    with col1:
        st.header("Resume Upload")
    with col2:
        st.write("") 
        st.write("")
        st.write("")
       
    with col3:
        st.write("")
               
        process_clicked = st.button("Process Resumes")
    uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)

    if process_clicked and job_description and uploaded_files:
        with st.spinner("Processing resumes..."):
            try:
                # Fix file formatting for multipart/form-data
                files = [
                    ("files", (file.name, file.getvalue(), file.type)) 
                    for file in uploaded_files
                ]
                
                data = {
                    "job_description": job_description
                }

                response = requests.post(
                    url=API_URL + "/upload/",
                    files=files,
                    data=data
                )

                if response.status_code == 200:
                    results = response.json()
                    st.success(f"Successfully processed {len(uploaded_files)} resumes!")

                    # Display Results
                    st.header("Top Matching Candidates")
                    for idx, result in enumerate(results['candidates'], 1):
                        with st.expander(f"#{idx} - {result['name']} (Score: {result['similarity']})"):
                            st.write("**Match Score:**", result['similarity'])
                            st.write("**AI Summary:**")
                            st.write(result['summary'])
                            st.divider()
                else:
                    st.error(f"Error processing resumes: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error("Could not connect to the backend server. Please ensure it's running.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
           
            

if __name__ == "__main__":
    
    main()