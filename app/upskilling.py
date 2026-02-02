import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_upskilling_recommendations(missing_skills: list) -> dict:
    """
    Always returns:
    {
      "courses": [ ... ]
    }
    Never returns empty if missing_skills exist.
    """

    if not missing_skills:
        return {"courses": []}

    prompt = f"""
You are a senior AI career mentor.

For EACH missing skill, recommend ONE concrete learning resource.

Rules:
- Return ONLY valid JSON
- No markdown
- No explanations
- Be realistic for STUDENTS / JUNIORS
- Prefer free or beginner-friendly resources

JSON schema (STRICT):
{{
  "courses": [
    {{
      "skill": "string",
      "recommended_course": "string",
      "platform": "Coursera | Udemy | YouTube | edX | Free",
      "reason": "short practical reason"
    }}
  ]
}}

Missing skills:
{missing_skills}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()
    content = re.sub(r"^```json|```$", "", content).strip()

    try:
        parsed = json.loads(content)

        # 🛡️ HARD SAFETY: enforce structure
        courses = parsed.get("courses", [])
        if not isinstance(courses, list):
            raise ValueError("Invalid courses format")

        return {"courses": courses}

    except Exception:
        # 🚨 FALLBACK: generate simple manual recommendations
        return {
            "courses": [
                {
                    "skill": skill,
                    "recommended_course": f"Introduction to {skill}",
                    "platform": "YouTube",
                    "reason": "Core foundational skill for the role"
                }
                for skill in missing_skills
            ]
        }
