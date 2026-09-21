from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.health import (
    VaccineCreate, VaccineResponse,
    VaccineProtocolCreate, VaccineProtocolResponse,
    MedicationCreate, MedicationResponse,
    SymptomCreate, SymptomResponse,
    WeightCreate, WeightResponse,
    ClinicalConsultationCreate, ClinicalConsultationResponse,
    TimelineEvent, ReminderItem
)
from app.services.health_service import HealthService
from app.middlewares.auth_guard import get_current_user, require_roles
from app.models.user import User

router = APIRouter(prefix="/health", tags=["Salud e Historial"])


# Protocolos de Refuerzo (RF-02 / RF-03)
@router.post("/protocols", response_model=VaccineProtocolResponse, status_code=status.HTTP_201_CREATED)
def create_vaccine_protocol(
    data: VaccineProtocolCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(["administrador", "veterinario"]))
):
    """Configura un protocolo de refuerzo por producto, especie y categoría de edad (RF-02)."""
    return HealthService.add_vaccine_protocol(db, data)


@router.get("/protocols", response_model=List[VaccineProtocolResponse])
def list_vaccine_protocols(
    tipo_aplicacion: Optional[str] = None,
    especie: Optional[str] = None,
    categoria_edad: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista protocolos de refuerzo activos con filtros opcionales."""
    return HealthService.list_vaccine_protocols(db, tipo_aplicacion, especie, categoria_edad)


# Consultas Médicas y Diagnósticos Profesionales (Exclusivo Veterinario)
@router.post("/{pet_id}/consultations", response_model=ClinicalConsultationResponse, status_code=status.HTTP_201_CREATED)
def add_consultation(
    pet_id: int,
    data: ClinicalConsultationCreate,
    db: Session = Depends(get_db),
    vet: User = Depends(require_roles(["veterinario"]))
):
    """Registra una consulta formal con anamnesis, constantes vitales y diagnóstico profesional."""
    return HealthService.add_clinical_consultation(db, pet_id, vet.id, data)


@router.get("/{pet_id}/consultations", response_model=List[ClinicalConsultationResponse])
def get_consultations(pet_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Obtiene el historial de diagnósticos y consultas médicas de la mascota."""
    return HealthService.get_consultations_by_pet(db, pet_id)


# Vacunas
@router.post("/{pet_id}/vaccines", response_model=VaccineResponse, status_code=status.HTTP_201_CREATED)
def add_vaccine(
    pet_id: int,
    data: VaccineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["veterinario", "propietario"]))
):
    """Registra una dosis de vacuna aplicada o esquema histórico."""
    return HealthService.add_vaccine(db, pet_id, current_user.id, data)


@router.get("/{pet_id}/vaccines", response_model=List[VaccineResponse])
def get_vaccines(pet_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Obtiene el historial de vacunación de una mascota."""
    return HealthService.get_vaccines_by_pet(db, pet_id)


# Medicamentos (Prescripción Médica Restringida a Veterinarios)
@router.post("/{pet_id}/medications", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
def add_medication(
    pet_id: int,
    data: MedicationCreate,
    db: Session = Depends(get_db),
    vet: User = Depends(require_roles(["veterinario"]))
):
    """Prescribe un fármaco o tratamiento médico activo. Exclusivo para médicos veterinarios."""
    return HealthService.add_medication(db, pet_id, vet.id, data)


@router.get("/{pet_id}/medications", response_model=List[MedicationResponse])
def get_medications(pet_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Lista los medicamentos y prescripciones registradas para la mascota."""
    return HealthService.get_medications_by_pet(db, pet_id)


# Recordatorios Activos de Vacunas y Medicación
@router.get("/{pet_id}/reminders", response_model=List[ReminderItem])
def get_reminders(pet_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Obtiene las alertas y recordatorios de vacunas próximas a vencer y tratamientos activos."""
    return HealthService.get_active_reminders(db, pet_id)


# Síntomas
@router.post("/{pet_id}/symptoms", response_model=SymptomResponse, status_code=status.HTTP_201_CREATED)
def add_symptom(
    pet_id: int,
    data: SymptomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario"]))
):
    """Registra la aparición de un síntoma o cambio conductual detectado en casa."""
    return HealthService.add_symptom(db, pet_id, current_user.id, data)


@router.get("/{pet_id}/symptoms", response_model=List[SymptomResponse])
def get_symptoms(pet_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Consulta la bitácora de síntomas observados en la mascota."""
    return HealthService.get_symptoms_by_pet(db, pet_id)


# Peso y Evolución
@router.post("/{pet_id}/weight", response_model=WeightResponse, status_code=status.HTTP_201_CREATED)
def add_weight(
    pet_id: int,
    data: WeightCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario", "veterinario"]))
):
    """Registra una medición periódica de peso corporal en kilogramos."""
    return HealthService.add_weight_record(db, pet_id, data)


@router.get("/{pet_id}/weight", response_model=List[WeightResponse])
def get_weights(pet_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Obtiene la curva histórica de peso corporal de la mascota."""
    return HealthService.get_weight_history(db, pet_id)


# Línea de Tiempo Unificada
@router.get("/{pet_id}/timeline", response_model=List[TimelineEvent])
def get_timeline(pet_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Obtiene el expediente cronológico consolidado (vacunas, fármacos, síntomas y peso)."""
    return HealthService.get_medical_timeline(db, pet_id)
