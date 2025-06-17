import os
os.system("pip install openai==0.28 --upgrade")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generator import generate_article

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-generador-one.vercel.app"],  # ✅ dominio frontend autorizado
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
    tema = data.get("tema")
    nivel = data.get("nivel", "Scopus")
    pais = data.get("pais", "Perú")  # ✅ Perú por defecto si no viene del frontend
    ruta_archivo = generate_article(tema, nivel, pais)
    return FileResponse(ruta_archivo, filename="articulo_generado.docx")
