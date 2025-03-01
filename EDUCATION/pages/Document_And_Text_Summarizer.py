import streamlit as st
import os
import fitz  # PyMuPDF for extracting text from PDFs
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key from environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to generate summary using Gemini
def summarize_text(text):
    prompt = f"Summarize the following text in a concise manner:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# Function to extract text from a PDF
def extract_text_from_pdf(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in pdf_document:  # Loop through each page
        text += page.get_text("text") + "\n"
    return text.strip()

# Streamlit UI
st.set_page_config(page_title="AI Summarizer", layout="wide")

st.sidebar.title("🔍 AI-Powered Summarizer")
choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize PDF"])

if choice == "Summarize Text":
    st.subheader("📄 Summarize Text using Google Gemini")
    text_input = st.text_area("Enter text to summarize:")

    if st.button("Summarize Text"):
        if text_input.strip():
            st.subheader("🔹 Summary:")
            summary = summarize_text(text_input)
            st.success(summary)
        else:
            st.warning("⚠️ Please enter some text to summarize.")

elif choice == "Summarize PDF":
    st.subheader("📁 Summarize PDF Document using Google Gemini")
    uploaded_file = st.file_uploader("Upload a Document (PDF OR DOCX)", type=["pdf","docx"])

    if uploaded_file is not None and st.button("Summarize PDF"):
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        if extracted_text:
            st.subheader("🔹 Summary:")
            summary = summarize_text(extracted_text)
            st.success(summary)
        else:
            st.warning("⚠️ Could not extract text from the uploaded PDF.")

