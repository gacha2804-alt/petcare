from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatConversacionCreate(BaseModel):
    id_mascota: int

class ChatMensajeCreate(BaseModel):
    contenido: str = Field(..., min_length=1)

class ChatMensajeOut(BaseModel):
    id: int
    id_conversacion: int
    remitente: str # "usuario", "asistente", "sistema"
    contenido: str
    fecha_envio: datetime
    contiene_informacion_clinica: bool
    es_orientacion_inicial: bool
    metadatos_json: Optional[str] = None

    class Config:
        from_attributes = True

class ChatConversacionOut(BaseModel):
    id: int
    id_usuario: int
    id_mascota: int
    id_cita: Optional[int] = None
    fecha_inicio: datetime
    fecha_ultima_actividad: datetime
    estado: str
    urgencia_detectada: bool
    clasificacion_urgencia: Optional[str] = None
    derivacion_requerida: bool
    mensajes: List[ChatMensajeOut] = []

    class Config:
        from_attributes = True

class ChatBotResponse(BaseModel):
    mensaje_asistente: ChatMensajeOut
    urgencia_detectada: bool
    clasificacion_urgencia: Optional[str] = None
    recomienda_valoracion: bool = False
    widget_agendamiento: Optional[Dict[str, Any]] = None
