from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.db.session import get_db
from app.models.sede import Sede, Disponibilidad
from app.schemas.sede import SedeOut, DisponibilidadOut
from app.services.agenda_service import agenda_service

router = APIRouter(prefix="/agenda", tags=["Agenda y Disponibilidad"])

@router.get("/sedes", response_model=List[SedeOut])
def listar_sedes(db: Session = Depends(get_db)):
    """Retorna las 2 sedes físicas habilitadas de PetCare."""
    return agenda_service.obtener_sedes(db=db)

@router.get("/disponibilidad", response_model=List[DisponibilidadOut])
def consultar_disponibilidad(
    sede_id: int = Query(..., description="ID de la sede (1 o 2)"),
    fecha: Optional[str] = Query(None, description="Fecha en formato YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Consulta la disponibilidad real de turnos libres para una sede y fecha."""
    if fecha:
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Utilice YYYY-MM-DD.")
    else:
        fecha_obj = date.today()

    slots = agenda_service.consultar_disponibilidad(db=db, sede_id=sede_id, fecha=fecha_obj)
    return slots
