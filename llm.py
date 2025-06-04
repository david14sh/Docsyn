import streamlit as st
import google.generativeai as genai

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")


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
        "Return ONLY the questions."
    )

    response = model.generate_content(prompt)
    return response.text


def answer_query(user_query, file_text):
    # try:
    gemini_chat = answer_model.start_chat(history=[])
    
    
    gemini_chat.send_message(
        "You are Docsyn, a powerful document analyzer. Your role is to assist with document-related queries "
        "by providing accurate, short unless otherwise specified, and context-aware responses."
    )
    
    gemini_chat.send_message(f"Refer to this document content:\n{file_text}")

    return gemini_chat
    


    # except Exception as e:
    #     return "I apologize, but I encountered an error while processing your query. Please try again."