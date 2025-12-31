## Connect Streamlit UI

import streamlit as st
from intake import intake_questions
from logic import Intake_Tag_Definitions
from logic import run_screening
from app import Scoring_logic

st.title("Supplier Baseline Screening (CSRD Friendly)")
st.caption("Decision-support triage for readiness and communication.")

intake = {}

st.header("Section A: Supplier Profile")
for key, q in INTAKE_QUESTIONS.items():
    intake[key] = st.selectbox(q["label"], [""] + q["options"], key=key)

if st.button("Run screening"):
    missing = [k for k, v in intake.items() if v == ""]
    if missing:
        st.error("Please answer all questions.")
    else:
        out = run_screening(intake)

        st.subheader("Results")
        st.json(out)  # quick hackathon output (we can prettify later)

