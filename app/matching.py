from typing import List, Dict, Set
from rapidfuzz import process, fuzz


# ============================================================
# 🧠 KNOWN SKILLS
# ============================================================

KNOWN_SKILLS = {
    "artificial intelligence", "machine learning", "deep learning",
    "nlp", "computer vision", "python", "tensorflow", "pytorch",
    "statistics", "data science", "feature engineering",
    "data preprocessing", "neural networks", "opencv",
    "language models", "aws", "docker", "kubernetes"
}


# ============================================================
# 🔄 SKILL ALIASES
# ============================================================

SKILL_ALIASES = {
    "ai": "artificial intelligence",
    "ml": "machine learning"
}


# ============================================================
# 🧠 SKILL ONTOLOGY GRAPH (Bidirectional)
# ============================================================

SKILL_GRAPH = {

    "artificial intelligence": {
        "machine learning", "deep learning", "nlp", "computer vision"
    },

    "machine learning": {
        "artificial intelligence", "statistics", "feature engineering",
        "data preprocessing"
    },

    "deep learning": {
        "artificial intelligence", "neural networks",
        "tensorflow", "pytorch"
    },

    "nlp": {
        "artificial intelligence", "language models"
    },

    "computer vision": {
        "artificial intelligence", "opencv"
    }
}


# ============================================================
# 🔍 NORMALIZATION
# ============================================================

def normalize(skill: str) -> str:
    skill = skill.lower().strip()
    skill = SKILL_ALIASES.get(skill, skill)

    match = process.extractOne(skill, KNOWN_SKILLS, scorer=fuzz.ratio)

    if match and match[1] > 85:
        return match[0]

    return skill


# ============================================================
# 🔧 EXPANSION ENGINE
# ============================================================

def expand_skills(skills: Set[str]) -> Set[str]:
    expanded = set(skills)

    for skill in skills:
        if skill in SKILL_GRAPH:
            expanded.update(SKILL_GRAPH[skill])

    return expanded


# ============================================================
# 🎯 WEIGHTING
# ============================================================

CORE_SKILLS = {
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "python",
    "data science"
}

OPTIONAL_SKILLS = {
    "aws", "docker", "kubernetes"
}

WEIGHTS = {
    "core": 3,
    "supporting": 2,
    "optional": 1
}


def classify(skill):
    if skill in CORE_SKILLS:
        return "core"
    if skill in OPTIONAL_SKILLS:
        return "optional"
    return "supporting"


# ============================================================
# 🧠 SMART MATCH SCORE
# ============================================================

def similarity(a, b):
    return fuzz.token_sort_ratio(a, b) / 100


# ============================================================
# 🚀 MATCH ENGINE
# ============================================================

def match_cv_to_job(cv: Dict, job: Dict) -> Dict:

    explicit = {normalize(s) for s in cv.get("skills", [])}
    job_skills = {normalize(s) for s in job.get("skills", [])}

    expanded_cv = expand_skills(explicit)

    matched = []
    missing = []

    score = 0
    max_score = 0

    similarity_bonus = 0

    for job_skill in job_skills:

        weight = WEIGHTS[classify(job_skill)]
        max_score += weight

        # Direct match
        if job_skill in expanded_cv:
            matched.append(job_skill)
            score += weight
            continue

        # Similarity match
        best_sim = max(
            [similarity(job_skill, s) for s in expanded_cv],
            default=0
        )

        if best_sim > 0.75:
            matched.append(f"{job_skill} (similar)")
            similarity_bonus += weight * best_sim
        else:
            missing.append(job_skill)

    final_score = score + similarity_bonus

    match_percentage = int((final_score / max_score) * 100) if max_score else 0


# ============================================================
# 🎓 DECISION LOGIC (Improved)
# ============================================================

    if match_percentage >= 80:
        decision = "Strong Match"
    elif match_percentage >= 65:
        decision = "Good Match"
    elif match_percentage >= 50:
        decision = "Medium Match (Junior)"
    elif match_percentage >= 35:
        decision = "Weak Match"
    else:
        decision = "Poor Match"


# ============================================================
# 📊 CONFIDENCE SCORE
# ============================================================

    diversity = len(expanded_cv) / (len(explicit) + 1)

    confidence = round(
        (match_percentage * 0.6 / 100) +
        (diversity * 0.4),
        2
    )


    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "decision": decision,
        "confidence": confidence,
        "details": {
            "expanded_cv_skills": sorted(expanded_cv)
        }
    }