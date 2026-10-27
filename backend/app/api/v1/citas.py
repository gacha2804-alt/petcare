from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.sede import Cita, Sede
from app.models.mascota import Mascota
from app.schemas.sede import CitaCreate, CitaOut
from app.services.agenda_service import agenda_service
from app.core.deps import get_current_user

router = APIRouter(prefix="/citas", tags=["Citas Veterinarias"])

@router.post("", response_model=CitaOut, status_code=status.HTTP_201_CREATED)
def crear_cita(
    data: CitaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea una cita presencial ejecutando una transacción atómica con bloqueo de filas (SELECT ... FOR UPDATE)
    para evitar reservas duplicadas en un mismo horario/slot.
    """
    cita = agenda_service.reservar_cita(
        db=db,
        id_propietario=current_user.id,
        id_mascota=data.id_mascota,
        id_sede=data.id_sede,
        id_disponibilidad=data.id_disponibilidad,
        motivo_consulta=data.motivo_consulta
    )

    sede = db.query(Sede).filter(Sede.id == cita.id_sede).first()
    mascota = db.query(Mascota).filter(Mascota.id == cita.id_mascota).first()

    return CitaOut(
        id=cita.id,
        id_mascota=cita.id_mascota,
        id_propietario=cita.id_propietario,
        id_sede=cita.id_sede,
        id_veterinario=cita.id_veterinario,
        id_agenda=cita.id_agenda,
        id_disponibilidad=cita.id_disponibilidad,
        fecha_cita=cita.fecha_cita,
        hora_cita=cita.hora_cita,
        motivo_consulta=cita.motivo_consulta,
        estado=cita.estado,
        fecha_solicitud=cita.fecha_solicitud,
        fecha_confirmacion=cita.fecha_confirmacion,
        sede_nombre=sede.nombre if sede else "Sede PetCare",
        mascota_nombre=mascota.nombre if mascota else "Mascota"
    )

@router.get("", response_model=List[CitaOut])
def listar_citas(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_roles = [ur.rol.nombre_rol for ur in current_user.roles]
    if "administrador" in user_roles or "veterinario" in user_roles or "personal_clinica" in user_roles:
        citas_db = db.query(Cita).order_by(Cita.fecha_cita.desc(), Cita.hora_cita.desc()).all()
    else:
        citas_db = db.query(Cita).filter(Cita.id_propietario == current_user.id).order_by(Cita.fecha_cita.desc(), Cita.hora_cita.desc()).all()

    resultado = []
    for c in citas_db:
        resultado.append(
            CitaOut(
                id=c.id,
                id_mascota=c.id_mascota,
                id_propietario=c.id_propietario,
                id_sede=c.id_sede,
                id_veterinario=c.id_veterinario,
                id_agenda=c.id_agenda,
                id_disponibilidad=c.id_disponibilidad,
                fecha_cita=c.fecha_cita,
                hora_cita=c.hora_cita,
                motivo_consulta=c.motivo_consulta,
                estado=c.estado,
                fecha_solicitud=c.fecha_solicitud,
                fecha_confirmacion=c.fecha_confirmacion,
                sede_nombre=c.sede.nombre if c.sede else "Sede PetCare",
                mascota_nombre=c.mascota.nombre if c.mascota else "Mascota"
            )
        )
    return resultado

@router.put("/{cita_id}/cancelar", response_model=CitaOut)
def cancelar_cita(
    cita_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cita = agenda_service.cancelar_cita(db=db, cita_id=cita_id, id_usuario=current_user.id)
    return CitaOut(
        id=cita.id,
        id_mascota=cita.id_mascota,
        id_propietario=cita.id_propietario,
        id_sede=cita.id_sede,
        id_veterinario=cita.id_veterinario,
        id_agenda=cita.id_agenda,
        id_disponibilidad=cita.id_disponibilidad,
        fecha_cita=cita.fecha_cita,
        hora_cita=cita.hora_cita,
        motivo_consulta=cita.motivo_consulta,
        estado=cita.estado,
        fecha_solicitud=cita.fecha_solicitud,
        fecha_confirmacion=cita.fecha_confirmacion,
        sede_nombre=cita.sede.nombre if cita.sede else "Sede PetCare",
        mascota_nombre=cita.mascota.nombre if cita.mascota else "Mascota"
    )
