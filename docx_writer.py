from docx import Document
from docx.shared import Pt

def save_article_to_docx(texto, ruta_salida):
    doc = Document()
    for parrafo in texto.split("\n\n"):
        if parrafo.strip():
            p = doc.add_paragraph(parrafo.strip())
            p.style.font.size = Pt(11)
    doc.save(ruta_salida)
