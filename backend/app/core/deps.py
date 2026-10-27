from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.usuario import Usuario, Rol
from app.models.auditoria import Auditoria

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[Usuario]:
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user = db.query(Usuario).filter(Usuario.id == int(user_id), Usuario.activo == True).first()
    return user

def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    if not token:
        # Fallback to test user if in dev and no token provided, or raise 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionaron credenciales de autenticación",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    user = db.query(Usuario).filter(Usuario.id == int(user_id), Usuario.activo == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado o inactivo"
        )
    return user

def require_roles(allowed_roles: List[str]):
    def role_checker(current_user: Usuario = Depends(get_current_user)):
        user_roles = [ur.rol.nombre_rol for ur in current_user.roles]
        if "administrador" in user_roles:
            return current_user
        if not any(role in user_roles for role in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Requiere uno de los roles: {allowed_roles}"
            )
        return current_user
    return role_checker

def registrar_auditoria(
    db: Session,
    usuario_id: Optional[int],
    tipo_operacion: str,
    entidad_afectada: str,
    id_registro_afectado: Optional[int] = None,
    detalles: Optional[str] = None
):
    try:
        log = Auditoria(
            id_usuario=usuario_id,
            tipo_operacion=tipo_operacion,
            entidad_afectada=entidad_afectada,
            id_registro_afectado=id_registro_afectado,
            detalles=detalles
        )
        db.add(log)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[AUDITORIA ERROR] {e}")
