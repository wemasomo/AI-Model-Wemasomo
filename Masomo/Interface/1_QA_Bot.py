import streamlit as st
import time
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from streamlit_option_menu import option_menu # type: ignore
import requests

st.title("We!Masomo Health Assistant")
st.markdown('\U0001F4AC Q&A Bot: ask health questions <br> \U0001F4DA Text Simplifier: make your health texts shorter', unsafe_allow_html=True)


def main():
    selected = option_menu(
        menu_title=None,  # No menu title
        options=["Q&A Bot", "Text Simplifier"],  # Menu options
        icons=["chat-heart", "highlighter"],  # Icons for the options
        menu_icon="emoji-smile",  # Icon for the menu
        default_index=0,  # Default selected option
        orientation="horizontal",  # Horizontal orientation
        styles={
            "icon": {"color": "#1B4C9A", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "--hover-color": "#FFD8CC",
            },
            "nav-link-selected": {"background-color": "#EA5B29"},
        }
    )

    # Conditional rendering based on selected option
    if selected == "Q&A Bot":

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Start chat with Hello
        if not st.session_state.messages:
            st.session_state.messages.append({"role": "assistant", "content": "Hello! \U0001F44B What do you want to talk about today?"})

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
                from Masomo.Interface.response_logic import response_generator
                response_placeholder = st.empty()  # Create a placeholder for the response
                response = response_generator(prompt)
                response_text = ""
                for word in response:
                    response_text += word
                    response_placeholder.markdown(response_text)
                    time.sleep(0.05)  # Simulate streaming delay

                st.session_state.messages.append({"role": "assistant", "content": response_text})

#################################################################################################

    elif selected == "Text Simplifier":
        # API base URL
        API_URL = "http://localhost:8000"  # Update when using a different host

        # Description
        st.write("""
        This tool helps you understand and learn more about sexual health by providing concise summaries of the information you input.
        """)

        # User input for the text
        text = st.text_area("Enter Your Text Here")

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
            st.markdown("Please enter some text to get a summary.")

if __name__ == "__main__":
    main()


####################################################################################3
