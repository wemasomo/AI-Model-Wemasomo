
from fastapi import FastAPI, Form
from pydantic import BaseModel
from Masomo.model.summarizer import Summarizer

app = FastAPI()
summarizer = Summarizer()

#app.state.model = model

class TextInput(BaseModel):
    content: str

@app.get('/')
def index():
    return {'greeting': 'wellcome to WeMasomo'}

@app.post("/summarize")
def summarize(content: str = Form(...)):
    summary = summarizer.summarize_text(content)
    return {"summary": summary}
