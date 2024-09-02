import streamlit as st
import requests

# API base URL
API_URL = "http://localhost:8000"  # Update if using a different host or port

# Application title
st.title("We!Masomo Health Assistant")

# Description
st.write("""
Welcome to the We!Masomo Health Assistant! This tool helps you understand and learn more about sexual health by providing concise summaries of the information you input.

**Summarize Text:** Get a quick summary of any provided text.

Enter your text below to get started.
""")

# User input for the text
text = st.text_area("Enter Your Text Here", "Type or paste your text about sexual health here.")

if text:
    if st.button("Get Summary"):
        # Send a GET request to the summarization endpoint
        response = requests.get(f"{API_URL}/summarize", params={"query": text})
        if response.ok:
            summary = response.json().get("summary")
            st.write("**Summary:**", summary)
        else:
            st.write("Error retrieving summary.")
else:
    st.write("Please enter some text to get a summary.")
