import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(content, question, language):
    prompt = f"""
    You are an AI teacher. Teach the following content to the user in a way that is very simple and easy to understand.
    Respond in {language} language. Make sure you do not miss any important points from the content while explaining.
    Everything needs to be explained without missing anything from the content(add relevant examples wherever required).
    If the user has asked some particular question answer it in a way which is simple to understand.
    Make the user grasp concept very well.

    Content to teach:
    {content}

    User's question:
    {question}
    """
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt
    )
    return response.text

# Set Page Config
st.set_page_config(page_title="Personalized AI Tutor", page_icon="🤖", layout="wide")
st.title("📘AI Teacher")

# Language selection
import streamlit as st

languages = {
    "English": "en",
    "Portuguese": "pt",
    "Spanish": "es",
    "German": "de",
    "French": "fr",
    "Italian": "it",
    "Dutch": "nl",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese": "zh",
    "Korean": "ko",
    "Hindi": "hi"
}

language = st.selectbox("🌍 Choose your language for learning:", list(languages.keys()))

# Input: Educational content
content = st.text_area("📄 Paste the paragraph/content you'd like to learn from:", height=200)

# Initialize chat history
if "msg2" not in st.session_state:
    st.session_state["msg2"] = [
        {"role": "assistant", "content": "Hi, I'm your AI Teacher! Ask me anything based on the content you pasted."}
    ]

# Display past messages
for msg in st.session_state.msg2:
    st.chat_message(msg["role"]).write(msg["content"])

# Input: User question
if prompt := st.chat_input("❓ Ask a question about the above content..."):
    st.session_state.msg2.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if content.strip() == "":
        response = "⚠️ Please paste some content above so I can help teach you based on it."
    else:
        response = get_gemini_response(content, prompt, language)

    st.session_state.msg2.append({'role': 'assistant', "content": response})
    st.chat_message("assistant").write(response)