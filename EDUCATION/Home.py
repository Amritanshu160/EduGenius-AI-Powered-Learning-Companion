import streamlit as st

# Page configuration
st.set_page_config(
    page_title="EduGenius",
    page_icon="🎓",
    layout="wide"
)

# Title and intro
st.title("🎓 EduGenius - Your AI-Powered Education Companion")
st.write("Welcome to EduGenius! Explore categorized tools designed to enhance your learning, productivity, and creativity.")

st.markdown("---")

# Learning Tools
with st.expander("📚 Learning Tools"):
    st.markdown("**📁 Chat With Multiple Files**: Interact with PDF, Word, and PPT files by asking questions and extracting information.")
    st.markdown("**📄 Text Summarizer**: Summarize long documents or text into concise points.")
    st.markdown("**📚 AI MCQs Generator**: Generate MCQs from text, files, YouTube videos, or audio.")
    st.markdown("**📋 AI Qs Paper Generator**: Generate Qs papers from text, files, YouTube videos, or audio.")
    st.markdown("**🤖 AI Content Teacher**: Explain content in multiple languages.")
    st.markdown("**🌐 Search Engine**: Perform advanced searches across the web.")
    st.markdown("**🔬 AI Researcher**: An AI-powered assistant that conducts in-depth research, analyzes web data, and delivers clear, insightful answers with sources.")
    st.markdown("**🖼️ Chat With Image**: Analyze and interact with images using AI.")

# Productivity Tools
with st.expander("⏱️ Productivity Tools"):
    st.markdown("**⏲️ Pomodoro Timer**: Boost productivity with focused Pomodoro sessions.")
    st.markdown("**🔄 File Converter**: Convert and merge PDFs, Word docs, PPTs, and images.")
    st.markdown("**✂️ Page Extractor**: Extract selected pages from PDF and content from selected word files.")
    st.markdown("**📊 Text To PPT**: Generate PowerPoint presentations instantly from a text prompt.")
    st.markdown("**📑 Files To PPT**: Generate PPTs from multiple files by extracting text from them.")

# Code & Writing Tools
with st.expander("💻 Code & Writing Tools"):
    st.markdown("**➗ Maths Solver**: Solve complex mathematical problems step-by-step.")
    st.markdown("**💻 Code Assistant**: Get help with coding problems and debug your code.")
    st.markdown("**📝 Grammar Checker**: Check and improve the grammar of your text.")
    st.markdown("**🛠️ Python App Generator**: Generate full Python apps from a text prompt.")

# Navigation
st.sidebar.title("Navigation")
st.sidebar.write("Select an app from the sidebar to get started.")

st.write("---")

st.write("Made with ❤️ by Amritanshu Bhardwaj")

st.write("© 2025 EduGenius. All rights reserved.")

