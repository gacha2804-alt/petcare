from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.core.config import settings
from app.api.v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API de Backend para la plataforma PetCare: Mascotas, Agenda, Citas y Asistente IA con Gemini",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos locales de subidas (fallback para dev)
uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Incluir Rutas de la API v1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "sistema": "PetCare Backend API",
        "estado": "operativo",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": "2026-10-25"}
