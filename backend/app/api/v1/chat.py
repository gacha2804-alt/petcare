import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.mascota import Mascota
from app.models.chat import ChatConversacion, ChatMensaje
from app.schemas.chat import (
    ChatConversacionCreate,
    ChatConversacionOut,
    ChatMensajeCreate,
    ChatMensajeOut,
    ChatBotResponse
)
from app.services.gemini_service import gemini_service
from app.core.deps import get_current_user, registrar_auditoria

router = APIRouter(prefix="/chat", tags=["Asistente IA y Triaje"])

@router.post("/conversaciones", response_model=ChatConversacionOut, status_code=status.HTTP_201_CREATED)
def crear_o_recuperar_conversacion(
    data: ChatConversacionCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Inicia o recupera una conversación con el asistente de IA.
    EXIGE obligatoriamente un id_mascota válido asociado al propietario autenticado (RF-09, Guardrail 3).
    """
    mascota = db.query(Mascota).filter(
        Mascota.id == data.id_mascota,
        Mascota.id_propietario == current_user.id
    ).first()

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La mascota especificada no existe o no pertenece al usuario autenticado."
        )

    # Buscar conversación activa reciente para esta mascota
    conv = db.query(ChatConversacion).filter(
        ChatConversacion.id_usuario == current_user.id,
        ChatConversacion.id_mascota == mascota.id,
        ChatConversacion.estado == "activa"
    ).order_by(ChatConversacion.fecha_ultima_actividad.desc()).first()

    if not conv:
        conv = ChatConversacion(
            id_usuario=current_user.id,
            id_mascota=mascota.id,
            estado="activa"
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)

        # Mensaje de bienvenida inicial empático del asistente
        msg_inicial = ChatMensaje(
            id_conversacion=conv.id,
            remitente="asistente",
            contenido=(
                f"¡Hola! Soy tu Asistente Clínico Inteligente de PetCare. "
                f"Estoy listo para orientarte en el cuidado preventivo y evaluar los síntomas de **{mascota.nombre}** ({mascota.especie}, {mascota.sexo}).\n\n"
                f"Por favor, cuéntame: ¿qué signos has observado o cuál es el motivo de tu consulta?"
            ),
            es_orientacion_inicial=True
        )
        db.add(msg_inicial)
        db.commit()
        db.refresh(conv)

    return conv

@router.get("/conversaciones/{conversacion_id}", response_model=ChatConversacionOut)
def obtener_conversacion(
    conversacion_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = db.query(ChatConversacion).filter(
        ChatConversacion.id == conversacion_id,
        ChatConversacion.id_usuario == current_user.id
    ).first()

    if not conv:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

    return conv

@router.get("/conversaciones/mascota/{mascota_id}", response_model=List[ChatConversacionOut])
def listar_conversaciones_mascota(
    mascota_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mascota = db.query(Mascota).filter(
        Mascota.id == mascota_id,
        Mascota.id_propietario == current_user.id
    ).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    return db.query(ChatConversacion).filter(
        ChatConversacion.id_usuario == current_user.id,
        ChatConversacion.id_mascota == mascota_id
    ).order_by(ChatConversacion.fecha_ultima_actividad.desc()).all()

@router.post("/conversaciones/{conversacion_id}/mensajes", response_model=ChatBotResponse)
def enviar_mensaje_chat(
    conversacion_id: int,
    data: ChatMensajeCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Envía un mensaje a la conversación del asistente Gemini, evaluando guardrails de urgencia,
    prevención de diagnósticos/recetas y desplegando el widget de agendamiento si es pertinente.
    """
    conv = db.query(ChatConversacion).filter(
        ChatConversacion.id == conversacion_id,
        ChatConversacion.id_usuario == current_user.id
    ).first()

    if not conv:
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

    mascota = db.query(Mascota).filter(Mascota.id == conv.id_mascota).first()
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota asociada no encontrada")

    # Guardar mensaje del usuario
    msg_usuario = ChatMensaje(
        id_conversacion=conv.id,
        remitente="usuario",
        contenido=data.contenido,
        contiene_informacion_clinica=True
    )
    db.add(msg_usuario)
    db.commit()

    # Recopilar historial reciente para el contexto de IA
    historial_db = db.query(ChatMensaje).filter(
        ChatMensaje.id_conversacion == conv.id
    ).order_by(ChatMensaje.fecha_envio.asc()).all()

    historial_formateado = [
        {"remitente": m.remitente, "contenido": m.contenido}
        for m in historial_db
    ]

    # Llamar al servicio Gemini con Guardrails
    resultado = gemini_service.procesar_mensaje(
        db=db,
        id_propietario=current_user.id,
        mascota=mascota,
        historial_mensajes=historial_formateado,
        nuevo_mensaje=data.contenido
    )

    # Actualizar estado de urgencia en la conversación
    if resultado["urgencia_detectada"]:
        conv.urgencia_detectada = True
        conv.clasificacion_urgencia = resultado["clasificacion_urgencia"]
        conv.derivacion_requerida = True

    conv.fecha_ultima_actividad = datetime.utcnow()

    # Guardar mensaje del asistente
    widget_json = json.dumps(resultado["widget_agendamiento"]) if resultado["widget_agendamiento"] else None
    msg_asistente = ChatMensaje(
        id_conversacion=conv.id,
        remitente="asistente",
        contenido=resultado["contenido"],
        contiene_informacion_clinica=True,
        metadatos_json=widget_json
    )
    db.add(msg_asistente)
    db.commit()
    db.refresh(msg_asistente)

    # Auditoría clínica si hubo detección de urgencia
    if resultado["urgencia_detectada"]:
        registrar_auditoria(
            db=db,
            usuario_id=current_user.id,
            tipo_operacion="ALERTA_EMERGENCIA_IA",
            entidad_afectada="chat_conversaciones",
            id_registro_afectado=conv.id,
            detalles=f"Emergencia detectada para mascota {mascota.nombre}: {data.contenido[:100]}"
        )

    return ChatBotResponse(
        mensaje_asistente=ChatMensajeOut.model_validate(msg_asistente),
        urgencia_detectada=resultado["urgencia_detectada"],
        clasificacion_urgencia=resultado["clasificacion_urgencia"],
        recomienda_valoracion=resultado["recomienda_valoracion"],
        widget_agendamiento=resultado["widget_agendamiento"]
    )
