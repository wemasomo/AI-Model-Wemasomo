from files import load_texts_from_csv, save_summaries_to_csv
from registry import load_model

# Summarize a text
def summarize_text(model, text):

    summary = model(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']


if __name__ == "__main__":
    model = load_model()

    # Load texts
    texts = load_texts_from_csv('input_texts.csv')

    # Generarate summaries
    summaries = [summarize_text(model, text) for text in texts]

    # Save summaries
    save_summaries_to_csv('output_summaries.csv', summaries)
