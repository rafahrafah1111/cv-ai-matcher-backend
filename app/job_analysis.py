def extract_job_skills_from_text(job_description: str) -> dict:
    """
    Dummy safe extractor to unblock pipeline.
    (سنرجع نذكّيه بعد ما يشتغل السيرفر)
    """
    if not job_description:
        return {"skills": []}

    text = job_description.lower()

    skills = []

    KEYWORDS = [
        "python",
        "sql",
        "machine learning",
        "data analysis",
        "statistics",
        "cybersecurity",
        "linux",
        "networking",
        "cloud",
        "aws",
        "azure",
        "docker"
    ]

    for k in KEYWORDS:
        if k in text:
            skills.append(k)

    return {"skills": skills}
