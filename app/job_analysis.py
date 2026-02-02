import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_job_skills_from_text(job_text: str) -> dict:
    """
    Extracts normalized hard skills from a job description.
    """

    system_prompt = """
You are a senior technical recruiter.

Your task:
- Extract ONLY hard/technical skills from the job description
- Ignore soft skills, buzzwords, and generic phrases
- Normalize skills (e.g. "Python programming" → "Python")
- Do NOT hallucinate skills not mentioned or clearly implied

Rules:
- Output ONLY valid JSON
- No explanations
- No markdown
"""

    user_prompt = f"""
Analyze the following job description.

Return JSON in this exact format:
{{
  "title": "",
  "skills": [
    "python",
    "sql",
    "machine learning"
  ]
}}

Job Description:
{job_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    content = response.choices[0].message.content.strip()
    content = re.sub(r"^```json|```$", "", content).strip()

    try:
        parsed = json.loads(content)

        parsed["skills"] = sorted(
            list(set(skill.strip().lower() for skill in parsed.get("skills", []) if skill))
        )

        return parsed

    except Exception:
        return {
            "title": "",
            "skills": [],
            "error": "Failed to parse job description",
            "raw_response": content
        }