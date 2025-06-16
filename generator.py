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
    prompt = f"Del siguiente título académico: {titulo}, extrae dos variables, una vinculada a la profesión y otra al contexto, escritas sin comillas ni numeración, en minúscula, separadas por salto de línea."
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
        f"A partir del siguiente texto informal: '{tema}', genera un título académico formal sin repetir palabras textuales del input. "
        f"Debe combinar una variable de la carrera (profesión/área técnica) y otra del entorno o sector (problema/contexto/lugar). "
        f"Ejemplo: si el input es 'soy ingeniero mecánico y trabajo en un puerto', el título podría ser 'Optimización de maquinaria pesada en operaciones logísticas portuarias'. "
        f"No uses comillas, ni fórmulas tipo 'un estudio sobre...'."
    )
    titulo = gpt(prompt_titulo)
    doc.add_heading(titulo, level=1)

    # CONTEXTO GENERAL
    doc.add_paragraph(gpt(
        f"Hazme un párrafo como este: La educación superior ha cobrado una relevancia estratégica en los últimos años... Redacta igual pero sobre el tema: {titulo}"
    ))

    # TRES PÁRRAFOS CUANTITATIVOS
    doc.add_paragraph(gpt(
        f"A nivel mundial, redacta un párrafo académico con tres datos cuantitativos exactos: uno porcentual, uno absoluto y uno comparativo. Añade un dato cualitativo. No pongas fuentes ni menciones institucionales."
    ))
    doc.add_paragraph(gpt(
        f"En América Latina, escribe otro párrafo con tres datos cuantitativos combinados sobre el mismo tema. Máximo un dato porcentual. Incluye también una afirmación cualitativa relevante, sin citas."
    ))
    doc.add_paragraph(gpt(
        f"A nivel nacional en Perú, redacta un párrafo con tres datos reales: uno porcentual, uno absoluto y uno comparativo, y complementa con un dato cualitativo. No incluyas ninguna institución, fuente ni encuesta."
    ))

    # PROBLEMA
    doc.add_paragraph(gpt(
        f"Redacta un solo párrafo fluido de máximo 100 palabras sobre el problema, causas y consecuencias vinculadas al tema: {titulo}. No uses frases metatextuales ni conectores de cierre."
    ))

    # JUSTIFICACIÓN
    doc.add_paragraph(gpt(
        f"Se justifica la realización de este estudio debido a la importancia del tema: {titulo}. Redacta un solo párrafo de aproximadamente 100 palabras, sin subtítulos ni comillas, siguiendo el estilo del modelo Word."
    ))

    # MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)
    doc.add_paragraph(gpt(
        f"Redacta un párrafo académico de 200 palabras con el nombre de una teoría, su autor o padre, contexto histórico y explicación detallada. Prohibido usar frases como 'una de las teorías más relevantes'."
    ))
    doc.add_paragraph(gpt(
        f"Redacta un segundo párrafo de teoría (200 palabras) iniciando con un conector fluido desde el anterior. Debe incluir otra teoría con nombre y autor. No usar 'además de la teoría de...' si no fue mencionada antes."
    ))

    # VARIABLES (con preámbulo interno y conectores entre variables)
    variables = extract_variables(titulo)
    var1 = variables[0] if len(variables) > 0 else "variable uno"
    var2 = variables[1] if len(variables) > 1 else "variable dos"

    doc.add_paragraph(gpt(
        f"Redacta un primer párrafo de la variable {var1}, empezando con un preámbulo académico dentro del mismo párrafo, seguido de la definición de la variable. No uses frases como 'la variable es'."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo de {var1}, detallando sus características o dimensiones en prosa académica fluida."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo de {var1}, explicando su relevancia práctica, académica o social, sin conectores de cierre."
    ))

    doc.add_paragraph(gpt(
        f"En relación con lo anterior, introduce el primer párrafo sobre la variable {var2}, con un conector fluido desde {var1}. Incluye su definición sin subtítulos ni frases metatextuales."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el segundo párrafo de {var2}, describiendo sus dimensiones, tipos o elementos constitutivos. Mantén continuidad textual con el anterior."
    ))
    doc.add_paragraph(gpt(
        f"Redacta el tercer párrafo de {var2}, destacando su implicancia práctica y conceptual en el fenómeno tratado en el título: {titulo}."
    ))

    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
