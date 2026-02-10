from .cv_ingestion import load_cv
from .cv_understanding import analyze_cv_with_gpt4o
from .job_analysis import extract_job_skills_from_text
from .matching import match_cv_to_job
from .upskilling import generate_upskilling_recommendations
from .career_roadmap import generate_career_roadmap


def run_pipeline(cv_file_path: str, job_description: str):
    """
    Full CV → Job matching pipeline.
    Returns stable, explainable, student-aware results.
    """

    try:
        # 1️⃣ Load CV text
        raw_cv_text = load_cv(cv_file_path)
        if not raw_cv_text:
            raise ValueError("Failed to extract text from CV")

        # 2️⃣ Analyze CV with GPT
        cv_structured = analyze_cv_with_gpt4o(raw_cv_text)
        if not isinstance(cv_structured, dict):
            raise ValueError("CV analysis failed")

        # 3️⃣ Analyze job description
        job_structured = extract_job_skills_from_text(job_description)
        if not isinstance(job_structured, dict):
            raise ValueError("Job analysis failed")

        # 4️⃣ Match CV to Job
        match_result = match_cv_to_job(cv_structured, job_structured)
        if not isinstance(match_result, dict):
            raise ValueError("Matching failed")

        missing_skills = match_result.get("missing_skills", [])
        matched_skills = match_result.get("matched_skills", [])

        # 🧠 5️⃣ SMART UPSKILLING SELECTION
        CORE_UPSKILL = {
            "deep learning",
            "machine learning",
            "data preprocessing",
            "feature engineering",
            "computer vision",
            "nlp",
            "statistics",
        }

        OPTIONAL_UPSKILL = {
            "cloud",
            "cloud platforms",
            "mlops",
            "ci/cd",
            "model deployment",
            "docker",
            "kubernetes",
        }

        # Pick core gaps first
        upskill_targets = [s for s in missing_skills if s in CORE_UPSKILL]

        # Limit to max 3 core skills
        upskill_targets = upskill_targets[:3]

        # If still less than 3, add ONE optional skill only
        if len(upskill_targets) < 3:
            optional = [s for s in missing_skills if s in OPTIONAL_UPSKILL]
            if optional:
                upskill_targets.append(optional[0])

        # 6️⃣ Generate upskilling recommendations ✅ FIXED
        upskilling_courses = generate_upskilling_recommendations(upskill_targets)

        # 7️⃣ Career roadmap
        career_roadmap = generate_career_roadmap(upskill_targets)
        if not isinstance(career_roadmap, list):
            career_roadmap = []

        # 🧠 8️⃣ Explainability
        explanation = {
            "strengths": matched_skills[:5],
            "main_gaps": missing_skills[:3],
            "summary": (
                "Candidate demonstrates strong core AI foundations suitable for a junior role."
                if "Junior" in match_result.get("decision", "")
                else "Candidate partially meets the role requirements and would benefit from targeted upskilling."
            ),
        }

        # 9️⃣ Final response
        return {
            "match_score": match_result.get("match_percentage", 0),
            "decision": match_result.get("decision", "Unknown"),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "upskilling": upskilling_courses,
            "career_roadmap": career_roadmap,
            "explanation": explanation,
        }

    except Exception as e:
        return {
            "match_score": 0,
            "decision": "Error",
            "matched_skills": [],
            "missing_skills": [],
            "upskilling": [],
            "career_roadmap": [],
            "explanation": {},
            "error": str(e),
        }