import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _safe_json_extract(text: str):
    text = re.sub(r"^```json|```$", "", text).strip()

    try:
        return json.loads(text)
    except Exception:
        return None


def generate_upskilling_recommendations(missing_skills: list):

    if not missing_skills:
        return []

    prompt = f"""
You are an elite AI career mentor.

Recommend REAL learning paths for each missing skill.

STRICT RULES:
- Courses MUST exist online
- Include VALID working links
- Platforms allowed:
  Coursera, Udemy, edX, DeepLearning.AI, FastAI, DataCamp, YouTube
- Recommend 2 courses per skill:
    1 beginner
    1 intermediate
- Include estimated duration
- Include price type (Free / Paid)
- Include rating (approximate is fine)
- Return ONLY valid JSON
- If unsure → skip skill

JSON schema:
{{
  "skills": [
    {{
      "skill": "string",
      "learning_path": [
        {{
          "course_name": "string",
          "platform": "string",
          "level": "Beginner | Intermediate",
          "duration": "string",
          "price": "Free | Paid",
          "rating": "string",
          "link": "string",
          "reason": "short explanation"
        }}
      ]
    }}
  ]
}}

Missing skills:
{missing_skills}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content.strip()
        parsed = _safe_json_extract(content)

        if not parsed:
            raise ValueError("Invalid JSON")

        return parsed.get("skills", [])

    except Exception:

        # ⭐ fallback احترافي
        fallback = {
            "computer vision": [
                {
                    "course_name": "Introduction to Computer Vision and Image Processing",
                    "platform": "Coursera (IBM)",
                    "level": "Beginner",
                    "duration": "4 weeks",
                    "price": "Free",
                    "rating": "4.6",
                    "link": "https://www.coursera.org/learn/introduction-computer-vision-watson-opencv",
                    "reason": "Strong OpenCV and CV fundamentals"
                }
            ],
            "tensorflow": [
                {
                    "course_name": "TensorFlow in Practice Specialization",
                    "platform": "Coursera",
                    "level": "Intermediate",
                    "duration": "3 months",
                    "price": "Paid",
                    "rating": "4.7",
                    "link": "https://www.coursera.org/professional-certificates/tensorflow-in-practice",
                    "reason": "Industry TensorFlow standard"
                }
            ],
            "natural language processing": [
                {
                    "course_name": "NLP Specialization",
                    "platform": "DeepLearning.AI",
                    "level": "Intermediate",
                    "duration": "3 months",
                    "price": "Paid",
                    "rating": "4.8",
                    "link": "https://www.deeplearning.ai/courses/natural-language-processing-specialization/",
                    "reason": "Real NLP production pipelines"
                }
            ],
            "cloud ai services": [
                {
                    "course_name": "Machine Learning Specialization",
                    "platform": "DeepLearning.AI",
                    "level": "Beginner",
                    "duration": "2 months",
                    "price": "Paid",
                    "rating": "4.9",
                    "link": "https://www.deeplearning.ai/courses/machine-learning-specialization/",
                    "reason": "Covers deployment and cloud ML"
                }
            ]
        }

        results = []

        for skill in missing_skills:
            key = skill.lower()

            if key in fallback:
                results.append({
                    "skill": skill,
                    "learning_path": fallback[key]
                })
            else:
                results.append({
                    "skill": skill,
                    "learning_path": [
                        {
                            "course_name": f"Introduction to {skill}",
                            "platform": "YouTube",
                            "level": "Beginner",
                            "duration": "Variable",
                            "price": "Free",
                            "rating": "4.5",
                            "link": f"https://www.youtube.com/results?search_query={skill}+course",
                            "reason": "Starter learning resource"
                        }
                    ]
                })

        return results
