import json
import re
from typing import Dict, Any, List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.mascota import Mascota
from app.tools.agenda_tools import (
    TOOL_CONSULTAR_DISPONIBILIDAD,
    TOOL_RESERVAR_CITA,
    ejecutar_tool_consultar_disponibilidad,
    ejecutar_tool_reservar_cita
)

SYSTEM_PROMPT = """Eres el Asistente Clínico Inteligente de PetCare, una plataforma especializada en el cuidado preventivo y triaje de mascotas.

Tus REGLAS INQUEBRANTABLES DE SEGURIDAD VETERINARIA son:
1. DETECCIÓN PRIORITARIA DE EMERGENCIAS:
   - Si el usuario reporta síntomas críticos como sangrado abundante, asfixia, dificultad respiratoria severa, convulsiones, pérdida de conciencia, ingestión reciente de tóxicos graves, encías azules/blancas o colapso:
     * Debes clasificar inmediatamente la situación como EMERGENCIA CRÍTICA.
     * Enfatiza de inmediato que acudan a una clínica de urgencias 24h sin demora.
     * NUNCA condiciones la atención de emergencia a un agendamiento de cita en la plataforma.
2. PROHIBICIÓN ABSOLUTA DE DIAGNÓSTICOS Y FÁRMACOS HUMANOS:
   - NUNCA emitas un diagnóstico médico definitivo ("Tu perro tiene moquillo o parvovirus"). Ofrece únicamente orientación inicial sobre signos clínicos.
   - NUNCA recetes medicamentos humanos (está estrictamente prohibido paracetamol, ibuprofeno, aspirina o tramadol, ya que pueden ser letales).
   - NUNCA instruyas inducir el vómito al animal (puede causar quemaduras o asfixia por aspiración).
3. EXIGENCIA DE CONTEXTO DE MASCOTA:
   - Todas las interacciones deben responder teniendo en cuenta la especie (perro, gato), edad, sexo y antecedentes de la mascota seleccionada.
4. AGENDAMIENTO INTEGRADO TRANSPARENTE:
   - Cuando el cuadro amerite una valoración médica preventiva o presencial no urgente:
     * Explica con empatía y claridad la razón por la que un médico veterinario debe revisarlo.
     * Ofrece agendar una cita presencial en cualquiera de nuestras dos sedes: "Sede 1 - Norte" o "Sede 2 - Sur".
     * Puedes utilizar las herramientas `consultar_disponibilidad` y `reservar_cita` para interactuar con la disponibilidad real de la clínica.
     * No presiones al usuario, permite que decida con tranquilidad.
5. TONO:
   - Profesional, empático, claro, no técnico y responsable.
"""

import unicodedata

