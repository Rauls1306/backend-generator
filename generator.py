import openai
import os
from docx import Document
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un redactor académico especializado en artículos científicos estilo Scopus Q1."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.65,
            max_tokens=1800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar contenido: {str(e)}"

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # Título
    titulo_prompt = f"Genera un título académico para un artículo Scopus Q1 con base en el tema: {tema}"
    titulo = gpt(titulo_prompt)
    doc.add_heading(titulo, level=1)

    # Introducción
    doc.add_heading("Introducción", level=2)

    prompts_intro = [
        f"Redacta un párrafo académico tipo Scopus Q1 que justifique la importancia de investigar sobre: {tema}",
        f"Redacta un párrafo que explique el problema sobre '{tema}' a nivel mundial, con redacción académica, sin datos numéricos.",
        f"Redacta un párrafo que exponga el problema de '{tema}' en América Latina, sin citas, estilo formal.",
        f"Redacta un párrafo académico sobre el problema de '{tema}' en Perú, sin mencionar instituciones ni usar cifras.",
        f"Redacta un párrafo que describa las causas y consecuencias del problema de '{tema}', sin listas ni puntos.",
        f"Redacta un párrafo de justificación académica que argumente por qué es relevante este artículo sobre '{tema}'.",
        f"Redacta el párrafo final de la introducción del artículo académico sobre '{tema}', enlazando con el marco teórico."
    ]

    for prompt in prompts_intro:
        doc.add_paragraph(gpt(prompt))

    # Marco teórico
    doc.add_heading("Marco teórico", level=2)

    prompts_marco = [
        f"Redacta un texto académico de 200 palabras sobre la Teoría de la Calidad Educativa Universitaria: incluye autor principal, contexto histórico y explicación.",
        f"Redacta un texto académico de 200 palabras sobre la Teoría de la Docencia Universitaria: autor principal, época, y aplicación.",
        f"Redacta tres párrafos académicos sobre la variable 'Competencias en docentes universitarios': definición, características, tipos.",
        f"Redacta tres párrafos académicos sobre la variable 'Educación superior de calidad': definición, criterios, enfoque actual."
    ]

    for prompt in prompts_marco:
        doc.add_paragraph(gpt(prompt))

    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
