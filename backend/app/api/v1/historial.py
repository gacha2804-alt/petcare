from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.mascota import Mascota
from app.models.clinico import HistorialClinico, ConsultaVeterinaria, Vacuna, Desparasitacion, PermisoHistorialClinico
from app.schemas.clinico import (
    HistorialOut,
    ConsultaCreate,
    ConsultaOut,
    VacunaCreate,
    VacunaOut,
    DesparasitacionCreate,
    DesparasitacionOut
)
from app.core.deps import get_current_user, registrar_auditoria

router = APIRouter(prefix="/historial", tags=["Historial Clínico"])

@router.get("/{mascota_id}", response_model=HistorialOut)
def obtener_historial_mascota(
    mascota_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Consulta el historial clínico consolidado de una mascota (RF-02, RNF-01).
    Solo el propietario o un veterinario con autorización vigente puede acceder.
    """
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    user_roles = [ur.rol.nombre_rol for ur in current_user.roles]
    es_propietario = mascota.id_propietario == current_user.id
    es_admin = "administrador" in user_roles

    if not es_propietario and not es_admin:
        # Verificar si es veterinario con permiso activo (RF-03, RNF-01)
        permiso = db.query(PermisoHistorialClinico).filter(
            PermisoHistorialClinico.id_mascota == mascota_id,
            PermisoHistorialClinico.id_veterinario == current_user.id,
            PermisoHistorialClinico.activo == True
        ).first()

        if not permiso and "veterinario" not in user_roles and "personal_clinica" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso no autorizado al historial clínico de esta mascota."
            )

    historial = db.query(HistorialClinico).filter(HistorialClinico.id_mascota == mascota_id).first()
    if not historial:
        # Si no existía, crearlo
        historial = HistorialClinico(
            id_mascota=mascota.id,
            id_propietario=mascota.id_propietario,
            observaciones_generales=f"Historial inicial de {mascota.nombre}"
        )
        db.add(historial)
        db.commit()
        db.refresh(historial)

    consultas_db = db.query(ConsultaVeterinaria).filter(ConsultaVeterinaria.id_mascota == mascota_id).all()
    vacunas_db = db.query(Vacuna).filter(Vacuna.id_mascota == mascota_id).all()
    desp_db = db.query(Desparasitacion).filter(Desparasitacion.id_mascota == mascota_id).all()

    return HistorialOut(
        id=historial.id,
        id_mascota=historial.id_mascota,
        id_propietario=historial.id_propietario,
        fecha_creacion=historial.fecha_creacion,
        observaciones_generales=historial.observaciones_generales,
        consultas=[ConsultaOut.model_validate(c) for c in consultas_db],
        vacunas=[VacunaOut.model_validate(v) for v in vacunas_db],
        desparasitaciones=[DesparasitacionOut.model_validate(d) for d in desp_db]
    )

@router.post("/vacunas", response_model=VacunaOut, status_code=status.HTTP_201_CREATED)
def agregar_vacuna(
    mascota_id: int,
    data: VacunaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    vacuna = Vacuna(
        id_mascota=mascota_id,
        nombre_vacuna=data.nombre_vacuna,
        fecha_aplicacion=data.fecha_aplicacion,
        fecha_proxima_recomendada=data.fecha_proxima_recomendada,
        lote=data.lote,
        dosis=data.dosis
    )
    db.add(vacuna)
    db.commit()
    db.refresh(vacuna)
    return vacuna

@router.post("/desparasitaciones", response_model=DesparasitacionOut, status_code=status.HTTP_201_CREATED)
def agregar_desparasitacion(
    mascota_id: int,
    data: DesparasitacionCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mascota = db.query(Mascota).filter(Mascota.id == mascota_id).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    desp = Desparasitacion(
        id_mascota=mascota_id,
        tipo_tratamiento=data.tipo_tratamiento,
        producto=data.producto,
        fecha_tratamiento=data.fecha_tratamiento,
        fecha_proxima_recomendada=data.fecha_proxima_recomendada
    )
    db.add(desp)
    db.commit()
    db.refresh(desp)
    return desp
