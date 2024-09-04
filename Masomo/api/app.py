from fastapi import FastAPI, HTTPException  # type: ignore
from Masomo.model.summarizer import Summarizer
from Masomo.model.qa_model import QuestionAnsweringModel
from Masomo.interface.response_logic import get_index, text_vectors
import pandas as pd
from pydantic import BaseModel

app = FastAPI()
summarizer = Summarizer()
qa_model = QuestionAnsweringModel()
df = pd.read_csv('raw_data/database.csv')

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

# API endpoint to handle Q&A
@app.post("/qa/")
def qa_endpoint(qa_prompt: QAPrompt):
    prompt = qa_prompt.prompt
    try:
        # Generate a response
        most_similar_index, max_score = get_index(prompt, text_vectors)
        relevant_text = df.iloc[most_similar_index]['text']
        print('👩‍🦯',most_similar_index)
        print('🏌️‍♀️',relevant_text)
        print('👱‍♀️',max_score)
        response = qa_model.answer_question(prompt, relevant_text)
        link = df.iloc[most_similar_index]['link']


        summary = df['summary'].iloc[most_similar_index]
        return {"response": response, "summary": summary, "link": link, "score": max_score}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


        # if text:
        #     if st.button("Get Summary"):
        #         # Send a GET request to the summarization endpoint
        #         response = requests.get(f"{API_URL}/summarize", params={"query": text})
        #         if response.ok:
        #             summary = response.json().get("summary")
        #             st.write("**Summary:**", summary)
        #         else:
        #             st.write("Error retrieving summary.")
        # else:
        #     st.markdown("Please enter some text to get a summary.")
