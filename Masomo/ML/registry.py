from transformers import pipeline

# Load the model
def load_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")
