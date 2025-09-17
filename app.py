import streamlit as st
from utils.pdf_utils import extract_text_from_pdf
from utils.qa_utils import QAEngine
from utils.voice_utils import speech_to_text, text_to_speech

# Initialize QA Engine (store in session state so it persists)
if "qa_engine" not in st.session_state:
    st.session_state.qa_engine = QAEngine()

st.title("🎤 Student Examination Agent")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.session_state.qa_engine.build_index(text)

    # 🎤 Greet user after upload
    st.write("PDF uploaded successfully ✅")
    text_to_speech("How can I help you?")

    st.subheader("Voice Question")
    if st.button("Ask with Voice"):
        voice_q = speech_to_text()
        if voice_q:
            st.write("**You asked (via voice):**", voice_q)
            answer = st.session_state.qa_engine.query(voice_q)
            st.write("**Answer:**", answer)
            text_to_speech(answer)
