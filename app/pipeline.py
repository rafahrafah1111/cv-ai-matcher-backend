def run_pipeline(cv_file_path: str, job_description: str):
    # 1️⃣ Load CV text
    raw_cv_text = load_cv(cv_file_path)

    # 2️⃣ Analyze CV with GPT
    cv_structured = analyze_cv_with_gpt4o(raw_cv_text)

    # 3️⃣ Extract job skills
    job_structured = extract_job_skills_from_text(job_description)

    # 4️⃣ Match CV to Job
    match_result = match_cv_to_job(cv_structured, job_structured)

    # 5️⃣ Upskilling recommendations (NOW RETURNS LIST ✅)
    upskilling = generate_upskilling_recommendations(
        match_result.get("missing_skills", [])
    )

    # 6️⃣ Career roadmap
    career_roadmap = generate_career_roadmap(
        match_result.get("missing_skills", [])
    )

    # 7️⃣ Clean response for frontend
    return {
        "match_score": match_result.get("match_percentage"),
        "decision": match_result.get("decision"),
        "matched_skills": match_result.get("matched_skills"),
        "missing_skills": match_result.get("missing_skills", [])[:5],
        "upskilling": upskilling,          # 👈 بدون .get
        "career_roadmap": career_roadmap
    }