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

def generate_article(tema, nivel, pais):
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

    # CONTEXTO GENERAL
    doc.add_paragraph(gpt(
        f"Redacta un texto así sobre la problemática del artículo titulado '{titulo}', mismo tamaño, mismo 1 párrafo, recuerda, sin usar datos cuantitativos. Modelo: Los polifenoles han demostrado tener un impacto positivo en la reducción de los niveles lipídicos en estudios con Rattus. Se ha encontrado que la administración de diversos extractos de plantas, frutas y otras fuentes naturales en ratas y ratones, que contienen altos niveles de polifenoles contribuyen a disminuir significativamente los niveles de colesterol, triglicéridos y lipoproteínas en ratas y ratones, con reducciones que oscilan entre el 15% y el 30% en comparación con grupos de control. Es así que un producto que también tiene estas características es el Rubus spp. que contiene antioxidantes y compuestos fenólicos que por sus propiedades bioactivas también pueden contribuir a la mejora del perfil lipídico, lo que revela un potencial efecto hipolipemiante. Su potencial la convierte en un candidato interesante para futuros estudios en el ámbito de la nutrición y la salud. Además, su fácil acceso y bajo costo pueden facilitar su incorporación en la dieta de diversas poblaciones. Por lo tanto, es esencial seguir investigando los efectos de la moral en la salud cardiovascular y su uso en estrategias de prevención. Por lo que, la mora Rubus spp. representa una opción viable y beneficiosa en el manejo de la hiperlipidemia en ratas."
    ))

    # MUNDIAL / LATAM / PAÍS SELECCIONADO
    doc.add_paragraph(gpt(
        f"Redacta un texto de 3 párrafos, c/u de 100 palabras, todo estilo scopus q1, sobre la problemática del artículo titulado '{titulo}'. "
        f"Cada párrafo es por un nivel: el primer párrafo nivel global o mundial, segundo nivel LATAM, tercero nivel nacional del país {pais}. "
        f"Cada párrafo debe tener 3 datos cuantitativos (solo uno porcentual, los otros 2 numericos, IMPORTANTE). "
        f"No incluyas citas ni menciones a instituciones ni ambigüedades como 'cerca de' o 'casi'. No uses conectores de cierre. "
        f"Cada párrafo debe iniciar mencionando el nivel (ejemplo: A nivel global, En Latinoamérica, En el contexto de {pais}). "
        f"Además, cada párrafo debe tener 2 datos cualitativos."
    ))

    # PROBLEMA / CAUSAS / CONSECUENCIAS
    doc.add_paragraph(gpt(
        f"Redáctame un párrafo como este sobre problema, causas y consecuencias sobre la problemática del artículo titulado '{titulo}', en 90 palabras, redactado como para scopus q1, sin datos cuantitativos, sin citas, sin tanta puntuación o separación en las oraciones, que sea un párrafo fluido. no menciones el titulo del articulo textualmente en este parrafo, Modelo: En ese sentido, se parte de la premisa que la administración de mora Rubus spp. en Rattus resulta en una reducción significativa de los niveles de lípidos en sangre (tratamiento de la hiperlipidemia). Se espera que los compuestos bioactivos presentes en Rubus spp., como polifenoles y antocianinas, contribuyan a mejorar el perfil lipídico y a mitigar los efectos adversos asociados con este trastorno metabólico. Por lo tanto, los experimentos en vivo constituyen una oportunidad para validar la eficacia de Rubus spp. como un enfoque natural en la prevención y manejo de la hiperlipidemia."
    ))

    # JUSTIFICACIÓN
    doc.add_paragraph(gpt(
        f"Redacta un párrafo de justificación, por relevancia, importancia, etc. (no lo hagas por niveles tipo tesis teórica, práctica o metodológica), de 100 palabras, estilo scopus q1, que empiece con la primera oración con preámbulo que contenga \"se justifica\", para el artículo titulado '{titulo}'. Sin mencionar el título del artículo en esta justificación."
    ))

    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
