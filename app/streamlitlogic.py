## Connect Streamlit UI
import sys
from pathlib import Path
# Add parent directory to Python path - MUST BE BEFORE OTHER IMPORTS
sys.path.insert(0, str(Path(__file__).parent.parent))

# NOW import your modules
import streamlit as st
from intake.intake_questions import INTAKE_QUESTIONS, QUESTION_TO_KEY
from logic.Intake_Tag_Definitions import TAG_DEFS, derive_tags, SECTOR_BASELINE_ASSUMPTIONS
from logic.scoring_nextstepsgenerator import run_screening
from logic.utils import normalize_answers

st.title("Supplier Baseline Screening (CSRD Friendly)")
st.caption("Decision-support triage for readiness and communication.")


# Initialize session state for answers
if 'answers' not in st.session_state:
    st.session_state.answers = {}

st.header("Section A: Supplier Profile")

# Iterate through questions - FIXED to match your data structure
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

if st.button("Run screening"):
    # Normalize answers to internal keys
    normalized = normalize_answers(st.session_state.answers)
    
    # Derive tags
    applied_tags = derive_tags(normalized)
    tags_dict = {t: True for t in applied_tags}
    
    # Run screening
    results = run_screening(tags_dict)
    
    st.subheader("Results")
    st.json(results)  # You can prettify this later


