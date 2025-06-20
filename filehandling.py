from io import BytesIO
import pdfplumber
from docx import Document
import streamlit as st

@st.cache_data(show_spinner=False)
def extract(file):
    if file.name.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''
    elif file.name.endswith('.docx'):
        doc = Document(BytesIO(file.read()))
        text = '\n'.join([para.text for para in doc.paragraphs])
    elif file.name.endswith('.txt'):
        text = file.getvalue().decode('utf-8')

    return text
