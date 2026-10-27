from app.schemas.auth import LoginRequest, TokenResponse, UserRegister, UserOut
from app.schemas.mascota import MascotaCreate, MascotaUpdate, MascotaOut
from app.schemas.clinico import VacunaCreate, VacunaOut, DesparasitacionCreate, DesparasitacionOut, ConsultaCreate, ConsultaOut, HistorialOut
from app.schemas.sede import SedeOut, DisponibilidadOut, CitaCreate, CitaOut
from app.schemas.chat import ChatConversacionCreate, ChatConversacionOut, ChatMensajeCreate, ChatMensajeOut, ChatBotResponse

__all__ = [
    "LoginRequest",
    "TokenResponse",
    "UserRegister",
    "UserOut",
    "MascotaCreate",
    "MascotaUpdate",
    "MascotaOut",
    "VacunaCreate",
    "VacunaOut",
    "DesparasitacionCreate",
    "DesparasitacionOut",
    "ConsultaCreate",
    "ConsultaOut",
    "HistorialOut",
    "SedeOut",
    "DisponibilidadOut",
    "CitaCreate",
    "CitaOut",
    "ChatConversacionCreate",
    "ChatConversacionOut",
    "ChatMensajeCreate",
    "ChatMensajeOut",
    "ChatBotResponse",
]
