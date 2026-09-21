from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class RoleResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: int
    rol_id: int
    rol_nombre: Optional[str] = None
    nombre_completo: str
    email: str
    telefono: Optional[str] = None
    activo: bool
    fecha_creacion: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None
