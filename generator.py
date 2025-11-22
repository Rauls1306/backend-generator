import os
import time
from datetime import datetime

import openai

# La API key se carga en main.py con load_dotenv()
# Aquí solo usamos openai.ChatCompletion


def gpt(prompt: str, max_tokens: int = 1800, temperature: float = 0.65) -> str:
    """
    Wrapper simple para llamadas a GPT-4 (openai==0.28)
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Error en GPT:", str(e))
        raise
    
def traducir_variable_al_ingles(variable_es: str) -> str:
    """
    Traduce la variable 1 al inglés para usarla en la búsqueda de ScienceDirect.
    """
    prompt = (
        "Traduce al inglés académico el siguiente concepto o variable de investigación.\n"
        "Devuelve solo la traducción, sin comillas ni explicación:\n\n"
        f"{variable_es}"
    )
    return gpt(prompt)

def generar_titulo_es(tema: str, pais: str, nivel: str) -> str:
    """
    Genera un título académico formal en español para un artículo de revisión.
    """
    prompt = (
        "Eres un experto en redacción académica de artículos de revisión bibliográfica.\n\n"
        f"Input del usuario: \"{tema}\" (país: {pais}, tipo de indexación: {nivel}).\n\n"
        "Genera UN solo título académico formal en español para una revisión bibliográfica o revisión crítica.\n"
        "Condiciones:\n"
        "- No repitas literalmente el texto del input.\n"
        "- No uses comillas ni expresiones como 'un estudio sobre', 'intersección entre', "
        "'análisis de la influencia de', 'revisión sistemática de'.\n"
        "- El título debe combinar una dimensión técnica/disciplina (por ejemplo 'medicina humana') "
        "con una dimensión contextual o problema (por ejemplo 'en el sistema de salud peruano').\n"
        "- Estilo Scopus (preciso, específico y formal).\n"
        "- Responde SOLO con el título."
    )
    return gpt(prompt)


def generar_titulo_en(titulo_es: str) -> str:
    """
    Traduce el título al inglés académico, sin comillas.
    """
    prompt = (
        "Traduce al inglés académico el siguiente título de artículo de revisión bibliográfica.\n"
        "Mantén la estructura y el tono formal. No uses comillas, no expliques nada.\n\n"
        f"Título en español: {titulo_es}"
    )
    return gpt(prompt)


def normalizar_indexacion(nivel: str) -> str:
    """
    Convierte el texto de indexación a un rótulo corto tipo el modelo (SCOPUSq3, SCOPUSq4, SCIELO, LATINDEX).
    """
    n = (nivel or "").lower()

    if "scopus" in n:
        if "q4" in n and "q3" in n:
            return "SCOPUSq3-q4"
        if "q4" in n:
            return "SCOPUSq4"
        return "SCOPUSq3"
    if "latindex" in n:
        return "LATINDEX"
    if "sci" in n:
        return "SCIELO"
    return nivel or ""


def extraer_variables_desde_titulo(titulo: str):
    """
    Extrae variable_1 (técnica) y variable_2 (contextual) desde el título,
    en minúsculas y sin adornos.
    """
    prompt = (
        "Del siguiente título académico de revisión bibliográfica:\n\n"
        f"\"{titulo}\"\n\n"
        "Identifica exactamente DOS variables principales:\n"
        "1) Una variable técnica o conceptual (por ejemplo: 'bioalcalinización celular', 'medicina humana').\n"
        "2) Una variable contextual, aplicada o de resultado (por ejemplo: 'tratamiento del cáncer de pulmón', "
        "'sistema de salud peruano').\n\n"
        "Devuelve SOLO las dos variables, en minúsculas, sin artículos iniciales, "
        "sin numeración, sin explicaciones, cada una en una línea diferente."
    )

    resultado = gpt(prompt)
    variables = [v.strip() for v in resultado.split("\n") if v.strip()]

    variable_1 = variables[0] if len(variables) > 0 else "variable técnica no identificada"
    variable_2 = variables[1] if len(variables) > 1 else "variable contextual no identificada"

    return variable_1, variable_2


def generar_resumen_y_palabras_clave(titulo_es: str, variable_1: str, variable_2: str, nivel: str, pais: str):
    """
    Genera:
      - Resumen (español)
      - Palabras clave (línea tipo 'palabra, palabra, ...')
    siguiendo el estilo del modelo.
    """
    # Ajustar bases de datos según nivel
    nivel_lower = (nivel or "").lower()
    if "scopus" in nivel_lower:
        bases = "Scopus (particularmente Q3) y SciELO"
        rango_anios = "2017 y 2025"
    elif "sci" in nivel_lower:
        bases = "SciELO y Scopus"
        rango_anios = "2017 y 2025"
    else:
        bases = "Scopus, SciELO y Latindex"
        rango_anios = "2017 y 2025"

    prompt_resumen = (
        "Redacta el RESUMEN de un artículo de revisión bibliográfica en español, siguiendo el estilo Scopus Q3.\n\n"
        f"Título del artículo: {titulo_es}\n"
        f"Variables principales: {variable_1} y {variable_2}\n"
        f"País de enfoque: {pais}\n"
        f"Bases de datos principales: {bases}\n"
        f"Rango de años de la literatura analizada: entre {rango_anios}.\n\n"
        "Condiciones para el resumen:\n"
        "- Extensión aproximada entre 180 y 220 palabras.\n"
        "- Menciona el objetivo general de la revisión.\n"
        "- Explica brevemente la metodología (revisión bibliográfica o revisión crítica de la literatura).\n"
        "- Resume los principales hallazgos y dimensiones analizadas.\n"
        "- Termina con una frase de conclusión general e implicancias.\n"
        "- No uses subtítulos dentro del resumen.\n"
    )

    resumen = gpt(prompt_resumen)

    prompt_palabras = (
        "A partir del siguiente resumen de un artículo de revisión, propón entre 5 y 7 palabras clave en español.\n"
        "Responde SOLO con las palabras clave en minúsculas, separadas por coma, sin explicación adicional.\n\n"
        f"Resumen:\n{resumen}"
    )
    palabras_clave = gpt(prompt_palabras)

    return resumen, palabras_clave


def generar_abstract_y_keywords(resumen: str, palabras_clave: str):
    """
    Genera:
      - Abstract en inglés
      - Keywords en inglés (misma cantidad y orden que las palabras clave)
    """
    prompt_abstract = (
        "Traduce y adapta al inglés académico el siguiente resumen de un artículo de revisión bibliográfica.\n"
        "Debe ser un ABSTRACT coherente, entre 180 y 220 palabras, estilo Scopus Q3/Q2.\n"
        "No expliques nada, devuelve solo el Abstract.\n\n"
        f"Resumen en español:\n{resumen}"
    )
    abstract = gpt(prompt_abstract)

    prompt_keywords = (
        "Traduce las siguientes palabras clave al inglés, manteniendo el orden y un estilo académico.\n"
        "Devuelve SOLO la lista en inglés, en minúsculas, separadas por coma.\n\n"
        f"Palabras clave en español: {palabras_clave}"
    )
    keywords = gpt(prompt_keywords)

    return abstract, keywords


def generar_introduccion(titulo_es: str, pais: str):
    """
    Genera la sección INTRODUCCION con:
      - 3 párrafos con instituciones internacionales/nacionales y datos (global, LATAM, país)
      - 1 párrafo de problema (sin referencias)
      - 1 párrafo de justificación (inicia con 'Se justifica')
    """
    # Párrafos con instituciones y datos (similar al modelo)
    prompt_intro_instituciones = (
        "Redacta TRES párrafos consecutivos para la INTRODUCCIÓN de un artículo de revisión bibliográfica "
        f"cuyo título es: \"{titulo_es}\".\n\n"
        "Estructura:\n"
        "Párrafo 1: panorama global (mundo) sobre la temática.\n"
        "Párrafo 2: situación en América Latina.\n"
        f"Párrafo 3: enfoque específico en el contexto de {pais}.\n\n"
        "Condiciones para CADA párrafo:\n"
        "- Entre 110 y 140 palabras.\n"
        "- Incluye al menos dos instituciones reconocidas (ej.: UNESCO, OMS/WHO, World Bank, OECD, "
        f"Ministerio de Salud de {pais}, Ministerio de Educación de {pais}, UNICEF, etc.).\n"
        "- Incluye al menos 2 o 3 datos cuantitativos (porcentajes, cifras de población, número de estudios, etc.).\n"
        "- Usa citas internas en estilo autor-fecha o institución-fecha, por ejemplo: "
        "(UNESCO, 2024), (OECD, 2025), Ministerio de Salud del Perú (2023).\n"
        "- La información debe situarse en los últimos 5-8 años.\n"
        "- Estilo académico, sin listas ni viñetas.\n"
    )
    intro_instituciones = gpt(prompt_intro_instituciones)
    time.sleep(1.5)

    # Problema (sin referencias)
    prompt_problema = (
        "Redacta UN solo párrafo (~90 palabras) de problema, causas y consecuencias, "
        f"relacionado con la temática del título: \"{titulo_es}\".\n\n"
        "Condiciones:\n"
        "- No incluyas citas a instituciones ni autores (sin referencias entre paréntesis).\n"
        "- No uses la palabra 'problema', 'causas' ni 'consecuencias' como subtítulos; integra todo en el discurso.\n"
        "- Estilo académico, tono crítico-reflexivo.\n"
        "- Enfocado en la realidad actual y las dificultades que justifican estudiar el tema.\n"
    )
    problema = gpt(prompt_problema)
    time.sleep(1.0)

    # Justificación
    prompt_justificacion = (
        "Redacta un párrafo de justificación (~100 palabras) para una revisión bibliográfica sobre la temática del título:\n"
        f"\"{titulo_es}\".\n\n"
        "Condiciones:\n"
        "- Debe iniciar EXACTAMENTE con la frase: 'Se justifica'.\n"
        "- Explica por qué el estudio es relevante en términos científicos, sociales y para la política pública.\n"
        "- No menciones explícitamente el título ni vuelvas a copiarlo.\n"
        "- No incluyas citas a autores ni instituciones.\n"
        "- Estilo Scopus Q3/Q2, prosa fluida.\n"
    )
    justificacion = gpt(prompt_justificacion)

    return intro_instituciones, problema, justificacion


def generar_marco_teorico(variable_1: str, variable_2: str):
    """
    Genera el MARCO TEORICO con:
      - Teoría 1 (asociada a variable_1)
      - Teoría 2 (asociada a variable_2)
      - 2 párrafos de concepto para variable_1
      - 2 párrafos de concepto para variable_2
    Inluye autores+años al estilo del modelo.
    """
    # Teorías
    prompt_teorias = (
        "Para una revisión bibliográfica que trabaja con las siguientes dos variables:\n"
        f"- {variable_1}\n"
        f"- {variable_2}\n\n"
        "Redacta DOS bloques de texto para el MARCO TEÓRICO, separados por doble salto de línea.\n"
        "Bloque 1: una teoría relevante asociada principalmente a la primera variable.\n"
        "Bloque 2: una teoría relevante asociada principalmente a la segunda variable.\n\n"
        "Condiciones para cada bloque:\n"
        "- Alrededor de 150–180 palabras.\n"
        "- Menciona claramente el nombre de la teoría y el apellido del autor o autores principales.\n"
        "- Incluye varias citas internas con apellidos y años entre paréntesis, por ejemplo (Drucker, 1954), "
        "(Isaka & Shimada, 2022).\n"
        "- Explica los supuestos clave de la teoría y cómo se relaciona con la variable.\n"
        "- Estilo académico en español, sin subtítulos ni listas.\n"
    )
    teorias_texto = gpt(prompt_teorias)
    bloques_teoria = [b.strip() for b in teorias_texto.split("\n\n") if b.strip()]
    while len(bloques_teoria) < 2:
        bloques_teoria.append("Teoría faltante.")
    teoria1, teoria2 = bloques_teoria[:2]
    time.sleep(1.5)

    # Conceptos
    prompt_conceptos = (
        "Redacta CUATRO párrafos para el MARCO TEÓRICO, separados por doble salto de línea, sobre las siguientes variables:\n"
        f"- {variable_1}\n"
        f"- {variable_2}\n\n"
        "Condiciones:\n"
        "- Párrafos 1 y 2: desarrollan el concepto teórico de la primera variable.\n"
        "- Párrafos 3 y 4: desarrollan el concepto teórico de la segunda variable.\n"
        "- Cada párrafo entre 110 y 130 palabras.\n"
        "- Cada párrafo debe iniciar con un conector de adición (ej.: 'De manera concordante,', "
        "'En consonancia con lo anterior,', 'Asimismo,', 'Además,').\n"
        "- Incluye al menos uno o dos apellidos de autores y años en cada párrafo, en estilo de cita interna "
        "por ejemplo (Gryshchenko et al., 2021), (Rakhimov, 2021).\n"
        "- Estilo académico, sin listas.\n"
    )
    conceptos_texto = gpt(prompt_conceptos)
    bloques_conceptos = [b.strip() for b in conceptos_texto.split("\n\n") if b.strip()]
    while len(bloques_conceptos) < 4:
        bloques_conceptos.append("Concepto faltante.")

    c1_p1, c1_p2, c2_p1, c2_p2 = bloques_conceptos[:4]

    return teoria1, teoria2, c1_p1, c1_p2, c2_p1, c2_p2


def generate_article(tema: str, nivel: str, pais: str):
    """
    FUNCIÓN PRINCIPAL (Fase 1 corregida para parecerse al MODELO).
    Devuelve:
      - titulo (español)
      - variable_1
      - variable_2
      - texto_articulo: con Título EN, SCOPUSq3, Resumen, Abstract, INTRODUCCION, MARCO TEORICO.
    """
    # 1) Título en español
    titulo_es = generar_titulo_es(tema, pais, nivel)
    time.sleep(1.5)

    # 2) Título en inglés
    titulo_en = generar_titulo_en(titulo_es)
    time.sleep(1.0)

    # 3) Rotulo de indexación (SCOPUSq3, etc.)
    index_label = normalizar_indexacion(nivel)

    # 4) Variables desde el título
    variable_1, variable_2 = extraer_variables_desde_titulo(titulo_es)
    print("📌 Variables extraídas:", variable_1, "/", variable_2)

    # 5) Resumen, palabras clave, abstract y keywords
    resumen_es, palabras_clave_es = generar_resumen_y_palabras_clave(titulo_es, variable_1, variable_2, nivel, pais)
    time.sleep(1.0)
    resumen_en, palabras_clave_en = generar_abstract_y_keywords(resumen_es, palabras_clave_es)
    time.sleep(1.0)

    # 6) Introducción (instituciones + problema + justificación)
    intro_instituciones, problema, justificacion = generar_introduccion(titulo_es, pais)
    time.sleep(1.0)

    # 7) Marco teórico (teorías + conceptos) con autores y años
    teoria1, teoria2, c1_p1, c1_p2, c2_p1, c2_p2 = generar_marco_teorico(variable_1, variable_2)

    # 8) Construir TEXTO FINAL con estructura similar al modelo
    partes = []

    # Título en inglés y rótulo de indexación van al inicio del texto (el título en español lo pone docx_writer como heading)
    if titulo_en:
        partes.append(titulo_en)
    if index_label:
        partes.append(index_label)

    # Resumen y palabras clave
    partes.append("RESUMEN")
    partes.append(resumen_es)
    partes.append(f"Palabras clave: {palabras_clave_es}")

    # Abstract y keywords
    partes.append("ABSTRACT")
    partes.append(resumen_en)
    partes.append(f"Keywords: {palabras_clave_en}")

    # Introducción
    partes.append("INTRODUCCION")
    partes.append(intro_instituciones)
    partes.append(problema)
    partes.append(justificacion)

    # Marco teórico
    partes.append("MARCO TEORICO")
    partes.append(teoria1)
    partes.append(teoria2)
    partes.append(c1_p1)
    partes.append(c1_p2)
    partes.append(c2_p1)
    partes.append(c2_p2)

    texto_articulo = "\n\n".join(p.strip() for p in partes if isinstance(p, str) and p.strip())

    if not texto_articulo or len(texto_articulo) < 400:
        raise ValueError("❌ El contenido del artículo es muy corto o está vacío.")

    return {
        "titulo": titulo_es,
        "variable_1": variable_1,
        "variable_2": variable_2,
        "texto_articulo": texto_articulo,
    }
