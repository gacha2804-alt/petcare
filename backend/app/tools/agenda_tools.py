from typing import Dict, Any, List
from datetime import date, datetime
from sqlalchemy.orm import Session
from app.services.agenda_service import agenda_service

# Declaración de Tools para Google Gemini (Function Calling)
TOOL_CONSULTAR_DISPONIBILIDAD = {
    "name": "consultar_disponibilidad",
    "description": "Consulta los horarios y turnos de disponibilidad reales en la base de datos para una de las 2 sedes de PetCare en una fecha dada.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "sede_id": {
                "type": "INTEGER",
                "description": "ID de la sede: 1 para 'Sede 1 - Norte' o 2 para 'Sede 2 - Sur'"
            },
            "fecha": {
                "type": "STRING",
                "description": "Fecha a consultar en formato YYYY-MM-DD (ej: '2026-10-26')"
            }
        },
        "required": ["sede_id", "fecha"]
    }
}

TOOL_RESERVAR_CITA = {
    "name": "reservar_cita",
    "description": "Ejecuta la reserva atómica de una cita veterinaria en la sede y horario seleccionados.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "id_mascota": {
                "type": "INTEGER",
                "description": "ID obligatorio de la mascota"
            },
            "id_sede": {
                "type": "INTEGER",
                "description": "ID de la sede (1 o 2)"
            },
            "id_disponibilidad": {
                "type": "INTEGER",
                "description": "ID del slot de disponibilidad obtenido previamente"
            },
            "motivo_consulta": {
                "type": "STRING",
                "description": "Motivo resumido de la consulta o síntoma observado"
            }
        },
        "required": ["id_mascota", "id_sede", "id_disponibilidad", "motivo_consulta"]
    }
}

def ejecutar_tool_consultar_disponibilidad(db: Session, sede_id: int, fecha_str: str) -> Dict[str, Any]:
    try:
        f_date = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except Exception:
        f_date = date.today()

    slots = agenda_service.consultar_disponibilidad(db=db, sede_id=sede_id, fecha=f_date)
    return {
        "sede_id": sede_id,
        "fecha": str(f_date),
        "total_disponibles": len(slots),
        "slots": [
            {
                "id_disponibilidad": s.id,
                "hora_inicio": s.hora_inicio,
                "hora_fin": s.hora_fin
            }
            for s in slots
        ]
    }

def ejecutar_tool_reservar_cita(
    db: Session,
    id_propietario: int,
    id_mascota: int,
    id_sede: int,
    id_disponibilidad: int,
    motivo_consulta: str
) -> Dict[str, Any]:
    try:
        cita = agenda_service.reservar_cita(
            db=db,
            id_propietario=id_propietario,
            id_mascota=id_mascota,
            id_sede=id_sede,
            id_disponibilidad=id_disponibilidad,
            motivo_consulta=motivo_consulta
        )
        return {
            "exito": True,
            "cita_id": cita.id,
            "fecha": str(cita.fecha_cita),
            "hora": cita.hora_cita,
            "estado": cita.estado,
            "mensaje": f"Cita confirmada exitosamente para las {cita.hora_cita} del {cita.fecha_cita}."
        }
    except Exception as e:
        return {
            "exito": False,
            "error": str(e)
        }
