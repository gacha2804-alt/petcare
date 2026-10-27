from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    correo_electronico: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: "UserOut"

class UserRegister(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    correo_electronico: EmailStr
    telefono: Optional[str] = None
    password: str = Field(..., min_length=6)
    rol: Optional[str] = "propietario"

class UserOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo_electronico: EmailStr
    telefono: Optional[str] = None
    roles: List[str] = []
    fecha_registro: datetime

    class Config:
        from_attributes = True

TokenResponse.model_rebuild()
