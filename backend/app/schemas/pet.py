from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class PetBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    especie: str = Field(..., min_length=1, max_length=50)  # Canino, Felino, etc.
    raza: Optional[str] = Field(None, max_length=100)
    sexo: str = Field(..., pattern="^(macho|hembra)$")
    fecha_nacimiento: Optional[date] = None
    esterilizado: bool = False
    peso_actual: Optional[float] = Field(None, ge=0.1, le=200.0)
    foto_url: Optional[str] = None
    contacto_emergencia_tel: Optional[str] = Field(None, max_length=30)
    condiciones_criticas: Optional[str] = None  # Alergias, enfermedades crónicas


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    especie: Optional[str] = Field(None, min_length=1, max_length=50)
    raza: Optional[str] = None
    sexo: Optional[str] = Field(None, pattern="^(macho|hembra)$")
    fecha_nacimiento: Optional[date] = None
    esterilizado: Optional[bool] = None
    peso_actual: Optional[float] = Field(None, ge=0.1, le=200.0)
    foto_url: Optional[str] = None
    contacto_emergencia_tel: Optional[str] = None
    condiciones_criticas: Optional[str] = None


class PetResponse(PetBase):
    id: int
    propietario_id: int
    codigo_qr_token: str
    activa: bool
    fecha_creacion: datetime

    model_config = {"from_attributes": True}


class PetSummary(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: Optional[str] = None
    sexo: str
    peso_actual: Optional[float] = None
    foto_url: Optional[str] = None
    codigo_qr_token: str

    model_config = {"from_attributes": True}
