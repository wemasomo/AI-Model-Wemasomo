import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset # type: ignore
import torch
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics.pairwise import cosine_similarity




# Define a custom cleaning function
def clean_text(text):
    """Clean the input text."""
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = ''.join(char for char in text if not char.isdigit())  # Remove numbers
    text = text.lower()  # Convert to lowercase
    text = ' '.join(text.split())  # Remove extra spaces

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])

    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

    return text

# Create a custom transformer for text cleaning
class TextCleaner(FunctionTransformer):
    def __init__(self, *args, **kwargs):
        super().__init__(func=None, validate=False, *args, **kwargs)

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        return np.array([clean_text(text) for text in X])

# Create a pipeline with cleaning and vectorization

df = pd.read_csv('raw_data/output_summaries.csv')

def fit_model():
    pipeline = Pipeline([
        ('cleaner', TextCleaner()),  # Cleaning step
        ('vectorizer', TfidfVectorizer(max_df=0.12))  # Vectorization step
    ])

    # Fit the pipeline and transform the 'text' column
    X = pipeline.fit_transform(df['text'])

    print("Feature names:", pipeline.named_steps['vectorizer'].get_feature_names_out())
    print("Transformed vectors:\n", X.toarray())

    # Save the pipeline to a file
    filename = 'text_processing_pipeline.sav'
    pickle.dump(pipeline, open(filename, 'wb'))
    return X

def new_vector(prompt):
    # Load the saved pipeline
    loaded_pipeline = pickle.load(open('text_processing_pipeline.sav', 'rb'))

    # Now you can use the loaded_pipeline to transform new data
    new_text = prompt
    new_vectors = loaded_pipeline.transform([new_text])

    # Calculate cosine similarity between new_text and all other texts
    X = fit_model()
    similarity_scores = cosine_similarity(new_vectors, X)

    # Get the indices of the top 3 most similar texts
    top_indices = similarity_scores.argsort()[0][-3:][::-1]

    # Get the summaries of the top 3 most similar texts and their scores
    results = []

    for index in top_indices:
        summary = df['summary'][index]
        #   website = df['link'][index]
        score = similarity_scores[0][index]
        results.append((summary, score))
    return results
