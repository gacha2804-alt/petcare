from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from app.db.session import Base

class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True, index=True)
    tipo_operacion = Column(String(100), nullable=False) # CREAR_CITA, CANCELAR_CITA, CONSULTA_HISTORIAL, etc.
    entidad_afectada = Column(String(100), nullable=False) # citas, permisos_historial, chat
    id_registro_afectado = Column(Integer, nullable=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    detalles = Column(Text, nullable=True)
