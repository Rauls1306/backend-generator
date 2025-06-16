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
                {"role": "system", "content": "Eres un redactor profesional de artículos científicos estilo Scopus Q1. No uses subtítulos, responde solo con prosa académica limpia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar contenido: {str(e)}"

def extract_variables(titulo):
    prompt = f"Extrae dos variables clave del siguiente título académico: '{titulo}'. Devuelve solo los nombres de las variables, sin explicación ni viñetas."
    resultado = gpt(prompt)
    return [v.strip() for v in resultado.split("\n") if v.strip()]

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema ingresado: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # TÍTULO
    prompt_titulo = f"Genera un título académico para un artículo científico serio a partir del siguiente texto informal o general. Interprétalo semánticamente y devuélvelo sin comillas: '{tema}'"
    titulo = gpt(prompt_titulo)
    doc.add_heading(titulo, level=1)

    # BLOQUE 1: CONTEXTO
    prompt_contexto = (
        f"Redacta un primer párrafo de introducción académica tipo Scopus Q1 vinculado al siguiente título: '{titulo}'. "
        "Hazlo como el modelo: 'La educación superior ha cobrado una relevancia estratégica...'. No debe ser genérico, debe girar en torno al tema del título."
    )
    doc.add_paragraph(gpt(prompt_contexto))

    # BLOQUE 2: PROBLEMÁTICA MUNDIAL, LATAM, PERÚ
    doc.add_paragraph(gpt(f"A nivel mundial, redacta un párrafo académico con datos cuantitativos reales, sin fuentes ni citas, sobre la problemática que aborda el título: '{titulo}'"))
    doc.add_paragraph(gpt(f"En América Latina, redacta otro párrafo académico con datos reales relacionados con ese mismo tema: '{titulo}'. No repitas datos del párrafo anterior."))
    doc.add_paragraph(gpt(f"En Perú, redacta un párrafo más, con datos reales vinculados a esa problemática. No menciones instituciones ni fuentes. Solo texto fluido, académico y coherente con el título: '{titulo}'"))

    # BLOQUE 3: PROBLEMA, CAUSAS Y CONSECUENCIAS
    prompt_problema = (
        f"Redacta un párrafo académico tipo Scopus Q1 sobre el problema, causas y consecuencias relacionadas con el tema: '{titulo}'. "
        "Debe ser un párrafo continuo, sin listas, sin puntuación excesiva, sin frases cortadas ni subtítulos."
    )
    doc.add_paragraph(gpt(prompt_problema))

    # BLOQUE 4: JUSTIFICACIÓN
    prompt_justificacion = (
        f"Se justifica la realización de este estudio debido a la importancia del tema: '{titulo}'. "
        "Redacta un párrafo de justificación formal, académico, de unas 200 palabras, que comience obligatoriamente con 'Se justifica'. "
        "Debe incluir relevancia social, impacto académico y contribución educativa."
    )
    doc.add_paragraph(gpt(prompt_justificacion))

    # SUBTÍTULO: MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)

    # BLOQUE 5: TEORÍAS
    prompt_teoria1 = f"Redacta un texto académico fluido (≈200 palabras) sobre una teoría relacionada con el título: '{titulo}', incluyendo autor, contexto histórico y definición, en prosa sin títulos ni marcas."
    doc.add_paragraph(gpt(prompt_teoria1))

    prompt_teoria2 = f"Redacta otro texto diferente (≈200 palabras) sobre una segunda teoría relacionada también con el tema: '{titulo}', con autor, contexto y explicación, en prosa continua."
    doc.add_paragraph(gpt(prompt_teoria2))

    # BLOQUE 6: VARIABLES EN 3 PÁRRAFOS CADA UNA
    variables = extract_variables(titulo)
    var1 = variables[0] if len(variables) > 0 else "Variable 1"
    var2 = variables[1] if len(variables) > 1 else "Variable 2"

    prompt_var1 = (
        f"Redacta tres párrafos académicos sobre la variable '{var1}' en relación con el título: '{titulo}'. "
        "1. Definición clara. 2. Características o dimensiones. 3. Importancia y relación con el fenómeno. No uses subtítulos, todo en prosa."
    )
    doc.add_paragraph(gpt(prompt_var1))

    prompt_var2 = (
        f"Ahora redacta tres párrafos académicos sobre la variable '{var2}' también en relación con el título: '{titulo}'. "
        "Misma estructura: definición, características, relevancia actual. Solo prosa continua, estilo SCOPUS Q1."
    )
    doc.add_paragraph(gpt(prompt_var2))

    # GUARDAR ARCHIVO
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
