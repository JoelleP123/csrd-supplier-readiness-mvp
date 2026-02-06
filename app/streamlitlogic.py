# ## Connect Streamlit UI
import sys
from pathlib import Path

# Add parent directory to Python path - MUST BE BEFORE OTHER IMPORTS
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from intake.intake_questions import INTAKE_QUESTIONS, QUESTION_TO_KEY
from logic.Intake_Tag_DefinitionsAssumptions import (
    TAG_DEFS,
    derive_tags,
    SECTOR_BASELINE_ASSUMPTIONS,
)
from logic.utils import normalize_answers



# --- TEMP: replace this with your real run_screening import ---
def run_screening(tags_dict: dict) -> dict:
    """
    Temporary stub so the app loads.
    Replace with your real run_screening implementation/import.
    """
    return {
        "status": "ok",
        "tags_received": list(tags_dict.keys()),
        "note": "Replace stub run_screening() with real logic.",
    }
# -------------------------------------------------------------

st.title("Supplier Baseline Screening (CSRD Friendly)")
st.caption("Decision-support triage for readiness and communication.")

# Initialize session state for answers
if "answers" not in st.session_state:
    st.session_state.answers = {}

st.header("Section A: Supplier Profile")

# Iterate through questions
for question_text, options in INTAKE_QUESTIONS.items():
    answer = st.selectbox(
        question_text,
        options,
        key=question_text
    )
    st.session_state.answers[question_text] = answer

    # Show sector assumptions for question 4
    if question_text == "Which sector best fits your operations?" and answer:
        if answer in SECTOR_BASELINE_ASSUMPTIONS:
            st.info(f"**Baseline assumptions for '{answer}':**")
            for assumption in SECTOR_BASELINE_ASSUMPTIONS[answer]:
                st.markdown(f"- {assumption}")

# Keep these in session_state so they survive reruns cleanly
if "results" not in st.session_state:
    st.session_state.results = None
if "applied_tags" not in st.session_state:
    st.session_state.applied_tags = []

if st.button("Run screening"):
    # Normalize answers to internal keys
    normalized = normalize_answers(st.session_state.answers)

    # Derive tags
    applied_tags = derive_tags(normalized) or []
    st.session_state.applied_tags = applied_tags

    # Build tags dict
    tags_dict = {t: True for t in applied_tags}

    # Run screening
    st.session_state.results = run_screening(tags_dict)

# Debug + output section (safe to render even before button click)
with st.expander("Debug", expanded=False):
    st.write("applied_tags:", st.session_state.applied_tags, type(st.session_state.applied_tags))

st.subheader("Results")
if st.session_state.results is None:
    st.info("Click **Run screening** to generate results.")
else:
    st.json(st.session_state.results)

