from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class VaccineProtocol(Base):
    __tablename__ = "protocolos_refuerzo"

    id = Column(Integer, primary_key=True, index=True)
    nombre_producto = Column(String(150), nullable=False)
    fabricante = Column(String(150), nullable=True)
    tipo_aplicacion = Column(String(30), default="vacuna", nullable=False)  # vacuna | desparasitacion
    especie = Column(String(50), nullable=False)  # perro, gato...
    categoria_edad = Column(String(30), nullable=False)  # cachorro | adulto | senior
    edad_min_meses = Column(Integer, nullable=True)
    edad_max_meses = Column(Integer, nullable=True)
    intervalo_refuerzo_dias = Column(Integer, nullable=False)  # días hasta la próxima dosis (RF-03)
    esquema_refuerzos = Column(Text, nullable=True)  # JSON: dosis iniciales y refuerzos adicionales en días
    requiere_alerta_previa_dias = Column(Integer, default=7)  # ventana de alerta semanal (RF-04, HU-01)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    aplicaciones = relationship("Vaccine", back_populates="protocolo")


class Vaccine(Base):
    __tablename__ = "vacunas"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    veterinario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    nombre_vacuna = Column(String(100), nullable=False)  # producto
    tipo_aplicacion = Column(String(30), default="vacuna", nullable=False)  # vacuna | desparasitacion
    fabricante = Column(String(150), nullable=True)
    lote = Column(String(50), nullable=True)
    dosis = Column(String(100), nullable=True)
    via_aplicacion = Column(String(50), nullable=True)  # SC, IM, IV, oral...
    peso_kg = Column(Float, nullable=True)
    edad_aplicacion = Column(String(30), nullable=True)  # meses o categoría (cachorro/adulto/senior)
    protocolo_id = Column(Integer, ForeignKey("protocolos_refuerzo.id", ondelete="SET NULL"), nullable=True, index=True)
    fecha_aplicacion = Column(Date, nullable=False)
    fecha_proxima_dosis = Column(Date, nullable=True, index=True)  # calculada por el protocolo (RF-03)
    novedades = Column(Text, nullable=True)
    observaciones = Column(Text, nullable=True)
    origen_registro = Column(String(30), default="profesional_veterinario")  # profesional_veterinario o propietario_hogar
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Pet", back_populates="vacunas")
    veterinario = relationship("User")
    protocolo = relationship("VaccineProtocol", back_populates="aplicaciones")


class Medication(Base):
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    veterinario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    nombre = Column(String(150), nullable=False)
    dosis = Column(String(100), nullable=False)
    frecuencia_horas = Column(Integer, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    indicaciones = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    origen_registro = Column(String(30), default="profesional_veterinario")  # profesional_veterinario
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Pet", back_populates="medicamentos")
    veterinario = relationship("User")


class ClinicalConsultation(Base):
    __tablename__ = "consultas_medicas"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    veterinario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False, index=True)
    fecha_consulta = Column(DateTime, default=datetime.utcnow, nullable=False)
    motivo = Column(String(255), nullable=False)
    anamnesis = Column(Text, nullable=True)
    constantes_vitales = Column(Text, nullable=True)  # Temp: 38.5C, FC: 110 lpm, etc.
    diagnostico_profesional = Column(Text, nullable=False)
    plan_tratamiento = Column(Text, nullable=False)
    notas_adicionales = Column(Text, nullable=True)
    origen_registro = Column(String(30), default="profesional_veterinario")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Pet", back_populates="consultas_medicas")
    veterinario = relationship("User")


class WeightRecord(Base):
    __tablename__ = "registros_peso"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    peso_kg = Column(Float, nullable=False)
    fecha_registro = Column(Date, nullable=False)
    notas = Column(String(255), nullable=True)
    origen_registro = Column(String(30), default="propietario_hogar")

    mascota = relationship("Pet", back_populates="registros_peso")


class FeedingRecord(Base):
    __tablename__ = "registros_alimentacion"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo_alimento = Column(String(100), nullable=False)
    marca = Column(String(100), nullable=True)
    cantidad_gramos_dia = Column(Integer, nullable=True)
    frecuencia_veces_dia = Column(Integer, nullable=True)
    observaciones = Column(Text, nullable=True)
    fecha_registro = Column(Date, nullable=False)
    origen_registro = Column(String(30), default="propietario_hogar")

    mascota = relationship("Pet", back_populates="registros_alimentacion")


class SymptomObservation(Base):
    __tablename__ = "sintomas_observaciones"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    tipo = Column(String(30), nullable=False)  # sintoma, observacion_conductual, anomalia
    descripcion = Column(Text, nullable=False)
    severidad = Column(String(20), default="leve")  # leve, moderada, grave
    fecha_inicio = Column(DateTime, nullable=False)
    resuelto = Column(Boolean, default=False)
    origen_registro = Column(String(30), default="propietario_hogar")
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Pet", back_populates="sintomas_observaciones")
    usuario = relationship("User")


class HealthDocument(Base):
    __tablename__ = "documentos_salud"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo = Column(String(150), nullable=False)
    tipo_documento = Column(String(50), nullable=True)  # laboratorio, radiografia, receta
    archivo_url = Column(Text, nullable=False)
    fecha_documento = Column(Date, nullable=False)
    origen_registro = Column(String(30), default="profesional_veterinario")
    fecha_subida = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Pet", back_populates="documentos")
