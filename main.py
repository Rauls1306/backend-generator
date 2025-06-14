from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generator import generate_article

app = FastAPI()

# CONFIGURACIÓN CORS FUNCIONAL
origins = [
    "https://frontend-generador-one.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API del generador de artículos funcionando."}

@app.post("/generar")
def generar_articulo(tema: str, nivel: str = "Scopus"):
    ruta_archivo = generate_article(tema, nivel)
    return FileResponse(ruta_archivo, filename="articulo_generado.docx")
