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
    prompt = f"Del siguiente título académico: {titulo}, extrae dos variables clave, en minúscula, sin comillas, sin numeración, en salto de línea."
    resultado = gpt(prompt)
    return [v.strip() for v in resultado.split("\n") if v.strip()]

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)
    doc.add_paragraph(f"Tema ingresado: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # TÍTULO
    prompt_titulo = f"A partir del siguiente texto informal: '{tema}', genera un título académico formal interpretado semánticamente. No uses comillas ni repitas frases textuales."
    titulo = gpt(prompt_titulo)
    doc.add_heading(titulo, level=1)

    # CONTEXTO GENERAL
    prompt_contexto = (
        "Hazme un párrafo como este: La educación superior ha cobrado una relevancia estratégica en los últimos años al convertirse en uno de los principales pilares para impulsar el desarrollo económico, social y cultural de los países. "
        "Su expansión y diversificación responden a las exigencias de una sociedad cada vez más compleja, interconectada y en constante transformación. En este escenario, las universidades desempeñan un rol central como generadoras de conocimiento, "
        "formadoras de capital humano y promotoras de innovación. No obstante, este protagonismo también implica desafíos significativos vinculados con la equidad en el acceso, la calidad del proceso formativo y la pertinencia de los programas ofrecidos. "
        "En consecuencia, surge la necesidad de analizar con mayor profundidad las dinámicas que configuran el quehacer universitario y sus implicancias en el marco de un modelo educativo centrado en el aprendizaje, la responsabilidad social y la excelencia académica. "
        f"Ahora redacta uno así, sobre el tema: {titulo}"
    )
    doc.add_paragraph(gpt(prompt_contexto))

    # PÁRRAFOS CUANTITATIVOS
    doc.add_paragraph(gpt(
        f"A nivel mundial, redacta un párrafo académico con exactamente tres datos cuantitativos: uno porcentual, uno absoluto y uno comparativo, sobre el tema: {titulo}. Añade un dato cualitativo. No menciones instituciones, encuestas ni fuentes."
    ))
    doc.add_paragraph(gpt(
        f"En América Latina, redacta otro párrafo con tres datos cuantitativos distintos (máximo un porcentaje) y una afirmación cualitativa sobre el mismo tema: {titulo}. No uses citas, estudios ni menciones a organismos."
    ))
    doc.add_paragraph(gpt(
        f"A nivel nacional en Perú, redacta un párrafo con tres datos cuantitativos combinados (uno porcentual, uno absoluto y uno comparativo) y una idea cualitativa. Prohibido usar frases como 'según estudios', ni nombres de instituciones."
    ))

    # PROBLEMA CAUSAS CONSECUENCIAS
    doc.add_paragraph(gpt(
        f"Redacta un solo párrafo de máximo 100 palabras, en prosa continua tipo SCOPUS Q1, sobre el problema, las causas y consecuencias del tema: {titulo}. Sin frases metatextuales ni conectores de cierre."
    ))

    # JUSTIFICACIÓN (solo un párrafo, 100 palabras, comienza con “Se justifica”)
    doc.add_paragraph(gpt(
        f"Se justifica la realización de este estudio debido a la importancia del tema: {titulo}. Redacta una justificación formal, coherente, de unas 100 palabras, como en el modelo del Word. Sin comillas."
    ))

    # MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)

    doc.add_paragraph(gpt(
        f"Redacta un párrafo académico de 200 palabras sobre una teoría relacionada con el título: {titulo}. Incluye el nombre de la teoría, su autor o padre, el contexto histórico y la explicación. No uses frases como 'uno de los marcos más relevantes'."
    ))

    doc.add_paragraph(gpt(
        f"Redacta un segundo párrafo de teoría, de 200 palabras, que inicie con un conector fluido desde el anterior. Debe contener otra teoría distinta con su nombre explícito y autor. Nada de 'además de la teoría de…' si no se ha mencionado antes."
    ))

    # VARIABLES (preámbulo, sin subtítulos, enlazadas)
    variables = extract_variables(titulo)
    var1 = variables[0] if len(variables) > 0 else "variable uno"
    var2 = variables[1] if len(variables) > 1 else "variable dos"

    doc.add_paragraph(gpt(
        f"A partir de lo desarrollado previamente, introduce en prosa la primera variable {var1}, comenzando con un preámbulo académico antes de definirla. Redacta su definición de forma integrada con el texto anterior, sin subtítulos ni comillas."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo sobre {var1}, detallando sus características, dimensiones o elementos constitutivos, enlazando naturalmente desde el anterior."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo sobre {var1}, explicando su relevancia práctica, académica y social en el contexto del fenómeno abordado en el título: {titulo}."
    ))

    doc.add_paragraph(gpt(
        f"En consonancia con lo anterior, introduce la segunda variable {var2} con una oración conectora. Luego desarrolla su definición en un párrafo fluido, sin etiquetas ni frases metatextuales."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo sobre {var2}, describiendo sus características o dimensiones de manera clara y académica, enlazada desde el párrafo anterior."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo sobre {var2}, destacando su implicancia práctica, teórica o contextual en relación al título generado: {titulo}."
    ))

    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
