import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key from environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to use Gemini Pro for grammar correction
model = genai.GenerativeModel("gemini-2.0-flash")

def correct_grammar(text):
    prompt = f"Correct any spelling and grammar mistakes in the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit App
st.set_page_config(page_title="Grammar & Spelling Corrector")

st.title("📝 AI-Powered Grammar & Spelling Corrector")
st.write("Enter text below, and the AI will correct spelling and grammar mistakes.")

text_area = st.text_area("Enter your text here:")

if st.button("Correct Text"):
    if text_area.strip():
        st.subheader("📌 Input Text:")
        st.info(text_area)

        corrected_text = correct_grammar(text_area)

        st.subheader("✅ Corrected Text:")
        st.success(corrected_text)
    else:
        st.warning("⚠️ Please enter some text before submitting.")
 