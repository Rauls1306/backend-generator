from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generator import generate_article
import os

# Forzar instalación de la versión funcional de OpenAI
os.system("pip install openai==0.28 --upgrade")

app = FastAPI()

# CORS habilitado para pruebas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir después
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API funcionando"}

@app.post("/generar")
async def generar_articulo(request: Request):
    data = await request.json()
    print("Datos recibidos:", data)  # 👈 Esto nos dirá qué llega desde el frontend
    tema = data.get("tema")
    nivel = data.get("nivel", "Scopus")
    pais = data.get("pais", "Perú")
    ruta_archivo = generate_article(tema, nivel, pais)
    return FileResponse(ruta_archivo, filename="articulo_generado.docx")
