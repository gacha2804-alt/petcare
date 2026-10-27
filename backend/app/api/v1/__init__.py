from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.mascotas import router as mascotas_router
from app.api.v1.agenda import router as agenda_router
from app.api.v1.citas import router as citas_router
from app.api.v1.chat import router as chat_router
from app.api.v1.historial import router as historial_router
from app.api.v1.cloudinary_upload import router as cloudinary_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(mascotas_router)
api_router.include_router(agenda_router)
api_router.include_router(citas_router)
api_router.include_router(chat_router)
api_router.include_router(historial_router)
api_router.include_router(cloudinary_router)
