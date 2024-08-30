import streamlit as st
import pandas as pd
from Masomo.model.qa_model import QuestionAnsweringModel

# Inicializar el modelo QA
qa_model = QuestionAnsweringModel()

# Cargar el archivo CSV (asegúrate de que la ruta sea correcta)
df = pd.read_csv('Masomo/raw_data/texts_database.csv')

# Título y descripción de la aplicación
st.title("Sexual Health QA Assistant")
st.write("""
    Welcome! Ask any questions you have about sexual health,
    and I'll provide answers based on the information we have.
""")

# Entrada del usuario
question = st.text_input("Type your question here:")

if st.button("Get Answer"):
    if question:
        # Encontrar el contexto más relevante
        relevant_text = qa_model.find_most_relevant_text(question, df)

        # Obtener la respuesta del modelo QA
        answer = qa_model.answer_question(question, relevant_text)

        # Mostrar la respuesta
        st.subheader("Answer:")
        st.write(answer)

        # Mostrar el contexto utilizado
        st.subheader("Context used:")
        st.write(relevant_text)
    else:
        st.write("Please enter a question.")
