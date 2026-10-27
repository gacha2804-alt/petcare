from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class MascotaCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    especie: str = Field(..., min_length=1, max_length=50) # Perro, Gato, etc.
    sexo: str = Field(..., min_length=1, max_length=20) # Macho, Hembra
    fecha_nacimiento: date
    datos_identificatorios: Optional[str] = None # Raza, color, microchip
    imagen_url: Optional[str] = None # Cloudinary secure_url

class MascotaUpdate(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    datos_identificatorios: Optional[str] = None
    imagen_url: Optional[str] = None

class MascotaOut(BaseModel):
    id: int
    id_propietario: int
    nombre: str
    especie: str
    sexo: str
    fecha_nacimiento: date
    datos_identificatorios: Optional[str] = None
    imagen_url: Optional[str] = None
    fecha_registro: datetime

    class Config:
        from_attributes = True
