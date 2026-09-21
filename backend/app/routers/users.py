from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.middlewares.auth_guard import get_current_user, require_roles
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("", response_model=List[UserResponse])
def list_users(
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_roles(["administrador"]))
):
    """Lista todos los usuarios del sistema. Exclusivo para administradores."""
    return UserService.list_users(db, role_filter=role)


@router.put("/me", response_model=UserResponse)
def update_own_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Permite al usuario autenticado actualizar sus datos personales."""
    return UserService.update_profile(db, current_user.id, data)
