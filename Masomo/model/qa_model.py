import pandas as pd
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class QuestionAnsweringModel:
    def __init__(self, model_name="deepset/roberta-base-squad2"):
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def find_most_relevant_text(self, question, df):
        texts = df['Text'].tolist()
        texts.append(question)
        vectorizer = TfidfVectorizer().fit_transform(texts)
        vectors = vectorizer.toarray()
        cosine_similarities = cosine_similarity([vectors[-1]], vectors[:-1]).flatten()
        best_index = cosine_similarities.argmax()
        return df['Text'].iloc[best_index]

    def answer_question(self, question, context):
        result = self.qa_pipeline(question=question, context=context)
        return result['answer']
