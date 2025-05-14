from utils.ocr import extract_text

with open("samples/databricks_note.docx", "rb") as f:
    f.filename = "databricks_note.docx"  # 👈 simulate Flask-style file object
    print(extract_text(f))

