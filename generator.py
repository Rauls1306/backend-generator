import openai
import os
from docx import Document
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar contenido: {str(e)}"

def extract_variables(titulo):
    prompt = f"Del siguiente título académico: {titulo}, extrae dos variables centrales. Devuelve solo los nombres, en minúsculas, sin comillas ni numeración, separados por salto de línea."
    resultado = gpt(prompt)
    return [v.strip() for v in resultado.split("\n") if v.strip()]

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema ingresado: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # TÍTULO
    prompt_titulo = f"A partir del siguiente texto informal o coloquial, genera un título académico formal interpretado semánticamente, sin usar comillas ni repetir frases literales: {tema}"
    titulo = gpt(prompt_titulo)
    doc.add_heading(titulo, level=1)

    # INTRODUCCIÓN
    doc.add_paragraph(gpt(
        "Hazme un párrafo como este: La educación superior ha cobrado una relevancia estratégica en los últimos años al convertirse en uno de los principales pilares para impulsar el desarrollo económico, social y cultural de los países. "
        "Su expansión y diversificación responden a las exigencias de una sociedad cada vez más compleja, interconectada y en constante transformación. En este escenario, las universidades desempeñan un rol central como generadoras de conocimiento, "
        "formadoras de capital humano y promotoras de innovación. No obstante, este protagonismo también implica desafíos significativos vinculados con la equidad en el acceso, la calidad del proceso formativo y la pertinencia de los programas ofrecidos. "
        "En consecuencia, surge la necesidad de analizar con mayor profundidad las dinámicas que configuran el quehacer universitario y sus implicancias en el marco de un modelo educativo centrado en el aprendizaje, la responsabilidad social y la excelencia académica. "
        f"Redacta un párrafo como ese, pero sobre el tema: {titulo}"
    ))

    doc.add_paragraph(gpt(f"A nivel mundial, redacta un párrafo académico con tres datos cuantitativos reales, sin fuentes ni citas, sobre la problemática reflejada en el título: {titulo}"))
    doc.add_paragraph(gpt(f"En América Latina, redacta un párrafo académico con tres datos cuantitativos reales sobre el mismo tema: {titulo}, sin instituciones ni referencias."))
    doc.add_paragraph(gpt(f"A nivel nacional en Perú, redacta un párrafo académico con tres datos cuantitativos reales sobre la problemática vinculada al título: {titulo}, sin mencionar nombres de organismos."))

    doc.add_paragraph(gpt(
        f"Redacta un único párrafo fluido de aproximadamente 100 palabras, tipo Scopus Q1, sobre el problema, las causas y las consecuencias del siguiente tema: {titulo}. No pongas puntos seguidos ni frases cortadas, redacta sin conectores de cierre."
    ))

    doc.add_paragraph(gpt(
        f"Se justifica la realización de este estudio debido a la importancia del siguiente tema: {titulo}. Redacta una justificación académica de unas 200 palabras, con tono formal, sin comillas, empezando con 'Se justifica' tal como en el modelo del Word."
    ))

    # MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)

    doc.add_paragraph(gpt(
        f"A partir del siguiente título: {titulo}, redacta un párrafo académico de aproximadamente 200 palabras que incluya el nombre de una teoría relacionada, el autor o creador principal, su contexto histórico, y una explicación clara en prosa, sin subtítulos ni comillas."
    ))

    doc.add_paragraph(gpt(
        f"Redacta un segundo párrafo de teoría, también de 200 palabras, con una teoría distinta relacionada al mismo título: {titulo}, enlazando conceptualmente desde la anterior sin subtítulo ni encabezado visible."
    ))

    variables = extract_variables(titulo)
    var1 = variables[0] if len(variables) > 0 else "variable uno"
    var2 = variables[1] if len(variables) > 1 else "variable dos"

    doc.add_paragraph(gpt(
        f"Redacta el primer párrafo sobre la variable {var1}, explicando su definición y conceptualización en relación con el título: {titulo}. Evita fórmulas metatextuales, usa prosa académica continua."
    ))

    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo sobre la variable {var1}, describiendo sus características, dimensiones o elementos constitutivos. Enlaza naturalmente desde el párrafo anterior."
    ))

    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo sobre la variable {var1}, explicando su importancia y vinculación directa con el fenómeno planteado en el título: {titulo}."
    ))

    doc.add_paragraph(gpt(
        f"Redacta el primer párrafo de la segunda variable {var2} con una frase conectora suave desde la variable anterior. Describe su definición y conceptualización, sin subtítulos, sin comillas."
    ))

    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo sobre la variable {var2}, detallando sus dimensiones, características o tipologías de forma académica, con continuidad del párrafo anterior."
    ))

    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo sobre la variable {var2}, destacando su relevancia científica, práctica o social, vinculándola al tema central del título: {titulo}."
    ))

    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