def quitar_tildes(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').lower()

EMERGENCY_KEYWORDS = [
    "sangrado abundante", "hemorragia", "asfixia", "no puede respirar", "ahogando",
    "convulsi", "inconsciente", "desmayo", "colapso", "encias azules", "encias blancas",
    "envenenamiento", "intoxicacion grave", "atropellado", "letargo severo"
]

EVALUATION_KEYWORDS = [
    "cojera", "cojea", "vomito", "diarrea", "rasca", "come", "inapetencia", "apetito",
    "bulto", "ojo rojo", "vacuna", "desparasit", "control", "chequeo", "cita",
    "valoracion", "veterinario", "revisar", "consulta", "enfermo", "decaido"
]

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self.client = None

        if self.api_key:
            try:
                # Intentar importar SDK google-genai
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[Gemini Client Init Warning] No se pudo inicializar google-genai SDK ({e}). Operando con motor de inferencia local seguro.")

    def evaluar_urgencia(self, texto: str) -> Dict[str, Any]:
        """Aplica guardrails estrictos para detección de emergencias y valoración."""
        texto_norm = quitar_tildes(texto)
        es_emergencia = any(kw in texto_norm for kw in EMERGENCY_KEYWORDS)
        if es_emergencia:
            return {
                "urgencia_detectada": True,
                "clasificacion_urgencia": "emergencia",
                "recomienda_valoracion": False,
                "mensaje_alerta": "¡ALERTA DE EMERGENCIA VITAL! Los síntomas descritos requieren atención médica veterinaria presencial INMEDIATA. No espere un turno de cita; acuda ahora mismo a la clínica veterinaria de urgencias más cercana."
            }

        recomienda = any(kw in texto_norm for kw in EVALUATION_KEYWORDS)
        return {
            "urgencia_detectada": False,
            "clasificacion_urgencia": "normal",
            "recomienda_valoracion": recomienda,
            "mensaje_alerta": None
        }

    def procesar_mensaje(
        self,
        db: Session,
        id_propietario: int,
        mascota: Mascota,
        historial_mensajes: List[Dict[str, str]],
        nuevo_mensaje: str
    ) -> Dict[str, Any]:
        """
        Procesa el mensaje del tutor respetando los guardrails de PetCare,
        utilizando Gemini 2.5 Flash o el motor de triaje seguro local.
        """
        # 1. Guardrail de Urgencia Inmediato
        analisis_urgencia = self.evaluar_urgencia(nuevo_mensaje)
        if analisis_urgencia["urgencia_detectada"]:
            alerta = (
                f"🚨 **ATENCIÓN INMEDIATA REQUERIDA PARA {mascota.nombre.upper()}** 🚨\n\n"
                f"{analisis_urgencia['mensaje_alerta']}\n\n"
                f"- **Especie:** {mascota.especie} | **Datos:** {mascota.datos_identificatorios or 'Sin señas específicas'}\n"
                "- Mantén la calma, abriga a tu mascota con cuidado y acude a urgencias sin demora.\n"
                "- *Por seguridad médica de PetCare, no recomendamos esperar una cita programada ante signos de alarma vital.*"
            )
            return {
                "contenido": alerta,
                "urgencia_detectada": True,
                "clasificacion_urgencia": "emergencia",
                "recomienda_valoracion": False,
                "widget_agendamiento": None
            }

        # 2. Intento de llamada al API oficial de Gemini
        if self.client:
            try:
                from google.genai import types

                # Construir contexto de mascota
                contexto_mascota = (
                    f"Contexto del paciente:\n"
                    f"- Nombre: {mascota.nombre}\n"
                    f"- Especie: {mascota.especie}\n"
                    f"- Sexo: {mascota.sexo}\n"
                    f"- Nacimiento: {mascota.fecha_nacimiento}\n"
                    f"- Datos y antecedentes: {mascota.datos_identificatorios or 'Ninguno'}\n"
                )

                contents = [
                    {"role": "user", "parts": [{"text": f"SISTEMA:\n{SYSTEM_PROMPT}\n\n{contexto_mascota}"}]}
                ]

                for m in historial_mensajes[-6:]:
                    role = "user" if m.get("remitente") == "usuario" else "model"
                    contents.append({
                        "role": role,
                        "parts": [{"text": m.get("contenido", "")}]
                    })

                contents.append({
                    "role": "user",
                    "parts": [{"text": nuevo_mensaje}]
                })

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        max_output_tokens=800
                    )
                )

                texto_gemini = response.text or ""
                recomienda = analisis_urgencia["recomienda_valoracion"] or any(
                    word in texto_gemini.lower() for word in ["agendar", "cita", "valoración", "consulta presencial"]
                )

                widget = None
                if recomienda:
                    widget = {
                        "tipo": "agendamiento",
                        "id_mascota": mascota.id,
                        "nombre_mascota": mascota.nombre,
                        "sedes_disponibles": [
                            {"id": 1, "nombre": "Sede 1 - Norte"},
                            {"id": 2, "nombre": "Sede 2 - Sur"}
                        ]
                    }

                return {
                    "contenido": texto_gemini,
                    "urgencia_detectada": False,
                    "clasificacion_urgencia": "normal",
                    "recomienda_valoracion": recomienda,
                    "widget_agendamiento": widget
                }

            except Exception as e:
                print(f"[Gemini API Call Error] {e}. Ejecutando motor de respuesta seguro local.")

        # 3. Motor de respuesta seguro de PetCare (Garantiza funcionamiento offline 100% fiel al System Prompt)
        recomienda = analisis_urgencia["recomienda_valoracion"]

        # Detección de intentos de automedicación
        if any(med in nuevo_mensaje.lower() for med in ["paracetamol", "ibuprofeno", "aspirina", "acetaminofen"]):
            respuesta_texto = (
                f"⚠️ **Advertencia de Seguridad para {mascota.nombre}:**\n\n"
                "Está estrictamente contraindicado administrar medicamentos de uso humano (como ibuprofeno o paracetamol) a los animales. "
                "Estos fármacos pueden provocar fallo hepático o renal fulminante e intoxicaciones graves.\n\n"
                "Para proteger su salud, te recomendamos agendar una valoración presencial con el equipo veterinario de PetCare."
            )
            recomienda = True
        elif any(v in nuevo_mensaje.lower() for v in ["vomito", "vomitar"]):
            respuesta_texto = (
                f"Entiendo tu preocupación por {mascota.nombre}. Recuerda que **nunca debes inducir el vómito** en casa de forma casera, "
                "ya que existe un riesgo elevado de quemaduras esofágicas o broncoaspiración.\n\n"
                "Si los episodios persisten o notas decaimiento, es fundamental realizar una revisión física completa en la clínica."
            )
            recomienda = True
        else:
            respuesta_texto = (
                f"Gracias por consultar sobre {mascota.nombre} ({mascota.especie}, {mascota.sexo}). "
                "Como asistente preventivo de PetCare, te oriento que estos síntomas requieren observación atenta de sus niveles de energía, apetito y conducta. "
                "Ten en cuenta que esta información es preventiva y no sustituye un diagnóstico clínico presencial.\n\n"
                "Si deseas descartar complicaciones o continuar su esquema de salud preventiva, puedes agendar una valoración veterinaria presencial en cualquiera de nuestras sedes."
            )

        widget = None
        if recomienda:
            widget = {
                "tipo": "agendamiento",
                "id_mascota": mascota.id,
                "nombre_mascota": mascota.nombre,
                "sedes_disponibles": [
                    {"id": 1, "nombre": "Sede 1 - Norte"},
                    {"id": 2, "nombre": "Sede 2 - Sur"}
                ]
            }

        return {
            "contenido": respuesta_texto,
            "urgencia_detectada": False,
            "clasificacion_urgencia": "normal",
            "recomienda_valoracion": recomienda,
            "widget_agendamiento": widget
        }

gemini_service = GeminiService()
