import streamlit as st
from groq import Groq
import re
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("DEEPSEEK_KEY"))

# App Title & Subtitle
st.title("IslamicSeek")
st.subheader("Created with DeepSeek-R1")

st.write("")

# Create input & button layout
col1, col2 = st.columns([4, 1])  # Adjust width ratio as needed

with col1:
    user_input = st.text_input(label="Ask Anything..!", label_visibility="collapsed", key="user_input", placeholder="Type your question here...")

with col2:
    send_button = st.button("Send", use_container_width=True)

# Only process when the button is clicked and input is not empty
if send_button and user_input:
    # Create a placeholder for status updates
    status_placeholder = st.empty()

    with status_placeholder.status("🔍 Researching Islamic sources...", expanded=True) as status:
        st.write("Consulting Quranic verses...")
        st.write("Reviewing Hadith collections...")

        # API Call
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{
                "role": "system",
                "content": """You are an Islamic scholar answering questions **only** related to Islam, the Quran, Hadith, and Islamic teachings. 

If a question is unrelated to Islam, **politely refuse** to answer and ask the user to ask something relevant. 
Do not provide answers on other topics such as politics, entertainment, science, or general knowledge.

Provide direct answers from Quran and Hadith without:
1. Internal monologue
2. Thinking phrases
3. Processing disclaimers."""
            }, {
                "role": "user",
                "content": user_input
            }],
            temperature=0.6,
            max_tokens=4096,
            top_p=0.95,
            stream=False,
        )

        # Get full response
        full_response = completion.choices[0].message.content

        # Remove unnecessary processing phrases
        filtered_response = re.sub(
            r'<think>.*?</think>|\(internal.*?\)|\[analysis\]', 
            '', 
            full_response, 
            flags=re.IGNORECASE | re.DOTALL
        )

        status.update(label="✅ Answer Prepared", state="complete", expanded=False)

    # Clear the status after response is displayed
    status_placeholder.empty()

    # Display response
    st.markdown("### Answer:")
    st.markdown(filtered_response)
