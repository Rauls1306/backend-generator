from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid

from generator import generate_article
from docx_writer import save_article_to_docx
from dotenv import load_dotenv
load_dotenv()

print("API KEY:", openai.api_key)
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción restringe esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class GeneradorInput(BaseModel):
    nombre: str
    pais: str
    tipoArticulo: str
    tema: str

class ArticuloRequest(BaseModel):
    tema: str
    nivel: str
    pais: str

@app.post("/generar-articulo")
def generar_articulo(data: GeneradorInput):
    try:
        # 🟡 DEBUG: Verifica los datos recibidos
        print("✅ Datos recibidos en el endpoint /generar-articulo:")
        print(data.model_dump())

        # Paso 1: Generar todo el contenido
        resultado = generate_article(data.tema, data.tipoArticulo, data.pais)

        # Paso 2: Guardar el documento Word
        filename = f"{uuid.uuid4()}.docx"
        output_dir = "./output"
        os.makedirs(output_dir, exist_ok=True)
        ruta_archivo = os.path.join(output_dir, filename)

        save_article_to_docx(resultado["texto_articulo"], ruta_archivo)

        # Paso 3: Devolver respuesta completa
        return {
            "titulo": resultado["titulo"],
            "variable_1": resultado["variable_1"],
            "variable_2": resultado["variable_2"],
            "texto_articulo": resultado["texto_articulo"],
            "archivo_generado": ruta_archivo
        }

    except Exception as e:
        # 🔴 Imprimir el error para depurar
        print("❌ Error durante la generación del artículo:")
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/generar-articulo")
# async def generar_articulo(request: Request):
#     body = await request.body()
#     print("🧾 Body recibido crudo:", body.decode())
#     return {"mensaje": "OK (solo para debug)"}