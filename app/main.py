from .cv_ingestion import load_cv
from .cv_understanding import analyze_cv_with_gpt4o
from .matching import match_cv_to_job
from .upskilling import generate_upskilling_recommendations
from .career_roadmap import generate_career_roadmap


def extract_job_skills_from_text(job_description: str) -> dict:
    """
    Simple job skill extraction (can be upgraded later to GPT).
    """
    keywords = [
        "python",
        "sql",
        "machine learning",
        "statistics",
        "data analysis",
        "deep learning",
        "nlp",
        "tableau",
    ]

    found_skills = []
    lower_text = job_description.lower()

    for kw in keywords:
        if kw in lower_text:
            found_skills.append(kw)

    return {
        "skills": found_skills,
        "raw_text": job_description
    }


def run_pipeline(cv_file_path: str, job_description: str) -> dict:
    # 1️⃣ Load & OCR CV
    raw_cv_text = load_cv(cv_file_path)

    # 2️⃣ Understand CV with GPT
    cv_structured = analyze_cv_with_gpt4o(raw_cv_text)

    # 3️⃣ Extract job skills
    job_structured = extract_job_skills_from_text(job_description)

    # 4️⃣ Match CV to Job
    match_result = match_cv_to_job(
        cv_structured["skills"],
        job_structured["skills"]
    )

    # 5️⃣ Upskilling recommendations
    upskilling = generate_upskilling_recommendations(
        match_result["missing_skills"]
    )

    # 6️⃣ Career Roadmap (30 / 60 / 90 days)
    career_roadmap = generate_career_roadmap(
        match_result["missing_skills"]
    )

    # 7️⃣ Final response
    return {
        "cv": cv_structured,
        "job": job_structured,
        "match_result": match_result,
        "upskilling_recommendations": upskilling,
        "career_roadmap": career_roadmap
    }