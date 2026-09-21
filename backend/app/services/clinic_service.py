import math
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.clinic import Clinic
from app.schemas.clinic import ClinicCreate, ClinicResponse


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula la distancia geodésica en kilómetros entre dos coordenadas GPS."""
    R = 6371.0  # Radio medio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


class ClinicService:
    @staticmethod
    def list_clinics(
        db: Session,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        only_urgencias: bool = False
    ) -> List[ClinicResponse]:
        query = db.query(Clinic).filter(Clinic.activa == True)
        if only_urgencias:
            query = query.filter(Clinic.tiene_urgencias_24h == True)
        
        clinics = query.all()
        results = []

        for c in clinics:
            resp = ClinicResponse.model_validate(c)
            if lat is not None and lon is not None:
                resp.distancia_km = haversine_distance(lat, lon, c.latitud, c.longitud)
            results.append(resp)

        # Si se proporcionaron coordenadas, ordenar por cercanía
        if lat is not None and lon is not None:
            results.sort(key=lambda x: x.distancia_km or float('inf'))

        return results

    @staticmethod
    def create_clinic(db: Session, data: ClinicCreate) -> ClinicResponse:
        clinic = Clinic(
            nombre=data.nombre.strip(),
            direccion=data.direccion.strip(),
            telefono=data.telefono.strip(),
            email=data.email.strip() if data.email else None,
            latitud=data.latitud,
            longitud=data.longitud,
            horario_atencion=data.horario_atencion,
            tiene_urgencias_24h=data.tiene_urgencias_24h,
            activa=True
        )
        db.add(clinic)
        db.commit()
        db.refresh(clinic)
        return ClinicResponse.model_validate(clinic)
