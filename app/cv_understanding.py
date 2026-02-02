import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)


def analyze_cv_with_gpt4o(raw_cv_text: str) -> Dict[str, Any]:
    """
    Uses GPT to deeply analyze a CV and extract high-quality structured data.
    Always returns a safe, structured dictionary.
    """

    system_prompt = """
You are a senior technical recruiter and CV analyst.

Your job:
- Carefully read the CV
- Extract ONLY information that is clearly supported by the CV
- Infer skills ONLY if they are strongly implied by experience or education
- Normalize skills (e.g. "Python programming" -> "Python")
- Prefer hard technical skills over soft skills
- Ignore buzzwords and fluff

STRICT RULES:
- Output ONLY valid JSON
- No markdown
- No explanations
- No comments
- No trailing commas
"""

    user_prompt = f"""
Analyze the CV text below and return structured data.

Required JSON schema:
{{
  "name": "",
  "title": "",
  "skills": [],
  "experience": [
    {{
      "role": "",
      "company": "",
      "years": "",
      "highlights": []
    }}
  ],
  "education": [
    {{
      "degree": "",
      "field": "",
      "institution": "",
      "year": ""
    }}
  ],
  "summary": ""
}}

CV TEXT:
{raw_cv_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.15,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1200
    )

    content = response.choices[0].message.content.strip()

    # 🧹 Remove accidental markdown fences
    content = re.sub(r"^```json|```$", "", content).strip()

    try:
        parsed = json.loads(content)

        # ✅ Hard safety normalization (VERY IMPORTANT)
        parsed = {
            "name": parsed.get("name", "") or "",
            "title": parsed.get("title", "") or "",
            "skills": sorted(
                list(
                    set(
                        skill.strip()
                        for skill in parsed.get("skills", [])
                        if isinstance(skill, str) and skill.strip()
                    )
                )
            ),
            "experience": parsed.get("experience", []) or [],
            "education": parsed.get("education", []) or [],
            "summary": parsed.get("summary", "") or ""
        }

        return parsed

    except Exception:
        # ❗ Fail-safe response (prevents 500 errors)
        return {
            "name": "",
            "title": "",
            "skills": [],
            "experience": [],
            "education": [],
            "summary": "",
            "error": "Failed to parse CV with GPT",
            "raw_response": content
        }