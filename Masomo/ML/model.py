from transformers import pipeline

def initialize_model():

    return pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_text(model, text):

    summary = model(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']
