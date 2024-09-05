import streamlit as st
import time
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import requests


logo_url = "https://www.wemasomo.com/_next/image?url=%2Fimg%2Flogo-text.png&w=384&q=75"

if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True

@st.dialog("Terms and Conditions")
def show_dialog():
    agree = st.checkbox("By checking this, you agree to our [Terms and Conditions](https://www.wemasomo.com/general-terms-and-conditions).")
    if agree:
        if st.button("Agree and continue"):
            st.session_state.show_welcome = False
            st.rerun()

if st.session_state.show_welcome:
    show_dialog()


st.markdown("""
    <div class="header" style="display: flex; justify-content: space-between; align-items: center;">
        <div style="flex: 1; text-align: left;">
            <h1>Health Assistant</h1>
            <h4>by We!Masomo</h4>
        </div>
        <div>
            <img src="https://www.wemasomo.com/img/logo-text.png" style="width: auto; height: 160px;"/>
        </div>
    </div>
    """, unsafe_allow_html=True)



st.markdown(
            """
            <div class="welcome-text">
                This tool provides two main features:
                <br><strong>\U0001F4AC Q&A Bot:</strong> Ask health-related questions and receive instant answers.
                <br><strong>\U0001F4DA Text Simplifier:</strong> Simplify complex health texts for easier understanding.
                <br><a href="https://www.wemasomo.com/contact" target="_blank" class="help-button">Help</a>
            </div>
            """,
            unsafe_allow_html=True
        )

CSS = """
.help-button {
    background-color: #1B4C9A20;
    padding: 0.5em;
    border-radius: 10px;
    text-align: center;
    margin-top: 1em;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
}
.st-emotion-cache-1rsyhoq a {
    color: #1B4C9A;
}
.help-button:hover {
    background-color: #C94A1960;
}
.welcome-text {
    background-color: #FFFFFF70;
    border-radius: 10px;
    padding: 1em;
}
h1 {
    color: #1B4C9A;
    padding: 0rem 0px 0.5rem;
}
h4 {
    color: #EA5B29;
    padding: 0rem 0px 1rem;
}
div[aria-label="dialog"]>button[aria-label="Close"] {
        display: none;
}
.stApp {
    background-color: #FFD8CC80;
}
.st-bw {
    height: 2.5rem;
    width: 50%;
}
.st-emotion-cache-jkfxgf {
    font-family: "Source Sans Pro", sans-serif;
}
.st-emotion-cache-4oy321 {
    background-color: #FFD8CC50;
}
.stChatMessage {
    padding-right: 1em;
}
.st-emotion-cache-4uzi61 {
    background: white;
    border: none;
}
.st-emotion-cache-bho8sy {
    background-color: #1B4C9A;
.st-emotion-cache-1ghhuty {
    background-color: #EA5B29;
}

"""


st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Q&A Bot", "Text Simplifier"])

with tab1:
    messages = st.container()
    # API base URL
    API_URL = "https://wemasomo-app-963445830256.europe-west10.run.app"  # Update when using a different host

    messages.chat_message("assistant").write("Hello! 👋 What do you want to talk about today?")

    # Accept user input
    if prompt := st.chat_input("What do you want to know more about?"):
        messages.chat_message("user").write(prompt)

        # Prepare headers (though GET doesn't usually need these)
        headers = {
            'accept': 'application/json',
        }

        # Send the GET request with the query parameter
        response = requests.get(f"{API_URL}/qa", params={'qa_prompt': prompt}, headers=headers)

        # Check the response status
        if response.ok:
            response_data = response.json()

            # Si el puntaje de la respuesta es mayor a 0.2, mostramos la respuesta
            if response_data.get('score', 0) > 0.2:
                # Extract the values from the JSON response
                response_text = response_data.get('response', '')
                summary_text = response_data.get('summary', '')
                link_text = response_data.get('link', '')

                # Combine the extracted values into a single string with each on a new line
                combined_text = f"**Short answer:** {response_text}  \n**On this topic:** {summary_text}  \n[**More info**]({link_text})"

                # Display the combined text in the chat interface
                messages.chat_message("assistant").markdown(combined_text, unsafe_allow_html=True)

            # Si el puntaje es menor a 0.2, mostramos el bloque de sugerencias
            else:
                with messages.chat_message("assistant").container():
                    st.write("We couldn't understand your question... \n Maybe you want to browse through these topics:")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.link_button("Cancer", "https://www.wemasomo.com/explore/cancer", use_container_width=True)
                        st.link_button("Contraception", "https://www.wemasomo.com/explore/contraception", use_container_width=True)
                        st.link_button("Endometriosis", "https://www.wemasomo.com/explore/endometriosis", use_container_width=True)
                        st.link_button("Male Specific Content", "https://www.wemasomo.com/explore/male%20specific%20content", use_container_width=True)
                        st.link_button("Sexually Transmitted Diseases", "https://www.wemasomo.com/explore/hiv", use_container_width=True)
                    with col2:
                        st.link_button("Menstruation", "https://www.wemasomo.com/explore/menstruation", use_container_width=True)
                        st.link_button("Mpox", "https://www.wemasomo.com/explore/mpox", use_container_width=True)
                        st.link_button("Parenting", "https://www.wemasomo.com/explore/parenting", use_container_width=True)
                        st.link_button("Pregnancy", "https://www.wemasomo.com/explore/pregnancy-guide", use_container_width=True)
                        st.link_button("Vaccination", "https://www.wemasomo.com/explore/vaccination", use_container_width=True)


#################################################################################################

with tab2:
    summary_box = st.container()

    # API base URL
    API_URL = "https://wemasomo-app-963445830256.europe-west10.run.app"  # Update when using a different host

    # Description
    summary_box.write("""
    This tool helps you understand and learn more about sexual health by providing concise summaries of the information you input.
    """)

    # User input for the text
    text = summary_box.text_area("Enter your text here")

    # Display the "Get Summary" button
    if summary_box.button("Get Summary"):
        if text:
            # Send a GET request to the summarization endpoint with query parameters
            response = requests.get(f"{API_URL}/summarize", params={"query": text})
            if response.ok:
                summary = response.json().get("summary")
                summary_box.write(summary)
            else:
                summary_box.write("Error retrieving summary.")
        else:
            summary_box.markdown("Please enter some text to get a summary.")



####################################################################################3
