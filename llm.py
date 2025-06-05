import streamlit as st
import google.generativeai as genai

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")

# Separate API key for answer model to distribute load
gemini_api = st.secrets['GEM_API_KEY']
genai.configure(api_key=gemini_api)
answer_model = genai.GenerativeModel("gemini-2.0-flash-lite")

@st.cache_data(show_spinner=False)
def summary(file_text, word_min, word_max):
    prompt = ( 
        f"You are to generate a summary from the file: {file_text}\n\n"
        f"The number of words in the summary should BE BETWEEN {word_min} AND {word_max} WORDS \n"
        f"If the max range: {word_max} is greater than the number of words in the document, you may include helpful external info to meet the word range.\n"
        "Return only the summary. No explanation or commentary."
    )

    response = model.generate_content(prompt)
    return response.text

@st.cache_data(show_spinner=False)
def ask_questions(file_text):
    prompt = (
        f"Based entirely on the following content: {file_text}, generate WASSCE-style questions:\n\n"
        "1. Questions MUST BE seventy percent objective and thirty percent theory\n"
        "2. Objective questions must have 4 options (A-D)\n"
        "3. Generate 15-30 questions based on content length\n"
        "Return only the questions. Nothing else."
    )

    response = model.generate_content(prompt)
    return response.text

@st.cache_data(show_spinner=False)
def answer_questions(questions):
    prompt = (
        f"Answer each question in this text: {questions}\n"
        "If it's an objective question, just choose from the options provided, no explanations\n"
        "If it's theory, give a concise answer, not too long, not too short, and not too vague\n"
        "Return ONLY the answers in the same order as the questions"
    )

    response = model.generate_content(prompt)
    return response.text

def answer_query(file_text):
    gemini_chat = answer_model.start_chat(history=[])
    
    gemini_chat.send_message(
        "You are Docsyn, a powerful document analyzer. Your role is to assist with document-related queries "
        "by providing accurate, concise, and context-aware responses."
    )
    
    gemini_chat.send_message(f"Refer to this document content:\n{file_text}")

    return gemini_chat