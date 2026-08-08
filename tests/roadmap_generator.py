import pandas as pd


def generate_roadmap(top_role, detected_skills):
    """
    Generate missing skills and a 4-week learning roadmap.
    """

    # Load job roles
    jobs = pd.read_csv("data/job_roles.csv")

    # Clean column names
    jobs.columns = jobs.columns.str.strip()

    # Convert "Job Role" to "Role"
    if "Job Role" in jobs.columns:
        jobs.rename(
            columns={"Job Role": "Role"},
            inplace=True
        )

    # Find selected role
    row = jobs[
        jobs["Role"].str.strip().str.lower()
        == top_role.strip().lower()
    ]

    if row.empty:
        return [], {}

    # Required skills for the role
    required = row.iloc[0]["Skills"].split(",")

    required = [
        skill.strip()
        for skill in required
        if skill.strip()
    ]

    # Normalize detected skills
    detected = {
        skill.strip().lower()
        for skill in detected_skills
    }

    # Find missing skills
    missing = [
        skill
        for skill in required
        if skill.lower() not in detected
    ]

    # Generate 4-week roadmap
    roadmap = {}

    for i, skill in enumerate(missing[:4]):
        roadmap[f"Week {i + 1}"] = (
            f"Learn and practice {skill}"
        )

    return missing, roadmap