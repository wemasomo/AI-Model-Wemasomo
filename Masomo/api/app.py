from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Masomo.model.summarizer import Summarizer
from Masomo.model.qa_model import QuestionAnsweringModel

app = FastAPI()
summarizer = Summarizer()
qa_model = QuestionAnsweringModel()

@app.on_event("startup")
def load_model():
    app.state.summarizer = Summarizer()
    app.state.qa_model = QuestionAnsweringModel()


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

#@app.get("/answer")
#def answer_question(question, text):
#    try:
#        answer = qa_model.answer_question(question, text)
#        return {"answer": answer}
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))
