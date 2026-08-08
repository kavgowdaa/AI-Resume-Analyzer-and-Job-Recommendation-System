import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_parser import extract_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import recommend_jobs

resume_path = "sample_resumes/sample_resume.docx"

# Extract resume text
text = extract_text(resume_path)

# Clean text
cleaned = clean_text(text)

# Extract skills
skills = extract_skills(cleaned)

# Recommend jobs
results = recommend_jobs(skills)

print("\n===== TOP JOB RECOMMENDATIONS =====\n")

for _, row in results.iterrows():
    print(f"{row['Role']} : {row['Match Score']:.2f}%")