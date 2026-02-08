from typing import List, Dict, Set
from rapidfuzz import process, fuzz


# ============================================================
# 🧠 LARGE TECH SKILL VOCABULARY
# ============================================================

KNOWN_SKILLS = {

    # Programming
    "python", "java", "c++", "c", "c#", "javascript", "typescript",
    "go", "rust", "scala", "r", "matlab", "bash",

    # AI / ML
    "machine learning", "deep learning", "reinforcement learning",
    "nlp", "computer vision", "recommendation systems",
    "neural networks", "transformer", "cnn", "rnn", "gan",
    "llm", "language models",

    # Frameworks
    "tensorflow", "pytorch", "keras", "scikit-learn",
    "xgboost", "lightgbm", "huggingface", "fastai",

    # Data Science
    "data science", "data analysis", "data mining",
    "data preprocessing", "feature engineering",
    "model evaluation", "statistics", "probability",
    "data visualization", "eda",

    # Libraries
    "numpy", "pandas", "matplotlib", "seaborn",
    "plotly", "opencv", "nltk", "spacy",

    # Big Data
    "spark", "hadoop", "kafka", "airflow",

    # Cloud
    "aws", "azure", "gcp", "cloud platforms",
    "cloud computing", "serverless", "lambda",

    # MLOps
    "mlops", "model deployment", "ci/cd",
    "docker", "kubernetes", "terraform",

    # Databases
    "sql", "postgresql", "mysql", "mongodb",
    "nosql", "redis", "data warehousing",

    # Software engineering
    "software engineering", "algorithms",
    "data structures", "design patterns",
    "microservices", "rest api",

    # AI Applications
    "speech recognition", "image processing",
    "text preprocessing", "tokenization",
    "sentiment analysis", "time series",
    "anomaly detection"
}


# ============================================================
# 🔍 SPELL CORRECTION
# ============================================================

def correct_skill(skill: str, threshold: int = 88) -> str:

    skill = skill.lower().strip()

    match = process.extractOne(skill, KNOWN_SKILLS, scorer=fuzz.ratio)

    if match and match[1] >= threshold:
        return match[0]

    return skill


# ============================================================
# 🧠 SKILL REASONING GRAPH
# ============================================================

SKILL_GRAPH = {

    "python": {
        "numpy", "pandas", "data preprocessing",
        "feature engineering", "algorithms",
        "data structures"
    },

    "machine learning": {
        "model evaluation", "statistics",
        "feature engineering", "data preprocessing"
    },

    "deep learning": {
        "neural networks", "tensorflow",
        "pytorch", "cnn", "rnn", "transformer"
    },

    "nlp": {
        "tokenization", "text preprocessing",
        "language models"
    },

    "computer vision": {
        "image processing", "opencv"
    }
}


# ============================================================
# 🎯 SKILL CLASSIFICATION
# ============================================================

CORE_SKILLS = {
    "python",
    "machine learning",
    "deep learning",
    "data science",
    "artificial intelligence"
}

OPTIONAL_SKILLS = {
    "aws", "azure", "gcp",
    "mlops", "docker",
    "kubernetes", "ci/cd",
    "model deployment"
}

SKILL_WEIGHTS = {
    "core": 3,
    "supporting": 2,
    "optional": 1,
}


# ============================================================
# 🔧 HELPERS
# ============================================================

def normalize(skill: str) -> str:
    return correct_skill(skill.strip().lower())


def classify_skill(skill: str) -> str:

    if skill in CORE_SKILLS:
        return "core"

    if skill in OPTIONAL_SKILLS:
        return "optional"

    return "supporting"


def extract_explicit_skills(skills: List[str]) -> Set[str]:
    return {normalize(s) for s in skills if s}


# ============================================================
# 🧠 INFERENCE ENGINE
# ============================================================

def infer_skills(explicit: Set[str], education: List[Dict]) -> Set[str]:

    inferred = set()

    # Skill reasoning
    for skill in explicit:
        if skill in SKILL_GRAPH:
            inferred.update(SKILL_GRAPH[skill])

    # Education reasoning
    for edu in education:

        text = f"{edu.get('degree', '')} {edu.get('field', '')}".lower()

        if "computer science" in text:
            inferred.update({"python", "algorithms", "data structures"})

        if "data science" in text:
            inferred.update({"machine learning", "statistics"})

        if "artificial intelligence" in text:
            inferred.update({"machine learning", "deep learning"})

    return inferred - explicit


# ============================================================
# 🎓 STUDENT DETECTION
# ============================================================

def is_student(cv: Dict) -> bool:

    experience = cv.get("experience", [])

    if len(experience) <= 1:
        return True

    summary = cv.get("summary", "").lower()

    return any(term in summary for term in ["student", "intern", "junior"])


# ============================================================
# 🚀 MATCH ENGINE
# ============================================================

def match_cv_to_job(cv: Dict, job: Dict) -> Dict:

    explicit = extract_explicit_skills(cv.get("skills", []))

    inferred = infer_skills(explicit, cv.get("education", []))

    job_skills = {normalize(s) for s in job.get("skills", [])}

    if not job_skills:
        return {
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": [],
            "decision": "No Job Skills",
            "confidence": 0
        }

    student_mode = is_student(cv)

    matched = []
    missing = []

    score = 0
    max_score = 0

    core_job = {s for s in job_skills if s in CORE_SKILLS}
    core_matched = set()

    for skill in job_skills:

        skill_type = classify_skill(skill)
        weight = SKILL_WEIGHTS[skill_type]

        if student_mode and skill_type == "optional":
            max_score += weight
            continue

        max_score += weight

        if skill in explicit:
            matched.append(skill)
            score += weight
            if skill in core_job:
                core_matched.add(skill)

        elif skill in inferred:
            matched.append(f"{skill} (inferred)")
            score += int(weight * 0.7)
            if skill in core_job:
                core_matched.add(skill)

        else:
            missing.append(skill)

    match_percentage = int((score / max_score) * 100) if max_score else 0

    core_coverage = (
        len(core_matched) / len(core_job)
        if core_job else 1
    )

    confidence = round(
        (core_coverage * 0.6) + (match_percentage / 100 * 0.4),
        2
    )

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
            "student_mode": student_mode
        }
    }