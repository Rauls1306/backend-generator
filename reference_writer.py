# reference_wirter.py
from docx import Document
from datetime import datetime
import re
import openai

def resumir_titulo(titulo, max_palabras=10):
    palabras = titulo.split()
    if len(palabras) <= max_palabras:
        return titulo
    return " ".join(palabras[:max_palabras])

def extraer_titulo_y_autor(teoria_texto):
    match = re.search(r"(teoría|modelo|enfoque) de ([\w\s]+?) propuesta? por ([\w\s]+)", teoria_texto.lower())
    if match:
        titulo = match.group(2).strip().title()
        autor = match.group(3).strip().title()
        return f"{titulo} – {autor}"
    return "Teoría no identificada"

def generate_references_from_text(cited_text: str) -> list:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un generador de referencias académicas en formato APA 7. Solo responde con la lista de referencias sin explicaciones."
                },
                {
                    "role": "user",
                    "content": f"Extrae y genera las referencias APA 7 basadas en las citas del siguiente texto:\n\n{cited_text}"
                }
            ]
        )
        raw = response.choices[0].message.content.strip()
        return [line.strip() for line in raw.split("\n") if line.strip()]
    except Exception as e:
        print("❌ Error generando referencias con OpenAI:", e)
        return ["Referencia simulada (2024)."]

def generate_reference_doc(titulo: str, pais: str, referencias_dict: dict) -> str:
    doc = Document()

    # Título principal
    doc.add_heading("Plantilla de referencias", level=0)
    titulo_resumido = resumir_titulo(titulo)
    doc.add_paragraph(titulo_resumido, style='Title')
    doc.add_paragraph("")

    # Secciones de referencias con textos ya citados
    secciones = [
        ("Problemática mundial", "mundial"),
        ("Problemática latinoamericana (LATAM)", "latam"),
        (f"Problemática nacional – {pais}", "peru"),
        ("Teoría 1", "teoria1"),
        ("Teoría 2", "teoria2"),
        ("Variable 1", "variable1"),
        ("Variable 2", "variable2"),
    ]

    for titulo_seccion, clave in secciones:
        doc.add_heading(titulo_seccion, level=2)
        textos_con_citas = referencias_dict.get(clave)

        if textos_con_citas and isinstance(textos_con_citas, list):
            texto_unido = "\n".join(textos_con_citas)
            referencias = generate_references_from_text(texto_unido)
            for ref in referencias:
                doc.add_paragraph(ref, style='Normal')
        else:
            doc.add_paragraph("(No se encontraron textos citados para esta sección)", style='Normal')

    # Guardar documento con timestamp
    filename = f"referencias_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
