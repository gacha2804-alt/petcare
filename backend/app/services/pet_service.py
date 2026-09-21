import uuid
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.pet import Pet
from app.models.health import WeightRecord
from app.models.user import User
from app.schemas.pet import PetCreate, PetUpdate, PetResponse, PetSummary


class PetService:
    @staticmethod
    def generate_unique_qr_token(db: Session, pet_name: str) -> str:
        """Genera un token alfanumérico único para el código QR."""
        prefix = "".join([c for c in pet_name.upper() if c.isalnum()][:4])
        suffix = uuid.uuid4().hex[:8].upper()
        token = f"QR-{prefix}-{suffix}"
        
        # Verificar unicidad
        while db.query(Pet).filter(Pet.codigo_qr_token == token).first():
            suffix = uuid.uuid4().hex[:8].upper()
            token = f"QR-{prefix}-{suffix}"
            
        return token

    @staticmethod
    def create_pet(db: Session, owner_id: int, data: PetCreate) -> PetResponse:
        qr_token = PetService.generate_unique_qr_token(db, data.nombre)
        
        pet = Pet(
            propietario_id=owner_id,
            nombre=data.nombre.strip(),
            especie=data.especie.strip(),
            raza=data.raza.strip() if data.raza else None,
            sexo=data.sexo,
            fecha_nacimiento=data.fecha_nacimiento,
            esterilizado=data.esterilizado,
            peso_actual=data.peso_actual,
            foto_url=data.foto_url,
            codigo_qr_token=qr_token,
            contacto_emergencia_tel=data.contacto_emergencia_tel,
            condiciones_criticas=data.condiciones_criticas,
            activa=True
        )
        db.add(pet)
        db.commit()
        db.refresh(pet)

        # Si se ingresó peso inicial, registrar en el historial de peso
        if data.peso_actual:
            weight_entry = WeightRecord(
                mascota_id=pet.id,
                peso_kg=data.peso_actual,
                fecha_registro=pet.fecha_creacion.date() if hasattr(pet.fecha_creacion, 'date') else data.fecha_nacimiento,
                notas="Peso inicial registrado en la creación de la mascota"
            )
            db.add(weight_entry)
            db.commit()

        return PetResponse.model_validate(pet)

    @staticmethod
    def get_pets_by_owner(db: Session, owner_id: int) -> List[PetSummary]:
        pets = db.query(Pet).filter(Pet.propietario_id == owner_id, Pet.activa == True).all()
        return [PetSummary.model_validate(p) for p in pets]

    @staticmethod
    def get_pet_detail(db: Session, pet_id: int, current_user: User) -> PetResponse:
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada o inactiva."
            )

        role_name = current_user.rol.nombre if current_user.rol else "propietario"
        
        # Verificación de permisos de acceso
        if role_name == "propietario" and pet.propietario_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene autorización para consultar los datos de esta mascota."
            )

        # Veterinarios, Personal de Clínica y Administradores tienen acceso de consulta clínica
        return PetResponse.model_validate(pet)

    @staticmethod
    def update_pet(db: Session, pet_id: int, owner_id: int, data: PetUpdate) -> PetResponse:
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.propietario_id == owner_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada o no pertenece al propietario."
            )

        update_data = data.model_dump(exclude_unset=True)
        peso_nuevo = update_data.get("peso_actual")
        
        for field, value in update_data.items():
            setattr(pet, field, value)

        # Si el peso cambió, agregar un nuevo registro al histórico
        if peso_nuevo is not None and peso_nuevo != pet.peso_actual:
            from datetime import date
            weight_entry = WeightRecord(
                mascota_id=pet.id,
                peso_kg=peso_nuevo,
                fecha_registro=date.today(),
                notas="Actualización de peso periódico"
            )
            db.add(weight_entry)

        db.commit()
        db.refresh(pet)
        return PetResponse.model_validate(pet)

    @staticmethod
    def delete_pet(db: Session, pet_id: int, owner_id: int) -> dict:
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.propietario_id == owner_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada o no pertenece al propietario."
            )

        # Baja lógica para preservar trazabilidad médica histórica
        pet.activa = False
        db.commit()
        return {
            "success": True,
            "message": f"La mascota '{pet.nombre}' ha sido dada de baja exitosamente."
        }

    @staticmethod
    def search_pets_for_staff(db: Session, query_str: Optional[str] = None) -> List[PetSummary]:
        """Permite a veterinarios y personal de clínica buscar mascotas por nombre o raza."""
        q = db.query(Pet).filter(Pet.activa == True)
        if query_str:
            search = f"%{query_str.lower()}%"
            q = q.filter((Pet.nombre.ilike(search)) | (Pet.codigo_qr_token.ilike(search)))
        
        pets = q.limit(50).all()
        return [PetSummary.model_validate(p) for p in pets]
