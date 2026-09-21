from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TriageRequest(BaseModel):
    mascota_id: int
    descripcion_sintomas: str = Field(..., min_length=10)


class TriageResponse(BaseModel):
    mascota_id: int
    nivel_urgencia: str  # bajo, moderado, alto
    orientacion_preventiva: str
    recomendaciones: List[str]
    sugerir_agendar_cita: bool
    disclaimer: str = (
        "AVISO IMPORTANTE: Esta orientación es generada por una Inteligencia Artificial "
        "con fines exclusivamente preventivos e informativos. No constituye un diagnóstico médico "
        "ni reemplaza la consulta profesional con un médico veterinario colegiado."
    )
    fecha_analisis: datetime


class ClinicalSummaryResponse(BaseModel):
    mascota_id: int
    nombre_mascota: str
    especie: str
    edad_aproximada_meses: Optional[int] = None
    resumen_ejecutivo: str
    sintomas_recientes: List[str]
    medicamentos_activos: List[str]
    vacunas_vigentes: List[str]
    alertas_detectadas: List[str]
    fecha_generacion: datetime
