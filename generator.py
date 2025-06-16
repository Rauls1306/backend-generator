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
            temperature=0.65,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al generar contenido: {str(e)}"

def extract_variables(titulo):
    prompt = f"Del siguiente título académico: {titulo}, extrae dos variables clave, escritas en minúscula, sin comillas, sin numerar, en formato de lista con salto de línea."
    resultado = gpt(prompt)
    return [v.strip() for v in resultado.split("\n") if v.strip()]

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema ingresado: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # TÍTULO
    prompt_titulo = f"A partir del siguiente texto informal: '{tema}', genera un título académico formal interpretado semánticamente. No uses comillas, no repitas frases literales ni coloquiales."
    titulo = gpt(prompt_titulo)
    doc.add_heading(titulo, level=1)

    # CONTEXTO
    prompt_contexto = (
        "Hazme un párrafo como este: La educación superior ha cobrado una relevancia estratégica en los últimos años al convertirse en uno de los principales pilares para impulsar el desarrollo económico, social y cultural de los países. "
        "Su expansión y diversificación responden a las exigencias de una sociedad cada vez más compleja, interconectada y en constante transformación. En este escenario, las universidades desempeñan un rol central como generadoras de conocimiento, "
        "formadoras de capital humano y promotoras de innovación. No obstante, este protagonismo también implica desafíos significativos vinculados con la equidad en el acceso, la calidad del proceso formativo y la pertinencia de los programas ofrecidos. "
        "En consecuencia, surge la necesidad de analizar con mayor profundidad las dinámicas que configuran el quehacer universitario y sus implicancias en el marco de un modelo educativo centrado en el aprendizaje, la responsabilidad social y la excelencia académica. "
        f"Redacta un párrafo como ese, pero sobre el tema: {titulo}"
    )
    doc.add_paragraph(gpt(prompt_contexto))

    # PÁRRAFOS CUANTITATIVOS
    doc.add_paragraph(gpt(
        f"A nivel mundial, redacta un párrafo académico con tres datos cuantitativos reales relacionados al tema '{titulo}': uno porcentual, uno absoluto (cantidad o año) y otro combinado. No uses frases como 'según estudios' ni menciones instituciones."
    ))

    doc.add_paragraph(gpt(
        f"En América Latina, redacta otro párrafo académico con tres datos cuantitativos reales sobre el mismo tema: '{titulo}', uno debe ser en número absoluto. No usar frases metatextuales ni nombres de organismos."
    ))

    doc.add_paragraph(gpt(
        f"A nivel nacional en Perú, redacta un párrafo académico con tres datos cuantitativos reales (al menos uno absoluto), sin citas ni frases como 'en recientes investigaciones'."
    ))

    # PROBLEMA – 100 palabras máx
    doc.add_paragraph(gpt(
        f"Redacta un único párrafo de máximo 100 palabras, sin frases metatextuales ni conectores de cierre, sobre el problema, causas y consecuencias del tema: {titulo}. Usa estilo Scopus Q1."
    ))

    # JUSTIFICACIÓN
    doc.add_paragraph(gpt(
        f"Se justifica la realización de este estudio debido a la importancia del tema: {titulo}. Redacta una justificación académica de 200 palabras como en el modelo del Word. Empieza con 'Se justifica', no uses comillas."
    ))

    # MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)

    doc.add_paragraph(gpt(
        f"A partir del título '{titulo}', redacta un párrafo académico de 200 palabras que incluya el nombre de una teoría, el autor principal o padre, el contexto histórico y una explicación detallada. No uses subtítulos."
    ))

    doc.add_paragraph(gpt(
        f"Redacta un segundo párrafo de 200 palabras sobre una teoría distinta relacionada con el título '{titulo}'. Inicia con un conector fluido desde la anterior. Incluye el nombre de la teoría y el autor."
    ))

    # VARIABLES
    variables = extract_variables(titulo)
    var1 = variables[0] if len(variables) > 0 else "variable uno"
    var2 = variables[1] if len(variables) > 1 else "variable dos"

    doc.add_paragraph(gpt(
        f"Redacta el primer párrafo sobre {var1}, definiéndola claramente y explicando su conceptualización. No escribas 'la variable'."
    ))

    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo sobre {var1}, detallando sus características, dimensiones o elementos constitutivos. Mantén el tono académico."
    ))

    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo sobre {var1}, explicando su relevancia práctica, académica o social en el contexto del título: {titulo}."
    ))

    doc.add_paragraph(gpt(
        f"En relación con lo anterior, inicia un nuevo párrafo sobre {var2}, enlazando desde la variable anterior. Define conceptualmente en estilo Scopus."
    ))

    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo sobre {var2}, describiendo sus características o dimensiones con claridad."
    ))

    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo sobre {var2}, resaltando su impacto en el fenómeno abordado en el título: {titulo}."
    ))

    # GUARDAR
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
