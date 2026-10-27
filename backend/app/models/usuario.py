from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, nullable=False, index=True)

    usuarios = relationship("UsuarioRol", back_populates="rol")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo_electronico = Column(String(150), unique=True, nullable=False, index=True)
    telefono = Column(String(30), nullable=True)
    password_hash = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

    roles = relationship("UsuarioRol", back_populates="usuario", cascade="all, delete-orphan")
    mascotas = relationship("Mascota", back_populates="propietario", cascade="all, delete-orphan")
    citas = relationship("Cita", back_populates="propietario", foreign_keys="[Cita.id_propietario]")
    conversaciones = relationship("ChatConversacion", back_populates="usuario")

class UsuarioRol(Base):
    __tablename__ = "usuario_roles"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    fecha_asignacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="roles")
    rol = relationship("Rol", back_populates="usuarios")
