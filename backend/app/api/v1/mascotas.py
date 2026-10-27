from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.mascota import Mascota
from app.models.clinico import HistorialClinico
from app.schemas.mascota import MascotaCreate, MascotaUpdate, MascotaOut
from app.core.deps import get_current_user, registrar_auditoria

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])

@router.get("", response_model=List[MascotaOut])
def listar_mascotas(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista todas las mascotas pertenecientes al propietario autenticado."""
    user_roles = [ur.rol.nombre_rol for ur in current_user.roles]
    if "administrador" in user_roles or "veterinario" in user_roles or "personal_clinica" in user_roles:
        # Personal clínico puede ver todas las mascotas si es necesario
        return db.query(Mascota).all()
    return db.query(Mascota).filter(Mascota.id_propietario == current_user.id).all()

@router.post("", response_model=MascotaOut, status_code=status.HTTP_201_CREATED)
def registrar_mascota(
    data: MascotaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Registra una nueva mascota vinculada al propietario autenticado y crea su historial clínico inicial."""
    nueva_mascota = Mascota(
        id_propietario=current_user.id,
        nombre=data.nombre,
        especie=data.especie,
        sexo=data.sexo,
        fecha_nacimiento=data.fecha_nacimiento,
        datos_identificatorios=data.datos_identificatorios,
        imagen_url=data.imagen_url
    )
    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)

    # Crear historial clínico vacío inicial (RF-01, RF-02)
    historial = HistorialClinico(
        id_mascota=nueva_mascota.id,
        id_propietario=current_user.id,
        observaciones_generales=f"Historial abierto para {nueva_mascota.nombre}"
    )
    db.add(historial)
    db.commit()

    registrar_auditoria(
        db=db,
        usuario_id=current_user.id,
        tipo_operacion="REGISTRAR_MASCOTA",
        entidad_afectada="mascotas",
        id_registro_afectado=nueva_mascota.id,
        detalles=f"Mascota registrada: {nueva_mascota.nombre} ({nueva_mascota.especie})"
    )

    return nueva_mascota

@router.get("/{mascota_id}", response_model=MascotaOut)
def obtener_mascota(
    mascota_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    
    user_roles = [ur.rol.nombre_rol for ur in current_user.roles]
    if mascota.id_propietario != current_user.id and "administrador" not in user_roles and "veterinario" not in user_roles and "personal_clinica" not in user_roles:
        raise HTTPException(status_code=403, detail="No tiene permisos para consultar esta mascota")
    
    return mascota

@router.put("/{mascota_id}", response_model=MascotaOut)
def actualizar_mascota(
    mascota_id: int,
    data: MascotaUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    if mascota.id_propietario != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para editar esta mascota")

    update_dict = data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(mascota, field, value)

    db.commit()
    db.refresh(mascota)
    return mascota
