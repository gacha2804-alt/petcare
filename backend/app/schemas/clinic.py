from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ClinicBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    direccion: str = Field(..., min_length=5, max_length=255)
    telefono: str = Field(..., min_length=5, max_length=50)
    email: Optional[str] = None
    latitud: float
    longitud: float
    horario_atencion: Optional[str] = None
    tiene_urgencias_24h: bool = False


class ClinicCreate(ClinicBase):
    pass


class ClinicResponse(ClinicBase):
    id: int
    activa: bool
    distancia_km: Optional[float] = None
    fecha_creacion: datetime

    model_config = {"from_attributes": True}
