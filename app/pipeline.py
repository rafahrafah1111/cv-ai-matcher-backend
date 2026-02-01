def run_pipeline(cv_file_path: str, job_description: str):
    # 1️⃣ Load CV text
    raw_cv_text = load_cv(cv_file_path)

    if not raw_cv_text:
        raise ValueError("Failed to extract text from CV")

    # 2️⃣ Analyze CV with GPT
    cv_structured = analyze_cv_with_gpt4o(raw_cv_text)

    if not isinstance(cv_structured, dict):
        raise ValueError("CV analysis failed")

    # 3️⃣ Extract job skills
    job_structured = extract_job_skills_from_text(job_description)

    if not isinstance(job_structured, dict):
        raise ValueError("Job analysis failed")

    # 4️⃣ Match CV to Job
    match_result = match_cv_to_job(cv_structured, job_structured)

    # 5️⃣ Upskilling recommendations (RETURNS LIST ✅)
    upskilling = generate_upskilling_recommendations(
        match_result.get("missing_skills", [])
    )

    # 6️⃣ Career roadmap
    career_roadmap = generate_career_roadmap(
        match_result.get("missing_skills", [])
    )

    # 7️⃣ Final clean response for frontend
    return {
        "match_score": match_result.get("match_percentage", 0),
        "decision": match_result.get("decision", "Unknown"),
        "matched_skills": match_result.get("matched_skills", []),
        "missing_skills": match_result.get("missing_skills", [])[:5],
        "upskilling": upskilling if isinstance(upskilling, list) else [],
        "career_roadmap": career_roadmap if career_roadmap else []
    }
