import mimetypes
import pdfplumber
import pytesseract
from PIL import Image
from docx import Document


def load_cv(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type and "pdf" in mime_type:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text.strip()

    if mime_type and "image" in mime_type:
        return pytesseract.image_to_string(Image.open(file_path)).strip()

    if file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError("Unsupported CV format")
