from pypdf import PdfReader
from docx import Document
import os


def extract_text(file_path):
    """
    Extract text from PDF or DOCX resume.
    Returns extracted text as a string.
    """

    text = ""

    # Check file extension
    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension == ".pdf":
            reader = PdfReader(file_path)

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        elif extension == ".docx":
            document = Document(file_path)

            for paragraph in document.paragraphs:
                text += paragraph.text + "\n"

        else:
            raise ValueError("Unsupported file format. Please upload PDF or DOCX.")

        return text.strip()

    except Exception as e:
        print(f"Error: {e}")
        return ""