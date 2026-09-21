from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: int
    usuario_id: int
    tipo: str
    titulo: str
    mensaje: str
    leida: bool
    referencia_id: Optional[int] = None
    fecha_creacion: datetime

    model_config = {"from_attributes": True}
