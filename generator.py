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

def extract_concepts(titulo):
    prompt = (
        f"Del siguiente título académico: {titulo}, extrae dos conceptos principales: uno técnico desde la profesión del usuario y otro contextual desde el entorno o sector involucrado. "
        f"Devuélvelos sin comillas, en minúsculas, sin numeración, separados por salto de línea."
    )
    resultado = gpt(prompt)
    return [v.strip() for v in resultado.split("\n") if v.strip()]

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading("Artículo generado automáticamente", 0)

    doc.add_paragraph(f"Tema ingresado: {tema}")
    doc.add_paragraph(f"Nivel de indexación: {nivel}")
    doc.add_paragraph("")

    # TÍTULO
    prompt_titulo = (
        f"A partir del siguiente input informal: '{tema}', genera un título académico formal con redacción Scopus. "
        f"Debe contener una combinación entre un concepto técnico derivado de la carrera y otro del entorno. "
        f"No repitas frases del input, no uses comillas ni fórmulas genéricas como 'un estudio sobre' o 'intersección entre'."
    )
    titulo = gpt(prompt_titulo)
    doc.add_heading(titulo, level=1)

    # CONTEXTO GENERAL (párrafo modelo)
    doc.add_paragraph(gpt(
        f"Hazme un párrafo como este: La educación superior ha cobrado una relevancia estratégica en los últimos años al convertirse en uno de los principales pilares para impulsar el desarrollo económico, social y cultural de los países. "
        f"Su expansión y diversificación responden a las exigencias de una sociedad cada vez más compleja, interconectada y en constante transformación. En este escenario, las universidades desempeñan un rol central como generadoras de conocimiento, "
        f"formadoras de capital humano y promotoras de innovación. No obstante, este protagonismo también implica desafíos significativos vinculados con la equidad en el acceso, la calidad del proceso formativo y la pertinencia de los programas ofrecidos. "
        f"En consecuencia, surge la necesidad de analizar con mayor profundidad las dinámicas que configuran el quehacer universitario y sus implicancias en el marco de un modelo educativo centrado en el aprendizaje, la responsabilidad social y la excelencia académica. "
        f"Redacta un párrafo como este, pero sobre el tema: {titulo}."
    ))

    # PÁRRAFO MUNDIAL
    doc.add_paragraph(gpt(
        f"A nivel mundial, redacta un párrafo académico con tres datos cuantitativos (uno porcentual, uno absoluto y uno comparativo) más un dato cualitativo, todos relacionados con el tema: {titulo}. "
        f"No menciones instituciones ni utilices frases como 'según estudios'."
    ))

    # PÁRRAFO LATINOAMÉRICA
    doc.add_paragraph(gpt(
        f"En América Latina, redacta otro párrafo con tres datos cuantitativos combinados más una afirmación cualitativa. "
        f"Evita menciones institucionales y mantén el tema centrado en: {titulo}."
    ))

    # PÁRRAFO PERÚ
    doc.add_paragraph(gpt(
        f"A nivel nacional en Perú, redacta un párrafo con tres datos (porcentual, absoluto, comparativo) y una afirmación cualitativa sobre el tema: {titulo}. "
        f"Prohibido usar nombres de organizaciones o estudios."
    ))

    # PROBLEMA / CAUSAS / CONSECUENCIAS
    doc.add_paragraph(gpt(
        f"Redacta un único párrafo de máximo 100 palabras sobre el problema, causas y consecuencias del siguiente tema: {titulo}. "
        f"Sin conectores de cierre, sin frases metatextuales, solo redacción académica fluida."
    ))

    # JUSTIFICACIÓN
    doc.add_paragraph(gpt(
        f"Se justifica la realización de este estudio debido a la importancia del tema: {titulo}. "
        f"Redacta un solo párrafo de unas 100 palabras en estilo Scopus, sin frases conclusivas, ni subtítulos."
    ))

    # MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)

    # TEORÍA 1 – 200 palabras
    doc.add_paragraph(gpt(
        f"Redacta un párrafo de aproximadamente 200 palabras sobre una teoría relacionada con el título: {titulo}. "
        f"Debe incluir una oración de preámbulo fluido, el nombre de la teoría, su autor o creador, el contexto histórico y una explicación completa. "
        f"No uses frases genéricas ni estructuras metatextuales."
    ))

    # TEORÍA 2 – 200 palabras con conector
    doc.add_paragraph(gpt(
        f"Redacta otro párrafo de 200 palabras sobre una segunda teoría relacionada con el mismo tema: {titulo}. "
        f"Inicia con un conector lógico desde el párrafo anterior. Incluye nombre de la teoría, autor y explicación. No contradigas la primera teoría."
    ))

    # EXTRAER CONCEPTOS
    conceptos = extract_concepts(titulo)
    concepto1 = conceptos[0] if len(conceptos) > 0 else "concepto técnico"
    concepto2 = conceptos[1] if len(conceptos) > 1 else "concepto contextual"

    # CONCEPTO 1 – 3 párrafos
    doc.add_paragraph(gpt(
        f"A partir del desarrollo anterior, redacta el primer párrafo sobre '{concepto1}', incluyendo un preámbulo integrado y su definición. No usar la palabra 'variable'."
    ))
    doc.add_paragraph(gpt(
        f"Redacta un segundo párrafo sobre '{concepto1}', explicando dimensiones, tipos o aspectos clave, evitando repetir la frase de inicio del anterior."
    ))
    doc.add_paragraph(gpt(
        f"Redacta un tercer párrafo sobre '{concepto1}', destacando su implicancia académica, técnica o social. Sin conectores de cierre."
    ))

    # CONCEPTO 2 – CORREGIDO: conector + sin repetición léxica
    doc.add_paragraph(gpt(
        f"En conexión con el concepto anterior, redacta el primer párrafo sobre '{concepto2}', iniciando con un conector, integrando su definición en tono académico sin repetir estructuras previas."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo sobre '{concepto2}', desarrollando sus características o dimensiones con una construcción sintáctica diferente a la anterior. No comenzar con el mismo nombre."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo sobre '{concepto2}' resaltando su relevancia académica o social. Empieza con una nueva estructura sin repetir inicios previos, sin usar conectores de cierre."
    ))

    # GUARDAR DOC
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
