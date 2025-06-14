import openai
from docx import Document
from datetime import datetime
import os

openai.api_key = "sk-live-temporal-abc123456789"  # Reemplazar por tu propia clave cuando desees

def gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Eres un redactor profesional de artículos científicos estilo Scopus."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content.strip()

def extract_variables(titulo):
    prompt = f"Extrae dos variables clave de este título académico: '{titulo}'. Devuelve solo los nombres de las variables, sin explicación."
    resultado = gpt(prompt)
    variables = resultado.replace("•", "").replace("-", "").split("\n")
    return [v.strip() for v in variables if v.strip()]

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema ingresado: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # BLOQUE 1: Generar título
    titulo = gpt(f"Genera un título académico para un artículo científico Scopus sobre el tema: {tema}")
    doc.add_heading(titulo, level=1)

    # BLOQUE 2: Extraer variables
    variables = extract_variables(titulo)
    var1 = variables[0] if len(variables) > 0 else "Variable 1"
    var2 = variables[1] if len(variables) > 1 else "Variable 2"

    # BLOQUE 3: Resumen
    resumen = gpt(f"Redacta el resumen académico de un artículo con el título '{titulo}' en estilo Scopus.")
    doc.add_heading("Resumen", level=2)
    doc.add_paragraph(resumen)

    # BLOQUE 4: Palabras clave
    keywords = gpt(f"Escribe 3 a 5 palabras clave para el artículo titulado '{titulo}'.")
    doc.add_heading("Palabras clave", level=2)
    doc.add_paragraph(keywords)

    # BLOQUE 5: Abstract
    abstract = gpt(f"Traduce al inglés el siguiente resumen para el artículo titulado '{titulo}':\n\n{resumen}")
    doc.add_heading("Abstract", level=2)
    doc.add_paragraph(abstract)

    # BLOQUE 6: Keywords
    eng_keywords = gpt(f"Traduce al inglés estas palabras clave: {keywords}")
    doc.add_heading("Keywords", level=2)
    doc.add_paragraph(eng_keywords)

    # BLOQUE 7: Introducción – nivel mundial
    intro_mundial = gpt(f"Redacta la introducción académica sobre '{tema}' a nivel mundial.")
    doc.add_heading("Introducción", level=2)
    doc.add_paragraph(intro_mundial)

    # BLOQUE 8: Introducción – nivel LATAM
    intro_latam = gpt(f"Continúa la introducción explicando la situación de '{tema}' en América Latina.")
    doc.add_paragraph(intro_latam)

    # BLOQUE 9: Introducción – nivel Perú
    intro_peru = gpt(f"Finaliza la introducción explicando la situación de '{tema}' en Perú.")
    doc.add_paragraph(intro_peru)

    # BLOQUE 10: Marco teórico
    doc.add_heading("Marco teórico", level=2)

    # BLOQUE 11: Teoría 1
    teoria1 = gpt(f"Escribe una teoría relevante sobre '{var1}' con autor, nombre de la teoría y explicación académica.")
    doc.add_paragraph(teoria1)

    # BLOQUE 12: Teoría 2
    teoria2 = gpt(f"Escribe otra teoría distinta sobre '{var2}' con autor, nombre de la teoría y explicación académica.")
    doc.add_paragraph(teoria2)

    # BLOQUE 13: Variable 1
    var1_def = gpt(f"Define académicamente la variable '{var1}' en el contexto del artículo titulado '{titulo}'.")
    doc.add_paragraph(var1_def)

    # BLOQUE 14: Variable 2
    var2_def = gpt(f"Define académicamente la variable '{var2}' en el contexto del artículo titulado '{titulo}'.")
    doc.add_paragraph(var2_def)

    # Finalizar y guardar
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
