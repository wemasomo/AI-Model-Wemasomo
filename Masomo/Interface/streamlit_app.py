# app.py
import streamlit as st
from Masomo.model.summarizer import Summarizer

# Inicializar el summarizer
summarizer = Summarizer()

# Título de la aplicación
st.title("Text Summarizer")

# Entrada de texto del usuario
user_input = st.text_area("Paste your text here", "")

# Botón para generar el resumen
if st.button("Summarize"):
    if user_input:
        summary = summarizer.summarize_text(user_input)
        st.subheader("Summary")
        st.write(summary)
    else:
        st.warning("Please paste some text to summarize!")
