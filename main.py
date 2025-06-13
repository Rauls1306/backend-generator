from fastapi import FastAPI
from fastapi.responses import FileResponse
from generator import generate_article

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API del generador de artículos funcionando."}

@app.post("/generar")
def generar_articulo(tema: str, nivel: str = "Scopus"):
    ruta_archivo = generate_article(tema, nivel)
    return FileResponse(ruta_archivo, filename="articulo_generado.docx")