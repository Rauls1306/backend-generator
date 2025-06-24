from docx import Document

def save_article_to_docx(texto, ruta_archivo):
    try:
        doc = Document()
        doc.add_heading("Artículo científico", 0)

        for linea in texto.split("\n"):
            if linea.strip():
                doc.add_paragraph(linea.strip())

        doc.save(ruta_archivo)
    except Exception as e:
        print("❌ Error al guardar el DOCX:", str(e))
        raise e
