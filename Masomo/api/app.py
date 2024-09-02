from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Masomo.model.summarizer import Summarizer
from Masomo.model.qa_model import QuestionAnsweringModel
import pandas as pd


app = FastAPI()
summarizer = Summarizer()

# Load your CSV file into a DataFrame
df = pd.read_csv('raw_data/database.csv')

@app.on_event("startup")
def load_model():
    app.state.summarizer = Summarizer()


@app.get('/')
def index():
 return {'greeting': 'wellcome to WeMasomo'}


@app.get("/summarize")
def summarize_text(query):
    try:
        summary = summarizer.summarize_text(query)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
