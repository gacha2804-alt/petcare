from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class SedeOut(BaseModel):
    id: int
    nombre: str
    direccion: str
    telefono: Optional[str] = None
    activa: bool
    es_una_de_dos_sedes: bool

    class Config:
        from_attributes = True

class DisponibilidadOut(BaseModel):
    id: int
    id_agenda: int
    fecha: date
    hora_inicio: str
    hora_fin: str
    disponible: bool
    ocupado: bool

    class Config:
        from_attributes = True

class CitaCreate(BaseModel):
    id_mascota: int
    id_sede: int
    id_disponibilidad: int
    motivo_consulta: str = Field(..., min_length=3)

class CitaOut(BaseModel):
    id: int
    id_mascota: int
    id_propietario: int
    id_sede: int
    id_veterinario: Optional[int] = None
    id_agenda: int
    id_disponibilidad: int
    fecha_cita: date
    hora_cita: str
    motivo_consulta: str
    estado: str
    fecha_solicitud: datetime
    fecha_confirmacion: Optional[datetime] = None
    sede_nombre: Optional[str] = None
    mascota_nombre: Optional[str] = None

    class Config:
        from_attributes = True
