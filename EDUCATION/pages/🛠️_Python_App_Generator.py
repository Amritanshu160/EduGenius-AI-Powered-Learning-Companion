import streamlit as st
import os
import zipfile
import io
import json
from google import genai

# Set up the page
st.set_page_config(page_title="AI App Builder", page_icon="🛠️", layout="wide")

client = genai.Client(api_key = "AIzaSyBWc7Ym6qMSo04uD-KtfT1JSin5AqhtyNg")


def generate_app_code(user_prompt):
    """
    Function to generate app code using Google Gemini based on user prompt
    """
    try:
        system_prompt = """
        You are an expert Streamlit developer. Your task is to generate complete Streamlit applications based on user requirements.
        
        For each request:
        1. Create a complete directory structure with all necessary files
        2. Include a main Python file (usually app.py or main.py)
        3. Include any additional files needed (CSS, assets, utils.py, etc.)
        4. Provide clear instructions on how to run the app
        5. Structure your response as JSON with the following format:
        
        {
            "directory_structure": {
                "folder_name": "name_of_main_folder",
                "files": {
                    "filename1.py": "file content here",
                    "subfolder/another_file.py": "content here",
                    "README.md": "instructions here"
                }
            },
            "instructions": "Brief instructions on how to run the app"
        }
        
        IMPORTANT: You must only respond with valid JSON. Do not include any markdown formatting or additional text.
        """
        
        # Gemini doesn't have system messages in the same way, so we prepend it
        full_prompt = f"{system_prompt}\n\nUser request: {user_prompt}"
        
        response = client.models.generate_content(
            model = "gemini-2.5-pro",
            contents = full_prompt
        )
        
        # Extract the JSON from Gemini's response
        generated_json = response.text
        
        # Gemini sometimes adds markdown formatting, so we clean it
        if generated_json.startswith("```json"):
            generated_json = generated_json[7:-3]  # Remove ```json and ```
        
        return json.loads(generated_json)
    
    except Exception as e:
        st.error(f"Error generating app code: {str(e)}")
        return None

def create_zip_file(directory_structure):
    """
    Create a zip file from the generated directory structure
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        folder_name = directory_structure.get("folder_name", "streamlit_app")
        files = directory_structure.get("files", {})
        
        for file_path, content in files.items():
            zip_file.writestr(f"{folder_name}/{file_path}", content)
    
    zip_buffer.seek(0)
    return zip_buffer

def display_directory_structure(directory_structure):
    """
    Display the generated directory structure in a user-friendly way
    """
    st.subheader("Generated App Structure")
    folder_name = directory_structure.get("folder_name", "streamlit_app")
    
    with st.expander(f"📁 {folder_name}"):
        files = directory_structure.get("files", {})
        for file_path in files:
            st.code(file_path, language="text")
            
        st.markdown("### Instructions")
        st.info(directory_structure.get("instructions", "No specific instructions provided."))

def display_file_content(directory_structure):
    """
    Display the content of selected files
    """
    files = directory_structure.get("files", {})
    if not files:
        st.warning("No files available to display.")
        return

    file_list = list(files.keys())
    selected_file = st.selectbox("Select a file to view", file_list)

    if selected_file:
        file_content = files.get(selected_file, "")
        st.subheader(f"📄 {selected_file}")

        if not file_content.strip():
            st.info("This file is empty.")
            return

        # Determine language for syntax highlighting
        file_extension = selected_file.split('.')[-1].lower()
        language_map = {
            'py': 'python',
            'md': 'markdown',
            'json': 'json',
            'css': 'css',
            'html': 'html',
            'js': 'javascript',
            'txt': 'text'
        }
        language = language_map.get(file_extension, 'text')

        st.code(file_content, language=language)


# Main app interface
st.title("🛠️ AI Streamlit App Builder")
st.markdown("Describe the app you want to build and our AI will generate the complete code for you!")

# User input
user_prompt = st.text_area(
    "Describe your Streamlit app:",
    value=st.session_state.get("user_prompt", ""),
    height=150,
    placeholder="e.g., 'I need a data visualization app that shows COVID-19 trends with interactive charts...'"
)


generate_button = st.button("Generate App", type="primary")

# Handle app generation
if generate_button and user_prompt:
    with st.spinner("🧠 Thinking... Generating your app code..."):
        generated_app = generate_app_code(user_prompt)
        if generated_app:
            # Store in session state
            st.session_state.generated_app = generated_app
            st.session_state.user_prompt = user_prompt

# Load from session if available
if "generated_app" in st.session_state:
    generated_app = st.session_state.generated_app
    directory_structure = generated_app.get("directory_structure", {})

    # Display app structure and contents
    display_directory_structure(directory_structure)
    display_file_content(directory_structure)

    # Prepare and display download button
    zip_buffer = create_zip_file(directory_structure)
    folder_name = directory_structure.get("folder_name", "streamlit_app")

    st.download_button(
        label="📥 Download Full App",
        data=zip_buffer,
        file_name=f"{folder_name}.zip",
        mime="application/zip",
        help="Download the complete app as a zip file"
    )


# Sidebar with examples
with st.sidebar:
    st.markdown("## Examples")
    example_prompts = [
        "A dashboard showing stock market trends with interactive charts",
        "An image classification app that identifies dog breeds",
        "A PDF text extractor and summarizer tool",
        "A personal finance tracker with data visualization",
        "A chatbot interface with response history"
    ]
    
    for example in example_prompts:
        if st.button(example, use_container_width=True):
            st.session_state.user_prompt = example
            st.rerun()
    
    st.markdown("---")
    st.markdown("### Tips for best results:")
    st.markdown("""
    - Be specific about features you want
    - Mention any particular charts or visualizations
    - Specify if you need data upload capabilities
    - Include any special requirements (auth, databases, etc.)
    """)

# If an example was clicked, update the text area
if 'user_prompt' in st.session_state:
    user_prompt = st.session_state.user_prompt