import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import os

# Load API keys from .env
load_dotenv()
serpapi_key = os.getenv("SERPAPI_API_KEY")

# Streamlit UI
st.set_page_config(page_title="Search Chatbot", layout="wide", page_icon="🌐")
st.title("LangChain Chatbot with Real-Time Search")

# Sidebar for Groq API key
st.sidebar.title("Settings")
groq_api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Default welcome message
if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot that can search the web. Ask me anything!"}
    ]

# Display chat history
for msg in st.session_state.message:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask me something..."):
    st.session_state.message.append({"role": "user", "content": prompt})
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
            f"You are a helpful assistant.\n"
            f"Based on the following information from a web search, answer the user's question.\n\n"
            f"User Question: {prompt}\n\n"
            f"Search Information:\n{search_results}\n\n"
            f"Please provide a clean answer with these characteristics:\n"
            f"- Write in simple, conversational language\n"
            f"- Format the response with proper paragraphs and spacing\n"
            f"- Include bullet points for lists\n"
            f"- Only return the response content, no metadata or additional formatting"
            f"- Always include the full direct URLs to sources in this exact format:\n"
            f"  Source: [Title of Source](full_URL_here)\n"
            f"- List all relevant URLs at the end of your response under 'Sources:'\n"
            f"- Never hide URLs behind shortened links or just show domain names\n"
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
            
            st.session_state.message.append({"role": "assistant", "content": clean_response})
            st.write(clean_response)
            
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        st.session_state.message.append({"role": "assistant", "content": error_msg})
        st.chat_message("assistant").write(error_msg)
