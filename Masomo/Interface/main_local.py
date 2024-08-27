import streamlit as st
import random
import time

from response_logic import response_logic

# Streamed response emulator
def response_generator():
    response = response_logic
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("We!Masomo Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})





# st.connection("pets_db", type="sql")
# conn = st.connection("sql")
# conn = st.connection("snowflake")

# class MyConnection(BaseConnection[myconn.MyConnection]):
#     def _connect(self, **kwargs) -> MyConnection:
#         return myconn.connect(**self._secrets, **kwargs)
#     def query(self, query):
#         return self._instance.query(query)

####################################################

# # Replace any single element.
# element = st.empty()
# element.line_chart(...)
# element.text_input(...)  # Replaces previous.

# # Insert out of order.
# elements = st.container()
# elements.line_chart(...)
# st.write("Hello")
# elements.text_input(...)  # Appears above "Hello".

# st.help(pandas.DataFrame)
# st.get_option(key)
# st.set_option(key, value)
# st.set_page_config(layout="wide")
# st.query_params[key]
# st.query_params.from_dict(params_dict)
# st.query_params.get_all(key)
# st.query_params.clear()
# st.html("<p>Hi!</p>")


###################################################

# # Insert a chat message container.
# with st.chat_message("user"):
#     st.write("Hello 👋")
#     st.line_chart(np.random.randn(30, 3))

# # Display a chat input widget at the bottom of the app.
# >>> st.chat_input("Say something")

# # Display a chat input widget inline.
# with st.container():
#     st.chat_input("Say something")

###################################################

# st.button("Click me")
# st.download_button("Download file", data)
# st.feedback("thumbs")
# st.link_button("Go to gallery", url)
# st.page_link("app.py", label="Home")
# st.data_editor("Edit data", data)
# st.checkbox("I agree")
# st.toggle("Enable")
# st.radio("Pick one", ["cats", "dogs"])
# st.selectbox("Pick one", ["cats", "dogs"])
# st.multiselect("Buy", ["milk", "apples", "potatoes"])
# st.slider("Pick a number", 0, 100)
# st.select_slider("Pick a size", ["S", "M", "L"])
# st.text_input("First name")
# st.number_input("Pick a number", 0, 10)
# st.text_area("Text to translate")
# st.date_input("Your birthday")
# st.time_input("Meeting time")
# st.file_uploader("Upload a CSV")
# st.camera_input("Take a picture")
# st.color_picker("Pick a color")
