import openai
from docx import Document
from datetime import datetime
import os

import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Eres un redactor profesional de artículos científicos Scopus."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.65,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar contenido: {str(e)}"

def extract_variables(titulo):
    prompt = f"Extrae dos variables clave del título académico: '{titulo}'. Devuelve solo los nombres de las variables, sin explicación."
    result = gpt(prompt)
    return [v.strip("-• 	") for v in result.split("\n") if v.strip()]

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # Título
    titulo = gpt(f"Genera un título académico para un artículo científico sobre: {tema}")
    doc.add_heading(titulo, level=1)

    # Variables
    variables = extract_variables(titulo)
    var1 = variables[0] if len(variables) > 0 else "Variable 1"
    var2 = variables[1] if len(variables) > 1 else "Variable 2"

    # Bloques
    bloques = [
        ("Resumen", f"Redacta el resumen del artículo titulado '{titulo}' en estilo académico."),
        ("Palabras clave", f"Redacta palabras clave para el artículo titulado '{titulo}' (3 a 5 claves separadas por comas)."),
        ("Abstract", f"Traduce al inglés el resumen anterior del artículo titulado '{titulo}'."),
        ("Keywords", f"Traduce al inglés las palabras clave anteriores."),
        ("Introducción", f"Escribe la introducción global sobre el tema '{tema}' a nivel mundial."),
        ("", f"Describe la situación del tema '{tema}' en América Latina."),
        ("", f"Describe la situación del tema '{tema}' en Perú."),
        ("Marco teórico", ""),
        ("", f"Expón una teoría relevante sobre '{var1}' con autor y explicación académica."),
        ("", f"Expón una teoría distinta sobre '{var2}' con autor y explicación académica."),
        ("", f"Define académicamente la variable '{var1}' en el contexto del artículo titulado '{titulo}'."),
        ("", f"Define académicamente la variable '{var2}' en el contexto del artículo titulado '{titulo}'."),
    ]

    for encabezado, prompt in bloques:
        if encabezado:
            doc.add_heading(encabezado, level=2)
        if prompt:
            contenido = gpt(prompt)
            doc.add_paragraph(contenido)

    # Guardar el archivo
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
