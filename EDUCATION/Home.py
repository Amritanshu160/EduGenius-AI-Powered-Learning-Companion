# Home.py
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Education App Suite",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 Education App Suite")
st.write("Welcome to the Education App Suite! Explore the following tools to enhance your learning and productivity.")

# App descriptions
st.subheader("Available Apps")
st.write("""
1. **Chat With PDF**: Interact with PDF documents by asking questions and extracting information.
2. **Maths Solver**: Solve complex mathematical problems step-by-step.
3. **Code Assistant**: Get help with coding problems and debug your code.
4. **Grammar Checker**: Check and improve the grammar of your text.
5. **Document and Text Summarizer**: Summarize long documents or text into concise points.
6. **Work With PDF and Word**: Edit, convert, and manage PDF and Word documents.
7. **Search Engine**: Perform advanced searches across documents and the web.
8. **Chat With Image**: Analyze and interact with images using AI.
9. **Pomodoro Timer**: Boost productivity with a Pomodoro timer for focused work sessions.
""")

# Navigation
st.sidebar.title("Navigation")
st.sidebar.write("Select an app from the sidebar to get started.")

# Footer
st.write("---")

st.write("Made with ❤️ by Amritanshu Bhardwaj")

st.write("© 2025 Education App Suite. All rights reserved.")
