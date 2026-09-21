from typing import List, Optional
from datetime import datetime, date, time, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.appointment import Appointment, AppointmentSlot, WaitlistEntry
from app.models.pet import Pet
from app.models.user import User
from app.models.clinic import Clinic
from app.models.notification import Notification
from app.schemas.appointment import (
    AppointmentCreate, AppointmentUpdateStatus, AppointmentResponse,
    SlotCreate, SlotResponse, WaitlistCreate, WaitlistResponse
)

VENTANA_ESPERA_MINUTOS = 15  # HU-07: tiempo para aceptar un cupo liberado


class AppointmentService:
    @staticmethod
    def _reservar_slot(db: Session, slot_id: int, appt: Appointment) -> None:
        slot = db.query(AppointmentSlot).filter(AppointmentSlot.id == slot_id).first()
        if not slot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario (slot) no encontrado.")
        if slot.estado != "disponible":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El horario seleccionado ya no está disponible.")
        if slot.fecha != appt.fecha_hora.date():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La fecha de la cita no coincide con la del horario.")
        slot.estado = "reservado"
        slot.cita_id = appt.id

    @staticmethod
    def _liberar_slot(db: Session, appt_id: int) -> Optional[AppointmentSlot]:
        """RF-09: libera el cupo vinculado a una cita y notifica al primero de la lista de espera."""
        slot = db.query(AppointmentSlot).filter(AppointmentSlot.cita_id == appt_id).first()
        if not slot:
            return None

        slot.estado = "disponible"
        slot.cita_id = None

        wait = db.query(WaitlistEntry).filter(
            WaitlistEntry.slot_id == slot.id,
            WaitlistEntry.estado == "en_espera"
        ).order_by(WaitlistEntry.fecha_solicitud.asc()).first()

        if wait:
            ahora = datetime.utcnow()
            wait.estado = "notificado"
            wait.fecha_notificacion = ahora
            wait.fecha_expiracion = ahora + timedelta(minutes=VENTANA_ESPERA_MINUTOS)
            notif = Notification(
                usuario_id=wait.usuario_id,
                tipo="cita",
                titulo="¡Se liberó un cupo! Tienes 15 minutos",
                mensaje=f"Un horario se ha liberado en tu lista de espera. Confírmalo dentro de los próximos {VENTANA_ESPERA_MINUTOS} minutos.",
                referencia_id=slot.id
            )
            db.add(notif)

        return slot

    @staticmethod
    def create_appointment(db: Session, owner_id: int, data: AppointmentCreate) -> AppointmentResponse:
        pet = db.query(Pet).filter(Pet.id == data.mascota_id, Pet.activa == True).first()
        if not pet or pet.propietario_id != owner_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no válida o no pertenece al usuario.")

        if data.slot_id:
            slot = db.query(AppointmentSlot).filter(AppointmentSlot.id == data.slot_id).first()
            if not slot:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario (slot) no encontrado.")
            if slot.estado != "disponible":
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El horario seleccionado ya no está disponible.")
            data.clinica_id = slot.clinica_id
            data.veterinario_id = slot.veterinario_id or data.veterinario_id
            data.fecha_hora = datetime.combine(slot.fecha, slot.hora_inicio)

        appt = Appointment(
            mascota_id=data.mascota_id,
            propietario_id=owner_id,
            clinica_id=data.clinica_id,
            veterinario_id=data.veterinario_id,
            fecha_hora=data.fecha_hora,
            motivo=data.motivo.strip(),
            estado="pendiente"
        )
        db.add(appt)
        db.flush()

        if data.slot_id:
            AppointmentService._reservar_slot(db, data.slot_id, appt)

        # Notificación interna de confirmación en proceso
        notif = Notification(
            usuario_id=owner_id,
            tipo="cita",
            titulo="Solicitud de Cita Enviada",
            mensaje=f"Tu solicitud de cita para {pet.nombre} ha sido recibida y está pendiente de confirmación.",
            referencia_id=appt.id
        )
        db.add(notif)

        db.commit()
        db.refresh(appt)
        return AppointmentResponse.model_validate(appt)

    @staticmethod
    def get_appointments_for_user(db: Session, current_user: User) -> List[AppointmentResponse]:
        role_name = current_user.rol.nombre if current_user.rol else "propietario"

        if role_name == "propietario":
            appts = db.query(Appointment).filter(Appointment.propietario_id == current_user.id).order_by(Appointment.fecha_hora.desc()).all()
        elif role_name == "veterinario":
            appts = db.query(Appointment).filter(
                (Appointment.veterinario_id == current_user.id) | (Appointment.veterinario_id == None)
            ).order_by(Appointment.fecha_hora.desc()).all()
        else:
            # Personal de clínica y Administrador
            appts = db.query(Appointment).order_by(Appointment.fecha_hora.desc()).all()

        return [AppointmentResponse.model_validate(a) for a in appts]

    @staticmethod
    def update_appointment_status(db: Session, appt_id: int, data: AppointmentUpdateStatus, current_user: User) -> AppointmentResponse:
        appt = db.query(Appointment).filter(Appointment.id == appt_id).first()
        if not appt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada.")

        appt.estado = data.estado
        if data.diagnostico_consulta:
            appt.diagnostico_consulta = data.diagnostico_consulta
        if data.indicaciones_consulta:
            appt.indicaciones_consulta = data.indicaciones_consulta

        # RF-09: al cancelar, liberar el cupo y notificar al primero de la lista de espera
        if data.estado == "cancelada":
            AppointmentService._liberar_slot(db, appt_id)

        # Notificar al propietario sobre el cambio de estado
        notif = Notification(
            usuario_id=appt.propietario_id,
            tipo="cita",
            titulo=f"Estado de Cita Actualizado: {data.estado.upper()}",
            mensaje=f"La cita para tu mascota ha cambiado a estado '{data.estado}'.",
            referencia_id=appt.id
        )
        db.add(notif)

        db.commit()
        db.refresh(appt)
        return AppointmentResponse.model_validate(appt)

    @staticmethod
    def create_slot(db: Session, data: SlotCreate) -> SlotResponse:
        clinic = db.query(Clinic).filter(Clinic.id == data.clinica_id, Clinic.activa == True).first()
        if not clinic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clínica no encontrada.")
        if data.veterinario_id:
            vet = db.query(User).filter(User.id == data.veterinario_id).first()
            if not vet:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinario no encontrado.")
        if data.hora_fin <= data.hora_inicio:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La hora de fin debe ser posterior a la de inicio.")

        slot = AppointmentSlot(
            clinica_id=data.clinica_id,
            veterinario_id=data.veterinario_id,
            fecha=data.fecha,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
            tipo_atencion=data.tipo_atencion,
            estado="disponible",
            notas=data.notas
        )
        db.add(slot)
        db.commit()
        db.refresh(slot)
        return SlotResponse.model_validate(slot)

    @staticmethod
    def list_slots(db: Session, clinica_id: int, fecha: date) -> List[SlotResponse]:
        slots = db.query(AppointmentSlot).filter(
            AppointmentSlot.clinica_id == clinica_id,
            AppointmentSlot.fecha == fecha
        ).order_by(AppointmentSlot.hora_inicio.asc()).all()
        return [SlotResponse.model_validate(s) for s in slots]

    @staticmethod
    def list_available_slots(db: Session, clinica_id: int, fecha: date) -> List[SlotResponse]:
        slots = db.query(AppointmentSlot).filter(
            AppointmentSlot.clinica_id == clinica_id,
            AppointmentSlot.fecha == fecha,
            AppointmentSlot.estado == "disponible"
        ).order_by(AppointmentSlot.hora_inicio.asc()).all()
        return [SlotResponse.model_validate(s) for s in slots]

    @staticmethod
    def join_waitlist(db: Session, owner_id: int, data: WaitlistCreate) -> WaitlistResponse:
        """RF-10 / HU-07: inscribe al propietario en la lista de espera de un horario o de la clínica."""
        if data.mascota_id:
            pet = db.query(Pet).filter(Pet.id == data.mascota_id, Pet.activa == True).first()
            if not pet or pet.propietario_id != owner_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no válida o no pertenece al usuario.")

        if data.slot_id:
            slot = db.query(AppointmentSlot).filter(AppointmentSlot.id == data.slot_id).first()
            if not slot:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario (slot) no encontrado.")
            if slot.estado == "disponible":
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El horario está disponible; agenda la cita directamente.")
            clinica_id = slot.clinica_id
        else:
            clinic = db.query(Clinic).filter(Clinic.id == data.clinica_id, Clinic.activa == True).first()
            if not clinic:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clínica no encontrada.")
            clinica_id = data.clinica_id

        duplicado = db.query(WaitlistEntry).filter(
            WaitlistEntry.usuario_id == owner_id,
            WaitlistEntry.slot_id == data.slot_id,
            WaitlistEntry.estado.in_(["en_espera", "notificado"])
        ).first()
        if duplicado:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya estás en la lista de espera de este horario.")

        entry = WaitlistEntry(
            clinica_id=clinica_id,
            slot_id=data.slot_id,
            usuario_id=owner_id,
            mascota_id=data.mascota_id,
            motivo=data.motivo,
            estado="en_espera"
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return WaitlistResponse.model_validate(entry)

    @staticmethod
    def list_waitlist(db: Session, current_user: User) -> List[WaitlistResponse]:
        role_name = current_user.rol.nombre if current_user.rol else "propietario"
        if role_name == "propietario":
            entries = db.query(WaitlistEntry).filter(WaitlistEntry.usuario_id == current_user.id).order_by(WaitlistEntry.fecha_solicitud.desc()).all()
        else:
            entries = db.query(WaitlistEntry).order_by(WaitlistEntry.fecha_solicitud.asc()).all()
        return [WaitlistResponse.model_validate(e) for e in entries]

    @staticmethod
    def take_waitlist_slot(db: Session, wait_id: int, current_user: User) -> AppointmentResponse:
        """HU-07: el primero de la lista acepta el cupo liberado dentro de la ventana de 15 min."""
        entry = db.query(WaitlistEntry).filter(WaitlistEntry.id == wait_id).first()
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de lista de espera no encontrado.")
        if entry.usuario_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el propietario puede tomar su cupo.")

        if entry.estado != "notificado":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro no está dentro de la ventana de notificación.")
        if not entry.fecha_expiracion or entry.fecha_expiracion < datetime.utcnow():
            entry.estado = "expirado"
            db.commit()
            raise HTTPException(status_code=status.HTTP_410_GONE, detail="La oferta de cupo ha expirado.")
        if not entry.mascota_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La inscripción no tiene una mascota asociada.")
        if not entry.slot_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La inscripción no tiene horario asociado.")

        slot = db.query(AppointmentSlot).filter(AppointmentSlot.id == entry.slot_id).first()
        if not slot or slot.estado != "disponible":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El horario ya no está disponible.")

        appt = Appointment(
            mascota_id=entry.mascota_id,
            propietario_id=entry.usuario_id,
            clinica_id=slot.clinica_id,
            veterinario_id=slot.veterinario_id,
            fecha_hora=datetime.combine(slot.fecha, slot.hora_inicio),
            motivo="Cupo tomado desde lista de espera",
            estado="confirmada"
        )
        db.add(appt)
        db.flush()

        slot.estado = "reservado"
        slot.cita_id = appt.id
        entry.estado = "tomado"

        notif = Notification(
            usuario_id=entry.usuario_id,
            tipo="cita",
            titulo="Cupo Confirmado",
            mensaje=f"Tu cita queda confirmada para el {slot.fecha} a las {slot.hora_inicio}.",
            referencia_id=appt.id
        )
        db.add(notif)

        db.commit()
        db.refresh(appt)
        return AppointmentResponse.model_validate(appt)

    @staticmethod
    def cancel_waitlist(db: Session, wait_id: int, current_user: User) -> None:
        entry = db.query(WaitlistEntry).filter(WaitlistEntry.id == wait_id).first()
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de lista de espera no encontrado.")
        if entry.usuario_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el propietario puede cancelar su inscripción.")
        entry.estado = "cancelado"
        db.commit()