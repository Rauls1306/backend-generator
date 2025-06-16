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
                {
                    "role": "system",
                    "content": "Eres un redactor experto en artículos científicos tipo Scopus Q1. Solo escribes prosa académica continua. No usas subtítulos, comillas innecesarias, ni citas. No expliques lo que haces. Solo devuelve contenido académico real, directo y serio."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar contenido: {str(e)}"

def extract_variables(titulo):
    prompt = f"Del siguiente título académico: {titulo}, extrae dos variables relevantes. Solo los nombres, sin explicación, sin comillas, sin numeración, sin adornos."
    resultado = gpt(prompt)
    return [v.strip() for v in resultado.split("\n") if v.strip()]

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema ingresado: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # TÍTULO
    prompt_titulo = f"A partir de este texto informal: '{tema}', genera un título académico serio, sin usar comillas ni repetir literalmente. Debe sonar como título de artículo SCOPUS real."
    titulo = gpt(prompt_titulo)
    doc.add_heading(titulo, level=1)

    # INTRODUCCIÓN
    # 1. Contexto
    prompt_contexto = (
        "Hazme un párrafo como este: La educación superior ha cobrado una relevancia estratégica en los últimos años al convertirse en uno de los principales pilares para impulsar el desarrollo económico, social y cultural de los países. "
        "Su expansión y diversificación responden a las exigencias de una sociedad cada vez más compleja, interconectada y en constante transformación. En este escenario, las universidades desempeñan un rol central como generadoras de conocimiento, "
        "formadoras de capital humano y promotoras de innovación. No obstante, este protagonismo también implica desafíos significativos vinculados con la equidad en el acceso, la calidad del proceso formativo y la pertinencia de los programas ofrecidos. "
        "En consecuencia, surge la necesidad de analizar con mayor profundidad las dinámicas que configuran el quehacer universitario y sus implicancias en el marco de un modelo educativo centrado en el aprendizaje, la responsabilidad social y la excelencia académica. "
        f"Redacta un párrafo igual, pero aplicado al tema del siguiente título: {titulo}"
    )
    doc.add_paragraph(gpt(prompt_contexto))

    # 2. Mundial
    doc.add_paragraph(gpt(f"A nivel mundial, redacta un párrafo académico con tres datos cuantitativos reales, sin fuentes ni citas, sobre la problemática reflejada en el título: {titulo}"))

    # 3. LATAM
    doc.add_paragraph(gpt(f"En América Latina, redacta un párrafo académico con tres datos cuantitativos reales sobre la misma problemática del título: {titulo}. No uses nombres de países, ni instituciones, ni comillas."))

    # 4. Perú
    doc.add_paragraph(gpt(f"A nivel nacional en Perú, redacta un párrafo con tres datos cuantitativos reales sobre la problemática abordada en el título: {titulo}, sin citar fuentes ni mencionar instituciones."))

    # 5. Problema, causas y consecuencias
    doc.add_paragraph(gpt(f"Redacta un párrafo académico fluido, sin puntuación excesiva ni frases cortadas, sobre el problema, causas y consecuencias vinculadas al siguiente tema: {titulo}"))

    # 6. Justificación
    doc.add_paragraph(gpt(f"Se justifica la realización de este estudio debido a la importancia del siguiente tema: {titulo}. Redacta una justificación académica formal de unas 200 palabras siguiendo el estilo de los prompts que te di."))

    # SUBTÍTULO MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)

    # 7. Teoría 1
    doc.add_paragraph(gpt(f"Redacta un texto de 200 palabras sobre una teoría relacionada con el título: {titulo}, incluyendo el autor principal, el contexto histórico en que surgió, y en qué consiste la teoría. No uses subtítulos."))

    # 8. Teoría 2
    doc.add_paragraph(gpt(f"Redacta otro texto distinto, de 200 palabras, sobre otra teoría relacionada con el título: {titulo}, también con autor, contexto histórico y contenido. Usa conectores para que fluya desde la anterior."))

    # 9. Variables
    variables = extract_variables(titulo)
    var1 = variables[0] if len(variables) > 0 else "Primera variable"
    var2 = variables[1] if len(variables) > 1 else "Segunda variable"

    # Variable 1 – 3 párrafos
    doc.add_paragraph(gpt(f"Redacta el primer párrafo sobre la variable '{var1}', explicando su definición y conceptualización en relación con el título: {titulo}."))
    doc.add_paragraph(gpt(f"Redacta el segundo párrafo sobre la variable '{var1}', describiendo sus características o dimensiones."))
    doc.add_paragraph(gpt(f"Redacta el tercer párrafo sobre la variable '{var1}', explicando su relevancia en el contexto del fenómeno descrito en el título."))

    # Variable 2 – 3 párrafos
    doc.add_paragraph(gpt(f"Redacta el primer párrafo sobre la variable '{var2}', explicando su definición y conceptualización en relación con el título: {titulo}."))
    doc.add_paragraph(gpt(f"Redacta el segundo párrafo sobre la variable '{var2}', describiendo sus características o dimensiones."))
    doc.add_paragraph(gpt(f"Redacta el tercer párrafo sobre la variable '{var2}', explicando su relevancia en el contexto del fenómeno descrito en el título."))

    # Guardar
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
