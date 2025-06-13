from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generator import generate_article

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar "*" por ["https://frontend-generador-one.vercel.app"] si quieres limitarlo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
