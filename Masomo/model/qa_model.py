from transformers import pipeline

class QuestionAnsweringModel:
    def __init__(self, model_name="deepset/bert-large-uncased-whole-word-masking-squad2"):
        # Cargar el pipeline de question-answering con el modelo especificado
        self.qa_pipeline = pipeline("question-answering", model=model_name)

    def answer_question(self, question: str, context: str) -> str:
        """
        Responde a una pregunta basada en el contexto proporcionado.
        :param question: Pregunta que necesita una respuesta.
        :param context: Texto del cual se extraerá la respuesta.
        :return: Respuesta generada por el modelo.
        """
        result = self.qa_pipeline(question=question, context=context)
        return result['answer']
