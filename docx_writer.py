from docx import Document

def save_article_to_docx(texto, ruta_salida):
    doc = Document()
    for parrafo in texto.split("\n\n"):
        doc.add_paragraph(parrafo.strip())
    doc.save(ruta_salida)
