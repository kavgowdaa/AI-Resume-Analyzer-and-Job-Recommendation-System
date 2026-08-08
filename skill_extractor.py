import pandas as pd
import re


def extract_skills(
    cleaned_text,
    skill_file="data/skill_dictionary.csv"
):
    """
    Extract technical skills from resume text
    using a predefined skill dictionary.
    """

    skills_df = pd.read_csv(
        skill_file,
        encoding="utf-8-sig"
    )

    # Clean column names
    skills_df.columns = (
        skills_df.columns
        .astype(str)
        .str.strip()
    )

    # Check that Skill column exists
    if "Skill" not in skills_df.columns:
        raise ValueError(
            f"'Skill' column not found. "
            f"Available columns: {list(skills_df.columns)}"
        )

    # Normalize resume text
    text = str(cleaned_text).lower()
    text = re.sub(r"\s+", " ", text)

    detected = []

    for skill in skills_df["Skill"].dropna():

        skill = str(skill).strip()

        if not skill:
            continue

        skill_lower = skill.lower()

        # Escape special regex characters
        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, text):
            detected.append(skill)

    return sorted(
        set(detected),
        key=str.lower
    )