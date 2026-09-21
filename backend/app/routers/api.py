from fastapi import APIRouter
from app.routers import auth, users, pets, health, appointments, notifications, emergency, clinics, ai

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(pets.router)
api_router.include_router(health.router)
api_router.include_router(appointments.router)
api_router.include_router(notifications.router)
api_router.include_router(emergency.router)
api_router.include_router(clinics.router)
api_router.include_router(ai.router)
