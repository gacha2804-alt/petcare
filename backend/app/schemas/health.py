from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Vacunas
class VaccineProtocolBase(BaseModel):
    nombre_producto: str = Field(..., min_length=2, max_length=150)
    fabricante: Optional[str] = Field(None, max_length=150)
    tipo_aplicacion: str = Field("vacuna", pattern="^(vacuna|desparasitacion)$")
    especie: str = Field(..., min_length=2, max_length=50)
    categoria_edad: str = Field(..., pattern="^(cachorro|adulto|senior|todas)$")
    edad_min_meses: Optional[int] = Field(None, ge=0)
    edad_max_meses: Optional[int] = Field(None, ge=0)
    intervalo_refuerzo_dias: int = Field(..., ge=1, le=3650)
    esquema_refuerzos: Optional[dict] = None
    requiere_alerta_previa_dias: int = Field(7, ge=0, le=90)
    descripcion: Optional[str] = None
    activo: bool = True


class VaccineProtocolCreate(VaccineProtocolBase):
    pass


class VaccineProtocolResponse(VaccineProtocolBase):
    id: int
    fecha_creacion: datetime

    model_config = {"from_attributes": True}


class VaccineBase(BaseModel):
    nombre_vacuna: str = Field(..., min_length=2, max_length=100)
    tipo_aplicacion: str = Field("vacuna", pattern="^(vacuna|desparasitacion)$")
    fabricante: Optional[str] = Field(None, max_length=150)
    lote: Optional[str] = None
    dosis: Optional[str] = Field(None, max_length=100)
    via_aplicacion: Optional[str] = Field(None, max_length=50)
    peso_kg: Optional[float] = Field(None, gt=0, le=200.0)
    edad_aplicacion: Optional[str] = Field(None, max_length=30)
    protocolo_id: Optional[int] = None
    fecha_aplicacion: date
    fecha_proxima_dosis: Optional[date] = None
    novedades: Optional[str] = None
    observaciones: Optional[str] = None


class VaccineCreate(VaccineBase):
    pass


class VaccineResponse(VaccineBase):
    id: int
    mascota_id: int
    veterinario_id: Optional[int] = None
    fecha_creacion: datetime
    aviso: Optional[str] = None

    model_config = {"from_attributes": True}


# Medicamentos
class MedicationBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    dosis: str = Field(..., min_length=1, max_length=100)
    frecuencia_horas: int = Field(..., ge=1, le=72)
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    indicaciones: Optional[str] = None
    activo: bool = True


class MedicationCreate(MedicationBase):
    pass


class MedicationResponse(MedicationBase):
    id: int
    mascota_id: int
    veterinario_id: Optional[int] = None
    fecha_creacion: datetime

    model_config = {"from_attributes": True}


# Peso
class WeightCreate(BaseModel):
    peso_kg: float = Field(..., ge=0.1, le=200.0)
    fecha_registro: date
    notas: Optional[str] = None


class WeightResponse(WeightCreate):
    id: int
    mascota_id: int

    model_config = {"from_attributes": True}


# Síntomas y Observaciones
class SymptomCreate(BaseModel):
    tipo: str = Field(..., pattern="^(sintoma|observacion_conductual|anomalia)$")
    descripcion: str = Field(..., min_length=3)
    severidad: str = Field("leve", pattern="^(leve|moderada|grave)$")
    fecha_inicio: datetime


class SymptomResponse(BaseModel):
    id: int
    mascota_id: int
    usuario_id: int
    tipo: str
    descripcion: str
    severidad: str
    fecha_inicio: datetime
    resuelto: bool
    fecha_registro: datetime

    model_config = {"from_attributes": True}


# Consultas Médicas y Diagnósticos Profesionales
class ClinicalConsultationCreate(BaseModel):
    motivo: str = Field(..., min_length=3, max_length=255)
    anamnesis: Optional[str] = None
    constantes_vitales: Optional[str] = None  # Temp, FC, FR, Mucosas
    diagnostico_profesional: str = Field(..., min_length=5)
    plan_tratamiento: str = Field(..., min_length=5)
    notas_adicionales: Optional[str] = None


class ClinicalConsultationResponse(ClinicalConsultationCreate):
    id: int
    mascota_id: int
    veterinario_id: int
    nombre_veterinario: Optional[str] = None
    tarjeta_profesional: Optional[str] = None
    fecha_consulta: datetime
    origen_registro: str = "profesional_veterinario"
    fecha_creacion: datetime

    model_config = {"from_attributes": True}


# Evento genérico enriquecido en el timeline médico
class TimelineEvent(BaseModel):
    tipo_evento: str  # consulta_diagnostico, vacuna, medicamento, peso, sintoma, cita
    id_referencia: int
    fecha: datetime
    titulo: str
    descripcion: str
    origen_registro: str  # profesional_veterinario | propietario_hogar
    autor_nombre: str
    autor_rol: str
    tarjeta_profesional: Optional[str] = None
    detalles: Optional[dict] = None


# Recordatorios Activos
class ReminderItem(BaseModel):
    tipo: str  # vacuna_proxima, vacuna_vencida, medicamento_toma, medicamento_fin
    titulo: str
    mensaje: str
    fecha_limite: date
    urgente: bool
    referencia_id: int

