# app/career_roadmap.py

ROADMAP_LIBRARY = {
    "sql": {
        "30": [
            "Learn SQL basics (SELECT, WHERE, ORDER BY)",
            "Practice queries on sample datasets"
        ],
        "60": [
            "Learn JOINs, GROUP BY, subqueries",
            "Build a small SQL project"
        ],
        "90": [
            "Use SQL with Python (pandas)",
            "Prepare SQL interview questions"
        ]
    },
    "statistics": {
        "30": [
            "Review mean, median, variance",
            "Understand probability basics"
        ],
        "60": [
            "Learn hypothesis testing",
            "Apply statistics in data analysis"
        ],
        "90": [
            "Use statistics in ML evaluation",
            "Prepare statistics interview questions"
        ]
    },
    "machine learning": {
        "30": [
            "Revise supervised vs unsupervised learning"
        ],
        "60": [
            "Build ML project using scikit-learn"
        ],
        "90": [
            "Optimize models and tune hyperparameters"
        ]
    }
}


def generate_career_roadmap(missing_skills: list) -> dict:
    roadmap = {
        "30_days": [],
        "60_days": [],
        "90_days": []
    }

    for skill in missing_skills:
        key = skill.lower()

        if key in ROADMAP_LIBRARY:
            roadmap["30_days"].extend(ROADMAP_LIBRARY[key]["30"])
            roadmap["60_days"].extend(ROADMAP_LIBRARY[key]["60"])
            roadmap["90_days"].extend(ROADMAP_LIBRARY[key]["90"])
        else:
            roadmap["30_days"].append(f"Learn fundamentals of {skill}")
            roadmap["60_days"].append(f"Apply {skill} in a small project")
            roadmap["90_days"].append(f"Use {skill} professionally and apply for jobs")

    return roadmap
