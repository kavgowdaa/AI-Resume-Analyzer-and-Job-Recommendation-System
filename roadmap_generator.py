import pandas as pd


def generate_roadmap(
    role,
    detected_skills,
    job_file="data/job_roles.csv"
):
    """
    Generate missing skills and a 4-week learning roadmap.
    """

    # Load job roles
    jobs_df = pd.read_csv(job_file)

    # Remove accidental spaces
    jobs_df.columns = jobs_df.columns.str.strip()

    # Rename CSV column
    if "Job Role" in jobs_df.columns:
        jobs_df.rename(
            columns={"Job Role": "Role"},
            inplace=True
        )

    # Check required columns
    if "Role" not in jobs_df.columns:
        raise ValueError(
            f"'Role' column not found. "
            f"Available columns: {list(jobs_df.columns)}"
        )

    if "Skills" not in jobs_df.columns:
        raise ValueError(
            "'Skills' column not found in job_roles.csv."
        )

    # Find selected role
    row = jobs_df[
        jobs_df["Role"].str.strip().str.lower()
        == role.strip().lower()
    ]

    if row.empty:
        return [], {}

    # Get required skills
    required_skills = [
        skill.strip()
        for skill in row.iloc[0]["Skills"].split(",")
        if skill.strip()
    ]

    # Normalize detected skills
    detected = {
        skill.strip().lower()
        for skill in detected_skills
    }

    # Find missing skills
    missing_skills = [
        skill
        for skill in required_skills
        if skill.lower() not in detected
    ]

    # Generate 4-week roadmap
    roadmap = {}

    for i, skill in enumerate(missing_skills[:4]):
        roadmap[f"Week {i + 1}"] = (
            f"Learn and practice {skill}"
        )

    return missing_skills, roadmap