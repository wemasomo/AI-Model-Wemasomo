import streamlit as st
import time
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

st.title("We!Masomo Search Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Start chat with Hello
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": "Hello! \n What do you want to talk about today?"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What do you want to know more about?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response in chat message container
    with st.chat_message("assistant"):
        from response_logic import response_generator
        response_placeholder = st.empty()  # Create a placeholder for the response
        response = response_generator(prompt)
        response_text = ""
        for word in response:
            response_text += word
            response_placeholder.markdown(response_text)
            time.sleep(0.05)  # Simulate streaming delay

        st.session_state.messages.append({"role": "assistant", "content": response_text})
