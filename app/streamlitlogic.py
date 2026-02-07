import streamlit as st

# ------------------------------------------------------------
# Safe imports with fallbacks (so the app ALWAYS loads)
# ------------------------------------------------------------
import_error = None

# Defaults (stubs) used if imports fail
INTAKE_QUESTIONS = {
    "Which sector best fits your operations?": [
        "", "Manufacturing", "Tourism", "Agriculture", "Services", "Other"
    ],
    "Where are your main operations located?": [
        "", "EU", "Non-EU (sells into EU)", "Non-EU (no EU exposure)", "Not sure"
    ],
    "Do you have a sustainability/ESG lead or team?": [
        "", "Yes", "No", "In progress"
    ],
}
QUESTION_TO_KEY = {
    "Which sector best fits your operations?": "sector",
    "Where are your main operations located?": "location",
    "Do you have a sustainability/ESG lead or team?": "owner",
}

SECTOR_BASELINE_ASSUMPTIONS = {
    "Manufacturing": ["Likely complex supply chain", "Higher CSRD cascade exposure"],
    "Tourism": ["Higher reputational risk", "Supplier footprint (travel, food, services)"],
    "Agriculture": ["Land/water impacts likely material", "Labor & seasonal workforce risks"],
    "Services": ["Lower direct footprint", "Data/privacy risk may be higher if AI used"],
}

def normalize_answers(answers: dict) -> dict:
    """Fallback normalizer: maps question text -> internal keys."""
    normalized = {}
    for q_text, value in answers.items():
        key = QUESTION_TO_KEY.get(q_text, q_text)
        normalized[key] = value
    return normalized

def derive_tags(normalized: dict) -> list:
    """Fallback tag derivation for UI testing."""
    tags = []
    sector = (normalized.get("sector") or "").strip()
    location = (normalized.get("location") or "").strip()
    owner = (normalized.get("owner") or "").strip()

    if sector and sector != "Other":
        tags.append("SECTOR_KNOWN")
    if "EU" in location:
        tags.append("EU_EXPOSURE")
    if owner == "No":
        tags.append("OWNER_GAP")

    # Example CSRD signal if EU exposure + manufacturing
    if "EU" in location and sector == "Manufacturing":
        tags.append("CSRD_CASCADE_SIGNAL")

    return tags

def run_screening(tags_dict: dict) -> dict:
    """Fallback screening so we can test the flow."""
    score = 0
    why = []

    if tags_dict.get("CSRD_CASCADE_SIGNAL"):
        score += 2
        why.append("EU exposure + manufacturing suggests CSRD cascade readiness work is likely relevant.")
    if tags_dict.get("EU_EXPOSURE"):
        score += 1
        why.append("EU exposure increases regulatory and buyer due diligence pressure.")
    if tags_dict.get("OWNER_GAP"):
        score += 1
        why.append("No clear ESG owner: governance and accountability likely need strengthening.")

    band = "Low" if score <= 1 else "Medium" if score <= 3 else "High"
    return {"score": score, "band": band, "why": why, "tags_received": list(tags_dict.keys())}

# Try real imports; if any fail, we keep the stubs above.
try:
    from intake.intake_questions import INTAKE_QUESTIONS as REAL_INTAKE_QUESTIONS, QUESTION_TO_KEY as REAL_QUESTION_TO_KEY
    INTAKE_QUESTIONS = REAL_INTAKE_QUESTIONS
    QUESTION_TO_KEY = REAL_QUESTION_TO_KEY

    from logic.Intake_Tag_DefinitionsAssumptions import (
        TAG_DEFS,  # unused here but fine if present
        derive_tags as REAL_DERIVE_TAGS,
        SECTOR_BASELINE_ASSUMPTIONS as REAL_SECTOR_BASELINE_ASSUMPTIONS,
    )
    derive_tags = REAL_DERIVE_TAGS
    SECTOR_BASELINE_ASSUMPTIONS = REAL_SECTOR_BASELINE_ASSUMPTIONS

    from logic.utils import normalize_answers as REAL_NORMALIZE_ANSWERS
    normalize_answers = REAL_NORMALIZE_ANSWERS

    from logic.scoringnextstepsgenerator import run_screening as REAL_RUN_SCREENING
    run_screening = REAL_RUN_SCREENING

except Exception as e:
    import_error = e  # shown in Debug expander; app still loads

# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
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
    answer = st.selectbox(question_text, options, key=f"q::{question_text}")
    st.session_state.answers[question_text] = answer

    # Show sector assumptions if this is the sector question
    if question_text.strip() == "Which sector best fits your operations?" and answer:
        assumptions = SECTOR_BASELINE_ASSUMPTIONS.get(answer)
        if assumptions:
            st.info("**Baseline assumptions:**\n- " + "\n- ".join(assumptions))

# Run button
if st.button("Run screening"):
    normalized = normalize_answers(st.session_state.answers)
    st.session_state.normalized = normalized

    applied_tags = derive_tags(normalized) or []
    applied_tags = list(dict.fromkeys(applied_tags))  # dedupe while preserving order
    st.session_state.applied_tags = applied_tags

    tags_dict = {t: True for t in applied_tags}

    try:
        st.session_state.results = run_screening(tags_dict)
    except Exception as e:
        st.session_state.results = None
        st.error("run_screening() crashed.")
        st.exception(e)

# Debug
with st.expander("Debug", expanded=False):
    if import_error is not None:
        st.warning("Some project modules did not import; using fallback stubs so the UI can run.")
        st.exception(import_error)

    st.write("answers:", st.session_state.answers)
    st.write("normalized:", st.session_state.normalized)
    st.write("applied_tags:", st.session_state.applied_tags)

# Results
st.subheader("Results")
if st.session_state.results is None:
    st.info("Click **Run screening** to generate results.")
else:
    results = st.session_state.results
    # Friendly view if keys exist
    score = results.get("score") if isinstance(results, dict) else None
    band = results.get("band") if isinstance(results, dict) else None
    why = results.get("why") if isinstance(results, dict) else None

    if score is not None:
        st.metric("Score", score)
    if band:
        st.success(f"Band: {band}")

    if isinstance(why, list) and why:
        st.markdown("**Why:**")
        for item in why:
            st.markdown(f"- {item}")

    with st.expander("Raw results JSON", expanded=False):
        st.json(results)
