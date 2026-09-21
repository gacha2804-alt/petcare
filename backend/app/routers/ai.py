from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.ai import TriageRequest, TriageResponse, ClinicalSummaryResponse
from app.services.ai_service import AIService
from app.middlewares.auth_guard import get_current_user, require_roles
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["Inteligencia Artificial"])


@router.post("/triage", response_model=TriageResponse)
def evaluate_symptoms(
    request: TriageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario", "veterinario"]))
):
    """
    Evalúa preventivamente los síntomas reportados para una mascota utilizando IA.
    Retorna el nivel de urgencia sugerido, orientación preventiva y recomendaciones.
    """
    return AIService.evaluate_symptoms(db, current_user.id, request)


@router.get("/clinical-summary/{pet_id}", response_model=ClinicalSummaryResponse)
def get_clinical_summary(
    pet_id: int,
    db: Session = Depends(get_db),
    vet: User = Depends(require_roles(["veterinario", "administrador"]))
):
    """
    Genera un resumen clínico ejecutivo estructurado con IA para el médico veterinario
    antes de iniciar una consulta médica.
    """
    return AIService.get_clinical_summary(db, pet_id)
