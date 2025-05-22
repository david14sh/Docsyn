import streamlit as st
import google.generativeai as genai

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash-latest")


gemini_api = st.secrets['GEM_API_KEY']
genai.configure(api_key=gemini_api)
answer_model = genai.GenerativeModel("gemini-2.0-flash-lite")



def summary(file_text, word_min, word_max):
    prompt = ( 
        f"You are to generate a summary of the following content strictly within {word_min} to {word_max} words from the file: {file_text}\n\n"
        f"I repeat, the number of words MUST NOT BE LESS THAN {word_min} and MUST NOT BE GREATER THAN {word_max}"
        f"If the max range: {word_max} is greater than the number of words in the document, you may include helpful external info to meet the word range.\n"
        "Return only the summary. No extra explanations or commentary."
    )

    response = model.generate_content(prompt)
    return response.text


def ask_questions(file_text):
    prompt = (
        f"Based entirely on the following content: {file_text}, generate a set of questions for student learning:\n\n"
        "There MUST be a balanced mix of theory and objective questions.\n"
        "Objective questions must have exactly 4 options (A–D) and can be direct or fill-in-the-blank.\n"
        "The total number of questions depends on the text length (e.g., 15 for 700–1000 words) and must not exceed 30.\n Use your own judgement to determine number of questions appropriate for document length\n"
        "Return only the questions. No explanation or commentary."
    )

    response = model.generate_content(prompt)
    return response.text


def answer_query(user_query, file_text):
    try:
        if "gemini_chat" not in st.session_state:
            st.session_state.gemini_chat = answer_model.start_chat(history=[])
            
            
            st.session_state.gemini_chat.send_message(
                "You are Docsyn, a powerful document analyzer. Your role is to assist with document-related queries "
                "by providing accurate, concise, and context-aware responses."
            )
            
            st.session_state.gemini_chat.send_message(f"Refer to this document content:\n{file_text}")
            
        # Send the current query and get response
        response = st.session_state.gemini_chat.send_message(user_query)
        return response.text

    except Exception as e:
        return "I apologize, but I encountered an error while processing your query. Please try again."