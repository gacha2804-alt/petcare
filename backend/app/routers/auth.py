from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, PasswordResetRequest, PasswordResetConfirm
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.middlewares.auth_guard import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """Registra un nuevo usuario con rol Propietario y retorna su token de acceso."""
    return AuthService.register_owner(db, data)


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Autentica a un usuario por correo y contraseña, retornando el token JWT."""
    return AuthService.authenticate_user(db, credentials)


@router.post("/password-reset-request")
def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    """Solicita la recuperación de contraseña enviando un enlace/código al correo."""
    return AuthService.request_password_reset(db, data.email)


@router.post("/password-reset-confirm")
def confirm_password_reset(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Aplica la nueva contraseña utilizando el token de recuperación."""
    return AuthService.confirm_password_reset(db, data)


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Cierre de sesión. En esquemas JWT sin estado, el cliente (web o móvil)
    debe eliminar el token de su almacenamiento local (localStorage o SecureStore).
    """
    return {
        "success": True,
        "message": "Sesión finalizada exitosamente en el cliente."
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Obtiene los datos del usuario autenticado actualmente."""
    return UserService.get_user_by_id(db, current_user.id)
