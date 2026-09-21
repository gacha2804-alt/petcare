from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Clinic(Base):
    __tablename__ = "clinicas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(String(255), nullable=False)
    telefono = Column(String(50), nullable=False)
    email = Column(String(150), nullable=True)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    horario_atencion = Column(String(100), nullable=True)
    tiene_urgencias_24h = Column(Boolean, default=False)
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    personal = relationship("ClinicStaff", back_populates="clinica", cascade="all, delete-orphan")
    citas = relationship("Appointment", back_populates="clinica")


class ClinicStaff(Base):
    __tablename__ = "personal_clinica"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    clinica_id = Column(Integer, ForeignKey("clinicas.id", ondelete="CASCADE"), nullable=False)
    tarjeta_profesional = Column(String(100), nullable=True)
    especialidad = Column(String(100), nullable=True)

    usuario = relationship("User", back_populates="personal_clinica")
    clinica = relationship("Clinic", back_populates="personal")
