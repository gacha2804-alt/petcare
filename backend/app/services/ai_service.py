import json
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.pet import Pet
from app.models.health import Vaccine, Medication, SymptomObservation, WeightRecord
from app.models.ai import AIConsultation, AIAlert
from app.schemas.ai import TriageRequest, TriageResponse, ClinicalSummaryResponse


class AIService:
    @staticmethod
    def _local_rule_based_triage(pet: Pet, sintomas_texto: str) -> dict:
        """Motor heurístico de triaje preventivo offline (garantiza funcionamiento sin API Key)."""
        texto = sintomas_texto.lower()
        
        # 0. SALVAGUARDA ESTRICTA ANTI-PRESCRIPCIÓN:
        # Si el usuario solicita fórmulas, dosis o recetas de medicamentos
        intento_prescripcion = [
            "dosis", "receta", "medicamento", "pastilla", "jarabe", "antibiotico",
            "paracetamol", "ibuprofeno", "amoxicilina", "desparasitante", "que le doy",
            "que medicina", "formular", "recetar", "inyeccion", "gotas"
        ]
        if any(p in texto for p in intento_prescripcion):
            return {
                "nivel_urgencia": "moderado",
                "orientacion": (
                    f"ADVERTENCIA DE SEGURIDAD FARMACOLÓGICA: Como sistema de Inteligencia Artificial preventiva, "
                    f"tengo estrictamente PROHIBIDO recetar, dosificar o formular medicamentos para {pet.nombre}. "
                    "La automedicación en animales puede ser mortal o provocar intoxicaciones irreversibles. "
                    "Cualquier fármaco o posología debe ser prescrito única y exclusivamente por un médico veterinario con tarjeta profesional vigente."
                ),
                "recomendaciones": [
                    "Bajo ninguna circunstancia administres medicamentos de uso humano a tu mascota.",
                    "Agenda una consulta presencial con un veterinario para obtener una receta médica válida.",
                    "Si tu mascota ingirió alguna sustancia tóxica o fármaco indebido, acude de inmediato a urgencias."
                ],
                "sugerir_cita": True
            }

        # Palabras clave de urgencia crítica
        alertas_rojas = [
            "convulsion", "sangre", "desmayo", "inconsciente", "no respira",
            "asfixia", "envenenamiento", "toxico", "atropellado", "fractura",
            "dificultad para respirar", "abdomen hinchado", "ojo salido"
        ]
        # Palabras de riesgo moderado
        alertas_amarillas = [
            "vomito", "diarrea", "cojera", "no come", "inapetente", "fiebre",
            "rascado excesivo", "letargo", "decaido", "tos", "secrecion"
        ]

        if any(r in texto for r in alertas_rojas):
            nivel = "alto"
            orientacion = (
                f"Los síntomas descritos en {pet.nombre} indican una posible situación de emergencia médica. "
                "Se aconseja acudir inmediatamente a un centro de urgencias veterinarias 24 horas."
            )
            recomendaciones = [
                "Mantén la calma y traslada a tu mascota evitando movimientos bruscos.",
                "No le administres medicamentos para humanos (como paracetamol o ibuprofeno), son altamente tóxicos.",
                "Llama a la clínica más cercana para avisar que vas en camino con una urgencia."
            ]
            sugerir_cita = True
        elif any(y in texto for y in alertas_amarillas):
            nivel = "moderado"
            orientacion = (
                f"Se detectan síntomas que ameritan valoración veterinaria presencial para {pet.nombre}. "
                "Aunque no parece una urgencia con riesgo vital inminente, es importante no dejar que evolucione."
            )
            recomendaciones = [
                "Monitorea si los síntomas persisten por más de 12-24 horas.",
                "Asegura acceso a agua fresca pero no fuerces la ingesta de alimento sólido.",
                "Agenda una cita con tu médico veterinario para un chequeo preventivo."
            ]
            sugerir_cita = True
        else:
            nivel = "bajo"
            orientacion = (
                f"Los síntomas o cambios reportados para {pet.nombre} sugieren un estado leve. "
                "Se recomienda observación preventiva en el hogar."
            )
            recomendaciones = [
                "Continúa observando su apetito, hidratación y nivel de energía.",
                "Registra cualquier cambio en la bitácora de síntomas de PetCare.",
                "Si notas decaimiento persistente, consulta a un veterinario."
            ]
            sugerir_cita = False

        return {
            "nivel_urgencia": nivel,
            "orientacion": orientacion,
            "recomendaciones": recomendaciones,
            "sugerir_cita": sugerir_cita
        }

    @staticmethod
    def evaluate_symptoms(db: Session, user_id: int, request: TriageRequest) -> TriageResponse:
        pet = db.query(Pet).filter(Pet.id == request.mascota_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada.")

        # Obtener contexto clínico breve
        ultimas_vacunas = db.query(Vaccine).filter(Vaccine.mascota_id == pet.id).order_by(Vaccine.fecha_aplicacion.desc()).limit(2).all()
        meds_activos = db.query(Medication).filter(Medication.mascota_id == pet.id, Medication.activo == True).all()

        contexto_str = (
            f"Especie: {pet.especie}, Raza: {pet.raza or 'Mestizo'}, Sexo: {pet.sexo}, Peso: {pet.peso_actual or 'N/D'} kg. "
            f"Condiciones previas: {pet.condiciones_criticas or 'Ninguna'}. "
            f"Medicamentos activos: {', '.join([m.nombre for m in meds_activos]) or 'Ninguno'}."
        )

        # Si hay API Key de Gemini configurada, podríamos llamar a la API externa
        # De lo contrario (o ante fallo), utilizamos el motor de reglas de inferencia
        triage_data = AIService._local_rule_based_triage(pet, request.descripcion_sintomas)

        # Guardar en histórico de consultas IA
        consulta = AIConsultation(
            mascota_id=pet.id,
            usuario_id=user_id,
            prompt_usuario=request.descripcion_sintomas,
            contexto_clinico_snapshot=contexto_str,
            respuesta_ia=triage_data["orientacion"],
            nivel_urgencia_sugerido=triage_data["nivel_urgencia"],
            recomendaciones="\n".join(triage_data["recomendaciones"]),
            disclaimer_aceptado=True
        )
        db.add(consulta)

        # Si el nivel es alto o moderado, generar una alerta de evolución preventiva
        if triage_data["nivel_urgencia"] in ["alto", "moderado"]:
            alerta = AIAlert(
                mascota_id=pet.id,
                tipo_alerta="sintomas_detectados",
                mensaje=f"Alerta IA: {triage_data['orientacion'][:200]}...",
                nivel_riesgo="critica" if triage_data["nivel_urgencia"] == "alto" else "atencion"
            )
            db.add(alerta)

        db.commit()

        return TriageResponse(
            mascota_id=pet.id,
            nivel_urgencia=triage_data["nivel_urgencia"],
            orientacion_preventiva=triage_data["orientacion"],
            recomendaciones=triage_data["recomendaciones"],
            sugerir_agendar_cita=triage_data["sugerir_cita"],
            fecha_analisis=datetime.utcnow()
        )

    @staticmethod
    def get_clinical_summary(db: Session, pet_id: int) -> ClinicalSummaryResponse:
        pet = db.query(Pet).filter(Pet.id == pet_id, Pet.activa == True).first()
        if not pet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada.")

        # Obtener antecedentes
        sintomas = db.query(SymptomObservation).filter(SymptomObservation.mascota_id == pet.id).order_by(SymptomObservation.fecha_inicio.desc()).limit(5).all()
        meds = db.query(Medication).filter(Medication.mascota_id == pet.id, Medication.activo == True).all()
        vacunas = db.query(Vaccine).filter(Vaccine.mascota_id == pet.id).order_by(Vaccine.fecha_aplicacion.desc()).limit(3).all()
        alertas = db.query(AIAlert).filter(AIAlert.mascota_id == pet.id, AIAlert.revisada == False).all()

        sintomas_list = [f"{s.descripcion} ({s.severidad}, {s.fecha_inicio.strftime('%Y-%m-%d')})" for s in sintomas]
        meds_list = [f"{m.nombre} ({m.dosis} c/{m.frecuencia_horas}h)" for m in meds]
        vacunas_list = [f"{v.nombre_vacuna} (aplicada: {v.fecha_aplicacion}, próx: {v.fecha_proxima_dosis or 'N/A'})" for v in vacunas]
        alertas_list = [a.mensaje for a in alertas]

        resumen_texto = (
            f"Paciente {pet.nombre} ({pet.especie} {pet.raza or ''}), peso registrado: {pet.peso_actual or 'N/D'} kg. "
            f"Actualmente cuenta con {len(meds_list)} tratamiento(s) activo(s) y {len(sintomas_list)} síntoma(s) "
            f"reciente(s) en seguimiento. Condiciones preexistentes: {pet.condiciones_criticas or 'Ninguna reportada'}."
        )

        return ClinicalSummaryResponse(
            mascota_id=pet.id,
            nombre_mascota=pet.nombre,
            especie=pet.especie,
            resumen_ejecutivo=resumen_texto,
            sintomas_recientes=sintomas_list or ["Sin síntomas recientes registrados."],
            medicamentos_activos=meds_list or ["Sin medicamentos activos."],
            vacunas_vigentes=vacunas_list or ["Sin vacunas registradas."],
            alertas_detectadas=alertas_list or ["Sin alertas críticas pendientes."],
            fecha_generacion=datetime.utcnow()
        )
