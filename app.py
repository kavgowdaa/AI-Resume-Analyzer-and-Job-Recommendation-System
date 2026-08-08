import streamlit as st
import tempfile
import pandas as pd
import os
import plotly.express as px

from resume_parser import extract_text
from text_cleaner import clean_text
from skill_extractor import extract_skills
from job_matcher import recommend_jobs
from roadmap_generator import generate_roadmap


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title(
    "📄 AI Resume Analyzer and Job Recommendation System"
)

st.write(
    "Upload your resume to analyze your skills, "
    "find suitable job roles, identify skill gaps, "
    "and generate a learning roadmap."
)

st.info(
    "ℹ️ Match scores are estimates based on job-related skills. "
    "They should not be considered hiring or rejection decisions."
)


# =========================================================
# RESUME UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "📤 Upload your Resume (PDF/DOCX)",
    type=["pdf", "docx"]
)

MAX_FILE_SIZE = 4.5 * 1024 * 1024


# =========================================================
# PROCESS RESUME
# =========================================================

if uploaded_file is not None:

    # -----------------------------------------------------
    # File size validation
    # -----------------------------------------------------

    if uploaded_file.size > MAX_FILE_SIZE:

        st.error(
            "❌ File is too large. "
            "Please upload a resume smaller than 4.5 MB."
        )

        st.stop()

    temp_path = None

    # -----------------------------------------------------
    # Save temporary file
    # -----------------------------------------------------

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(
            uploaded_file.name
        )[1]
    ) as tmp:

        tmp.write(uploaded_file.getvalue())
        temp_path = tmp.name

    try:

        # =================================================
        # 1. RESUME PARSING
        # =================================================

        resume_text = extract_text(temp_path)

        if not resume_text or not resume_text.strip():

            st.error(
                "❌ Could not extract text from the uploaded resume."
            )

            st.stop()

        # =================================================
        # 2. TEXT CLEANING
        # =================================================

        cleaned_text = clean_text(resume_text)

        # =================================================
        # 3. SKILL EXTRACTION
        # =================================================

        skills = extract_skills(cleaned_text)

        # =================================================
        # 4. JOB MATCHING
        # =================================================

        all_jobs = recommend_jobs(skills)

        if all_jobs is None or all_jobs.empty:

            st.warning(
                "⚠️ No suitable job roles were found."
            )

            st.stop()

        # Top 3 recommendations
        top_jobs = all_jobs.head(3).copy()

        st.success(
            "✅ Resume analyzed successfully!"
        )

        # =================================================
        # RESUME INFORMATION
        # =================================================

        st.subheader("📄 Resume Information")

        st.write(
            f"**Uploaded File:** {uploaded_file.name}"
        )

        # =================================================
        # SUMMARY METRICS
        # =================================================

        st.subheader(
            "📊 Resume Analysis Overview"
        )

        best_role = all_jobs.iloc[0]["Role"]

        best_score = float(
            all_jobs.iloc[0]["Match Score"]
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🛠 Skills Detected",
                len(skills)
            )

        with col2:

            st.metric(
                "💼 Roles Analyzed",
                len(all_jobs)
            )

        with col3:

            st.metric(
                "🏆 Best Match",
                best_role
            )

        with col4:

            st.metric(
                "🎯 Match Score",
                f"{best_score:.2f}%"
            )

        # =================================================
        # DETECTED SKILLS
        # =================================================

        st.header("🛠 Detected Skills")

        if skills:

            skill_columns = st.columns(4)

            for index, skill in enumerate(skills):

                with skill_columns[
                    index % 4
                ]:

                    st.success(skill)

        else:

            st.warning(
                "⚠️ No technical skills were detected."
            )

        # =================================================
        # TOP 3 JOB RECOMMENDATIONS
        # =================================================

        st.header(
            "💼 Top Job Recommendations"
        )

        for _, row in top_jobs.iterrows():

            role = row["Role"]

            score = float(
                row["Match Score"]
            )

            st.subheader(role)

            st.progress(
                min(int(score), 100)
            )

            st.write(
                f"**Match Score:** {score:.2f}%"
            )

        # =================================================
        # MATCH SCORE CHART
        # =================================================

        st.header(
            "📊 Job Match Score Comparison"
        )

        chart_data = top_jobs[
            ["Role", "Match Score"]
        ].copy()

        chart_data = chart_data.sort_values(
            by="Match Score",
            ascending=True
        )

        fig = px.bar(
            chart_data,
            x="Match Score",
            y="Role",
            orientation="h",
            text="Match Score",
            title="Top 3 Resume-to-Job Role Match"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig.update_layout(
            xaxis_title="Match Score (%)",
            yaxis_title="Job Role",
            xaxis_range=[0, 100],
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =================================================
        # TARGET ROLE SELECTION
        # =================================================

        st.header(
            "🎯 Select Target Role"
        )

        available_roles = (
            all_jobs["Role"]
            .dropna()
            .tolist()
        )

        default_index = (
            available_roles.index(best_role)
            if best_role in available_roles
            else 0
        )

        selected_role = st.selectbox(
            "Choose a role to analyze your skill gap:",
            available_roles,
            index=default_index
        )

        # =================================================
        # SELECTED ROLE SCORE
        # =================================================

        selected_row = all_jobs[
            all_jobs["Role"] == selected_role
        ]

        if selected_row.empty:

            st.error(
                "Selected role was not found."
            )

            st.stop()

        selected_score = float(
            selected_row.iloc[0]["Match Score"]
        )

        st.metric(
            f"🎯 {selected_role} Match Score",
            f"{selected_score:.2f}%"
        )

        # =================================================
        # SKILL GAP + ROADMAP
        # =================================================

        missing_skills, roadmap = generate_roadmap(
            selected_role,
            skills
        )

        # =================================================
        # MISSING SKILLS
        # =================================================

        st.header(
            f"📉 Missing Skills for {selected_role}"
        )

        if missing_skills:

            st.warning(
                f"You have {len(missing_skills)} "
                f"skill gap(s) for this role."
            )

            missing_columns = st.columns(3)

            for index, skill in enumerate(
                missing_skills
            ):

                with missing_columns[
                    index % 3
                ]:

                    st.error(
                        f"❌ {skill}"
                    )

        else:

            st.success(
                "🎉 No missing skills detected "
                "for this role!"
            )

        # =================================================
        # LEARNING ROADMAP
        # =================================================

        st.header(
            "📅 Learning Roadmap"
        )

        if roadmap:

            if isinstance(roadmap, dict):

                for week, task in roadmap.items():

                    st.write(
                        f"**{week}** : {task}"
                    )

            elif isinstance(roadmap, list):

                for item in roadmap:

                    st.write(
                        f"📚 {item}"
                    )

        else:

            st.info(
                "No learning roadmap is required. "
                "You already have the detected skills "
                "for this role."
            )

        # =================================================
        # DOWNLOAD REPORT
        # =================================================

        st.header(
            "📥 Download Analysis Report"
        )

        report = ""

        report += "=" * 60 + "\n"
        report += (
            "AI RESUME ANALYZER AND "
            "JOB RECOMMENDATION SYSTEM\n"
        )
        report += "=" * 60 + "\n\n"

        report += (
            f"Resume: {uploaded_file.name}\n\n"
        )

        # -------------------------------------------------
        # Skills
        # -------------------------------------------------

        report += "-" * 40 + "\n"
        report += "DETECTED SKILLS\n"
        report += "-" * 40 + "\n"

        for skill in skills:

            report += f"- {skill}\n"

        report += "\n"

        # -------------------------------------------------
        # Top recommendations
        # -------------------------------------------------

        report += "-" * 40 + "\n"
        report += "TOP JOB RECOMMENDATIONS\n"
        report += "-" * 40 + "\n"

        for _, row in top_jobs.iterrows():

            report += (
                f"{row['Role']} - "
                f"{float(row['Match Score']):.2f}%\n"
            )

        report += "\n"

        # -------------------------------------------------
        # Target role
        # -------------------------------------------------

        report += "-" * 40 + "\n"
        report += "SELECTED TARGET ROLE\n"
        report += "-" * 40 + "\n"

        report += (
            f"{selected_role}\n"
        )

        report += (
            f"Match Score: "
            f"{selected_score:.2f}%\n\n"
        )

        # -------------------------------------------------
        # Missing skills
        # -------------------------------------------------

        report += "-" * 40 + "\n"
        report += "MISSING SKILLS\n"
        report += "-" * 40 + "\n"

        if missing_skills:

            for skill in missing_skills:

                report += f"- {skill}\n"

        else:

            report += (
                "No missing skills detected.\n"
            )

        report += "\n"

        # -------------------------------------------------
        # Roadmap
        # -------------------------------------------------

        report += "-" * 40 + "\n"
        report += "LEARNING ROADMAP\n"
        report += "-" * 40 + "\n"

        if isinstance(roadmap, dict):

            for week, task in roadmap.items():

                report += (
                    f"{week}: {task}\n"
                )

        elif isinstance(roadmap, list):

            for item in roadmap:

                report += f"{item}\n"

        else:

            report += (
                "No roadmap required.\n"
            )

        report += "\n"

        # -------------------------------------------------
        # Responsible AI
        # -------------------------------------------------

        report += "=" * 60 + "\n"
        report += "RESPONSIBLE AI NOTICE\n"
        report += "=" * 60 + "\n"

        report += (
            "Match scores are estimates based on "
            "job-related skills.\n"
            "They should not be considered hiring "
            "or rejection decisions.\n"
            "The system does not use protected "
            "personal attributes for scoring.\n"
        )

        st.download_button(
            label="⬇️ Download Analysis Report",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )

        # =================================================
        # RESPONSIBLE AI
        # =================================================

        st.divider()

        st.subheader(
            "🤖 Responsible AI"
        )

        st.caption(
            "This system evaluates job-related "
            "technical skills only. It does not use "
            "gender, age, religion, nationality, "
            "photograph, marital status, or disability "
            "for scoring. Match scores are estimates "
            "and should not be treated as automatic "
            "hiring or rejection decisions."
        )

    finally:

        # =================================================
        # DELETE TEMPORARY FILE
        # =================================================

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            os.remove(temp_path)