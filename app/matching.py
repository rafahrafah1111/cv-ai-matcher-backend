from typing import List, Dict, Set


# 🧠 General skill reasoning graph (domain-agnostic)
SKILL_GRAPH = {
    "python": {
        "data preprocessing",
        "feature engineering",
        "algorithms",
        "data structures",
        "numpy",
        "pandas",
    },
    "machine learning": {
        "statistics",
        "model evaluation",
        "feature engineering",
        "data preprocessing",
    },
    "deep learning": {
        "neural networks",
        "tensorflow",
        "pytorch",
    },
    "computer vision": {
        "image processing",
        "opencv",
    },
    "nlp": {
        "text preprocessing",
        "tokenization",
        "language models",
    },
}

# 🎯 Core skills define suitability for the role
CORE_SKILLS = {
    "python",
    "machine learning",
    "deep learning",
    "data science",
    "artificial intelligence",
}

# 🧩 Optional / advanced skills (should not penalize students harshly)
OPTIONAL_SKILLS = {
    "cloud",
    "cloud platforms",
    "aws",
    "gcp",
    "azure",
    "mlops",
    "ci/cd",
    "docker",
    "kubernetes",
    "model deployment",
}

# ⚖️ Skill weights
SKILL_WEIGHTS = {
    "core": 3,
    "supporting": 2,
    "optional": 1,
}


def normalize(skill: str) -> str:
    return skill.strip().lower()


def classify_skill(skill: str) -> str:
    if skill in CORE_SKILLS:
        return "core"
    if skill in OPTIONAL_SKILLS:
        return "optional"
    return "supporting"


def extract_explicit_skills(skills: List[str]) -> Set[str]:
    return {normalize(s) for s in skills if s}


def infer_skills(explicit: Set[str], education: List[Dict]) -> Set[str]:
    """
    Infer logically connected skills based on known skills and education.
    """
    inferred = set()

    # 🔹 Skill-based inference
    for skill in explicit:
        if skill in SKILL_GRAPH:
            inferred.update(SKILL_GRAPH[skill])

    # 🔹 Education-based inference (generic & scalable)
    for edu in education:
        text = f"{edu.get('degree', '')} {edu.get('field', '')}".lower()

        if "computer science" in text:
            inferred.update({"python", "algorithms", "data structures"})
        if "data science" in text:
            inferred.update({"machine learning", "statistics"})
        if "artificial intelligence" in text:
            inferred.update({"machine learning", "deep learning"})

    return inferred - explicit


def is_student(cv: Dict) -> bool:
    experience = cv.get("experience", [])
    summary = cv.get("summary", "").lower()

    if len(experience) <= 1:
        return True

    student_terms = ["student", "intern", "junior", "undergraduate"]
    return any(term in summary for term in student_terms)


def match_cv_to_job(cv: Dict, job: Dict) -> Dict:
    explicit = extract_explicit_skills(cv.get("skills", []))
    inferred = infer_skills(explicit, cv.get("education", []))
    job_skills = {normalize(s) for s in job.get("skills", [])}

    if not job_skills:
        return {
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": [],
            "decision": "No Job Skills Provided",
            "confidence": 0.0,
        }

    student_mode = is_student(cv)

    matched = []
    missing = []

    score = 0
    max_score = 0

    core_skills_in_job = {s for s in job_skills if s in CORE_SKILLS}
    core_matched = set()

    for skill in job_skills:
        skill_type = classify_skill(skill)
        weight = SKILL_WEIGHTS[skill_type]

        # Optional skills shouldn't punish students
        if student_mode and skill_type == "optional":
            max_score += weight
            continue

        max_score += weight

        if skill in explicit:
            matched.append(skill)
            score += weight
            if skill in core_skills_in_job:
                core_matched.add(skill)

        elif skill in inferred:
            matched.append(f"{skill} (inferred)")
            score += int(weight * 0.7)
            if skill in core_skills_in_job:
                core_matched.add(skill)

        else:
            missing.append(skill)

    match_percentage = int((score / max_score) * 100) if max_score else 0

    core_coverage = (
        len(core_matched) / len(core_skills_in_job)
        if core_skills_in_job else 1
    )

    # 📊 Confidence score (0 → 1)
    confidence = round(
        (core_coverage * 0.6) + (match_percentage / 100 * 0.4),
        2
    )

    # 🧠 Decision logic (academic & fair)
    if core_coverage >= 0.6:
        decision = "Medium Match (Junior)"
    elif match_percentage >= 60:
        decision = "Medium Match"
    elif match_percentage >= 40:
        decision = "Weak Match"
    else:
        decision = "Poor Match"

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "decision": decision,
        "confidence": confidence,
        "details": {
            "explicit_skills": sorted(explicit),
            "inferred_skills": sorted(inferred),
            "core_coverage": round(core_coverage, 2),
            "student_mode": student_mode,
            "score": score,
            "max_score": max_score,
        },
    }