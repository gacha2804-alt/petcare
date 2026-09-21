from datetime import date
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.appointment import (
    AppointmentCreate, AppointmentUpdateStatus, AppointmentResponse,
    SlotCreate, SlotResponse, WaitlistCreate, WaitlistResponse
)
from app.services.appointment_service import AppointmentService
from app.middlewares.auth_guard import get_current_user, require_roles
from app.models.user import User

router = APIRouter(prefix="/appointments", tags=["Citas Médicas"])


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario"]))
):
    """Solicita una cita médica presencial para la mascota (puede reservar un horario/slot)."""
    return AppointmentService.create_appointment(db, current_user.id, data)


@router.get("", response_model=List[AppointmentResponse])
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista las citas según el rol: del propietario, de la clínica o asignadas al veterinario."""
    return AppointmentService.get_appointments_for_user(db, current_user)


@router.put("/{appt_id}/status", response_model=AppointmentResponse)
def update_status(
    appt_id: int,
    data: AppointmentUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza el estado de la cita (confirmada, completada o cancelada). Al cancelar libera el cupo (RF-09)."""
    return AppointmentService.update_appointment_status(db, appt_id, data, current_user)


# Horarios / Slots disponibles (RF-08)
@router.post("/slots", response_model=SlotResponse, status_code=status.HTTP_201_CREATED)
def create_slot(
    data: SlotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["personal_clinica", "administrador"]))
):
    """Crea un horario de atención disponible en la clínica."""
    return AppointmentService.create_slot(db, data)


@router.get("/slots", response_model=List[SlotResponse])
def list_slots(
    clinica_id: int,
    fecha: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todos los horarios de una clínica para una fecha (tablero del día, RF-11)."""
    return AppointmentService.list_slots(db, clinica_id, fecha)


@router.get("/slots/available", response_model=List[SlotResponse])
def list_available_slots(
    clinica_id: int,
    fecha: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista horarios disponibles para reprogramar o agendar (HU-05)."""
    return AppointmentService.list_available_slots(db, clinica_id, fecha)


# Lista de Espera (RF-10 / HU-07)
@router.post("/waitlist", response_model=WaitlistResponse, status_code=status.HTTP_201_CREATED)
def join_waitlist(
    data: WaitlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario"]))
):
    """Inscribe al propietario en la lista de espera de un horario o de la clínica."""
    return AppointmentService.join_waitlist(db, current_user.id, data)


@router.get("/waitlist", response_model=List[WaitlistResponse])
def list_waitlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Muestra la lista de espera: propia (propietario) o completa (personal de clínica)."""
    return AppointmentService.list_waitlist(db, current_user)


@router.post("/waitlist/{wait_id}/take", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def take_waitlist_slot(
    wait_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario"]))
):
    """Acepta el cupo liberado dentro de la ventana de 15 minutos (HU-07)."""
    return AppointmentService.take_waitlist_slot(db, wait_id, current_user)


@router.delete("/waitlist/{wait_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_waitlist(
    wait_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["propietario"]))
):
    """Cancela la inscripción del propietario en la lista de espera."""
    AppointmentService.cancel_waitlist(db, wait_id, current_user)