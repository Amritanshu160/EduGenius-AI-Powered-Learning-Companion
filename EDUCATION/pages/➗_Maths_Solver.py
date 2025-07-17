import streamlit as st
from google import genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load API Key from environment variables
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="Maths Solver",layout="wide", page_icon="➗")

def extract_text_from_image_gemini(image):
    # Send image to Gemini Pro Vision
    response = client.models.generate_content(
        model= "gemini-2.5-flash",
        contents= [image, "Extract the text from this image."]
    )
    return response.text.strip() if response.text else "No text detected."

def solve_math_problem(text_input):
    """Sends the math problem to Gemini AI for solving"""
    prompt = f"Solve this math problem step by step and provide detailed step by step easy to understand explanation of the approach used to solve the problem:{text_input}"
    response = client.models.generate_content(
        model= "gemini-2.5-pro",
        contents = prompt
    )
    return response.text

# Streamlit UI
st.title("Math Problem Solver using Gemini AI")

input_type = st.radio("Select Input Type:", ("Text", "Image"))

if input_type == "Text":
    text_problem = st.text_area("Enter your math problem:")
    if st.button("Solve") and text_problem:
        solution = solve_math_problem(text_problem)
        st.success(solution)

elif input_type == "Image":
    uploaded_file = st.file_uploader("Upload an image of the math problem", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Extract & Solve"):
            extracted_text = extract_text_from_image_gemini(image)

            if extracted_text:
                st.write("Extracted Text:", extracted_text)
                solution = solve_math_problem(extracted_text)
                st.success(solution)
            else:
                st.error("No text could be extracted from the image. Try a clearer image.")



