from typing import List, Dict, Set


# 🔹 Skill normalization map (implicit → explicit signals)
IMPLICIT_SKILL_MAP = {
    "sql": {
        "pandas",
        "numpy",
        "data analysis",
        "exploratory data analysis",
        "eda",
        "tableau",
        "database",
        "data visualization",
    },
    "statistics": {
        "data science",
        "machine learning",
        "model evaluation",
        "probability",
        "analysis",
    },
    "machine learning": {
        "scikit-learn",
        "sklearn",
        "model training",
        "classification",
        "regression",
        "ml",
    },
}


def normalize_skill(skill: str) -> str:
    """Normalize skill text for matching"""
    return skill.strip().lower()


def extract_explicit_skills(cv_skills: List[str]) -> Set[str]:
    """Extract normalized explicit skills from CV"""
    return {normalize_skill(skill) for skill in cv_skills if skill}


def infer_skills(
    explicit_skills: Set[str],
    education: List[Dict]
) -> Set[str]:
    """
    Infer implicit skills from explicit skills and education
    """
    inferred = set()

    # 🔹 Infer from explicit skills
    for target_skill, indicators in IMPLICIT_SKILL_MAP.items():
        if explicit_skills.intersection(indicators):
            inferred.add(target_skill)

    # 🔹 Infer from education
    for edu in education:
        degree = normalize_skill(edu.get("degree", ""))
        field = normalize_skill(edu.get("field", ""))

        combined = degree + " " + field

        if "data science" in combined:
            inferred.update({"statistics", "sql"})
        if "computer science" in combined:
            inferred.update({"python", "algorithms"})
        if "artificial intelligence" in combined:
            inferred.add("machine learning")

    return inferred


def match_cv_to_job(cv: Dict, job: Dict) -> Dict:
    """
    Match CV against job description using weighted explicit + inferred skills
    """
    cv_skills = cv.get("skills", [])
    education = cv.get("education", [])
    job_skills = job.get("skills", [])

    if not job_skills:
        return {
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": [],
            "decision": "No Job Skills Provided"
        }

    explicit_skills = extract_explicit_skills(cv_skills)
    inferred_skills = infer_skills(explicit_skills, education)

    normalized_job_skills = {normalize_skill(skill) for skill in job_skills}

    matched = []
    missing = []

    score = 0
    max_score = len(normalized_job_skills) * 2  # explicit = 2 points

    for skill in normalized_job_skills:
        if skill in explicit_skills:
            matched.append(skill)
            score += 2
        elif skill in inferred_skills:
            matched.append(f"{skill} (inferred)")
            score += 1
        else:
            missing.append(skill)

    match_percentage = int((score / max_score) * 100)

    # 🧠 Smarter decision logic
    if match_percentage >= 80:
        decision = "Strong Match"
    elif match_percentage >= 50:
        decision = "Medium Match"
    else:
        decision = "Weak Match"

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "decision": decision,
        "details": {
            "explicit_skills_used": sorted(explicit_skills),
            "inferred_skills_used": sorted(inferred_skills),
            "scoring": {
                "score": score,
                "max_score": max_score
            }
        }
    }