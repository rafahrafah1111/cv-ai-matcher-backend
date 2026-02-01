# app/upskilling.py

UPSKILLING_CATALOG = {
    "sql": {
        "level": "Beginner",
        "resources": [
            {
                "title": "SQL for Data Science (Coursera)",
                "type": "Course",
                "url": "https://www.coursera.org/learn/sql-for-data-science"
            },
            {
                "title": "W3Schools SQL Tutorial",
                "type": "Tutorial",
                "url": "https://www.w3schools.com/sql/"
            }
        ]
    },
    "statistics": {
        "level": "Beginner",
        "resources": [
            {
                "title": "Statistics for Data Science (Khan Academy)",
                "type": "Course",
                "url": "https://www.khanacademy.org/math/statistics-probability"
            },
            {
                "title": "StatQuest with Josh Starmer",
                "type": "YouTube",
                "url": "https://www.youtube.com/@statquest"
            }
        ]
    },
    "machine learning": {
        "level": "Intermediate",
        "resources": [
            {
                "title": "Machine Learning by Andrew Ng",
                "type": "Course",
                "url": "https://www.coursera.org/learn/machine-learning"
            }
        ]
    },
    "python": {
        "level": "Beginner",
        "resources": [
            {
                "title": "Python for Everybody",
                "type": "Course",
                "url": "https://www.coursera.org/specializations/python"
            }
        ]
    }
}


def generate_upskilling_recommendations(missing_skills: list) -> list:
    recommendations = []

    for skill in missing_skills:
        skill_key = skill.lower()

        if skill_key in UPSKILLING_CATALOG:
            data = UPSKILLING_CATALOG[skill_key]

            recommendations.append({
                "skill": skill.title(),
                "recommended_level": data["level"],
                "resources": data["resources"]
            })
        else:
            # fallback لو مهارة مش موجودة بالكتالوج
            recommendations.append({
                "skill": skill.title(),
                "recommended_level": "Unknown",
                "resources": []
            })

    return recommendations
