import streamlit as st
import requests

# API base URL
API_URL = "http://localhost:8000"  # Update if using a different host or port

# Application title
st.title("WeMasomo Health Assistant")

# Description
st.write("""
Welcome to the WeMasomo Health Assistant! This tool helps you understand and learn more about sexual health.

1. **Summarize Text:** Get a quick summary of any provided text.
2. **Ask Questions:** Ask specific questions and receive answers based on the provided text.

Enter your text below and choose what you want to do.
""")

# User input for the text
text = st.text_area("Enter Your Text Here", "Type or paste your text about sexual health here.")

# Functionality selection
if text:
    option = st.selectbox("Choose an Option", ("Select an option", "Summarize Text", "Ask Questions"))

    if option == "Summarize Text":
        if st.button("Get Summary"):
            response = requests.get(f"{API_URL}/summarize", params={"query": text})
            if response.ok:
                summary = response.json().get("summary")
                st.write("**Summary:**", summary)
            else:
                st.write("Error retrieving summary.")

    elif option == "Ask Questions":
        question = st.text_input("Enter Your Question Here", "Type your question about sexual health here.")

        if st.button("Get Answer"):
            if question:
                response = requests.get(f"{API_URL}/answer", params={"text": text, "question": question})
                if response.ok:
                    answer = response.json().get("answer")
                    st.write("**Answer:**", answer)
                else:
                    st.write("Error retrieving answer.")
            else:
                st.write("Please enter your question.")
else:
    st.write("Please enter some text or a question to get started.")
