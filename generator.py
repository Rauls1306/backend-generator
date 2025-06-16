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
        f"Del siguiente título académico: {titulo}, extrae dos conceptos distintos. "
        f"Uno debe ser técnico, derivado de la carrera o profesión, y el otro debe ser contextual, relacionado al entorno, problema o sector. "
        f"Devuélvelos sin comillas, en minúsculas, separados por salto de línea."
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
        f"A partir del siguiente texto informal: '{tema}', genera un título académico interpretado semánticamente. "
        f"Debe contener una combinación entre un concepto técnico desde la carrera y otro contextual desde el entorno, sin repetir frases del input literal, sin comillas ni fórmulas genéricas."
    )
    titulo = gpt(prompt_titulo)
    doc.add_heading(titulo, level=1)

    # CONTEXTO GENERAL (PÁRRAFO MODELO)
    doc.add_paragraph(gpt(
        f"Hazme un párrafo como este: La educación superior ha cobrado una relevancia estratégica... "
        f"Redacta uno igual sobre el tema: {titulo}."
    ))

    # PÁRRAFO MUNDIAL
    doc.add_paragraph(gpt(
        f"A nivel mundial, redacta un párrafo académico con exactamente tres datos cuantitativos: uno porcentual, uno absoluto y uno comparativo. "
        f"Incluye un dato cualitativo complementario. No menciones fuentes, instituciones ni encuestas. No uses frases como 'según estudios'."
    ))

    # PÁRRAFO LATINOAMÉRICA
    doc.add_paragraph(gpt(
        f"En América Latina, escribe un párrafo con tres datos cuantitativos reales, bien distribuidos (máximo un porcentaje) y un dato cualitativo. "
        f"No usar conectores de cierre ni frases metatextuales."
    ))

    # PÁRRAFO PERÚ
    doc.add_paragraph(gpt(
        f"A nivel nacional en Perú, redacta un párrafo con tres datos reales y una afirmación cualitativa. "
        f"Evita frases como 'de acuerdo con' o 'en recientes investigaciones'."
    ))

    # PÁRRAFO PROBLEMA / CAUSAS / CONSECUENCIAS
    doc.add_paragraph(gpt(
        f"Redacta un único párrafo de máximo 100 palabras, en estilo Scopus Q1, sobre el problema, sus causas y consecuencias. "
        f"No uses frases metatextuales ni conectores de cierre. Sin puntos cortantes."
    ))

    # PÁRRAFO JUSTIFICACIÓN
    doc.add_paragraph(gpt(
        f"Se justifica la realización de este estudio debido a la importancia del tema: {titulo}. "
        f"Redacta un solo párrafo de aproximadamente 100 palabras, en prosa continua, sin comillas ni frases de cierre como 'por ello' o 'finalmente'."
    ))

    # SUBTÍTULO MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)

    # TEORÍA 1
    doc.add_paragraph(gpt(
        f"Redacta un párrafo académico de 200 palabras con el nombre explícito de una teoría, el autor o padre que la creó, el contexto histórico y su explicación completa. "
        f"No digas 'una teoría relevante es…'. Usa prosa académica directa."
    ))

    # TEORÍA 2
    doc.add_paragraph(gpt(
        f"Redacta otro párrafo académico de 200 palabras sobre una teoría distinta, enlazada con la anterior mediante un conector fluido. "
        f"Debe contener nombre de teoría y autor también. No repetir fórmulas ni usar conectores de cierre."
    ))

    # EXTRAER CONCEPTOS
    conceptos = extract_concepts(titulo)
    concepto1 = conceptos[0] if len(conceptos) > 0 else "concepto técnico"
    concepto2 = conceptos[1] if len(conceptos) > 1 else "concepto contextual"

    # CONCEPTO 1 – PÁRRAFO 1 (CON PREÁMBULO INTERNO)
    doc.add_paragraph(gpt(
        f"A partir de lo anteriormente desarrollado, redacta el primer párrafo explicando el concepto '{concepto1}'. "
        f"Comienza con un preámbulo dentro del mismo párrafo, seguido de su definición académica. No uses subtítulos ni la palabra 'variable'."
    ))

    # CONCEPTO 1 – PÁRRAFO 2
    doc.add_paragraph(gpt(
        f"Redacta un segundo párrafo sobre '{concepto1}', detallando sus características, dimensiones o aplicaciones. "
        f"No repitas la frase inicial del párrafo anterior. Usa conectores suaves, sin cierre."
    ))

    # CONCEPTO 1 – PÁRRAFO 3
    doc.add_paragraph(gpt(
        f"Redacta un tercer párrafo sobre '{concepto1}', explicando su relevancia práctica, teórica o social. "
        f"No empieces con 'la importancia de...', ni con la palabra 'concepto'."
    ))

    # CONCEPTO 2 – PÁRRAFO 1 (CON CONECTOR)
    doc.add_paragraph(gpt(
        f"En relación con lo anterior, redacta el primer párrafo del concepto '{concepto2}'. "
        f"Comienza con una frase conectiva desde el anterior, y define académicamente el concepto sin usar comillas ni metatexto."
    ))

    # CONCEPTO 2 – PÁRRAFO 2
    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo sobre '{concepto2}', explicando dimensiones o aspectos relevantes sin repetir la misma frase inicial. "
        f"Evita conectores de cierre."
    ))

    # CONCEPTO 2 – PÁRRAFO 3
    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo sobre '{concepto2}' destacando su implicancia contextual o funcional. "
        f"No usar frases de conclusión ni reiteraciones de la estructura anterior."
    ))

    # GUARDAR DOCUMENTO
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
