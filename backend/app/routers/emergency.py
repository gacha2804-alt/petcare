from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.emergency import EmergencyProfileResponse
from app.services.emergency_service import EmergencyService

router = APIRouter(prefix="/emergency", tags=["Emergencias y QR"])


@router.get("/{qr_token}", response_model=EmergencyProfileResponse)
def get_emergency_profile(qr_token: str, db: Session = Depends(get_db)):
    """
    ENDPOINT PÚBLICO: Permite acceder al perfil de emergencia de una mascota
    escaneando su código QR sin requerir inicio de sesión.
    Retorna exclusivamente los datos indispensables para auxilio o rescate.
    """
    return EmergencyService.get_public_emergency_profile(db, qr_token)
