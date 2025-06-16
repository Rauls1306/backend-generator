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

    # CONTEXTO
    doc.add_paragraph(gpt(
        f"Hazme un párrafo como este: La educación superior ha cobrado una relevancia estratégica en los últimos años... Redacta uno igual sobre el tema: {titulo}."
    ))

    # MUNDIAL
    doc.add_paragraph(gpt(
        f"A nivel mundial, redacta un párrafo académico con tres datos cuantitativos (uno porcentual, uno absoluto y uno comparativo) más un dato cualitativo, todos relacionados con el tema: {titulo}. "
        f"No menciones instituciones ni utilices frases como 'según estudios'."
    ))

    # LATAM
    doc.add_paragraph(gpt(
        f"En América Latina, redacta otro párrafo con tres datos cuantitativos combinados más una afirmación cualitativa. "
        f"Evita menciones institucionales y mantén el tema centrado en: {titulo}."
    ))

    # PERÚ
    doc.add_paragraph(gpt(
        f"A nivel nacional en Perú, redacta un párrafo con tres datos (porcentual, absoluto, comparativo) y una afirmación cualitativa sobre el tema: {titulo}. "
        f"Prohibido usar nombres de organizaciones o estudios."
    ))

    # PROBLEMA
    doc.add_paragraph(gpt(
        f"Redacta un único párrafo de máximo 100 palabras sobre el problema, causas y consecuencias del siguiente tema: {titulo}. "
        f"Sin conectores de cierre, sin frases metatextuales, solo redacción académica fluida."
    ))

    # JUSTIFICACIÓN
    doc.add_paragraph(gpt(
        f"Se justifica sí o sí la realización de este estudio debido a la importancia del tema: {titulo}. "
        f"Redacta un solo párrafo de unas 100 palabras en estilo Scopus, sin frases conclusivas, ni subtítulos."
    ))

    # MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)

    doc.add_paragraph(gpt(
        f"Redacta un párrafo de aproximadamente 200 palabras sobre una teoría relacionada con el título: {titulo}. "
        f"Debe incluir una oración de preámbulo fluido, el nombre de la teoría, su autor o creador, el contexto histórico y una explicación completa. "
        f"No uses frases genéricas ni estructuras metatextuales."
    ))

    doc.add_paragraph(gpt(
        f"Redacta otro párrafo de 200 palabras sobre una segunda teoría relacionada con el mismo tema: {titulo}. "
        f"Inicia con un conector lógico desde el párrafo anterior. Incluye nombre de la teoría, autor y explicación. No contradigas la primera teoría."
    ))

    # EXTRAER CONCEPTOS
    conceptos = extract_concepts(titulo)
    concepto1 = conceptos[0] if len(conceptos) > 0 else "concepto técnico"
    concepto2 = conceptos[1] if len(conceptos) > 1 else "concepto contextual"

    # CONCEPTO 1 – PÁRRAFO 1
    doc.add_paragraph(gpt(
        f"Redacta el primer párrafo sobre '{concepto1}', comenzando con un preámbulo dentro del mismo párrafo, seguido de su definición precisa. "
        f"No uses la palabra 'variable'. Usa prosa académica, sin frases repetitivas ni de cierre."
    ))

    # CONCEPTO 1 – PÁRRAFO 2
    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo sobre '{concepto1}', detallando sus características, componentes o dimensiones. "
        f"No repetir la misma frase inicial del párrafo anterior. Evita conclusiones."
    ))

    # CONCEPTO 1 – PÁRRAFO 3
    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo sobre '{concepto1}', explicando su relevancia práctica, académica o profesional. "
        f"Evita conectar con frases tipo 'en resumen' o 'por lo tanto'. No repitas el mismo inicio que en los párrafos anteriores."
    ))

    # CONCEPTO 2 – TRES PÁRRAFOS CON PROMPT EXACTO
    doc.add_paragraph(gpt(
        f"Redacta 3 párrafos sobre el concepto '{concepto2}' c/u de 100 palabras, que al inicio c/u tenga un conector de adición y que el 2 y 3er párrafo no mencionen el nombre del concepto '{concepto2}' en la primera oración, a partir de la 2da sí se puede. Que entre los 3 párrafos se hable de definición, características, tipos, etc."
    ))

    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename

