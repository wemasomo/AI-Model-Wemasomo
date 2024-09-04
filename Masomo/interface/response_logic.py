# Import necessary libraries
import string
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, HTTPException  # type: ignore
from Masomo.model.qa_model import QuestionAnsweringModel

# Initialize FastAPI
app = FastAPI()

# Load the QA model and data
qa_model = QuestionAnsweringModel()
df = pd.read_csv('database.csv')
vectorizer = TfidfVectorizer()
text_vectors = vectorizer.fit_transform(df['text'])  # Fit the vectorizer on the text data

def find_most_relevant_text(prompt, text_vectors, texts):
    question_vec = vectorizer.transform([prompt])
    similarity_scores = cosine_similarity(question_vec, text_vectors).flatten()
    most_similar_index = similarity_scores.argmax()
    return texts.iloc[most_similar_index]

def get_index(prompt, text_vectors):
    question_vec = vectorizer.transform([prompt])
    similarity_scores = cosine_similarity(question_vec, text_vectors).flatten()
    most_similar_index = similarity_scores.argmax()
    return most_similar_index, similarity_scores[most_similar_index]

# Commented as it seems unused atm, most_similar_index can be extracted some other way



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
