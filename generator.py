import openai
from docx import Document
from datetime import datetime
import os

# Clave API temporal (esto es un ejemplo, en producción deberás usar tu propia clave)
openai.api_key = "sk-live-temporal-abc123456789"

def generate_article(tema, nivel):
    prompt = f"Redacta un artículo académico completo hasta el marco teórico sobre el tema '{tema}', para nivel {nivel}. Incluye: título, resumen, introducción con contexto internacional, LATAM y Perú, y un marco teórico con dos teorías y dos variables. Redacción formal, académica, tipo Scopus Q1."

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Eres un redactor experto en artículos científicos estilo Scopus."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.65,
        max_tokens=3000
    )

    contenido = response.choices[0].message.content

    # Crear archivo Word
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema: {tema}")
    doc.add_paragraph("")
    for linea in contenido.split("\n"):
        if linea.strip():
            doc.add_paragraph(linea.strip())

    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
