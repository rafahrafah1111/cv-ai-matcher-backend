import json
import re
import os
from dotenv import load_dotenv
from openai import OpenAI

# ✅ حمّلي .env أول شيء
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print("OPENAI_API_KEY loaded:", bool(api_key))

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)


def analyze_cv_with_gpt4o(raw_cv_text: str):
    prompt = f"""
You are an AI that extracts structured data from a CV.

Return ONLY valid JSON.
Do not include explanations.
Do not include markdown.
Do not include code blocks.

JSON format:
{{
  "name": "",
  "skills": [],
  "experience": [],
  "education": [],
  "summary": ""
}}

CV TEXT:
{raw_cv_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # تنظيف لو GPT لفّ JSON
    content = re.sub(r"^```json|```$", "", content).strip()

    try:
        return json.loads(content)
    except Exception:
        return {
            "error": "Invalid JSON from model",
            "raw_response": content
        }
