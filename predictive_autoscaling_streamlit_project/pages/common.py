
from pathlib import Path
import streamlit as st
import pandas as pd

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"


# --------------------------------------------------
# LOAD CSV FILES
# --------------------------------------------------

@st.cache_data
def load_csv(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    return pd.read_csv(file_path)


# --------------------------------------------------
# APPLY WEBSITE STYLE
# --------------------------------------------------

def apply_style():

    css_file = ROOT / "styles.css"

    if css_file.exists():

        with open(css_file, "r", encoding="utf-8") as file:
            css = file.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        )

    else:
        st.warning("styles.css file was not found.")


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

PROJECT_TITLE = (
    "Predictive Energy-Aware Auto-Scaling "
    "for Cost-Efficient Cloud Resource Management"
)

INSTITUTION = "National Institute of Technology Warangal"

DEPARTMENT = "M.Tech – Computer Science and Engineering"

TEAM_MEMBERS = [
    "Hrishikesh Chandra (26CSM1R05)",
    "Prakash Kumar (26CSM1R16)"
]

MENTOR = "Prof. Manoj Kumar Patra"
