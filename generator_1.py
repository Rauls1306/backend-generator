import openai
import os
import time
from docx import Document
from docx_writer import save_article_to_docx
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
    time.sleep(2)

    # CONTEXTO GENERAL
    contexto = gpt(
        f"Redacta un texto así sobre la problemática del artículo titulado '{titulo}', mismo tamaño, mismo 1 párrafo, recuerda, sin usar datos cuantitativos, NO MENCIONES EL TITULO DE LA INVESTIGACION. HAZLO COMO ESTE MODELO: Los polifenoles han demostrado tener un impacto positivo en la reducción de los niveles lipídicos en estudios con Rattus. Se ha encontrado que la administración de diversos extractos de plantas, frutas y otras fuentes naturales en ratas y ratones, que contienen altos niveles de polifenoles contribuyen a disminuir significativamente los niveles de colesterol, triglicéridos y lipoproteínas en ratas y ratones, con reducciones que oscilan entre el 15% y el 30% en comparación con grupos de control. Es así que un producto que también tiene estas características es el Rubus spp. que contiene antioxidantes y compuestos fenólicos que por sus propiedades bioactivas también pueden contribuir a la mejora del perfil lipídico, lo que revela un potencial efecto hipolipemiante. Su potencial la convierte en un candidato interesante para futuros estudios en el ámbito de la nutrición y la salud. Además, su fácil acceso y bajo costo pueden facilitar su incorporación en la dieta de diversas poblaciones. Por lo tanto, es esencial seguir investigando los efectos de la moral en la salud cardiovascular y su uso en estrategias de prevención. Por lo que, la mora Rubus spp. representa una opción viable y beneficiosa en el manejo de la hiperlipidemia en ratas."
    )
    time.sleep(2)

    # MUNDIAL / LATAM / PAÍS SELECCIONADO
    mundial_latam_peru = gpt(
        f"Redacta un texto de 3 párrafos, c/u de 100 palabras, todo estilo scopus q1, sobre la problemática del artículo titulado '{titulo}'. "
        f"Cada párrafo es por un nivel: el primer párrafo nivel global o mundial, segundo nivel LATAM, tercero nivel nacional del país {pais}. "
        f"Cada párrafo debe tener 3 datos cuantitativos (solo uno porcentual, los otros 2 numericos, IMPORTANTEeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee). "
        f"No incluyas citas ni menciones a instituciones (IMPORTANTISIMO) ni ambigüedades como 'cerca de' o 'casi'. No uses conectores de cierre. "
        f"Cada párrafo debe iniciar mencionando el nivel (ejemplo: A nivel global, En Latinoamérica, En el contexto de {pais}). "
        f"Además, cada párrafo debe tener 2 datos cualitativos. TODA SOLO INFORMACION DE LOS ULTIMOS 5 AÑOS. importante, no uses la palabra \"CUALITATIVA\" ni similares"
    )
    mundial, latam, peru = mundial_latam_peru.split("\n")[:3]
    time.sleep(2)

    # PROBLEMA / CAUSAS / CONSECUENCIAS
    problema = gpt(
        f"Redáctame un párrafo como este sobre problema, causas y consecuencias sobre la problemática del artículo titulado '{titulo}', en 90 palabras, redactado como para scopus q1, sin datos cuantitativos, sin citas, sin tanta puntuación o separación en las oraciones, que sea un párrafo fluido. no menciones el titulo del articulo textualmente en este parrafo, Modelo: En ese sentido, se parte de la premisa que la administración de mora Rubus spp. en Rattus resulta en una reducción significativa de los niveles de lípidos en sangre (tratamiento de la hiperlipidemia). Se espera que los compuestos bioactivos presentes en Rubus spp., como polifenoles y antocianinas, contribuyan a mejorar el perfil lipídico y a mitigar los efectos adversos asociados con este trastorno metabólico. Por lo tanto, los experimentos en vivo constituyen una oportunidad para validar la eficacia de Rubus spp. como un enfoque natural en la prevención y manejo de la hiperlipidemia."
    )
    time.sleep(2)

    # JUSTIFICACIÓN
    justificacion = gpt(
        f"Redacta un párrafo de justificación, por relevancia, importancia, etc. (no lo hagas por niveles tipo tesis teórica, práctica o metodológica), de 100 palabras, estilo scopus q1, que empiece con la primera oración con preámbulo que contenga \"se justifica\", para el artículo titulado '{titulo}'. Sin mencionar el título del artículo en esta justificación."
    )
    time.sleep(2)

    # MARCO TEÓRICO
    doc.add_heading("Marco teórico", level=2)

    # TEORÍA 1
    teorias = gpt(
        f"A partir de esta investigación titulada '{titulo}', busca 2 teorías en las que se podría basar, y de ellas, de cada una, redacta un párrafo de 150 palabras que tenga en la primera oración una especie de preámbulo, y a partir de la segunda ya menciones el nombre de la teoría, el padre (principal propulsor) y de qué trata. Importante: no menciones el título de la investigación en ningún párrafo ni uses conectores de cierre. Sin subtítulos, todo prosa. NO MENCIONES LIBROS. NO USES AMBIGUEDADES COMO, PODRIA SER, TODO EXACTO, EN VEZ DE PORDRIA SER, PON, ES. NO USES LAS PALABRAS, POR EJEMPLO, CRUCIAL"
    )
    teoria1, teoria2 = teorias.split("\n\n")[:2]
    time.sleep(2)

    # VARIABLES (2 x 2 párrafos)
    conceptos = gpt(
        f"A partir de esta investigación titulada '{titulo}', extrae sus dos variables principales (generales, sin especificación). Luego, de cada una redacta un texto de dos párrafos (IMPORTANTE en total 4 PARRAFOS), cada párrafo de 100 palabras. IMPORTANTE: Cada párrafo debe comenzar con un CONECTOR DE ADICION (EJEMPLOS: de manera concordante, en consonancia con lo anterior, siguiendo esa orientación) ESTO ES IMPORTANTISIMOOOOO, y a partir de la segunda desarrollar definición, características, tipos, conceptos, etc. Ambos textos deben ir en prosa continua, sin subtítulos, IMPORTANTE: NO EXPLIQUES QUE HAS ESCOGIDO LAS VARIABLES, NO UTILICES LA PALABRA VARIABLE NI SIMILARES, NO MENCIONAR EL TITULO DE LA INVESTIGACION, NO HABLES EN PRIMERA PERSONA (EJ: HABLAMOS) IMPORTANTEEEEEEEEEEEEEEEEEEEEEEE. NO USES CONECTORES DE CIERRE. LEE TODAS LAS INIDCACIONES."
    )
    conceptos_divididos = conceptos.split("\n\n")
    
    # Proteger contra respuestas incompletas
    while len(conceptos_divididos) < 5:
        conceptos_divididos.append("")
    
    concepto1_p1, concepto1_p2 = conceptos_divididos[0], conceptos_divididos[1]
    concepto2_p1, concepto2_p2, concepto2_p3 = conceptos_divididos[2], conceptos_divididos[3], conceptos_divididos[4]

    generated_text = {
        "contexto": contexto,
        "mundial": mundial,
        "latam": latam,
        "peru": peru,
        "problema": problema,
        "justificacion": justificacion,
        "teoria1": teoria1,
        "teoria2": teoria2,
        "concepto1_p1": concepto1_p1,
        "concepto1_p2": concepto1_p2,
        "concepto2_p1": concepto2_p1,
        "concepto2_p2": concepto2_p2,
        "concepto2_p3": concepto2_p3
    }

    from citation_generator import CitationGenerator

    cg = CitationGenerator(title=titulo, generated_text=generated_text)
    cg.generate_all_references()
    cg.generate_all_citations()
    text_with_citations = cg.insert_all_citations()
    reference_list = cg.get_references_list()

    final_article = ""
    for key in [
        "contexto", "mundial", "latam", "peru", "problema", "justificacion",
        "teoria1", "teoria2",
        "concepto1_p1", "concepto1_p2",
        "concepto2_p1", "concepto2_p2", "concepto2_p3"
    ]:
        if key in text_with_citations:
            final_article += text_with_citations[key] + "\n\n"

    final_article += "Referencias\n"
    for ref in reference_list:
        final_article += ref + "\n"

    final_article = final_article.strip()  # ← ✅ Esto es nuevo

    if not final_article:
        raise ValueError("El contenido del artículo está vacío. No se generará el Word.")
    
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    save_article_to_docx(final_article, filename)
    return filename  
