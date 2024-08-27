import os
import pandas as pd

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load CSV file
def load_texts_from_csv(filename):
    file_path = os.path.join(BASE_DIR, 'data', filename)
    df = pd.read_csv(file_path)
    return df['text'].tolist()

# Save summaries in CSV
def save_summaries_to_csv(filename, summaries):
    file_path = os.path.join(BASE_DIR, 'data', filename)
    df = pd.DataFrame(summaries, columns=['summary'])
    df.to_csv(file_path, index=False)
