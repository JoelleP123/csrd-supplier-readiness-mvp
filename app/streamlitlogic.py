# ----------------------------
# Streamlit UI
# ----------------------------

import streamlit as st

st.title("Supplier Baseline Screening")
st.caption("version: proves UI → normalize → tags → screening → report.")

if "answers" not in st.session_state:
    st.session_state.answers = {}
if "results" not in st.session_state:
    st.session_state.results = None
if "applied_tags" not in st.session_state:
    st.session_state.applied_tags = []
if "normalized" not in st.session_state:
    st.session_state.normalized = {}

st.header("Section A: Supplier Profile")

for question_text, options in INTAKE_QUESTIONS.items():
    answer = st.selectbox(question_text, options, key=question_text)
    st.session_state.answers[question_text] = answer

    if question_text == "Which sector best fits your operations?" and answer:
        if answer in SECTOR_BASELINE_ASSUMPTIONS:
            st.info(f"Baseline assumptions for {answer}:")
            for a in SECTOR_BASELINE_ASSUMPTIONS[answer]:
                st.markdown(f"- {a}")

if st.button("Run screening"):
    normalized = normalize_answers(st.session_state.answers)
    st.session_state.normalized = normalized

    applied_tags = derive_tags(normalized) or []
    applied_tags = list(dict.fromkeys(applied_tags))
    st.session_state.applied_tags = applied_tags

    tags_dict = {t: True for t in applied_tags}
    st.session_state.results = run_screening(tags_dict)

with st.expander("Debug", expanded=False):
    st.write("answers:", st.session_state.answers)
    st.write("normalized:", st.session_state.normalized)
    st.write("applied_tags:", st.session_state.applied_tags)
    st.write("type(applied_tags):", str(type(st.session_state.applied_tags)))

st.subheader("Results")
if st.session_state.results is None:
    st.info("Click **Run screening** to generate results.")
else:
    st.metric("Score", st.session_state.results.get("score", 0))
    st.success(st.session_state.results.get("band", ""))
    why = st.session_state.results.get("why", [])
    if isinstance(why, list) and why:
        st.markdown("**Why:**")
        for item in why:
            st.markdown(f"- {item}")

    with st.expander("Raw results JSON", expanded=False):
        st.json(st.session_state.results)
