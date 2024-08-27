import pandas as pd

def load_texts_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df['text'].tolist()

def save_summaries_to_csv(file_path, summaries):
    df = pd.DataFrame(summaries, columns=['summary'])
    df.to_csv(file_path, index=False)
