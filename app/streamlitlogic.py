# app/streamlitlogic.py
import sys
from pathlib import Path
import streamlit as st

# Ensure repo root is on PYTHONPATH (Streamlit Cloud-safe)
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- Real project imports ---
from intake.intake_questions import INTAKE_QUESTIONS
from logic.utils import normalize_answers
from logic.Intake_Tag_DefinitionsAssumptions import derive_tags, SECTOR_BASELINE_ASSUMPTIONS
from logic.scoringnextstepsgenerator import run_screening


st.title("Supplier Baseline Screening (CSRD Friendly)")
st.caption("Decision-support triage for readiness and communication.")

# Session state init
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "results" not in st.session_state:
    st.session_state.results = None
if "applied_tags" not in st.session_state:
    st.session_state.applied_tags = []
if "normalized" not in st.session_state:
    st.session_state.normalized = {}

st.header("Section A: Supplier Profile")

# Render questions
for question_text, options in INTAKE_QUESTIONS.items():
    answer = st.selectbox(question_text, options, key=question_text)
    st.session_state.answers[question_text] = answer

    # Optional: show sector assumptions
    if question_text == "Which sector best fits your operations?" and answer:
        if answer in SECTOR_BASELINE_ASSUMPTIONS:
            st.info(f"Baseline assumptions for '{answer}':")
            for a in SECTOR_BASELINE_ASSUMPTIONS[answer]:
                st.markdown(f"- {a}")

# Run screening button
if st.button("Run screening"):
    normalized = normalize_answers(st.session_state.answers)
    st.session_state.normalized = normalized

    applied_tags = derive_tags(normalized) or []
    # de-dupe while preserving order
    applied_tags = list(dict.fromkeys(applied_tags))
    st.session_state.applied_tags = applied_tags

    tags_dict = {t: True for t in applied_tags}

    # IMPORTANT: run_screening must not rely on any global applied_tags
    st.session_state.results = run_screening(tags_dict)

# Debug
with st.expander("Debug", expanded=False):
    st.write("answers:", st.session_state.answers)
    st.write("normalized:", st.session_state.normalized)
    st.write("applied_tags:", st.session_state.applied_tags)

st.subheader("Results")
if st.session_state.results is None:
    st.info("Click **Run screening** to generate results.")
else:
    # If your run_screening returns your real structure, show it
    st.json(st.session_state.results)

