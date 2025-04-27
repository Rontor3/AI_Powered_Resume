import streamlit as st
from PyPDF2 import PdfReader
from llm_utils import extract_relevant_jd, generate_resume_feedback, get_llm,standalone_resume_feedback
from embed_utils import get_embedder, compute_similarity

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

st.set_page_config(page_title="AI-Powered Resume & JD Matcher", layout="centered")
st.title("🧠 AI-Powered Resume & JD Matcher")

resume_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_file = st.sidebar.file_uploader("Upload Job Description (PDF)", type=["pdf"])
resume_text_input = st.sidebar.text_area("Or paste Resume Text", "")
jd_text_input = st.sidebar.text_area("Or paste JD Text", "")

llm= get_llm()
embedder = get_embedder()


resume_text = extract_text_from_pdf(resume_file) if resume_file else resume_text_input.strip()
jd_text = extract_text_from_pdf(jd_file) if jd_file else jd_text_input.strip()
if st.sidebar.button("Submit"):
    # Store resume and JD in session state for later use
    if resume_text:
        st.session_state["resume_text"] = resume_text
    else:
        st.warning("⚠️ Please upload a Resume before submitting.")

    if jd_text:
        st.session_state["jd_text"] = jd_text
    else:
        st.warning("⚠️ Please upload a Job Description (JD) if you want JD Matching.")

# Page Navigation
page = st.radio("📄 View", ["JD Matching Score", "Resume Feedback"])

# JD Matching Score Section
if page == "JD Matching Score":
    st.subheader("📊 JD Matching Score")
    jd_text = st.session_state.get("jd_text")
    resume_text = st.session_state.get("resume_text")

    if jd_text and resume_text:
        if st.button("Run JD Matching"):
            with st.spinner("🔍 Extracting relevant job description..."):
                cleaned_jd = extract_relevant_jd(jd_text, llm)
                st.session_state["cleaned_jd"] = cleaned_jd

            with st.spinner("🔗 Computing semantic similarity..."):
                similarity_score = compute_similarity(resume_text, st.session_state["cleaned_jd"], embedder)
                st.session_state["similarity_score"] = similarity_score

            with st.spinner("📊 Generating JD Matching Score..."):
                jd_matching_feedback = generate_resume_feedback(
                    resume_text,
                    st.session_state["cleaned_jd"],
                    st.session_state["similarity_score"],
                    llm
                )
                st.session_state["jd_matching_feedback"] = jd_matching_feedback

        if "similarity_score" in st.session_state and "jd_matching_feedback" in st.session_state:
            # Display the JD Matching Score
            st.markdown(f"### 🔗 **Matching Score:** {st.session_state['similarity_score'] * 100:.2f}%")
            st.progress(int(st.session_state['similarity_score'] * 100))

            # Display Feedback in Collapsible Section
            with st.expander("📋 Detailed JD Matching Feedback", expanded=True):
                st.markdown(f"""
                <div style="background-color: #f4f8fb; padding: 15px; border-radius: 10px; color: #333;">
                    {st.session_state['jd_matching_feedback']}
                </div>
                """, unsafe_allow_html=True)    
        else:
            st.warning("⚠️ Click 'Run JD Matching' to compute the JD Matching Score.")
    else:
        st.warning("⚠️ Please upload both Resume and JD first.")

# Resume Feedback Section
elif page == "Resume Feedback":
    st.subheader("🧾 Resume Feedback")
    resume_text = st.session_state.get("resume_text")

    if resume_text:
        if st.button("Run Resume Feedback"):
            with st.spinner("🧠 Generating ATS Resume Feedback..."):
                # Call the LLM to generate feedback dynamically
                ats_feedback = standalone_resume_feedback(resume_text, llm)
                st.session_state["ats_feedback"] = ats_feedback

        if "ats_feedback" in st.session_state:
            # Display the LLM-generated ATS Feedback dynamically with black background and white text
            st.markdown("""
            <div style="background-color: #000000; padding: 20px; border-radius: 10px; text-align: center; color: #ffffff;">
                <h3 style="color: #ffffff;">🧠 ATS Feedback</h3>
                <p style="font-size: 18px; font-weight: bold;">
                    {feedback}
                </p>
            </div>
            """.format(feedback=st.session_state["ats_feedback"]), unsafe_allow_html=True)
        else:
            st.warning("⚠️ Click 'Run Resume Feedback' to generate feedback.")
else:
    st.warning("⚠️ Please upload a Resume first.")