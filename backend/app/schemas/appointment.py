from datetime import datetime, date, time
from typing import Optional
from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    mascota_id: int
    clinica_id: int
    veterinario_id: Optional[int] = None
    slot_id: Optional[int] = None
    fecha_hora: datetime
    motivo: str = Field(..., min_length=5)


class AppointmentUpdateStatus(BaseModel):
    estado: str = Field(..., pattern="^(pendiente|confirmada|cancelada|completada)$")
    diagnostico_consulta: Optional[str] = None
    indicaciones_consulta: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    mascota_id: int
    propietario_id: int
    veterinario_id: Optional[int] = None
    clinica_id: int
    fecha_hora: datetime
    motivo: str
    estado: str
    diagnostico_consulta: Optional[str] = None
    indicaciones_consulta: Optional[str] = None
    fecha_creacion: datetime

    model_config = {"from_attributes": True}


class SlotCreate(BaseModel):
    clinica_id: int
    veterinario_id: Optional[int] = None
    fecha: date
    hora_inicio: time
    hora_fin: time
    tipo_atencion: str = Field("consulta", pattern="^(consulta|vacunacion|urgencia)$")
    notas: Optional[str] = None


class SlotResponse(BaseModel):
    id: int
    clinica_id: int
    veterinario_id: Optional[int] = None
    fecha: date
    hora_inicio: time
    hora_fin: time
    tipo_atencion: str
    estado: str
    cita_id: Optional[int] = None
    notas: Optional[str] = None
    fecha_creacion: datetime

    model_config = {"from_attributes": True}


class WaitlistCreate(BaseModel):
    clinica_id: int
    slot_id: Optional[int] = None
    mascota_id: Optional[int] = None
    motivo: Optional[str] = Field(None, max_length=255)


class WaitlistResponse(BaseModel):
    id: int
    clinica_id: int
    slot_id: Optional[int] = None
    usuario_id: int
    mascota_id: Optional[int] = None
    motivo: Optional[str] = None
    estado: str
    fecha_solicitud: datetime
    fecha_notificacion: Optional[datetime] = None
    fecha_expiracion: Optional[datetime] = None

    model_config = {"from_attributes": True}
