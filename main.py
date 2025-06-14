from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generator import generate_article

app = FastAPI()

# CORS para permitir solicitudes desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes reemplazar * por ["https://frontend-generador-one.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta principal
@app.get("/")
def root():
    return {"message": "API del generador de artículos funcionando."}

# Ruta para generar el artículo (usada por el frontend)
@app.post("/generar")
def generar_articulo(tema: str, nivel: str = "Scopus"):
    ruta_archivo = generate_article(tema, nivel)
    return FileResponse(ruta_archivo, filename="articulo_generado.docx")
