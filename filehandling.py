from io import BytesIO
from reportlab.pdfgen import canvas
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
    p = canvas.Canvas(buffer)
    textobject = p.beginText(40, 800)
    for line in text.split('\n'):
        textobject.textLine(line)
    p.drawText(textobject)
    p.save()
    buffer.seek(0)
    return buffer
