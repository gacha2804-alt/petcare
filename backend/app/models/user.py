from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuarios = relationship("User", back_populates="rol")


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    nombre_completo = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    telefono = Column(String(30), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    rol = relationship("Role", back_populates="usuarios")
    mascotas = relationship("Pet", back_populates="propietario", cascade="all, delete-orphan")
    citas_como_propietario = relationship("Appointment", back_populates="propietario", foreign_keys="Appointment.propietario_id")
    citas_como_veterinario = relationship("Appointment", back_populates="veterinario", foreign_keys="Appointment.veterinario_id")
    notificaciones = relationship("Notification", back_populates="usuario", cascade="all, delete-orphan")
    personal_clinica = relationship("ClinicStaff", back_populates="usuario", uselist=False)
