from io import BytesIO
from fpdf import FPDF
import pdfplumber
from docx import Document
import streamlit as st

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
    else:
        st.error("Unsupported file type")
    return text

def create_pdf(text):
    buffer = BytesIO()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buffer.write(pdf_bytes)
    buffer.seek(0)
    return buffer

