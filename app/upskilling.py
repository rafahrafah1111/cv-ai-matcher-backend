import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_upskilling_recommendations(missing_skills: list) -> list:
    """
    Generate concrete upskilling recommendations for missing skills.
    """

    if not missing_skills:
        return []

    prompt = f"""
You are a senior career mentor.

Based on the missing skills below, recommend practical learning resources.

Rules:
- Return ONLY valid JSON
- No explanations
- No markdown
- Be concise and practical

JSON format:
[
  {{
    "skill": "",
    "recommended_course": "",
    "platform": "",
    "reason": ""
  }}
]

Missing skills:
{missing_skills}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()
    content = re.sub(r"^```json|```$", "", content).strip()

    try:
        return json.loads(content)
    except Exception:
        return []
