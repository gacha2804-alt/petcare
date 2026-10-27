from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from fastapi import HTTPException, status
from datetime import date, datetime
from typing import List, Optional
from app.models.sede import Sede, Agenda, Disponibilidad, Cita
from app.models.mascota import Mascota
from app.core.deps import registrar_auditoria

class AgendaService:
    @staticmethod
    def obtener_sedes(db: Session) -> List[Sede]:
        return db.query(Sede).filter(Sede.activa == True).all()

    @staticmethod
    def consultar_disponibilidad(db: Session, sede_id: int, fecha: date) -> List[Disponibilidad]:
        """
        Retorna los slots libres de una sede para una fecha específica desde la BD real.
        """
        agenda = db.query(Agenda).filter(
            Agenda.id_sede == sede_id,
            Agenda.fecha == fecha,
            Agenda.activa == True
        ).first()

        if not agenda:
            return []

        slots = db.query(Disponibilidad).filter(
            Disponibilidad.id_agenda == agenda.id,
            Disponibilidad.disponible == True,
            Disponibilidad.ocupado == False
        ).order_by(Disponibilidad.hora_inicio).all()

        return slots

    @staticmethod
    def reservar_cita(
        db: Session,
        id_propietario: int,
        id_mascota: int,
        id_sede: int,
        id_disponibilidad: int,
        motivo_consulta: str
    ) -> Cita:
        """
        Lógica de Reserva Atómica con bloqueo de fila (SELECT ... FOR UPDATE).
        Garantiza que dos usuarios no puedan apartar el mismo slot simultáneamente.
        """
        # Verificar que la mascota pertenezca al propietario
        mascota = db.query(Mascota).filter(
            Mascota.id == id_mascota,
            Mascota.id_propietario == id_propietario
        ).first()
        if not mascota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada o no pertenece al usuario autenticado."
            )

        # Transacción con bloqueo de fila
        try:
            query = select(Disponibilidad).where(Disponibilidad.id == id_disponibilidad)
            if db.bind and db.bind.dialect.name == "postgresql":
                # Bloqueo estricto a nivel de fila en PostgreSQL
                query = query.with_for_update()

            slot = db.execute(query).scalar_one_or_none()

            if not slot:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El horario de disponibilidad solicitado no existe."
                )

            if slot.ocupado or not slot.disponible:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El horario seleccionado ya no se encuentra disponible (ocupado por otra cita)."
                )

            agenda = db.query(Agenda).filter(Agenda.id == slot.id_agenda).first()
            if not agenda or agenda.id_sede != id_sede:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La disponibilidad seleccionada no coincide con la sede indicada."
                )

            # Marcar slot como ocupado
            slot.ocupado = True
            slot.disponible = False

            # Crear cita
            nueva_cita = Cita(
                id_mascota=id_mascota,
                id_propietario=id_propietario,
                id_sede=id_sede,
                id_veterinario=agenda.id_veterinario,
                id_agenda=agenda.id,
                id_disponibilidad=slot.id,
                fecha_cita=slot.fecha,
                hora_cita=slot.hora_inicio,
                motivo_consulta=motivo_consulta,
                estado="confirmada",
                fecha_solicitud=datetime.utcnow(),
                fecha_confirmacion=datetime.utcnow()
            )

            db.add(nueva_cita)
            db.commit()
            db.refresh(nueva_cita)

            # Registrar trazabilidad de auditoría
            registrar_auditoria(
                db=db,
                usuario_id=id_propietario,
                tipo_operacion="CREAR_CITA",
                entidad_afectada="citas",
                id_registro_afectado=nueva_cita.id,
                detalles=f"Cita reservada para mascota {mascota.nombre} en Sede {id_sede} el {slot.fecha} a las {slot.hora_inicio}"
            )

            return nueva_cita

        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en la transacción de agendamiento: {str(e)}"
            )

    @staticmethod
    def cancelar_cita(db: Session, cita_id: int, id_usuario: int) -> Cita:
        cita = db.query(Cita).filter(Cita.id == cita_id).first()
        if not cita:
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        if cita.id_propietario != id_usuario:
            raise HTTPException(status_code=403, detail="No autorizado para cancelar esta cita")

        cita.estado = "cancelada"
        if cita.disponibilidad:
            cita.disponibilidad.ocupado = False
            cita.disponibilidad.disponible = True

        db.commit()
        db.refresh(cita)

        registrar_auditoria(
            db=db,
            usuario_id=id_usuario,
            tipo_operacion="CANCELAR_CITA",
            entidad_afectada="citas",
            id_registro_afectado=cita.id,
            detalles=f"Cita #{cita.id} cancelada por usuario"
        )
        return cita

agenda_service = AgendaService()
