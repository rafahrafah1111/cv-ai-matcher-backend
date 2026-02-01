def analyze_job_description(job_description: str) -> dict:
    known_skills = [
        "python", "sql", "excel", "data analysis", "machine learning",
        "nlp", "flask", "api", "statistics", "power bi", "tableau",
        "git", "cloud", "aws", "docker", "deep learning"
    ]

    text_lower = job_description.lower()

    extracted_skills = [
        skill for skill in known_skills if skill in text_lower
    ]

    return {
        "skills": extracted_skills,
        "raw_text": job_description
    }
