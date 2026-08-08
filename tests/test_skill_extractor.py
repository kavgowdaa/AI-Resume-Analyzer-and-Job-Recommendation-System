import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_parser import extract_text
from text_cleaner import clean_text
from skill_extractor import extract_skills

resume_path = "sample_resumes/sample_resume.docx"

text = extract_text(resume_path)
cleaned = clean_text(text)

skills = extract_skills(cleaned)

print("\n===== DETECTED SKILLS =====\n")

for skill in skills:
    print("✓", skill)