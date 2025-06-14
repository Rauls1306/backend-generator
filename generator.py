import openai
from docx import Document
from datetime import datetime
import os

# Clave API de desarrollo (temporal, sólo para pruebas en entorno cerrado)
openai.api_key = "sk-temp-prueba-1234567890abcdefg"  # Reemplazar por la clave real cuando tengas una propia

def generate_article(tema, nivel):
    prompt = f"Redacta un artículo científico académico hasta el marco teórico sobre el tema: '{tema}', para un nivel de publicación {nivel}. El artículo debe incluir: título, resumen, introducción con contexto mundial, LATAM y Perú, y un marco teórico con dos teorías y dos variables. Usa redacción profesional estilo Scopus."

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Eres un redactor de artículos científicos nivel Scopus Q1."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=3000
    )

    contenido = response.choices[0].message.content

    # Crear documento Word
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema: {tema}")
    doc.add_paragraph("")
    for parrafo in contenido.split("\n"):
        if parrafo.strip():
            doc.add_paragraph(parrafo.strip())

    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename