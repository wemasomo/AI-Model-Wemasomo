import string
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import streamlit as st
from Masomo.model.qa_model import QuestionAnsweringModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

qa_model = QuestionAnsweringModel()
df = pd.read_csv('raw_data/database.csv')
vectorizer = TfidfVectorizer()

# Returns website pages
def website_content():
    with st.container():
        st.divider()
        st.write("We couldn't understand your question... \n Maybe you want to browse through these topics:")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.link_button("Cancer", "https://www.wemasomo.com/explore/cancer")
            st.link_button("Male Specific Content", "https://www.wemasomo.com/explore/male%20specific%20content")
            st.link_button("Pregnancy", "https://www.wemasomo.com/explore/pregnancy-guide")

        with col2:
            st.link_button("Contraception", "https://www.wemasomo.com/explore/contraception")
            st.link_button("Menstruation", "https://www.wemasomo.com/explore/menstruation")
            st.link_button("Vaccination", "https://www.wemasomo.com/explore/vaccination")

        with col3:
            st.link_button("Endometriosis", "https://www.wemasomo.com/explore/endometriosis")
            st.link_button("Mpox", "https://www.wemasomo.com/explore/mpox")

        with col4:
            st.link_button("Sexually Transmitted Diseases", "https://www.wemasomo.com/explore/hiv")
            st.link_button("Parenting", "https://www.wemasomo.com/explore/parenting")


def find_most_relevant_text(prompt, text_vectors, texts):
    question_vec = vectorizer.transform([prompt])
    similarity_scores = cosine_similarity(question_vec, text_vectors).flatten()
    most_similar_index = similarity_scores.argmax()
    return texts.iloc[most_similar_index]

def get_index(prompt, text_vectors):
    question_vec = vectorizer.transform([prompt])
    similarity_scores = cosine_similarity(question_vec, text_vectors).flatten()
    most_similar_index = similarity_scores.argmax()
    return most_similar_index

# Streamed response emulator
def response_generator(prompt, text_vectors, df):
    """Generate a response in a streamed manner."""
    # Get the most similar index
    most_similar_index = get_index(prompt, text_vectors)

    # Get the most relevant text using the index
    relevant_text = df.iloc[most_similar_index]['text']

    # Generate the response
    response = qa_model.answer_question(prompt, relevant_text)

    if response is not None:
        st.write(f"{df['summary'].iloc[most_similar_index]}")
    else:
        return website_content()


    # If the response is not a string, handle it differently
    if isinstance(response, str):
        for word in response.split():
            yield word + " "
            time.sleep(0.05)
    else:
        # Handle cases where response is not a string
        return response


# def question_keyword():
#   get prompt (user input),
#   remove stopwords,
#   extract keywords
#   compare keywords with keywords from the text database
#   if keyword match is succesful:
#       return summary + link
#       and return question: does that answer your question?
#           if yes: return "Good reading"
#           else: show 2 extra articles
#   else:
#       return "We couldnt understand your question.
#       You can ask a different question or browse through these topics (buttons to 10 categories)"


# _________________________________________________________________________________________________________

# def response_logic_mockup(prompt):
#     """Generate a mockup response based on keywords in the prompt."""

#     fake_dict = {'Endometriosis': "Endometriosis is a disease in which tissue similar to the lining of the uterus grows outside the uterus. It can cause severe pain in the pelvis and make it harder to get pregnant. Endometriosis can start at a person’s first menstrual period and last until menopause. With endometriosis, tissue similar to the lining of the uterus grows outside the uterus. This leads to inflammation and scar tissue forming in the pelvic region and (rarely) elsewhere in the body \n https://www.wemasomo.com/explore/endometriosis/endometriosis",
#                  'Period': 'The Menstrual Cycle is the time from the first day of a woman’s period bleeding to the day before her next period. The length of the menstrual cycle varies from woman to woman, but the average is to have periods every 28 days. Regular menstrual cycles that are longer or shorter than this, from 21 to 40 days, are normal. \n https://www.wemasomo.com/explore/menstruation/menstrual-cycle',
#                  'STI': 'HIV and AIDS education has been part of the school curriculum in Kenya since 2003. However, a study shows that only 54% of young women and 64% of young men (aged 15-24) had comprehensive knowledge about HIV prevention.\n https://www.wemasomo.com/explore/hiv/HIV%20Prevention%20Measurements'}

#     # Return mockup response based on detected keywords
#     if 'endometriosis' in prompt:
#         return fake_dict['Endometriosis']
#     elif 'period' in prompt:
#         return fake_dict['Period']
#     elif 'hiv' in prompt:
#         return fake_dict['STI']
#     else:
#         return website_content()


# _________________________________________________________________________________________________________

# def response_logic(prompt):
#     """Process the prompt with response logic."""
#     results = qa_model.answer_question(prompt)
#     # if results[0][1] > 0.2:
#     #     st.write(f"{results[0][0]}\nRead more: {results[0][1]}")
#     #     # with st.container():
#     #     #     st.write("Did you find what you were looking for?")
#     #     #     st.button('no')
    #     #     st.button('yes')
    #         # if selected == 1:
    #         #     st.markdown(f"Have a good read!")
    #         # else:
    #         #     print(f"Maybe these other articles will answer your question: \n{results[1][0]}\nRead more: {results[1][1]}\n{results[2][0]}\nRead more: {results[2][1]}")
    # else:
    #     return website_content
