from typing import Optional
from pydantic import BaseModel


class EmergencyProfileResponse(BaseModel):
    id: int
    nombre: str
    especie: str
    raza: Optional[str] = None
    sexo: str
    foto_url: Optional[str] = None
    contacto_emergencia_tel: Optional[str] = None
    condiciones_criticas: Optional[str] = None
    nombre_propietario: str
    mensaje_alerta: str = "Esta mascota tiene un perfil de emergencia activo en PetCare."

    model_config = {"from_attributes": True}
