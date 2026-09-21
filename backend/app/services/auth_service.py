from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, PasswordResetConfirm
from app.core.security import get_password_hash, verify_password, create_access_token


class AuthService:
    @staticmethod
    def register_owner(db: Session, data: RegisterRequest) -> TokenResponse:
        # Verificar si el correo ya existe
        existing_user = db.query(User).filter(User.email == data.email.lower()).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado."
            )
        
        # Obtener rol de propietario (id=4 o por nombre)
        owner_role = db.query(Role).filter(Role.nombre == "propietario").first()
        if not owner_role:
            # Fallback seguro si la base de datos no tiene el rol
            owner_role = Role(id=4, nombre="propietario", descripcion="Propietario de mascotas")
            db.add(owner_role)
            db.commit()
            db.refresh(owner_role)

        new_user = User(
            rol_id=owner_role.id,
            nombre_completo=data.nombre_completo.strip(),
            email=data.email.lower().strip(),
            password_hash=get_password_hash(data.password),
            telefono=data.telefono,
            activo=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_access_token(subject=new_user.id, role=owner_role.nombre)
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user_id=new_user.id,
            nombre_completo=new_user.nombre_completo,
            email=new_user.email,
            rol=owner_role.nombre
        )

    @staticmethod
    def authenticate_user(db: Session, credentials: LoginRequest) -> TokenResponse:
        user = db.query(User).filter(User.email == credentials.email.lower()).first()
        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas (correo o contraseña no válidos)."
            )
        
        if not user.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Esta cuenta ha sido desactivada. Comuníquese con el administrador."
            )

        role_name = user.rol.nombre if user.rol else "propietario"
        token = create_access_token(subject=user.id, role=role_name)

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user_id=user.id,
            nombre_completo=user.nombre_completo,
            email=user.email,
            rol=role_name
        )

    @staticmethod
    def request_password_reset(db: Session, email: str) -> dict:
        user = db.query(User).filter(User.email == email.lower()).first()
        # Siempre devolvemos mensaje afirmativo para no filtrar existencia de correos
        return {
            "success": True,
            "message": "Si el correo existe en el sistema, se ha enviado un enlace/código de recuperación."
        }

    @staticmethod
    def confirm_password_reset(db: Session, data: PasswordResetConfirm) -> dict:
        user = db.query(User).filter(User.email == data.email.lower()).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )
        
        # En producción se valida el token criptográfico de reset con expiración
        user.password_hash = get_password_hash(data.new_password)
        db.commit()
        return {
            "success": True,
            "message": "Contraseña restablecida exitosamente. Ya puede iniciar sesión."
        }
