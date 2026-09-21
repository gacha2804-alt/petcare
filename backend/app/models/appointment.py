from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Appointment(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    propietario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    veterinario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True, index=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id", ondelete="CASCADE"), nullable=False, index=True)
    fecha_hora = Column(DateTime, nullable=False, index=True)
    motivo = Column(Text, nullable=False)
    estado = Column(String(30), default="pendiente")  # pendiente, confirmada, cancelada, completada
    diagnostico_consulta = Column(Text, nullable=True)
    indicaciones_consulta = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Pet", back_populates="citas")
    propietario = relationship("User", back_populates="citas_como_propietario", foreign_keys=[propietario_id])
    veterinario = relationship("User", back_populates="citas_como_veterinario", foreign_keys=[veterinario_id])
    clinica = relationship("Clinic", back_populates="citas")


class AppointmentSlot(Base):
    __tablename__ = "horarios_atencion"

    id = Column(Integer, primary_key=True, index=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id", ondelete="CASCADE"), nullable=False, index=True)
    veterinario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True, index=True)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    tipo_atencion = Column(String(30), default="consulta")  # consulta | vacunacion | urgencia
    estado = Column(String(20), default="disponible")  # disponible | reservado | bloqueado | liberado
    cita_id = Column(Integer, ForeignKey("citas.id", ondelete="SET NULL"), nullable=True)
    notas = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    clinica = relationship("Clinic")
    veterinario = relationship("User", foreign_keys=[veterinario_id])
    cita = relationship("Appointment")
    lista_espera = relationship("WaitlistEntry", back_populates="slot", cascade="all, delete-orphan")


class WaitlistEntry(Base):
    __tablename__ = "lista_espera"

    id = Column(Integer, primary_key=True, index=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id", ondelete="CASCADE"), nullable=False)
    slot_id = Column(Integer, ForeignKey("horarios_atencion.id", ondelete="SET NULL"), nullable=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=True)
    motivo = Column(String(255), nullable=True)
    estado = Column(String(20), default="en_espera")  # en_espera | notificado | tomado | expirado | cancelado
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    fecha_notificacion = Column(DateTime, nullable=True)  # inicio de la ventana de 15 min (HU-07)
    fecha_expiracion = Column(DateTime, nullable=True)  # fecha_notificacion + 15 min

    slot = relationship("AppointmentSlot", back_populates="lista_espera")
    clinica = relationship("Clinic")
    usuario = relationship("User")
    mascota = relationship("Pet")
