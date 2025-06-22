from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generator import generate_article
import os

# Si ya tienes instalada openai, puedes comentar esta línea
os.system("pip install openai==0.28 --upgrade")

app = FastAPI()

# CORS configurado correctamente para el frontend en Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-generator-one.vercel.app"],  # tu frontend en vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API funcionando"}

@app.post("/generar")
async def generar_articulo(request: Request):
    try:
        data = await request.json()
        print("Datos recibidos:", data)

        tema = data.get("tema")
        nivel = data.get("nivel", "Scopus")
        pais = data.get("pais", "Perú")

        ruta_archivo = generate_article(tema, nivel, pais)
        return FileResponse(ruta_archivo, filename="articulo_generado.docx")
    except Exception as e:
        print(f"❌ Error en /generar: {str(e)}")
        return {"error": f"No se pudo generar el artículo: {str(e)}"}
