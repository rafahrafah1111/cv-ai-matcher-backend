import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)


def analyze_cv_with_gpt4o(raw_cv_text: str):
    """
    Uses GPT to deeply analyze a CV and extract high-quality structured data.
    """

    system_prompt = """
You are a senior technical recruiter and CV analyst.

Your job:
- Read the CV carefully
- Infer missing but obvious skills (do NOT hallucinate)
- Normalize skills (e.g. "Python programming" → "Python")
- Prefer HARD SKILLS over soft skills
- Extract real experience, not fluff

Rules:
- Output ONLY valid JSON
- No markdown
- No explanations
- No trailing commas
"""

    user_prompt = f"""
Analyze the following CV text and return structured data.

Required JSON schema:
{{
  "name": "Full name if available, otherwise empty string",
  "title": "Current or most recent professional title",
  "skills": [
    "List of technical skills only (languages, frameworks, tools, concepts)"
  ],
  "experience": [
    {{
      "role": "",
      "company": "",
      "years": "",
      "highlights": ["short bullet achievements"]
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
  "summary": "1–2 sentence professional summary inferred from CV"
}}

CV TEXT:
{raw_cv_text}
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

    # Clean accidental markdown
    content = re.sub(r"^```json|```$", "", content).strip()

    try:
        parsed = json.loads(content)

        # 🧹 Safety normalization
        parsed["skills"] = sorted(
            list(set(skill.strip() for skill in parsed.get("skills", []) if skill))
        )

        return parsed

    except Exception:
        return {
            "error": "Invalid JSON from model",
            "raw_response": content
        }
