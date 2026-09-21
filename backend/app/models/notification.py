from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Notification(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo = Column(String(50), nullable=False)  # cita, vacuna, medicamento, alerta_ia
    titulo = Column(String(150), nullable=False)
    mensaje = Column(Text, nullable=False)
    leida = Column(Boolean, default=False)
    referencia_id = Column(Integer, nullable=True)  # ID de la cita o mascota
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("User", back_populates="notificaciones")
