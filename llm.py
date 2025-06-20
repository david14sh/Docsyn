import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, RetryError, ServiceUnavailable
import requests.exceptions

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")


gemini_api = st.secrets['GEM_API_KEY']
genai.configure(api_key=gemini_api)
answer_model = genai.GenerativeModel("gemini-2.0-flash-lite")

def handle_api_errors(func):
    """Decorator to handle common API errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ResourceExhausted:
            st.error("You've hit your limit, try again tomorrow")
        except (RetryError, ServiceUnavailable, requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout):
            st.error("Please check your network and try again")
    return wrapper

@handle_api_errors
@st.cache_data(show_spinner=False)
def summary(file_text, word_min, word_max, mode):
    prompt = ( 
        f"You are to generate a summary from the file: {file_text} using {mode}\n\n"
        f"The number of words in the summary should BE BETWEEN {word_min} AND {word_max} WORDS \n"
        f"If the max range: {word_max} is greater than the number of words in the document, you may include helpful external info to meet the word range.\n"
        "Return only the summary. No explanation or commentary."
    )

    response = model.generate_content(prompt)
    return response.text

@handle_api_errors
@st.cache_data(show_spinner=False)
def ask_questions(file_text):
    prompt = (
        f"Based ENTIRELY on the following content: {file_text}, generate WASSCE-style questions:\n\n"
        "1. Questions MUST BE seventy percent objective and thirty percent theory\n"
        "2. Objective questions must have 4 options (A-D)\n"
        "3. Generate 15-30 questions based on content length\n"
        "Return only the questions. Nothing else."
    )

    response = model.generate_content(prompt)
    return response.text

@handle_api_errors
@st.cache_data(show_spinner=False)
def answer_questions(questions,file_text):
    prompt = (
        f"Answer each question in this text: {questions}\n"
        f"Refer to the origin of the questions: {file_text} if needed.\n "
        "If it's an objective question, just choose from the options provided, no explanations\n"
        "If it's theory, give a concise answer, not too long, not too short, and not too vague\n"
        "Return ONLY the answers in the same order as the questions"
    )

    response = model.generate_content(prompt)
    return response.text

@handle_api_errors
def answer_query(query,file):
    if "gemini_chat" not in st.session_state:
        st.session_state.gemini_chat = answer_model.start_chat(history=[])
    
        st.session_state.gemini_chat.send_message([
            f"You are Docsyn, a powerful document analyzer. Your role is to assist with document-related queries by providing accurate, to-the-point, and context-aware responses. Use the following document to answer the question: {file}"
        ])
    
    response = st.session_state.gemini_chat.send_message(query)
    return response.text
