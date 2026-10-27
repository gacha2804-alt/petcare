from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class VacunaCreate(BaseModel):
    nombre_vacuna: str
    fecha_aplicacion: date
    fecha_proxima_recomendada: Optional[date] = None
    lote: Optional[str] = None
    dosis: Optional[str] = None

class VacunaOut(BaseModel):
    id: int
    id_mascota: int
    nombre_vacuna: str
    fecha_aplicacion: date
    fecha_proxima_recomendada: Optional[date] = None
    lote: Optional[str] = None
    dosis: Optional[str] = None

    class Config:
        from_attributes = True

class DesparasitacionCreate(BaseModel):
    tipo_tratamiento: str # Interna, Externa
    producto: str
    fecha_tratamiento: date
    fecha_proxima_recomendada: Optional[date] = None

class DesparasitacionOut(BaseModel):
    id: int
    id_mascota: int
    tipo_tratamiento: str
    producto: str
    fecha_tratamiento: date
    fecha_proxima_recomendada: Optional[date] = None

    class Config:
        from_attributes = True

class ConsultaCreate(BaseModel):
    id_mascota: int
    motivo_consulta: str
    diagnostico_registrado: str
    observaciones: Optional[str] = None
    id_sede: Optional[int] = None

class ConsultaOut(BaseModel):
    id: int
    id_historial: int
    id_mascota: int
    id_veterinario: int
    id_sede: Optional[int] = None
    fecha_consulta: datetime
    motivo_consulta: str
    diagnostico_registrado: str
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True

class HistorialOut(BaseModel):
    id: int
    id_mascota: int
    id_propietario: int
    fecha_creacion: datetime
    observaciones_generales: Optional[str] = None
    consultas: List[ConsultaOut] = []
    vacunas: List[VacunaOut] = []
    desparasitaciones: List[DesparasitacionOut] = []

    class Config:
        from_attributes = True
