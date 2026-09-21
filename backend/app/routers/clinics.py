from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.clinic import ClinicCreate, ClinicResponse
from app.services.clinic_service import ClinicService
from app.middlewares.auth_guard import require_roles
from app.models.user import User

router = APIRouter(prefix="/clinics", tags=["Veterinarias y Geolocalización"])


@router.get("", response_model=List[ClinicResponse])
def list_clinics(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    urgencias: bool = False,
    db: Session = Depends(get_db)
):
    """
    Lista las clínicas veterinarias disponibles. Si se envían coordenadas GPS (lat, lon),
    calcula la distancia en kilómetros y las ordena de la más cercana a la más lejana.
    """
    return ClinicService.list_clinics(db, lat=lat, lon=lon, only_urgencias=urgencias)


@router.post("", response_model=ClinicResponse, status_code=status.HTTP_201_CREATED)
def create_clinic(
    data: ClinicCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles(["administrador"]))
):
    """Registra una nueva sede de clínica veterinaria. Exclusivo para administradores."""
    return ClinicService.create_clinic(db, data)
