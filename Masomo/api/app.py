from fastapi import FastAPI, HTTPException  # type: ignore
from Masomo.model.summarizer import Summarizer
from Masomo.model.qa_model import QuestionAnsweringModel
from Masomo.Interface.response_logic import get_index, text_vectors
import pandas as pd

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
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoint to handle Q&A
@app.post("/qa/")
def qa_endpoint(prompt: str):
    try:
        # Generate a response
        most_similar_index = get_index(prompt, text_vectors)
        relevant_text = df.iloc[most_similar_index]['text']
        response = qa_model.answer_question(prompt, relevant_text)

        if response:
            summary = df['summary'].iloc[most_similar_index]
            return {"response": response, "summary": summary}
        else:
            # If the model can't generate a response, suggest topics
            topics = [
                {"name": "Cancer", "url": "https://www.wemasomo.com/explore/cancer"},
                {"name": "Male Specific Content", "url": "https://www.wemasomo.com/explore/male%20specific%20content"},
                {"name": "Pregnancy", "url": "https://www.wemasomo.com/explore/pregnancy-guide"},
                {"name": "Contraception", "url": "https://www.wemasomo.com/explore/contraception"},
                {"name": "Menstruation", "url": "https://www.wemasomo.com/explore/menstruation"},
                {"name": "Vaccination", "url": "https://www.wemasomo.com/explore/vaccination"},
                {"name": "Endometriosis", "url": "https://www.wemasomo.com/explore/endometriosis"},
                {"name": "Mpox", "url": "https://www.wemasomo.com/explore/mpox"},
                {"name": "Sexually Transmitted Diseases", "url": "https://www.wemasomo.com/explore/hiv"},
                {"name": "Parenting", "url": "https://www.wemasomo.com/explore/parenting"}
            ]
            return {"message": "We couldn't understand your question... Maybe you want to browse through these topics:", "topics": topics}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
