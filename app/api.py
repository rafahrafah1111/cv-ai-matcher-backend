from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from .pipeline import run_pipeline

app = FastAPI()

# ✅ CORS مضبوط بشكل كامل (ضروري لـ Lovable + المتصفح)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 🔥 مهم جدًا
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Health check (يمنع مشاكل GET / و cold start)
@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/analyze-cv")
async def analyze_cv(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    temp_path = f"temp_{file.filename}"

    try:
        # 💾 حفظ الملف مؤقتًا
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🧠 تشغيل البايبلاين
        result = run_pipeline(
            cv_file_path=temp_path,
            job_description=job_description
        )

        return result

    finally:
        # 🧹 تنظيف الملف حتى ما يتراكم على Render
        if os.path.exists(temp_path):
            os.remove(temp_path)
