from fastapi import FastAPI, HTTPException
from Masomo.model.summarizer import Summarizer

app = FastAPI()
summarizer = Summarizer()


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
