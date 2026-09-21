from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.pet import Pet
from app.models.user import User
from app.schemas.emergency import EmergencyProfileResponse


class EmergencyService:
    @staticmethod
    def get_public_emergency_profile(db: Session, qr_token: str) -> EmergencyProfileResponse:
        pet = db.query(Pet).filter(Pet.codigo_qr_token == qr_token.strip(), Pet.activa == True).first()
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Código QR no válido o mascota no registrada en el sistema PetCare."
            )

        owner = db.query(User).filter(User.id == pet.propietario_id).first()
        owner_name = owner.nombre_completo if owner else "Propietario no disponible"
        emergency_phone = pet.contacto_emergencia_tel or (owner.telefono if owner else "No especificado")

        return EmergencyProfileResponse(
            id=pet.id,
            nombre=pet.nombre,
            especie=pet.especie,
            raza=pet.raza,
            sexo=pet.sexo,
            foto_url=pet.foto_url,
            contacto_emergencia_tel=emergency_phone,
            condiciones_criticas=pet.condiciones_criticas or "Sin condiciones críticas ni alergias registradas.",
            nombre_propietario=owner_name,
            mensaje_alerta="¡Hola! Si encontraste a esta mascota perdida o en emergencia, comunícate de inmediato al teléfono de contacto."
        )
