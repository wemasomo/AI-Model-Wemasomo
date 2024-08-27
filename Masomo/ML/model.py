from transformers import pipeline
import pandas as pd

def load_texts_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df['text'].tolist()

def save_summaries_to_csv(file_path, summaries):
    df = pd.DataFrame(summaries, columns=['summary'])
    df.to_csv(file_path, index=False)


def initialize_model():

    return pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_text(model, text):

    summary = model(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']
