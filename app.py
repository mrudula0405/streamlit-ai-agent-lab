
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Page configuration
st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered"
)

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY", "")

# Application heading
st.title("🤖 AI Agent with Input Validation")
st.write("Ask a question and get an AI-generated answer.")

# Input field
question = st.text_input(
    "Enter your question:",
    max_chars=201,
    placeholder="Example: Explain Artificial Intelligence"
)

# Submit button
if st.button("Submit", type="primary"):

    # Input validation
    if not question.strip():
        st.warning("Please enter a valid question.")

    elif question.strip().isdigit():
        st.warning("Please enter a question, not only numbers.")

    elif not any(char.isalpha() for char in question):
        st.warning("Your question must contain at least one letter.")

    elif len(question.strip()) < 3:
        st.warning("Your question must contain at least 3 characters.")

    elif len(question) > 200:
        st.warning("Your question must not exceed 200 characters.")

    else:
        st.success("Question accepted!")

        # Generate AI response
        if not api_key:
            try:
                api_key = st.secrets["GOOGLE_API_KEY"]
            except (KeyError, FileNotFoundError):
                api_key = ""

        if not api_key:
            st.error(
                "API key not configured. Add GOOGLE_API_KEY "
                "to your local .env file or cloud secrets."
            )
        else:
            try:
                client = genai.Client(api_key=api_key)

                with st.spinner("AI is generating your answer..."):
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=question
                    )

                st.subheader("🤖 AI Response")
                st.write(response.text)

            except Exception as e:
                st.error(f"Unable to generate a response: {e}")
