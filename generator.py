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
                {"role": "system", "content": "Eres un redactor académico profesional experto en artículos científicos tipo Scopus Q1."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar contenido: {str(e)}"

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema ingresado: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # BLOQUE 0 – Generar TÍTULO desde tema libre
    prompt_titulo = f"Genera un título académico formal a partir del siguiente texto informal o general, interpretándolo semánticamente y sin usar comillas: '{tema}'"
    titulo = gpt(prompt_titulo)
    doc.add_heading(titulo, level=1)

    # BLOQUE 1 – CONTEXTO
    prompt_contexto = (
        "Hazme un párrafo como este: La educación superior ha cobrado una relevancia estratégica en los últimos años al convertirse en uno de los principales pilares para impulsar el desarrollo económico, social y cultural de los países. "
        "Su expansión y diversificación responden a las exigencias de una sociedad cada vez más compleja, interconectada y en constante transformación. En este escenario, las universidades desempeñan un rol central como generadoras de conocimiento, "
        "formadoras de capital humano y promotoras de innovación. No obstante, este protagonismo también implica desafíos significativos vinculados con la equidad en el acceso, la calidad del proceso formativo y la pertinencia de los programas ofrecidos. "
        "En consecuencia, surge la necesidad de analizar con mayor profundidad las dinámicas que configuran el quehacer universitario y sus implicancias en el marco de un modelo educativo centrado en el aprendizaje, la responsabilidad social y la excelencia académica."
    )
    doc.add_paragraph(gpt(prompt_contexto))

    # BLOQUE 2 – PROBLEMÁTICA MUNDIAL, LATAM, PERÚ
    doc.add_paragraph(gpt(f"Redacta un párrafo académico con datos cuantitativos reales, sin citas, sobre la problemática mundial relacionada con el siguiente tema: {titulo}"))
    doc.add_paragraph(gpt(f"Ahora redacta un párrafo con datos cuantitativos reales, sin citas ni instituciones, sobre esa misma problemática pero en América Latina."))
    doc.add_paragraph(gpt(f"Finalmente, redacta un párrafo con datos cuantitativos reales, sin fuentes visibles ni citas, sobre esa problemática aplicada al Perú."))

    # BLOQUE 3 – PROBLEMA, CAUSAS Y CONSECUENCIAS
    prompt_problema = (
        "Redacta un párrafo académico tipo Scopus Q1 sobre el problema, las causas y consecuencias del siguiente tema: "
        f"{titulo}. No uses puntos seguidos ni separación entre frases, debe ser un párrafo fluido sin exceso de puntuación."
    )
    doc.add_paragraph(gpt(prompt_problema))

    # BLOQUE 4 – JUSTIFICACIÓN
    prompt_justificacion = (
        f"Se justifica la realización de este estudio debido a la importancia y relevancia del siguiente tema: {titulo}. "
        "Redacta un párrafo académico de aproximadamente 200 palabras, comenzando obligatoriamente con 'Se justifica'. "
        "Debe tener tono Scopus Q1, destacar impacto educativo, pertinencia social, urgencia de abordaje e implicancias académicas."
    )
    doc.add_paragraph(gpt(prompt_justificacion))

    # BLOQUE 5 – MARCO TEÓRICO: TEORÍAS
    prompt_teoria1 = (
        f"Redacta 200 palabras en prosa académica sobre una teoría adecuada relacionada con el tema '{titulo}', incluyendo fundador, contexto histórico y en qué consiste. "
        "No pongas subtítulos ni identifiques la teoría como 'Teoría de…', solo texto corrido."
    )
    doc.add_paragraph(gpt(prompt_teoria1))

    prompt_teoria2 = (
        f"Redacta otro texto de 200 palabras sobre una segunda teoría distinta también relacionada con el tema '{titulo}', en el mismo formato. "
        "No pongas encabezados ni identifiques explícitamente que se trata de una 'teoría'. Solo prosa fluida."
    )
    doc.add_paragraph(gpt(prompt_teoria2))

    # BLOQUE 6 – MARCO TEÓRICO: VARIABLES
    prompt_var1 = (
        f"A partir del siguiente título, extrae la primera variable principal. Luego redacta tres párrafos académicos: (1) definición y conceptualización, "
        "(2) características o dimensiones, (3) importancia en relación con el tema. Título: {titulo}"
    )
    doc.add_paragraph(gpt(prompt_var1))

    prompt_var2 = (
        f"Ahora haz lo mismo para una segunda variable relevante del título: {titulo}. Redacta tres párrafos: definición, características, y relevancia actual. "
        "Todo en prosa continua, sin subtítulos."
    )
    doc.add_paragraph(gpt(prompt_var2))

    # GUARDAR ARCHIVO
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
