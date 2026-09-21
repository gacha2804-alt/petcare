from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.pet import PetCreate, PetUpdate, PetResponse, PetSummary
from app.services.pet_service import PetService
from app.middlewares.auth_guard import get_current_user, require_roles
from app.models.user import User

router = APIRouter(prefix="/pets", tags=["Mascotas"])


@router.post("", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(
    data: PetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario"]))
):
    """Registra una nueva mascota vinculada al propietario autenticado."""
    return PetService.create_pet(db, current_user.id, data)


@router.get("", response_model=List[PetSummary])
def get_my_pets(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario"]))
):
    """Lista todas las mascotas activas pertenecientes al propietario autenticado."""
    return PetService.get_pets_by_owner(db, current_user.id)


@router.get("/search/directory", response_model=List[PetSummary])
def search_pets(
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    staff: User = Depends(require_roles(["veterinario", "personal_clinica", "administrador"]))
):
    """Búsqueda de mascotas por nombre o código QR para personal médico y clínico."""
    return PetService.search_pets_for_staff(db, q)


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Consulta la ficha completa de una mascota. Requiere ser el dueño o personal autorizado."""
    return PetService.get_pet_detail(db, pet_id, current_user)


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(
    pet_id: int,
    data: PetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario"]))
):
    """Actualiza los datos biográficos, peso o características de la mascota del propietario."""
    return PetService.update_pet(db, pet_id, current_user.id, data)


@router.delete("/{pet_id}")
def delete_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario"]))
):
    """Da de baja lógica a una mascota del propietario."""
    return PetService.delete_pet(db, pet_id, current_user.id)
