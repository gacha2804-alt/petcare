from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import get_password_hash


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> UserResponse:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
        
        return UserResponse(
            id=user.id,
            rol_id=user.rol_id,
            rol_nombre=user.rol.nombre if user.rol else None,
            nombre_completo=user.nombre_completo,
            email=user.email,
            telefono=user.telefono,
            activo=user.activo,
            fecha_creacion=user.fecha_creacion
        )

    @staticmethod
    def update_profile(db: Session, user_id: int, data: UserUpdate) -> UserResponse:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
        
        if data.nombre_completo is not None:
            user.nombre_completo = data.nombre_completo.strip()
        if data.telefono is not None:
            user.telefono = data.telefono.strip()
        
        db.commit()
        db.refresh(user)
        return UserService.get_user_by_id(db, user_id)

    @staticmethod
    def list_users(db: Session, role_filter: Optional[str] = None) -> List[UserResponse]:
        query = db.query(User)
        if role_filter:
            query = query.join(Role).filter(Role.nombre == role_filter)
        
        users = query.all()
        return [
            UserResponse(
                id=u.id,
                rol_id=u.rol_id,
                rol_nombre=u.rol.nombre if u.rol else None,
                nombre_completo=u.nombre_completo,
                email=u.email,
                telefono=u.telefono,
                activo=u.activo,
                fecha_creacion=u.fecha_creacion
            )
            for u in users
        ]

    @staticmethod
    def create_staff_user(db: Session, nombre_completo: str, email: str, password: str, rol_nombre: str, telefono: Optional[str] = None) -> UserResponse:
        """Permite al administrador dar de alta veterinarios o personal de clínica."""
        existing = db.query(User).filter(User.email == email.lower()).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado.")
        
        role = db.query(Role).filter(Role.nombre == rol_nombre).first()
        if not role:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El rol '{rol_nombre}' no existe.")

        new_user = User(
            rol_id=role.id,
            nombre_completo=nombre_completo.strip(),
            email=email.lower().strip(),
            password_hash=get_password_hash(password),
            telefono=telefono,
            activo=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserService.get_user_by_id(db, new_user.id)
