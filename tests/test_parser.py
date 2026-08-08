import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_parser import extract_text

resume_path = "sample_resumes/sample_resume.docx"

text = extract_text(resume_path)

print("\n===== EXTRACTED TEXT =====\n")
print(text)