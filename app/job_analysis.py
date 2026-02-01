import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_job_skills_from_text(job_description: str) -> dict:
    prompt = f"""
You are an expert technical recruiter.

Extract skills from the job description.

Return ONLY valid JSON.

JSON format:
{{
  "skills": []
}}

Job Description:
{job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()
    content = re.sub(r"^```json|```$", "", content).strip()

    try:
        return json.loads(content)
    except Exception:
        return {
            "skills": []
        }
