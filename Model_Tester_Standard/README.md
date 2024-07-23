# AI Model Tester

AI Model Tester is a simple Streamlit application that allows users to interact with and test various AI models from OpenAI and Anthropic. It provides a user-friendly interface to send prompts to different AI models and view their responses.

## Features

- Test multiple AI models including GPT-3.5, GPT-4, Claude-2, and Claude-3 variants
- Easy-to-use interface built with Streamlit
- Secure handling of API keys through environment variables
- Conversation history tracking

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-model-tester.git
   cd ai-model-tester
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Usage

1. Ensure your virtual environment is activated (if you're using one).

2. Run the Streamlit app:
   ```
   streamlit run 4o-Mini.py
   ```

3. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

4. Select an AI model from the dropdown menu.

5. Enter your message in the text area and click "Send".

6. View the AI's response and the conversation history.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This tool is for educational and testing purposes only. Ensure you comply with the terms of service of the AI providers (OpenAI and Anthropic) when using their models.