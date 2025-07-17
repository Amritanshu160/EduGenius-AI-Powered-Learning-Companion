import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="Code Assistant",layout="wide",page_icon="💻")


# Streamlit UI
st.title("💻 Multi-language Code Assistant")
st.markdown("AI-powered code assistant supporting multiple languages!")

# Select programming language
language = st.selectbox("Select Programming Language", ["Python", "JavaScript", "C++", "Java", "C#", "Go", "Rust", "Swift", "Ruby", "PHP"])

# Code input area
input = st.text_area("Enter your input:")


def get_ai_response(language, user_input):
    
    prompt = (f"You are a multilingual coding assistant. The user has provided the following input: '{user_input}' "
              f"and the respective coding language: '{language}'. Provide an optimized code based on the user's request. "
              f"Ensure the code is efficient, well-structured, and easy to understand. "
              f"Give a detailed explanation for each line of code, provide a "
              f"step-by-step explanation in an easy and understandable way. Additionally, suggest possible improvements "
              f"or modifications to enhance the code further and also provide sample output at the end.")

    response = client.models.generate_content(
        model= "gemini-2.5-pro",
        contents = prompt
    )
    
    return response.text if response else "No response generated."


# Generate AI response on button click
if st.button("Get AI Response"): 
    if input.strip():
        with st.spinner("Processing with AI..."):
            response = get_ai_response(language, input)
            st.subheader("🤖 AI Response:")
            st.code(response)
    else:
        st.warning("Please enter some code to analyze.")


