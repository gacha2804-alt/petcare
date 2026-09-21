from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class AIConsultation(Base):
    __tablename__ = "consultas_ia"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    prompt_usuario = Column(Text, nullable=False)
    contexto_clinico_snapshot = Column(Text, nullable=True)
    respuesta_ia = Column(Text, nullable=False)
    nivel_urgencia_sugerido = Column(String(20), nullable=True)  # bajo, moderado, alto
    recomendaciones = Column(Text, nullable=True)
    disclaimer_aceptado = Column(Boolean, default=True)
    fecha_consulta = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Pet", back_populates="consultas_ia")
    usuario = relationship("User")


class AIAlert(Base):
    __tablename__ = "alertas_evolucion_ia"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo_alerta = Column(String(50), nullable=False)  # perdida_peso, sintomas_recurrentes, vacuna_vencida
    mensaje = Column(Text, nullable=False)
    nivel_riesgo = Column(String(20), nullable=False)  # informativa, atencion, critica
    revisada = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    mascota = relationship("Pet", back_populates="alertas_ia")
