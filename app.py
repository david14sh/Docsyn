import streamlit as st
from llm import summary, ask_questions, answer_query
from filehandling import create_pdf, extract
import time

# Streamlit UI
st.set_page_config(page_title="Docsyn", page_icon="logo.png")

st.logo("logo.png")
st.markdown("## **Welcome to Docsyn - Your Document Analyst**")
uploaded_file = st.file_uploader(label="Upload your PDF or Word document to get started!", type=["pdf", "txt", "docx"])

features = ["Smart Document Summaries","Instant Study Questions","Document Q&A Assistant"]

with st.sidebar:
    st.title("Docsyn")
    st.sidebar.markdown("#### Key Features")
    st.markdown(
        """
        <style>
        .pill {
            display: inline-block;
            padding: 0.5em 1.2em;
            margin-bottom: 0.5em;
            border-radius: 999px;
            background: #d3e3fd;
            color: #2457b5;
            font-weight: 600;
            font-size: 1em;
            white-space: nowrap;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    for feature in features:
        st.markdown(f'<div class="pill">{feature}</div>', unsafe_allow_html=True)

    st.sidebar.markdown("#### How To Use")
    st.sidebar.write("""
    - Upload a document to get started!
    - Ask a question about your document to get an answer.
                     """)
    
    st.sidebar.markdown("#### Tips")
    st.sidebar.write("""
    - Keep your prompt concise and to the point.
    - Ask specific questions to get more accurate answers.
    - Remember, AI can make mistakes, so always verify the answer.
                     """)
    

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def type_text(text):
    t = st.empty()
    for i in range(len(text) + 1):
        t.markdown(text[:i])
        time.sleep(0.01)  

if uploaded_file:
    text = extract(uploaded_file)

    if st.toggle("Show Summary & Questions"):
        if "range" not in st.session_state:
            @st.dialog("Select Your Range")
            def show_range_dialog():
                word_min = st.number_input("Minimum word count: ", min_value=0, max_value=5000)
                word_max = st.number_input("Maximum word count: ", min_value=word_min, max_value=10000)
                if st.button("Confirm Range"):
                    st.session_state.range = {"min": word_min, "max": word_max}
                    st.rerun()
            show_range_dialog()
        else:
            with st.spinner("Generating Summary..."):
                summ, questions = st.tabs(['Summary', 'Questions'])
                summary_text = summary(text, st.session_state.range['min'], st.session_state.range['max'])
                pdf = create_pdf(summary_text)

                summ.write(summary_text)
                summ.download_button(
                    label="📄 Download as PDF",  
                    data=pdf,
                    file_name="summary.pdf",
                    mime="application/pdf" 
                )

                questions_text = ask_questions(text)
                questions.write(questions_text)

    elif "range" in st.session_state: 
        del st.session_state["range"]

    st.divider()
    transparent = "https://upload.wikimedia.org/wikipedia/commons/c/ca/1x1.png"
    for chat_item in st.session_state.chat_history:
        for user_msg, ai_response in chat_item.items():
            with st.chat_message("User", avatar=transparent):
                st.markdown(user_msg)
            with st.chat_message("Docsyn", avatar="logo.png"):
                st.markdown(ai_response)

    user_input = st.chat_input("Ask a question about your document...")
    if user_input:
        if not "response" in st.session_state:
            st.session_state.response = answer_query(user_input, text)

        with st.chat_message("User", avatar=transparent):
            st.markdown(user_input)
        response = st.session_state.response.send_message(user_input)
        st.session_state.chat_history.append({user_input:response.text})

        with st.chat_message("Docsyn", avatar="logo.png"):
            type_text(response.text)

else:
    st.session_state.clear()


