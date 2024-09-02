import streamlit as st
import time
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


from streamlit_option_menu import option_menu # type: ignore

# 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
EXAMPLE_NO = 2

st.title("We!Masomo Search Assistant")
st.markdown('\U0001F4AC Q&A Bot: ask health questions <br> \U0001F4DA Text Simplifier: make your health texts shorter', unsafe_allow_html=True)


def streamlit_menu(example=2):
    # if example == 1:
    #     # 1. as sidebar menu
    #     with st.sidebar:
    #         selected = option_menu(
    #             menu_title="Main Menu",  # required
    #             options=["Home", "Projects", "Contact"],  # required
    #             icons=["house", "book", "envelope"],  # optional
    #             menu_icon="cast",  # optional
    #             default_index=0,  # optional
    #         )
    #     return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Q&A Bot", "Text Simplifier"],  # required
            icons=["chat-heart", "highlighter"],  # optional
            menu_icon="emoji-smile",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                # "container": {"padding": "0!important", "background-color": "#eeeeee"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#salmon",
                },
                "nav-link-selected": {"background-color": "salmon"},
            }
        )
        return selected

    # if example == 3:
    #     # 2. horizontal menu with custom style
    #     selected = option_menu(
    #         menu_title=None,  # required
    #         options=["Home", "Projects", "Contact"],  # required
    #         icons=["house", "book", "envelope"],  # optional
    #         menu_icon="cast",  # optional
    #         default_index=0,  # optional
    #         orientation="horizontal",
    #         styles={
    #             "container": {"padding": "0!important", "background-color": "#fafafa"},
    #             "icon": {"color": "orange", "font-size": "25px"},
    #             "nav-link": {
    #                 "font-size": "25px",
    #                 "text-align": "left",
    #                 "margin": "0px",
    #                 "--hover-color": "#eee",
    #             },
    #             "nav-link-selected": {"background-color": "green"},
    #         },
    #     )
    #     return selected


selected = streamlit_menu(example=EXAMPLE_NO)


####################################################################################3

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
        from response_logic import response_generator
        response_placeholder = st.empty()  # Create a placeholder for the response
        response = response_generator(prompt)
        response_text = ""
        for word in response:
            response_text += word
            response_placeholder.markdown(response_text)
            time.sleep(0.05)  # Simulate streaming delay

        st.session_state.messages.append({"role": "assistant", "content": response_text})
