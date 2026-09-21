from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Pet(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    propietario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)  # Canino, Felino, etc.
    raza = Column(String(100), nullable=True)
    sexo = Column(String(10), nullable=False)  # macho, hembra
    fecha_nacimiento = Column(Date, nullable=True)
    esterilizado = Column(Boolean, default=False)
    peso_actual = Column(Float, nullable=True)
    foto_url = Column(Text, nullable=True)
    codigo_qr_token = Column(String(100), unique=True, nullable=False, index=True)
    contacto_emergencia_tel = Column(String(30), nullable=True)
    condiciones_criticas = Column(Text, nullable=True)  # Alergias o enfermedades preexistentes
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    propietario = relationship("User", back_populates="mascotas")
    vacunas = relationship("Vaccine", back_populates="mascota", cascade="all, delete-orphan")
    medicamentos = relationship("Medication", back_populates="mascota", cascade="all, delete-orphan")
    consultas_medicas = relationship("ClinicalConsultation", back_populates="mascota", cascade="all, delete-orphan")
    registros_peso = relationship("WeightRecord", back_populates="mascota", cascade="all, delete-orphan")
    registros_alimentacion = relationship("FeedingRecord", back_populates="mascota", cascade="all, delete-orphan")
    sintomas_observaciones = relationship("SymptomObservation", back_populates="mascota", cascade="all, delete-orphan")
    documentos = relationship("HealthDocument", back_populates="mascota", cascade="all, delete-orphan")
    citas = relationship("Appointment", back_populates="mascota", cascade="all, delete-orphan")
    consultas_ia = relationship("AIConsultation", back_populates="mascota", cascade="all, delete-orphan")
    alertas_ia = relationship("AIAlert", back_populates="mascota", cascade="all, delete-orphan")
