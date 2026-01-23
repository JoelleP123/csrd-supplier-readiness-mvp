## Connect Streamlit UI

import streamlit as st
from intake.intake_questions import INTAKE_QUESTIONS, QUESTION_TO_KEY
from logic import scoring_logic

import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Now import
from intake.intake_questions import INTAKE_QUESTIONS, QUESTION_TO_KEY
from logic.sector_assumptions import SECTOR_BASELINE_ASSUMPTIONS
from logic.Intake_Tag_Definitions import TAG_DEFS, derive_tags

st.title("Supplier Baseline Screening (CSRD Friendly)")
st.caption("Decision-support triage for readiness and communication.")

intake = {}

st.header("Section A: Supplier Profile")
for key, q in intake_questions.items():
    intake[key] = st.selectbox(q["label"], [""] + q["options"], key=key)

if st.button("Run screening"):
    missing = [k for k, v in intake.items() if v == ""]
    if missing:
        st.error("Please answer all questions.")
    else:
        out = run_screening(intake)

        st.subheader("Results")
        st.json(out)  # quick hackathon output (we can prettify later)

