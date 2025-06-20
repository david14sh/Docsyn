# Docsyn - AI-Powered Document Analysis

Docsyn is a powerful document analysis system that uses AI to help you read less and learn more. Upload any document and get instant summaries, study questions, and intelligent Q&A assistance.

## Features

- **Smart Document Summaries**: Generate concise summaries with customizable word counts and formats
- **Instant Study Questions**: Get WASSCE-style questions (70% objective, 30% theory) based on your document
- **Document Q&A Assistant**: Ask questions about your document and get accurate, context-aware answers



### How It Works:
1. User uploads a document (PDF, DOCX, TXT)
2. Document is uploaded to Gemini 
4. All subsequent questions reference the uploaded document
5. Initial insights are automatically generated and displayed

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Upload your document (PDF, DOCX, or TXT)
3. Choose to generate summaries and questions, or start chatting with your document
4. Ask questions and get intelligent, context-aware responses

## File Support

- **PDF**: Full text extraction with pdfplumber
- **DOCX**: Document processing with python-docx
- **TXT**: Direct text file support

## API Keys Required

Set up your Streamlit secrets with:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `GEM_API_KEY`: Alternative Gemini API key (if needed)

## Architecture

- **Frontend**: Streamlit for interactive UI
- **AI Engine**: Google Gemini 2.0 Flash Lite
- **File Processing**: Custom extractors for PDF, DOCX, and TXT files 