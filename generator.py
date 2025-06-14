from docx import Document
from datetime import datetime

def generate_article(tema, nivel):
    doc = Document()
    doc.add_heading(f"Artículo generado automáticamente – {nivel}", 0)
    doc.add_paragraph(f"Tema: {tema}")
    doc.add_paragraph("Este es un ejemplo de artículo generado automáticamente.")
    doc.add_paragraph("Contendrá: resumen, introducción, marco teórico, metodología, etc.")
    filename = f"/tmp/articulo_{datetime.now().strftime('%Y%m%d%H%M%S')}.docx"
    doc.save(filename)
    return filename
