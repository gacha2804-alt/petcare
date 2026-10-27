from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Sede(Base):
    __tablename__ = "sedes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False) # "Sede 1 - Norte", "Sede 2 - Sur"
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(30), nullable=True)
    activa = Column(Boolean, default=True)
    es_una_de_dos_sedes = Column(Boolean, default=True)

    agendas = relationship("Agenda", back_populates="sede", cascade="all, delete-orphan")
    citas = relationship("Cita", back_populates="sede")

class Agenda(Base):
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, index=True)
    id_sede = Column(Integer, ForeignKey("sedes.id", ondelete="CASCADE"), nullable=False, index=True)
    id_veterinario = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha = Column(Date, nullable=False, index=True)
    activa = Column(Boolean, default=True)

    sede = relationship("Sede", back_populates="agendas")
    slots = relationship("Disponibilidad", back_populates="agenda", cascade="all, delete-orphan")

class Disponibilidad(Base):
    __tablename__ = "disponibilidad"

    id = Column(Integer, primary_key=True, index=True)
    id_agenda = Column(Integer, ForeignKey("agenda.id", ondelete="CASCADE"), nullable=False, index=True)
    fecha = Column(Date, nullable=False, index=True)
    hora_inicio = Column(String(10), nullable=False) # "09:00"
    hora_fin = Column(String(10), nullable=False)    # "09:30"
    disponible = Column(Boolean, default=True)
    ocupado = Column(Boolean, default=False)

    agenda = relationship("Agenda", back_populates="slots")
    cita = relationship("Cita", back_populates="disponibilidad", uselist=False)

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    id_propietario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    id_sede = Column(Integer, ForeignKey("sedes.id"), nullable=False, index=True)
    id_veterinario = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    id_agenda = Column(Integer, ForeignKey("agenda.id"), nullable=False)
    id_disponibilidad = Column(Integer, ForeignKey("disponibilidad.id"), nullable=False, unique=True)
    fecha_cita = Column(Date, nullable=False)
    hora_cita = Column(String(10), nullable=False)
    motivo_consulta = Column(Text, nullable=False)
    estado = Column(String(50), default="confirmada") # solicitada, confirmada, cancelada, atendida
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    fecha_confirmacion = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Mascota", back_populates="citas")
    propietario = relationship("Usuario", back_populates="citas", foreign_keys=[id_propietario])
    sede = relationship("Sede", back_populates="citas")
    disponibilidad = relationship("Disponibilidad", back_populates="cita")
