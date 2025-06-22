from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from generator import generate_article
import os

app = FastAPI()

# Middleware CORS (habilita solicitudes desde el dominio de Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-generator-one.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta para preflight OPTIONS (necesaria para evitar 400 Bad Request)
@app.options("/generar")
async def preflight_handler():
    return JSONResponse(status_code=200, content={"ok": True})

@app.get("/")
def root():
    return {"message": "API funcionando"}

@app.post("/generar")
async def generar_articulo(request: Request):
    data = await request.json()
    print("Datos recibidos:", data)

    tema = data.get("tema")
    nivel = data.get("nivel", "Scopus")
    pais = data.get("pais", "Perú")

    try:
        ruta_archivo = generate_article(tema, nivel, pais)
        return FileResponse(ruta_archivo, filename="articulo_generado.docx")
    except Exception as e:
        print(f"Error al generar el artículo: {str(e)}")
        return JSONResponse(status_code=500, content={"error": f"No se pudo generar el artículo: {str(e)}"})
