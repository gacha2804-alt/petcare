from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.usuario import Usuario, Rol, UsuarioRol
from app.schemas.auth import LoginRequest, TokenResponse, UserRegister, UserOut
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.correo_electronico == login_data.correo_electronico).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas (correo o contraseña no válidos)."
        )
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario se encuentra inactivo."
        )

    roles = [ur.rol.nombre_rol for ur in user.roles]
    token = create_access_token(subject=user.id)

    user_out = UserOut(
        id=user.id,
        nombre=user.nombre,
        apellido=user.apellido,
        correo_electronico=user.correo_electronico,
        telefono=user.telefono,
        roles=roles,
        fecha_registro=user.fecha_registro
    )
    return TokenResponse(access_token=token, token_type="bearer", usuario=user_out)

@router.post("/register", response_model=TokenResponse)
def register(reg_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(Usuario).filter(Usuario.correo_electronico == reg_data.correo_electronico).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una cuenta registrada con este correo electrónico."
        )

    nuevo_usuario = Usuario(
        nombre=reg_data.nombre,
        apellido=reg_data.apellido,
        correo_electronico=reg_data.correo_electronico,
        telefono=reg_data.telefono,
        password_hash=get_password_hash(reg_data.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # Asignar rol por defecto
    rol_obj = db.query(Rol).filter(Rol.nombre_rol == reg_data.rol).first()
    if not rol_obj:
        rol_obj = db.query(Rol).filter(Rol.nombre_rol == "propietario").first()

    if rol_obj:
        user_rol = UsuarioRol(id_usuario=nuevo_usuario.id, id_rol=rol_obj.id)
        db.add(user_rol)
        db.commit()

    db.refresh(nuevo_usuario)
    roles = [ur.rol.nombre_rol for ur in nuevo_usuario.roles]
    token = create_access_token(subject=nuevo_usuario.id)

    user_out = UserOut(
        id=nuevo_usuario.id,
        nombre=nuevo_usuario.nombre,
        apellido=nuevo_usuario.apellido,
        correo_electronico=nuevo_usuario.correo_electronico,
        telefono=nuevo_usuario.telefono,
        roles=roles,
        fecha_registro=nuevo_usuario.fecha_registro
    )
    return TokenResponse(access_token=token, token_type="bearer", usuario=user_out)

@router.get("/me", response_model=UserOut)
def me(current_user: Usuario = Depends(get_current_user)):
    roles = [ur.rol.nombre_rol for ur in current_user.roles]
    return UserOut(
        id=current_user.id,
        nombre=current_user.nombre,
        apellido=current_user.apellido,
        correo_electronico=current_user.correo_electronico,
        telefono=current_user.telefono,
        roles=roles,
        fecha_registro=current_user.fecha_registro
    )
