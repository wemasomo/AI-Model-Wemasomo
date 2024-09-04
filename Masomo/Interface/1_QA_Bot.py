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

CSS = """
.stApp {
    background-color: #FFD8CC;
}

.st-bw {
    height: 2.5rem;
    width: 50%;
}

.st-emotion-cache-jkfxgf {
    font-family: "Source Sans Pro", sans-serif;
}

.st-emotion-cache-4uzi61 {
    background-color: white
}

.stChatMessage {
    background-color: #FFD8CC
}


#tabs-bui1-tab-0 {

}
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Q&A Bot", "Shortener"])

# Conditional rendering based on selected option
with tab1:
    messages = st.container(border=True)
    # API base URL
    API_URL = "http://localhost:8000"  # Update when using a different host

    messages.chat_message("assistant").write("Hello! \U0001F44B What do you want to talk about today?")
    # Accept user input
    if prompt := st.chat_input("What do you want to know more about?"):
        messages.chat_message("user").write(prompt)
        # Add user message to chat history
        # st.session_state.messages.append({"role": "user", "content": prompt})

        # # Display user message in chat message container
        # with st.chat_message("user"):
        #     st.markdown(prompt)

        # Generate and display assistant response in chat message container
        # with st.chat_message("assistant"):
        # response_placeholder = st.empty()  # Create a placeholder for the response
        response = requests.post(f"{API_URL}/qa",  json={"prompt": prompt})
            # if response.ok:
            #     answer = response.json().get("answer")


            ######## IS THIS WHAT I'M SUPPOSED TO DO??? ########
        if response.json().get('score') > 0.2:
            messages.chat_message("assistant").write(response.json())
        else:
            with messages.chat_message("assistant").container():
                st.write("We couldn't understand your question... \n Maybe you want to browse through these topics:")
                col1, col2 = st.columns(2)
                with col1:
                    st.link_button("Cancer", "https://www.wemasomo.com/explore/cancer", use_container_width=True)
                    st.link_button("Contraception", "https://www.wemasomo.com/explore/contraception", use_container_width=True)
                # with col2:
                    st.link_button("Endometriosis", "https://www.wemasomo.com/explore/endometriosis", use_container_width=True)
                    st.link_button("Sexually Transmitted Diseases", "https://www.wemasomo.com/explore/hiv", use_container_width=True)
                    st.link_button("Male Specific Content", "https://www.wemasomo.com/explore/male%20specific%20content", use_container_width=True)
                with col2:
                    st.link_button("Menstruation", "https://www.wemasomo.com/explore/menstruation", use_container_width=True)
                    st.link_button("Mpox", "https://www.wemasomo.com/explore/mpox", use_container_width=True)
                    st.link_button("Parenting", "https://www.wemasomo.com/explore/parenting", use_container_width=True)
                    st.link_button("Pregnancy", "https://www.wemasomo.com/explore/pregnancy-guide", use_container_width=True)
                    st.link_button("Vaccination", "https://www.wemasomo.com/explore/vaccination", use_container_width=True)


            # response = qa_endpoint(prompt)
            # response_text = ""
            # for word in response:
            #     response_text += word
            #     response_placeholder.markdown(response_text)
            #     time.sleep(0.05)  # Simulate streaming delay

            # st.session_state.messages.append({"role": "assistant", "content": response})

#################################################################################################

with tab2:
    summary_box = st.container()

    # API base URL
    API_URL = "http://localhost:8000"  # Update when using a different host

    # Description
    summary_box.write("""
    This tool helps you understand and learn more about sexual health by providing concise summaries of the information you input.
    """)

    # User input for the text
    text = summary_box.text_area("Enter Your Text Here")

    if text:
        if summary_box.button("Get Summary"):
            # Send a GET request to the summarization endpoint
            response = requests.get(f"{API_URL}/summarize", params={"query": text})
            if response.ok:
                summary = response.json().get("summary")
                summary_box.write(summary)
            else:
                summary_box.write("Error retrieving summary.")
    else:
        summary_box.markdown("Please enter some text to get a summary.")


####################################################################################3
