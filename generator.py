import openai
from docx import Document
from datetime import datetime
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un redactor profesional de artículos científicos estilo Scopus Q1."},
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
    titulo_prompt = f"Genera un título académico Scopus Q1 basado en el tema: '{tema}'."
    titulo = gpt(titulo_prompt)
    doc.add_heading(titulo, level=1)

    # Resumen
    resumen_prompt = f"Redacta el RESUMEN del artículo titulado '{titulo}', con estilo Scopus Q1, máximo 200 palabras, estilo impersonal, con redacción académica sólida."
    doc.add_heading("Resumen", level=2)
    doc.add_paragraph(gpt(resumen_prompt))

    # Palabras clave
    keywords_prompt = f"Escribe 5 palabras clave en español separadas por coma para el artículo titulado '{titulo}'."
    doc.add_heading("Palabras clave", level=2)
    doc.add_paragraph(gpt(keywords_prompt))

    # Abstract
    abstract_prompt = f"Traduce el siguiente resumen al inglés: {gpt(resumen_prompt)}"
    doc.add_heading("Abstract", level=2)
    doc.add_paragraph(gpt(abstract_prompt))

    # Keywords (en inglés)
    eng_keywords_prompt = f"Traduce las siguientes palabras clave al inglés: {gpt(keywords_prompt)}"
    doc.add_heading("Keywords", level=2)
    doc.add_paragraph(gpt(eng_keywords_prompt))

    # Introducción Mundial
    intro_mundial_prompt = f"Redacta la introducción del artículo sobre '{tema}' a nivel MUNDIAL, con enfoque académico, sin opinión, usando evidencia y lenguaje formal."
    doc.add_heading("Introducción", level=2)
    doc.add_paragraph(gpt(intro_mundial_prompt))

    # Introducción LATAM
    intro_latam_prompt = f"Redacta un párrafo que describa la situación de '{tema}' en América Latina, con datos y tono académico."
    doc.add_paragraph(gpt(intro_latam_prompt))

    # Introducción Perú
    intro_peru_prompt = f"Redacta un párrafo sobre la situación del tema '{tema}' específicamente en Perú, con tono académico, citando posibles instituciones peruanas."
    doc.add_paragraph(gpt(intro_peru_prompt))

    # Marco teórico
    doc.add_heading("Marco teórico", level=2)

    # Teoría 1
    teoria1_prompt = f"Redacta un bloque académico sobre la primera teoría relacionada con el tema '{tema}', indicando el nombre de la teoría, su autor, año, y explicación."
    doc.add_paragraph(gpt(teoria1_prompt))

    # Teoría 2
    teoria2_prompt = f"Redacta un segundo bloque teórico con otra teoría diferente que también relacione con el tema '{tema}', incluyendo autor y año."
    doc.add_paragraph(gpt(teoria2_prompt))

    # Variable 1
    var1_prompt = f"Define académicamente una variable clave del tema '{tema}', en máximo 150 palabras, con enfoque conceptual."
    doc.add_paragraph(gpt(var1_prompt))

    # Variable 2
    var2_prompt = f"Define otra variable distinta también relevante para el tema '{tema}', con el mismo estilo académico."
    doc.add_paragraph(gpt(var2_prompt))

    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
