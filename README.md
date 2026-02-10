JO Match AI
Intelligent CV and Job Matching System
Project Overview

JO Match AI is an intelligent Artificial Intelligence–based system designed to analyze resumes (CVs) and job descriptions in order to evaluate candidate–job compatibility. The system leverages Natural Language Processing (NLP), skill reasoning, and AI-driven inference to provide accurate, explainable, and fair matching results.

The project aims to support students, junior candidates, and job seekers by identifying their strengths, detecting skill gaps, and generating personalized upskilling recommendations and career development guidance.

Project Objectives

The main objectives of this project are:

Automate resume analysis using AI techniques

Extract structured data from unstructured CV documents

Analyze job descriptions to identify required and optional skills

Perform intelligent skill matching using reasoning rather than keyword matching

Handle spelling errors and inconsistent skill naming in CVs

Provide fair evaluation for student and junior profiles

Generate explainable matching results and confidence scores

Recommend personalized learning paths and career roadmaps

System Architecture

The system is implemented as a modular AI pipeline with the following stages:

CV Upload and Text Extraction

AI-based CV Understanding

Job Description Skill Extraction

Intelligent Skill Matching Engine

Match Scoring and Decision Logic

Upskilling Recommendation Generator

Career Roadmap Generator

Structured JSON Output for Frontend Consumption

Each module is designed to be independent, testable, and extensible.

Technologies Used
Backend

Python

FastAPI

Uvicorn

Pydantic

Artificial Intelligence and NLP

OpenAI GPT Models

Natural Language Processing

Skill Knowledge Graph

Fuzzy String Matching (RapidFuzz)

Document Processing

PDFPlumber

OCR Utilities (Tesseract support)

Deployment

Render Cloud Platform

Core Features
1. CV Understanding Module

This module uses AI to deeply analyze CV text and extract structured information, including:

Candidate name and professional summary

Technical skills only (languages, frameworks, tools, concepts)

Education background

Work experience (roles, companies, highlights)

The system normalizes extracted skills and avoids hallucination by applying strict parsing rules.

2. Job Description Analysis

The job analysis module extracts required and optional skills from free-text job descriptions using NLP and AI reasoning.
This allows the system to adapt to different job roles without hardcoding job-specific logic.

3. Intelligent Skill Matching Engine

This is the core innovation of the project.

Instead of relying on exact keyword matching, the system applies:

Explicit Skill Matching

Skills directly listed in the CV are matched against job requirements.

Implicit Skill Inference

The system infers logically related skills using a predefined skill reasoning graph.
For example:

Python implies data preprocessing, feature engineering, and algorithms

Machine learning implies statistics and model evaluation

Fuzzy Skill Matching

The system detects and corrects misspelled technical skills such as:

transfprmer → transformer

pytroch → pytorch

This significantly improves robustness against human errors in CV writing.

4. Student-Aware Evaluation Logic

The system detects student or junior profiles based on experience and summary analysis.
Advanced industry skills (such as cloud platforms or MLOps) do not heavily penalize students, ensuring fair evaluation.

5. Weighted Skill Scoring

Skills are categorized into three groups:

Core Skills (highest weight)

Supporting Skills (medium weight)

Optional or Advanced Skills (lowest weight)

This weighted approach produces more realistic and explainable match scores.

6. Explainable AI Output

For each analysis, the system returns:

Match score (percentage)

Matching decision

Matched skills

Missing skills

Confidence score

Detailed explanation of strengths and gaps

This makes the AI decision transparent and suitable for academic evaluation.

7. Upskilling Recommendation System

Based on missing core skills, the system generates personalized learning recommendations, including:

Skill to improve

Suggested course

Learning platform

Justification for recommendation

Recommendations are limited and prioritized to avoid overwhelming the candidate.

8. Career Roadmap Generator

The system provides a structured career development roadmap based on the most important missing skills, supporting long-term growth planning.

Project Structure
app/
 ├── api.py
 ├── pipeline.py
 ├── matching.py
 ├── cv_understanding.py
 ├── job_analysis.py
 ├── upskilling.py
 ├── career_roadmap.py
 ├── cv_ingestion.py
 └── rag.py

How to Run the Project Locally
Step 1: Clone the Repository
git clone <repository-url>
cd CV_AI_MATCHER

Step 2: Create Virtual Environment
python -m venv .venv
source .venv/bin/activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Configure Environment Variables

Create a .env file and add:

OPENAI_API_KEY=your_openai_api_key

Step 5: Run the Backend Server
uvicorn app.api:app --reload

Step 6: Access API Documentation
http://127.0.0.1:8000/docs

Deployment

The backend is deployed on the Render cloud platform and supports cold start handling and CORS-enabled frontend communication.

Testing Scenarios

The system supports testing with:

Multiple CV formats

Different job descriptions

Misspelled technical skills

Student and junior profiles

AI and data-related job roles

Academic Contribution

This project demonstrates:

Practical application of Artificial Intelligence in recruitment

Explainable AI decision-making

Skill reasoning graph design

Robust NLP-based document analysis

Fair evaluation strategies for junior candidates

Author

Rafah Ziad Alnabulsy

University Project

Graduation Project
Artificial Intelligence Program

Project Status

The project is fully functional, modular, and ready for academic evaluation and future extension.

Future Improvements

Multilingual CV support

Recruiter dashboard interface

Job recommendation engine

Interview preparation assistant

Resume quality scoring