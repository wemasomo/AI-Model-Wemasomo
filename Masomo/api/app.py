from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Masomo.model.summarizer import Summarizer
from Masomo.model.qa_model import QuestionAnsweringModel
import pandas as pd

app = FastAPI()
summarizer = Summarizer()
qa_model = QuestionAnsweringModel()

# Load your CSV file into a DataFrame
df = pd.read_csv('raw_data/database.csv')

@app.on_event("startup")
def load_model():
    app.state.summarizer = Summarizer()
    app.state.qa_model = QuestionAnsweringModel()

class TextInput(BaseModel):
    content: str

class QuestionRequest(BaseModel):
    text: str
    question: str

@app.get('/')
def index():
    return {'greeting': 'welcome to WeMasomo'}

@app.get("/answer")
def answer_question(question: str, text: str):
    try:
        # Get the answer from the QA model
        answer = qa_model.answer_question(question, text)

        # Generate a summary of the text
        summary = summarizer.summarize_text(text)

        # Find the link for the given text
        matching_row = df[df['text'] == text]

        if not matching_row.empty:
            article_link = matching_row.iloc[0]['link']
        else:
            article_link = "No link available"

        return {"answer": answer, "summary": summary, "link": article_link}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
