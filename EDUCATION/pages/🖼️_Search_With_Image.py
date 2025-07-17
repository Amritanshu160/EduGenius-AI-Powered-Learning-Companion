from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from google import genai
from PIL import Image

st.set_page_config(page_title="Search With Image", page_icon="🖼️", layout="wide")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize chat history
if "msg" not in st.session_state:
    st.session_state.msg = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can analyze images. Upload an image and ask me about it!"}
    ]

def get_gemini_response(input, image):
    if input != "":
        response = client.models.generate_content(model="gemini-2.5-flash", contents=[input, image])
    else:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=[image])
    return response.text

st.header("Chat with Image")

# Image upload section (comes first)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Horizontal line to separate upload section from chat
st.markdown("---")

# Display chat messages from history (only text)
for msg in st.session_state.msg:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input (at the bottom)
if prompt := st.chat_input(placeholder="Ask me about the image..."):
    # Add user question to chat history
    st.session_state.msg.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get response only if an image is uploaded
    if image is not None:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_gemini_response(prompt, image)
                st.session_state.msg.append({"role": "assistant", "content": response})
                st.write(response)
    else:
        with st.chat_message("assistant"):
            response = "Please upload an image first so I can analyze it."
            st.session_state.msg.append({"role": "assistant", "content": response})
            st.write(response)