import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_career_roadmap(missing_skills: list) -> dict:
    """
    Generate a realistic 30/60/90 day career roadmap.
    """

    prompt = f"""
You are an expert career coach.

Create a realistic 30/60/90 day roadmap to help a candidate close skill gaps.

Rules:
- Return ONLY valid JSON
- No markdown
- No generic advice
- Focus on concrete actions

JSON format:
{{
  "30_days": ["action1", "action2"],
  "60_days": ["action1", "action2"],
  "90_days": ["action1", "action2"]
}}

Missing skills:
{missing_skills}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    content = response.choices[0].message.content.strip()
    content = re.sub(r"^```json|```$", "", content).strip()

    try:
        return json.loads(content)
    except Exception:
        return {
            "error": "Invalid JSON from model",
            "raw_response": content
        }