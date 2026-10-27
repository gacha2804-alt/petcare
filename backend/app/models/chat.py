from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class ChatConversacion(Base):
    __tablename__ = "chat_conversaciones"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id", ondelete="CASCADE"), nullable=False, index=True)
    id_cita = Column(Integer, ForeignKey("citas.id", ondelete="SET NULL"), nullable=True)
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_ultima_actividad = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = Column(String(50), default="activa") # activa, cerrada
    urgencia_detectada = Column(Boolean, default=False)
    clasificacion_urgencia = Column(String(50), nullable=True) # normal, moderada, emergencia
    derivacion_requerida = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="conversaciones")
    mascota = relationship("Mascota", back_populates="conversaciones")
    mensajes = relationship("ChatMensaje", back_populates="conversacion", cascade="all, delete-orphan", order_by="ChatMensaje.fecha_envio")

class ChatMensaje(Base):
    __tablename__ = "chat_mensajes"

    id = Column(Integer, primary_key=True, index=True)
    id_conversacion = Column(Integer, ForeignKey("chat_conversaciones.id", ondelete="CASCADE"), nullable=False, index=True)
    remitente = Column(String(30), nullable=False) # "usuario", "asistente", "sistema"
    contenido = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, default=datetime.utcnow)
    contiene_informacion_clinica = Column(Boolean, default=False)
    es_orientacion_inicial = Column(Boolean, default=False)
    metadatos_json = Column(Text, nullable=True) # JSON serializado con tool outputs o badges

    conversacion = relationship("ChatConversacion", back_populates="mensajes")
