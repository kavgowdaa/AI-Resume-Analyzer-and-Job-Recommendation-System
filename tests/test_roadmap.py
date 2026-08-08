import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_parser import extract_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import recommend_jobs
from roadmap_generator import generate_roadmap

resume = extract_text("sample_resumes/sample_resume.docx")
cleaned = clean_text(resume)
skills = extract_skills(cleaned)

jobs = recommend_jobs(cleaned)

top_role = jobs.iloc[0]["Role"]

missing, roadmap = generate_roadmap(top_role, skills)

print("\nTop Role:", top_role)

print("\nMissing Skills:")
for skill in missing:
    print("-", skill)

print("\nLearning Roadmap:")
for task in roadmap:
    print(task)