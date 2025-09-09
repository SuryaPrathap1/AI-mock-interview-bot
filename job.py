import streamlit as st
import speech_recognition as sr
import os
import time
from datetime import datetime
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.schema.output_parser import StrOutputParser
import pyttsx3
from fpdf import FPDF

# ------------------- SETUP -------------------
st.set_page_config(page_title="Job Interview Chatbot (Voice)", page_icon="🎙️", layout="wide")

# ------------------ VOICE ENGINE ------------------
engine = pyttsx3.init()
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass

# ------------------ INTERVIEW TYPE SELECTION ------------------
if "interview_type_selected" not in st.session_state:
    st.session_state.interview_type_selected = False

if not st.session_state.interview_type_selected:
    st.title("🎙️ Select Interview Type")
    interview_type = st.radio("Please choose the type of interview:", ["Technical (TR)", "HR", "Managerial (MR)"])
    if interview_type:
        st.session_state.interview_type = interview_type
        st.session_state.interview_type_selected = True
        if interview_type != "Technical (TR)":
            speak(f"Welcome to the {interview_type} interview panel. Let's begin!")
        st.experimental_rerun()

# ------------------- SIDEBAR -------------------
if st.session_state.interview_type_selected:
    st.sidebar.title("🎯 Interview Settings")
    interview_type = st.session_state.interview_type
    sub_topic = None

    if interview_type == "Technical (TR)":
        sub_topic = st.sidebar.selectbox("Choose Technical Topic:", [
            "Programming", "Data Structures", "Algorithms", "DBMS", "Operating Systems", "Computer Networks", "OOP", "Software Engineering"
        ])
        speak(f"Welcome to the Technical interview on {sub_topic}. Let's begin!")
    else:
        sub_topic = None  # HR or MR skips topic selection

    timer_enabled = st.sidebar.checkbox("⏱️ Timed Responses", value=True)

    # ------------------- MODEL INIT -------------------
    API_KEY = "AIzaSyDJM8XW4_R164ZSChlOVH_2vOrFTmfx9BM"
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY)

    # ------------------ PROMPT ------------------
    specific_prompt = f"Ask unlimited {interview_type} interview questions related to {sub_topic}." if sub_topic else f"Conduct a full {interview_type} interview."
    SYSTEM_PROMPT = f"""
    You are an AI interviewer conducting a mock {interview_type} interview.
    {specific_prompt}
    Ask one question at a time and wait for the candidate's response.
    After each response, provide feedback on:
    - content
    - clarity
    - fluency
    - tone and modulation
    - confidence level (confident/hesitant)
    Give a score out of 10.
    If the user says or types 'end interview', summarize performance and give suggestions.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template("{question}")
    ])

    # (Remaining code unchanged)
