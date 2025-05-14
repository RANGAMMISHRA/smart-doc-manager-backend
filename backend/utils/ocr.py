# backend/utils/ocr.py

import pytesseract
from pdf2image import convert_from_bytes
from docx import Document
from io import BytesIO

def extract_text(file):
    filename = file.filename.lower()
    try:
        file.seek(0)  # Always reset before reading

        if filename.endswith(".pdf"):
            images = convert_from_bytes(file.read())
            text = " ".join([pytesseract.image_to_string(img) for img in images])
            print("✅ PDF Text Extracted:", text[:100])
            return text

        elif filename.endswith(".docx"):
            # ✅ Use BytesIO for Flask's file stream
            file_stream = BytesIO(file.read())
            doc = Document(file_stream)
            text = "\n".join([para.text for para in doc.paragraphs])
            print("✅ DOCX Text Extracted:", text[:100])
            return text

        elif filename.endswith(".txt"):
            text = file.read().decode("utf-8")
            print("✅ TXT Text Extracted:", text[:100])
            return text

        else:
            return "Unsupported file type"

    except Exception as e:
        print("❌ OCR error:", e)
        return ""
