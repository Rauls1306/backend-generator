import os
os.system("pip install openai==0.28 --upgrade")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import Request
from generator import generate_article

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Usa * para pruebas, luego puedes restringir
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
    pais = data.get("pais", "Perú")  # ✅ por defecto, si no se envía desde frontend
    ruta_archivo = generate_article(tema, nivel, pais)
    return FileResponse(ruta_archivo, filename="articulo_generado.docx")
