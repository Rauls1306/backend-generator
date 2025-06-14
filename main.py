from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generator import generate_article

app = FastAPI()

# CORS CORRECTO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-generador-one.vercel.app"],  # Aquí se especifica tu dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API funcionando"}

@app.post("/generar")
def generar_articulo(tema: str, nivel: str = "Scopus"):
    ruta_archivo = generate_article(tema, nivel)
    return FileResponse(ruta_archivo, filename="articulo_generado.docx")
