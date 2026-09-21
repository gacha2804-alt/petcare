from typing import List, Optional
from datetime import datetime, date, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.health import Vaccine, Medication, WeightRecord, SymptomObservation, ClinicalConsultation, VaccineProtocol
from app.models.pet import Pet
from app.models.user import User
from app.models.clinic import ClinicStaff
from app.models.notification import Notification
from app.schemas.health import (
    VaccineCreate, VaccineResponse,
    VaccineProtocolCreate, VaccineProtocolResponse,
    MedicationCreate, MedicationResponse,
    SymptomCreate, SymptomResponse,
    WeightCreate, WeightResponse,
    ClinicalConsultationCreate, ClinicalConsultationResponse,
    TimelineEvent, ReminderItem
)


class HealthService:
    @staticmethod
    def add_clinical_consultation(
        db: Session, pet_id: int, vet_id: int, data: ClinicalConsultationCreate
    ) -> ClinicalConsultationResponse:
        """Registra una consulta médica profesional con diagnóstico emitido por un veterinario."""
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada.")

        vet = db.query(User).filter(User.id == vet_id).first()
        staff_info = db.query(ClinicStaff).filter(ClinicStaff.usuario_id == vet_id).first()
        tarjeta = staff_info.tarjeta_profesional if staff_info else "Col. Vet."

        consultation = ClinicalConsultation(
            mascota_id=pet_id,
            veterinario_id=vet_id,
            fecha_consulta=datetime.utcnow(),
            motivo=data.motivo.strip(),
            anamnesis=data.anamnesis,
            constantes_vitales=data.constantes_vitales,
            diagnostico_profesional=data.diagnostico_profesional.strip(),
            plan_tratamiento=data.plan_tratamiento.strip(),
            notas_adicionales=data.notas_adicionales,
            origen_registro="profesional_veterinario"
        )
        db.add(consultation)

        # Generar notificación automática al propietario con el nuevo diagnóstico
        notif = Notification(
            usuario_id=pet.propietario_id,
            tipo="cita",
            titulo=f"Nuevo Diagnóstico Registrado para {pet.nombre}",
            mensaje=f"El Dr(a). {vet.nombre_completo} ha registrado la consulta: {data.diagnostico_profesional[:100]}...",
            referencia_id=pet_id
        )
        db.add(notif)

        db.commit()
        db.refresh(consultation)

        return ClinicalConsultationResponse(
            id=consultation.id,
            mascota_id=consultation.mascota_id,
            veterinario_id=consultation.veterinario_id,
            nombre_veterinario=vet.nombre_completo if vet else "Médico Veterinario",
            tarjeta_profesional=tarjeta,
            fecha_consulta=consultation.fecha_consulta,
            motivo=consultation.motivo,
            anamnesis=consultation.anamnesis,
            constantes_vitales=consultation.constantes_vitales,
            diagnostico_profesional=consultation.diagnostico_profesional,
            plan_tratamiento=consultation.plan_tratamiento,
            notas_adicionales=consultation.notas_adicionales,
            origen_registro="profesional_veterinario",
            fecha_creacion=consultation.fecha_creacion
        )

    @staticmethod
    def get_consultations_by_pet(db: Session, pet_id: int) -> List[ClinicalConsultationResponse]:
        consultations = db.query(ClinicalConsultation).filter(ClinicalConsultation.mascota_id == pet_id).order_by(ClinicalConsultation.fecha_consulta.desc()).all()
        results = []
        for c in consultations:
            vet = db.query(User).filter(User.id == c.veterinario_id).first()
            staff = db.query(ClinicStaff).filter(ClinicStaff.usuario_id == c.veterinario_id).first()
            results.append(ClinicalConsultationResponse(
                id=c.id,
                mascota_id=c.mascota_id,
                veterinario_id=c.veterinario_id,
                nombre_veterinario=vet.nombre_completo if vet else "Médico Veterinario",
                tarjeta_profesional=staff.tarjeta_profesional if staff else "Matrícula Profesional",
                fecha_consulta=c.fecha_consulta,
                motivo=c.motivo,
                anamnesis=c.anamnesis,
                constantes_vitales=c.constantes_vitales,
                diagnostico_profesional=c.diagnostico_profesional,
                plan_tratamiento=c.plan_tratamiento,
                notas_adicionales=c.notas_adicionales,
                origen_registro=c.origen_registro or "profesional_veterinario",
                fecha_creacion=c.fecha_creacion
            ))
        return results

    @staticmethod
    def add_vaccine(db: Session, pet_id: int, user_id: int, data: VaccineCreate) -> VaccineResponse:
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada.")

        user = db.query(User).filter(User.id == user_id).first()
        is_vet = user and user.rol and user.rol.nombre == "veterinario"
        origen = "profesional_veterinario" if is_vet else "propietario_hogar"

        tipo = data.tipo_aplicacion or "vacuna"
        protocolo, fecha_proxima, aviso = HealthService._resolver_protocolo(db, pet, data, tipo)

        vaccine = Vaccine(
            mascota_id=pet_id,
            veterinario_id=user_id if is_vet else None,
            nombre_vacuna=data.nombre_vacuna.strip(),
            tipo_aplicacion=tipo,
            fabricante=data.fabricante,
            lote=data.lote,
            dosis=data.dosis,
            via_aplicacion=data.via_aplicacion,
            peso_kg=data.peso_kg,
            edad_aplicacion=data.edad_aplicacion,
            protocolo_id=protocolo.id if protocolo else None,
            fecha_aplicacion=data.fecha_aplicacion,
            fecha_proxima_dosis=fecha_proxima or data.fecha_proxima_dosis,
            novedades=data.novedades,
            observaciones=data.observaciones,
            origen_registro=origen
        )
        db.add(vaccine)

        # Crear recordatorio anticipado para el dueño si hay próxima dosis
        if vaccine.fecha_proxima_dosis:
            notif = Notification(
                usuario_id=pet.propietario_id,
                tipo="vacuna",
                titulo=f"Recordatorio: Vacuna {data.nombre_vacuna} programada",
                mensaje=f"La próxima dosis de {data.nombre_vacuna} para {pet.nombre} está programada para el {vaccine.fecha_proxima_dosis}.",
                referencia_id=pet_id
            )
            db.add(notif)

        db.commit()
        db.refresh(vaccine)

        response = VaccineResponse.model_validate(vaccine)
        if aviso:
            response.aviso = aviso
        return response

    @staticmethod
    def _resolver_protocolo(db: Session, pet: Pet, data: VaccineCreate, tipo: str):
        """Resuelve el protocolo de refuerzo (RF-02/RF-03) y calcula la próxima fecha.

        - Si se indica protocolo_id, valida que exista y lo usa.
        - Si no, busca coincidencia por producto + tipo + especie.
        - Si no hay protocolo, retorna un aviso (HU-03) sin calcular fecha automática.
        """
        protocolo = None
        fecha_proxima = data.fecha_proxima_dosis
        aviso = None

        if data.protocolo_id:
            protocolo = db.query(VaccineProtocol).filter(
                VaccineProtocol.id == data.protocolo_id, VaccineProtocol.activo == True
            ).first()
            if not protocolo:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Protocolo de refuerzo no encontrado.")
            if not fecha_proxima:
                fecha_proxima = data.fecha_aplicacion + timedelta(days=protocolo.intervalo_refuerzo_dias)
        else:
            protocolo = db.query(VaccineProtocol).filter(
                VaccineProtocol.activo == True,
                VaccineProtocol.tipo_aplicacion == tipo,
                func.lower(VaccineProtocol.nombre_producto) == func.lower(data.nombre_vacuna.strip())
            ).filter(
                (func.lower(VaccineProtocol.especie) == func.lower(pet.especie)) |
                (func.lower(VaccineProtocol.especie) == "general")
            ).order_by(VaccineProtocol.categoria_edad.asc()).first()

            if protocolo and not fecha_proxima:
                fecha_proxima = data.fecha_aplicacion + timedelta(days=protocolo.intervalo_refuerzo_dias)

        if not protocolo and not data.protocolo_id:
            aviso = "Este producto no tiene un protocolo de refuerzo configurado; no se calculó la próxima fecha automáticamente."

        return protocolo, fecha_proxima, aviso

    @staticmethod
    def add_vaccine_protocol(db: Session, data: VaccineProtocolCreate) -> VaccineProtocolResponse:
        """Configura un protocolo de refuerzo por producto, especie y categoría de edad (RF-02)."""
        existente = db.query(VaccineProtocol).filter(
            VaccineProtocol.tipo_aplicacion == data.tipo_aplicacion,
            func.lower(VaccineProtocol.nombre_producto) == func.lower(data.nombre_producto.strip()),
            func.lower(VaccineProtocol.especie) == func.lower(data.especie.strip()),
            VaccineProtocol.categoria_edad == data.categoria_edad
        ).first()
        if existente:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Ya existe un protocolo para este producto, especie y categoría de edad.")

        protocolo = VaccineProtocol(
            nombre_producto=data.nombre_producto.strip(),
            fabricante=data.fabricante,
            tipo_aplicacion=data.tipo_aplicacion,
            especie=data.especie.strip(),
            categoria_edad=data.categoria_edad,
            edad_min_meses=data.edad_min_meses,
            edad_max_meses=data.edad_max_meses,
            intervalo_refuerzo_dias=data.intervalo_refuerzo_dias,
            esquema_refuerzos=data.esquema_refuerzos,
            requiere_alerta_previa_dias=data.requiere_alerta_previa_dias,
            descripcion=data.descripcion,
            activo=data.activo
        )
        db.add(protocolo)
        db.commit()
        db.refresh(protocolo)
        return VaccineProtocolResponse.model_validate(protocolo)

    @staticmethod
    def list_vaccine_protocols(
        db: Session,
        tipo_aplicacion: Optional[str] = None,
        especie: Optional[str] = None,
        categoria_edad: Optional[str] = None
    ) -> List[VaccineProtocolResponse]:
        """Lista protocolos de refuerzo con filtros opcionales por tipo, especie y categoría."""
        query = db.query(VaccineProtocol).filter(VaccineProtocol.activo == True)
        if tipo_aplicacion:
            query = query.filter(VaccineProtocol.tipo_aplicacion == tipo_aplicacion)
        if especie:
            query = query.filter(func.lower(VaccineProtocol.especie) == especie.lower())
        if categoria_edad:
            query = query.filter(VaccineProtocol.categoria_edad == categoria_edad)
        return [VaccineProtocolResponse.model_validate(p) for p in query.order_by(VaccineProtocol.nombre_producto.asc()).all()]

    @staticmethod
    def get_vaccines_by_pet(db: Session, pet_id: int) -> List[VaccineResponse]:
        vaccines = db.query(Vaccine).filter(Vaccine.mascota_id == pet_id).order_by(Vaccine.fecha_aplicacion.desc()).all()
        return [VaccineResponse.model_validate(v) for v in vaccines]

    @staticmethod
    def add_medication(db: Session, pet_id: int, vet_id: int, data: MedicationCreate) -> MedicationResponse:
        """Solo los profesionales veterinarios pueden prescribir fármacos."""
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada.")

        med = Medication(
            mascota_id=pet_id,
            veterinario_id=vet_id,
            nombre=data.nombre.strip(),
            dosis=data.dosis.strip(),
            frecuencia_horas=data.frecuencia_horas,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin,
            indicaciones=data.indicaciones,
            activo=data.activo,
            origen_registro="profesional_veterinario"
        )
        db.add(med)

        # Notificar al dueño sobre el nuevo tratamiento prescrito
        notif = Notification(
            usuario_id=pet.propietario_id,
            tipo="medicamento",
            titulo=f"Nuevo Tratamiento Prescrito para {pet.nombre}",
            mensaje=f"Se ha recetado {data.nombre} ({data.dosis} cada {data.frecuencia_horas}h). Revisa las indicaciones en la app.",
            referencia_id=pet_id
        )
        db.add(notif)

        db.commit()
        db.refresh(med)
        return MedicationResponse.model_validate(med)

    @staticmethod
    def get_medications_by_pet(db: Session, pet_id: int) -> List[MedicationResponse]:
        meds = db.query(Medication).filter(Medication.mascota_id == pet_id).order_by(Medication.fecha_inicio.desc()).all()
        return [MedicationResponse.model_validate(m) for m in meds]

    @staticmethod
    def add_symptom(db: Session, pet_id: int, user_id: int, data: SymptomCreate) -> SymptomResponse:
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada.")

        symptom = SymptomObservation(
            mascota_id=pet_id,
            usuario_id=user_id,
            tipo=data.tipo,
            descripcion=data.descripcion.strip(),
            severidad=data.severidad,
            fecha_inicio=data.fecha_inicio,
            origen_registro="propietario_hogar"
        )
        db.add(symptom)
        db.commit()
        db.refresh(symptom)
        return SymptomResponse.model_validate(symptom)

    @staticmethod
    def get_symptoms_by_pet(db: Session, pet_id: int) -> List[SymptomResponse]:
        symptoms = db.query(SymptomObservation).filter(SymptomObservation.mascota_id == pet_id).order_by(SymptomObservation.fecha_inicio.desc()).all()
        return [SymptomResponse.model_validate(s) for s in symptoms]

    @staticmethod
    def add_weight_record(db: Session, pet_id: int, data: WeightCreate) -> WeightResponse:
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada.")

        weight = WeightRecord(
            mascota_id=pet_id,
            peso_kg=data.peso_kg,
            fecha_registro=data.fecha_registro,
            notas=data.notas,
            origen_registro="propietario_hogar"
        )
        pet.peso_actual = data.peso_kg
        db.add(weight)
        db.commit()
        db.refresh(weight)
        return WeightResponse.model_validate(weight)

    @staticmethod
    def get_weight_history(db: Session, pet_id: int) -> List[WeightResponse]:
        weights = db.query(WeightRecord).filter(WeightRecord.mascota_id == pet_id).order_by(WeightRecord.fecha_registro.asc()).all()
        return [WeightResponse.model_validate(w) for w in weights]

    @staticmethod
    def get_active_reminders(db: Session, pet_id: int) -> List[ReminderItem]:
        """Calcula y lista recordatorios activos de vacunas próximas/vencidas y tratamientos vigentes."""
        reminders: List[ReminderItem] = []
        today = date.today()
        proxima_semana = today + timedelta(days=14)

        # 1. Vacunas
        vaccines = db.query(Vaccine).filter(Vaccine.mascota_id == pet_id, Vaccine.fecha_proxima_dosis != None).all()
        for v in vaccines:
            if v.fecha_proxima_dosis <= today:
                reminders.append(ReminderItem(
                    tipo="vacuna_vencida",
                    titulo=f"¡Vacuna Vencida! ({v.nombre_vacuna})",
                    mensaje=f"La dosis programada para {v.fecha_proxima_dosis} está vencida. Agenda cita para revacunación.",
                    fecha_limite=v.fecha_proxima_dosis,
                    urgente=True,
                    referencia_id=v.id
                ))
            elif v.fecha_proxima_dosis <= proxima_semana:
                reminders.append(ReminderItem(
                    tipo="vacuna_proxima",
                    titulo=f"Próxima Vacuna: {v.nombre_vacuna}",
                    mensaje=f"Faltan pocos días para la fecha programada ({v.fecha_proxima_dosis}).",
                    fecha_limite=v.fecha_proxima_dosis,
                    urgente=False,
                    referencia_id=v.id
                ))

        # 2. Medicamentos activos
        meds = db.query(Medication).filter(Medication.mascota_id == pet_id, Medication.activo == True).all()
        for m in meds:
            if m.fecha_fin and m.fecha_fin >= today:
                dias_restantes = (m.fecha_fin - today).days
                reminders.append(ReminderItem(
                    tipo="medicamento_toma",
                    titulo=f"Tratamiento Activo: {m.nombre}",
                    mensaje=f"Dosis: {m.dosis} cada {m.frecuencia_horas} horas. Finaliza en {dias_restantes} día(s) ({m.fecha_fin}).",
                    fecha_limite=m.fecha_fin,
                    urgente=False,
                    referencia_id=m.id
                ))

        return reminders

    @staticmethod
    def get_medical_timeline(db: Session, pet_id: int) -> List[TimelineEvent]:
        """
        Consolida cronológicamente todos los eventos de salud, diferenciando explícitamente
        entre registros profesionales emitidos por veterinarios y observaciones de hogar.
        """
        events: List[TimelineEvent] = []

        # 1. Consultas y Diagnósticos Profesionales (Veterinario)
        consultations = db.query(ClinicalConsultation).filter(ClinicalConsultation.mascota_id == pet_id).all()
        for c in consultations:
            vet = db.query(User).filter(User.id == c.veterinario_id).first()
            staff = db.query(ClinicStaff).filter(ClinicStaff.usuario_id == c.veterinario_id).first()
            events.append(TimelineEvent(
                tipo_evento="consulta_diagnostico",
                id_referencia=c.id,
                fecha=c.fecha_consulta,
                titulo=f"Diagnóstico Clínico: {c.motivo}",
                descripcion=f"DIAGNÓSTICO: {c.diagnostico_profesional} | TRATAMIENTO: {c.plan_tratamiento}",
                origen_registro="profesional_veterinario",
                autor_nombre=vet.nombre_completo if vet else "Médico Veterinario",
                autor_rol="Veterinario",
                tarjeta_profesional=staff.tarjeta_profesional if staff else "Matrícula Prof.",
                detalles={
                    "anamnesis": c.anamnesis,
                    "constantes_vitales": c.constantes_vitales,
                    "notas_adicionales": c.notas_adicionales
                }
            ))

        # 2. Vacunas (Profesional o Histórica)
        vaccines = db.query(Vaccine).filter(Vaccine.mascota_id == pet_id).all()
        for v in vaccines:
            vet = db.query(User).filter(User.id == v.veterinario_id).first() if v.veterinario_id else None
            staff = db.query(ClinicStaff).filter(ClinicStaff.usuario_id == v.veterinario_id).first() if v.veterinario_id else None
            es_vet = v.origen_registro == "profesional_veterinario"
            events.append(TimelineEvent(
                tipo_evento="vacuna",
                id_referencia=v.id,
                fecha=datetime.combine(v.fecha_aplicacion, datetime.min.time()),
                titulo=f"Inmunización: {v.nombre_vacuna}",
                descripcion=f"Lote: {v.lote or 'S/N'}. Próxima revacunación: {v.fecha_proxima_dosis or 'No requerida'}.",
                origen_registro=v.origen_registro or "profesional_veterinario",
                autor_nombre=vet.nombre_completo if vet else "Registro Histórico",
                autor_rol="Veterinario" if es_vet else "Propietario",
                tarjeta_profesional=staff.tarjeta_profesional if staff else None,
                detalles={"observaciones": v.observaciones, "lote": v.lote}
            ))

        # 3. Medicamentos y Prescripciones (Profesional Veterinario)
        meds = db.query(Medication).filter(Medication.mascota_id == pet_id).all()
        for m in meds:
            vet = db.query(User).filter(User.id == m.veterinario_id).first() if m.veterinario_id else None
            staff = db.query(ClinicStaff).filter(ClinicStaff.usuario_id == m.veterinario_id).first() if m.veterinario_id else None
            events.append(TimelineEvent(
                tipo_evento="medicamento",
                id_referencia=m.id,
                fecha=datetime.combine(m.fecha_inicio, datetime.min.time()),
                titulo=f"Prescripción Médica: {m.nombre}",
                descripcion=f"Posología: {m.dosis} cada {m.frecuencia_horas} horas. Indicaciones: {m.indicaciones or 'Según criterio médico'}.",
                origen_registro="profesional_veterinario",
                autor_nombre=vet.nombre_completo if vet else "Médico Veterinario",
                autor_rol="Veterinario",
                tarjeta_profesional=staff.tarjeta_profesional if staff else None,
                detalles={"activo": m.activo, "fecha_fin": str(m.fecha_fin) if m.fecha_fin else None}
            ))

        # 4. Síntomas y Observaciones (Propietario / Hogar)
        symptoms = db.query(SymptomObservation).filter(SymptomObservation.mascota_id == pet_id).all()
        for s in symptoms:
            user = db.query(User).filter(User.id == s.usuario_id).first()
            events.append(TimelineEvent(
                tipo_evento="sintoma",
                id_referencia=s.id,
                fecha=s.fecha_inicio,
                titulo=f"Observación de Hogar: {s.tipo.replace('_', ' ').capitalize()}",
                descripcion=f"Severidad aparente: {s.severidad.upper()}. Descripción: {s.descripcion}",
                origen_registro="propietario_hogar",
                autor_nombre=user.nombre_completo if user else "Propietario",
                autor_rol="Propietario",
                tarjeta_profesional=None,
                detalles={"resuelto": s.resuelto, "severidad": s.severidad}
            ))

        # 5. Pesajes (Propietario / Hogar)
        weights = db.query(WeightRecord).filter(WeightRecord.mascota_id == pet_id).all()
        for w in weights:
            events.append(TimelineEvent(
                tipo_evento="peso",
                id_referencia=w.id,
                fecha=datetime.combine(w.fecha_registro, datetime.min.time()),
                titulo=f"Control de Peso: {w.peso_kg} kg",
                descripcion=w.notas or "Control de rutina en casa",
                origen_registro="propietario_hogar",
                autor_nombre="Propietario",
                autor_rol="Propietario",
                tarjeta_profesional=None,
                detalles={"peso_kg": w.peso_kg}
            ))

        # Ordenar cronológicamente descendente (más reciente primero)
        events.sort(key=lambda x: x.fecha, reverse=True)
        return events
