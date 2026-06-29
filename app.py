import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import speech_recognition as sr
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except Exception:
        return "Sorry, I couldn't understand your voice."

st.set_page_config(page_title="AI Mock Interview", page_icon="🎤")

st.title("🎤 AI Mock Interview System")

name = st.text_input("Enter your Name")

role = st.selectbox(
    "Select Job Role",
    ["Software Developer", "Data Analyst", "Python Developer", "Data Scientist"]
)

if st.button("Start Interview"):
    st.success(f"Welcome {name}!")
    st.write(f"Interview Role: {role}")

    prompt = f"""
    You are an expert interviewer.
    Conduct a mock interview for a {role}.
    Ask only ONE interview question.
    """

    response = model.generate_content(prompt)

    st.subheader("🤖 AI Interviewer")
    st.write(response.text)

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer"):

        evaluation_prompt = f"""
        Interview Question:
        {response.text}

        Candidate Answer:
        {answer}

        Give:
        1. Technical Score (out of 10)
        2. Communication Score (out of 10)
        3. Strengths
        4. Improvements
        """

        evaluation = model.generate_content(evaluation_prompt)

        st.subheader("📊 AI Feedback")
        st.write(evaluation.text)