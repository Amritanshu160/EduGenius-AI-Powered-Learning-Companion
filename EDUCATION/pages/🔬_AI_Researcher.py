import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import os

# Load API keys from .env
load_dotenv()
serpapi_key = os.getenv("SERPAPI_API_KEY")

# Streamlit UI
st.set_page_config(page_title="AI Researcher", layout="wide", page_icon="🔬")
st.title("An AI-Researcher with Real-Time Search")

# Sidebar for Groq API key
st.sidebar.title("Settings")
groq_api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Default welcome message
if "msg3" not in st.session_state:
    st.session_state["msg3"] = [
        {"role": "assistant", "content": "Hi, I'm your AI Research Assistant. I dive deep into topics, analyze the latest findings, and synthesize insights from across the web to help you understand complex ideas clearly."}
    ]

# Display chat history
for msg in st.session_state.msg3:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask me something..."):
    st.session_state.msg3.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Setup LLM
        llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192", streaming=True)

        # Setup SerpAPI
        search = SerpAPIWrapper(
            serpapi_api_key=serpapi_key,
            params={
                "engine": "google",
                "hl": "en",
            }
        )

        # Search the web
        search_results = search.run(prompt)

        # Combine the search result into a nice prompt for LLM
        final_prompt = (
        f"You are an AI Research Assistant.\n"
        f"Your task is to conduct a thorough investigation based on the user's question using the following data obtained from web searches and available resources.\n\n"
        f"User Research Query: {prompt}\n\n"
        f"Collected Research Material:\n{search_results}\n\n"
        f"Based on the information provided:\n"
        f"- Synthesize the key ideas, findings, and trends from all sources\n"
        f"- Critically evaluate the information—point out agreements, contradictions, and uncertainties\n"
        f"- Identify any gaps or unexplored areas in the topic that need further investigation\n"
        f"- Use a clear and logical structure with headings or bullet points where appropriate\n"
        f"- Explain complex concepts in simple, easy-to-understand language\n"
        f"- Offer potential insights, implications, or future directions based on your analysis\n"
        f"- Ensure the response is thoughtful, well-organized, and not just a summary\n"
        f"- Do NOT include any system or model metadata, instructions, or code formatting in your answer\n"
        f"- Always include full direct URLs to the original sources in this exact format:\n"
        f"  Source: [Title of Source](full_URL_here)\n"
        f"- At the end, provide a 'Sources:' section listing all relevant URLs used in the research\n"
        f"- Never use shortened links or display only domain names"
        )


        with st.chat_message("assistant"):
            response = llm.invoke(final_prompt)
            
            # Extract just the content text from the response
            if hasattr(response, 'content'):
                clean_response = response.content
            else:
                clean_response = str(response)
            
            # Remove any remaining metadata strings if present
            clean_response = clean_response.split('additional_kwargs')[0].strip()
            
            st.session_state.msg3.append({"role": "assistant", "content": clean_response})
            st.write(clean_response)
            
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        st.session_state.msg3.append({"role": "assistant", "content": error_msg})
        st.chat_message("assistant").write(error_msg)