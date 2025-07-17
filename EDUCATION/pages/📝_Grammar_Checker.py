import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load API Key
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize chat history
if "msg1" not in st.session_state:
    st.session_state.msg1 = [
        {"role": "assistant", "content": "Hello! I'm your Grammar Helper. Ask me anything about English grammar."}
    ]

def get_grammar_response(user_input):
    # Basic prompt engineering
    system_prompt = (
        "You are an expert English grammar teacher. Your responses should:\n"
        "1. Be clear and educational\n"
        "2. Correct mistakes when found\n"
        "3. Explain grammar rules when asked\n"
        "4. Provide examples when helpful\n"
        "5. Maintain a friendly, professional tone\n\n"
        "User's input: " + user_input
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[system_prompt]
    )
    return response.text.strip()

# App Interface
st.set_page_config(page_title="Grammar Helper", page_icon="📝",layout="wide")
st.title("Grammar Helper Chatbot")

# Display chat history
for msg in st.session_state.msg1:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Type your question or text here..."):
    # Add user message
    st.session_state.msg1.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_grammar_response(prompt)
        st.session_state.msg1.append({"role": "assistant", "content": response})
        st.write(response)
 