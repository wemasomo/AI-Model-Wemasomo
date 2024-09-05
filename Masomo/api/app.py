from fastapi import FastAPI, HTTPException, Query
from Masomo.model.summarizer import Summarizer
from Masomo.model.qa_model import QuestionAnsweringModel
from Masomo.interface.response_logic import get_index, text_vectors
import pandas as pd
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
summarizer = Summarizer()
qa_model = QuestionAnsweringModel()
df = pd.read_csv('Masomo/interface/database.csv')

@app.on_event("startup")
def load_model():
    app.state.summarizer = Summarizer()
    app.state.qa_model = QuestionAnsweringModel()

@app.get('/')
def index():
 return {'greeting': 'welcome to WeMasomo'}

@app.get("/summarize")
def summarize_text(query):
    try:
        summary = summarizer.summarize_text(query)
        print(summary)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class QAPrompt(BaseModel):
    prompt: str

@app.get("/qa")
def qa_endpoint(qa_prompt: Optional[str] = Query(None, description="Question to be answered")):
    try:
        # Verifica que el prompt no esté vacío
        if not qa_prompt:
            raise HTTPException(status_code=400, detail="qa_prompt parameter is required")

        # Procesa el prompt y genera una respuesta
        prompt = qa_prompt
        most_similar_index, max_score = get_index(prompt, text_vectors)
        relevant_text = df.iloc[most_similar_index]['text']
        link = df.iloc[most_similar_index]['link']
        summary = df['summary'].iloc[most_similar_index]

        print('👩‍🦯', most_similar_index)
        print('🏌️‍♀️', relevant_text)
        print('👱‍♀️', max_score)

        response = qa_model.answer_question(prompt, relevant_text)

        # Retorna la respuesta, el resumen y el enlace
        return {"response": response, "summary": summary, "link": link, "score": max_score}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
