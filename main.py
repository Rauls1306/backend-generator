from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.routing import APIRoute
from generator import generate_article

app = FastAPI()

# CORS: permitir desde Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-generator-one.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API funcionando"}

# RUTA MANUAL OPCIONAL para OPTIONS si sigue dando 400
@app.options("/generar")
async def preflight_handler():
    return JSONResponse(content={"ok": True}, status_code=200)

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
        print(f"Error al generar el artículo: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"No se pudo generar el artículo: {str(e)}"},
        )
