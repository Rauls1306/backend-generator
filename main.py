from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid

from generator import generate_article
from docx_writer import save_article_to_docx

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

@app.post("/generar-articulo")
def generar_articulo(data: GeneradorInput):
    try:
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
        print("❌ Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

