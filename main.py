from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generator import generate_article
import os

# Instalar versión correcta de OpenAI si es necesario
os.system("pip install openai==0.28 --upgrade")

# Forzar redeploy - sin impacto
app = FastAPI()

# Desbloqueo total de CORS para pruebas (luego puedes restringir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    print("Datos recibidos:", data)

    tema = data.get("tema")
    nivel = data.get("nivel", "Scopus")
    pais = data.get("pais", "Perú")

    try:
        ruta_archivo = generate_article(tema, nivel, pais)
        return FileResponse(
            ruta_archivo,
            filename="articulo_generado.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}
