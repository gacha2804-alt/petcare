from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class HistorialClinico(Base):
    __tablename__ = "historial_clinico"

    id = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    id_propietario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    observaciones_generales = Column(Text, nullable=True)

    mascota = relationship("Mascota", back_populates="historial")
    consultas = relationship("ConsultaVeterinaria", back_populates="historial", cascade="all, delete-orphan")

class ConsultaVeterinaria(Base):
    __tablename__ = "consultas_veterinarias"

    id = Column(Integer, primary_key=True, index=True)
    id_historial = Column(Integer, ForeignKey("historial_clinico.id", ondelete="CASCADE"), nullable=False, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    id_veterinario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    id_sede = Column(Integer, ForeignKey("sedes.id"), nullable=True)
    fecha_consulta = Column(DateTime, default=datetime.utcnow)
    motivo_consulta = Column(Text, nullable=False)
    diagnostico_registrado = Column(Text, nullable=False)
    observaciones = Column(Text, nullable=True)

    historial = relationship("HistorialClinico", back_populates="consultas")

class Vacuna(Base):
    __tablename__ = "vacunas"

    id = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    nombre_vacuna = Column(String(100), nullable=False)
    fecha_aplicacion = Column(Date, nullable=False)
    fecha_proxima_recomendada = Column(Date, nullable=True)
    lote = Column(String(50), nullable=True)
    dosis = Column(String(50), nullable=True)

    mascota = relationship("Mascota", back_populates="vacunas")

class Desparasitacion(Base):
    __tablename__ = "desparasitaciones"

    id = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo_tratamiento = Column(String(50), nullable=False) # Interna / Externa
    producto = Column(String(100), nullable=False)
    fecha_tratamiento = Column(Date, nullable=False)
    fecha_proxima_recomendada = Column(Date, nullable=True)

    mascota = relationship("Mascota", back_populates="desparasitaciones")

class PermisoHistorialClinico(Base):
    __tablename__ = "permisos_historial_clinico"

    id = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    id_veterinario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    fecha_autorizacion = Column(DateTime, default=datetime.utcnow)
    fecha_revocacion = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True)
