from .cv_ingestion import load_cv
from .cv_understanding import analyze_cv_with_gpt4o
from .job_analysis import extract_job_skills_from_text
from .matching import match_cv_to_job
from .upskilling import generate_upskilling_recommendations
from .career_roadmap import generate_career_roadmap


def run_pipeline(cv_file_path: str, job_description: str):
    """
    Full AI pipeline:
    CV + Job Description -> Match + Upskilling + Roadmap
    """

    # 1️⃣ Load & parse CV (PDF → text)
    raw_cv_text = load_cv(cv_file_path)

    if not raw_cv_text:
        return {
            "error": "Failed to read CV file"
        }

    # 2️⃣ Analyze CV with GPT
    cv_structured = analyze_cv_with_gpt4o(raw_cv_text)

    if "error" in cv_structured:
        return {
            "error": "CV analysis failed",
            "details": cv_structured
        }

    # 3️⃣ Analyze job description with GPT
    job_structured = extract_job_skills_from_text(job_description)

    if "error" in job_structured:
        return {
            "error": "Job description analysis failed",
            "details": job_structured
        }

    # 4️⃣ Match CV to Job
    match_result = match_cv_to_job(
        cv=cv_structured,
        job=job_structured
    )

    # 5️⃣ Upskilling recommendations
    missing_skills = match_result.get("missing_skills", [])

    upskilling = generate_upskilling_recommendations(missing_skills)

    # 6️⃣ Career roadmap
    career_roadmap = generate_career_roadmap(missing_skills)

    # 7️⃣ Final clean response for frontend
    return {
        "match_score": match_result.get("match_percentage", 0),
        "decision": match_result.get("decision", ""),
        "matched_skills": match_result.get("matched_skills", []),
        "missing_skills": missing_skills[:5],  # top 5 only
        "upskilling": upskilling.get("courses", []),
        "career_roadmap": career_roadmap
    }
