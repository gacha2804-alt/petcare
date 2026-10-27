from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    id_propietario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False) # Perro, Gato, Ave, etc.
    sexo = Column(String(20), nullable=False) # Macho, Hembra
    fecha_nacimiento = Column(Date, nullable=False)
    datos_identificatorios = Column(Text, nullable=True) # Raza, color, microchip
    imagen_url = Column(String(500), nullable=True) # Cloudinary secure_url
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    propietario = relationship("Usuario", back_populates="mascotas")
    historial = relationship("HistorialClinico", back_populates="mascota", uselist=False, cascade="all, delete-orphan")
    citas = relationship("Cita", back_populates="mascota", cascade="all, delete-orphan")
    vacunas = relationship("Vacuna", back_populates="mascota", cascade="all, delete-orphan")
    desparasitaciones = relationship("Desparasitacion", back_populates="mascota", cascade="all, delete-orphan")
    conversaciones = relationship("ChatConversacion", back_populates="mascota", cascade="all, delete-orphan")
