import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_jobs(
    detected_skills,
    job_file="data/job_roles.csv"
):
    """
    Calculate resume-to-job-role match scores
    using TF-IDF + skill-based matching.

    Returns all job roles sorted by Match Score.
    """

    jobs_df = pd.read_csv(job_file)

    # Clean column names
    jobs_df.columns = jobs_df.columns.str.strip()

    # Check Skills column
    if "Skills" not in jobs_df.columns:
        raise ValueError(
            "job_roles.csv must contain a 'Skills' column."
        )

    # Support different role-column names
    if "Role" not in jobs_df.columns:

        possible_role_columns = [
            "Job Role",
            "JobRole",
            "Job_Role",
            "Role Name",
            "Job"
        ]

        for column in possible_role_columns:

            if column in jobs_df.columns:

                jobs_df.rename(
                    columns={column: "Role"},
                    inplace=True
                )

                break

    if "Role" not in jobs_df.columns:

        raise ValueError(
            f"Could not find a role column. "
            f"Available columns: {list(jobs_df.columns)}"
        )

    # -----------------------------------------
    # Resume skills
    # -----------------------------------------

    detected_skills = [
        str(skill).strip()
        for skill in detected_skills
    ]

    resume_text = " ".join(detected_skills)

    # -----------------------------------------
    # TF-IDF similarity
    # -----------------------------------------

    documents = (
        [resume_text]
        + jobs_df["Skills"].fillna("").astype(str).tolist()
    )

    vectorizer = TfidfVectorizer()

    tfidf = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf[0:1],
        tfidf[1:]
    )[0]

    tfidf_scores = similarity * 100

    # -----------------------------------------
    # Skill-based matching
    # -----------------------------------------

    skill_scores = []

    resume_skills = {
        skill.lower().strip()
        for skill in detected_skills
    }

    for skills in jobs_df["Skills"].fillna(""):

        required = [
            skill.strip().lower()
            for skill in str(skills).split(",")
            if skill.strip()
        ]

        matched = len(
            set(required) & resume_skills
        )

        score = (
            matched / len(required) * 100
            if required
            else 0
        )

        skill_scores.append(score)

    # -----------------------------------------
    # Combine scores
    # -----------------------------------------

    jobs_df["TF-IDF Score"] = tfidf_scores

    jobs_df["Skill Score"] = skill_scores

    jobs_df["Match Score"] = (
        jobs_df["TF-IDF Score"] * 0.4
        + jobs_df["Skill Score"] * 0.6
    )

    jobs_df["Match Score"] = (
        jobs_df["Match Score"].round(2)
    )

    # Sort highest first
    jobs_df = jobs_df.sort_values(
        by="Match Score",
        ascending=False
    ).reset_index(drop=True)

    return jobs_df