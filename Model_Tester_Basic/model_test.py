import streamlit as st
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize clients
openai_client = OpenAI(api_key=openai_api_key)
groq_client = Groq(api_key=groq_api_key)

def get_ai_response(prompt, provider, model, temperature=0.7):
    try:
        if provider == "OpenAI":
            response = openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return response.choices[0].message.content
        elif provider == "Groq":
            response = groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

st.title("AI Assistant with OpenAI and Groq Support")

# Provider selection
provider = st.selectbox("Select Provider", ["OpenAI", "Groq"])

# Model selection
if provider == "OpenAI":
    model_options = ["gpt-4o-mini", "gpt-4o"]
else:  # Groq
    model_options = ["llama2-70b-4096", "mixtral-8x7b-32768"]
model = st.selectbox("Select AI Model", model_options)

# Temperature slider
temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# File upload
uploaded_file = st.file_uploader("Choose a file", type=["txt"])
if uploaded_file is not None:
    file_contents = uploaded_file.read().decode("utf-8")
    st.write("File contents:")
    st.write(file_contents)

# User input
user_input = st.text_area("Enter your message:")

if st.button("Send"):
    if user_input:
        if uploaded_file:
            prompt = f"File contents:\n{file_contents}\n\nUser question: {user_input}"
        else:
            prompt = user_input
        
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt, provider, model, temperature)
        
        st.write("AI Response:")
        st.write(response)
    else:
        st.warning("Please enter a message.")