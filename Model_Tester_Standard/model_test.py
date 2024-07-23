import os
import streamlit as st
from dotenv import load_dotenv
import openai
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import tiktoken

# Load environment variables
load_dotenv()

# Set up API clients
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_ai_response(model, prompt, temperature, max_tokens):
    try:
        if model.startswith("gpt"):
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content, response.usage.total_tokens
        elif model.startswith("claude"):
            response = anthropic.completions.create(
                model=model,
                prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
                temperature=temperature,
                max_tokens_to_sample=max_tokens
            )
            return response.completion, num_tokens_from_string(prompt + response.completion, "cl100k_base")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, 0

st.title("AI Model Tester")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Model selection
model = st.selectbox(
    "Select AI Model",
    ("gpt-3.5-turbo", "gpt-4", "gpt-4o", "gpt-4o-mini", "claude-2", "claude-3-opus-20240229", "claude-3-sonnet-20240229")
)

# Model parameter adjustment
col1, col2 = st.columns(2)
with col1:
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
with col2:
    max_tokens = st.slider("Max Tokens", 50, 500, 150, 50)

# File upload
uploaded_file = st.file_uploader("Choose a text file", type="txt")
if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    st.text_area("File Content", content, height=100)
    if st.button("Use File Content"):
        user_input = content
else:
    # User input
    user_input = st.text_area("Enter your message:")

if st.button("Send"):
    if user_input:
        with st.spinner("AI is thinking..."):
            response, tokens = get_ai_response(model, user_input, temperature, max_tokens)
        if response:
            st.text_area("AI Response:", value=response, height=300)
            st.info(f"Total tokens used: {tokens}")
            # Add user input and AI response to conversation history
            st.session_state.messages.append({"role": "user", "content": user_input, "tokens": num_tokens_from_string(user_input, "cl100k_base")})
            st.session_state.messages.append({"role": "assistant", "content": response, "tokens": tokens - num_tokens_from_string(user_input, "cl100k_base")})
    else:
        st.warning("Please enter a message or upload a file.")

# Display conversation history
st.subheader("Conversation History:")
for message in st.session_state.messages:
    st.text(f"{message['role'].capitalize()} (Tokens: {message['tokens']}): {message['content']}")

# Display total token usage
total_tokens = sum(message['tokens'] for message in st.session_state.messages)
st.info(f"Total tokens used in this conversation: {total_tokens}")