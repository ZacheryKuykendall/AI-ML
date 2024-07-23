import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSearchAPIWrapper, SerpAPIWrapper
from langchain_community.tools import Tool
from langchain.agents import AgentType, create_react_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import traceback
from openai import OpenAIError

# Load environment variables
load_dotenv()

# Model selection function
def get_llm(model_name, temperature=0):
    return ChatOpenAI(model_name=model_name, temperature=temperature)

# Custom Search Tool with improved error handling
def custom_search(query: str) -> str:
    """Custom search function that combines results from multiple search engines."""
    print(f"Custom search called with query: {query}")  # Debug print
    results = []
    
    try:
        google_search = GoogleSearchAPIWrapper()
        google_results = google_search.run(query)
        results.append(f"Google Search Results:\n{google_results}")
    except Exception as e:
        results.append(f"Google Search failed: {str(e)}")
    
    try:
        serpapi_search = SerpAPIWrapper()
        serpapi_results = serpapi_search.run(query)
        results.append(f"SerpAPI Results:\n{serpapi_results}")
    except Exception as e:
        results.append(f"SerpAPI Search failed: {str(e)}")
    
    return "\n\n".join(results)

# Streamlit UI
st.title("Advanced AI Assistant with Enhanced Search")

# Model selection
model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo-16k"]
selected_model = st.selectbox("Select AI Model", model_options)

# Initialize LLM
llm = get_llm(selected_model)

# Initialize tools
search_tool = Tool(
    name="CustomSearch",
    func=custom_search,
    description="A powerful search tool that combines results from Google and SerpAPI. Use this for any questions about current events, facts, or information that might not be in your training data."
)
tools = [search_tool]

# Initialize memory
memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

# System template
system_template = """You are a helpful AI assistant with access to a powerful custom search engine. 
ALWAYS use the CustomSearch tool when asked about current events, recent information, or specific facts.
Do not rely on your training data for such information as it may be outdated.
Your CustomSearch tool provides the most up-to-date information.

Available tools: {tools}

Use the following format: